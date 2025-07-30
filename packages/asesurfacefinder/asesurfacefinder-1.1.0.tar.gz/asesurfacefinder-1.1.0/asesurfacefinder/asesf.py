from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import shuffle
import numpy as np
from ase.build import add_adsorbate
from ase.geometry.analysis import Analysis
from ase.neighborlist import natural_cutoffs
from scipy import sparse
from importlib.metadata import version, PackageNotFoundError

from asesurfacefinder.utils import (
    descgen_mbtr, descgen_soap,
    get_site_coordination, get_absolute_abspos, sample_ads_pos,
    has_elems, guess_tags, check_tags
)
from asesurfacefinder.sample_bounds import SampleBounds
from asesurfacefinder.exception import NoSurfaceError, SurfaceTagError, NonPeriodicError

from ase import Atoms
from collections.abc import Sequence
from typing import Union
from dscribe.descriptors.descriptorlocal import DescriptorLocal


class SurfaceFinder:
    def __init__(self, surfaces: Sequence[Atoms], 
                 labels: Sequence[str]=None,
                 sample_bounds: Sequence[dict]=[],
                 site_coordinations: Sequence[dict]=[],
                 clf: RandomForestClassifier=None,
                 descriptor: Union[DescriptorLocal, str]='SOAP',
                 sample_defaults: SampleBounds = SampleBounds(0.1, 1.0, 2.75),
                 verbose: bool=True):
        '''Predicts location of adsorbates on surfaces.
        
        Given a list of ASE surfaces with correctly initialised
        high-symmetry adsorption points, trains a random forest
        classification model to predict the high-symmetry point
        that adsorbates are bound to.

        Each surface can take a dictionary of `SampleBounds` that
        defines the volume above each surface site in which 
        adsorption points are sampled during training. If this is
        not provided for a particular surface/site, this falls
        back to the bounds in `sample_defaults`.

        Can evaluate its own performance on generated surface/adsorbate
        examples in a secondary validation step.

        If greater control over the hyperparameters of
        `sklearn.ensemble.RandomForestClassifier` is desired, a
        previously setup instance of the class can be passed.

        Arguments:
            surfaces: List of ASE `Atoms` objects representing surfaces with correctly maped high-symmetry adsorption points.
            labels: Optional list of names for surfaces, must be of equal length to `surfaces` if provided.
            sample_bounds: Optional list of dicts specifying `SampleBounds` instances for each surface site.
            site_coordinations: Optional list of dicts specifying integer coordination of each surface site.
            clf: Optional `RandomForestClassifier` instance.
            descriptor: Optional local descriptor type, must be one of ['SOAP', 'LMBTR'] or an instantiated generator fron DScribe.
            sample_defaults: Default `SampleBounds` to fall back on when one is not specified for a site in `sample_bounds`.
            verbose: Whether to print information to stdout.
        '''
        if labels == None:
            self.labels = [str(i+1) for i in range(len(surfaces))]
        elif len(surfaces) != len(labels):
            raise ValueError('Incorrect number of labels for provided number of surfaces.')
        else:
            self.labels = labels

        if len(sample_bounds) != 0 and len(sample_bounds) != len(surfaces):
            raise ValueError('Incorrect number of sample bounds dicts for provided number of surfaces.')
        if len(site_coordinations) != 0 and len(site_coordinations) != len(surfaces):
            raise ValueError('Incorrect number of site coordination dicts for provided number of surfaces.')
        
        self.elements = []
        self.surface_sites = []
        self.site_coordinations = [{} for _ in range(len(surfaces))]
        self.surfaces = []
        self.sample_bounds = [{} for _ in range(len(surfaces))]
        for i, surface in enumerate(surfaces):
            if sum(surface.cell[2]) == 0.0:
                surface.center(10.0, axis=2)
            self.surfaces.append(surface)

            for elem in surface.get_chemical_symbols():
                if elem not in self.elements:
                    self.elements.append(elem)

            try:
                info = surface.info['adsorbate_info']
            except KeyError:
                raise ValueError(f'Surface at index {i} is missing "adsorbate_info" dict.')
            
            sites = info['sites'].keys()
            self.surface_sites.append(sites)
            for site in sites:
                if len(sample_bounds) == 0 or site not in sample_bounds[i].keys():
                    self.sample_bounds[i][site] = sample_defaults
                else:
                    self.sample_bounds[i][site] = sample_bounds[i][site]

                if len(site_coordinations) == 0 or site not in site_coordinations[i].keys():
                    self.site_coordinations[i][site] = get_site_coordination(surface, site, self.sample_bounds[i][site])
                else:
                    self.site_coordinations[i][site] = site_coordinations[i][site]

        self.n_surfaces = len(surfaces)
        self.clf_preconfig = clf
        if type(descriptor) == str:
            if descriptor == 'SOAP':
                self.desc = descgen_soap(self.elements)
            elif descriptor == 'LMBTR' or descriptor == 'MBTR':
                self.desc = descgen_mbtr(self.elements)
            else:
                raise ValueError('Unknown descriptor type specified.')
        else:
            self.desc = descriptor

        self.verbose = verbose

        try:
            _version = version(__package__ or __name__)
        except PackageNotFoundError:
            _version = '[Not installed]'
        print(f'ASESurfaceFinder v{_version}')
        print('-----------------------')
        print('Loaded surfaces:')
        for i in range(self.n_surfaces):
            print(f' - Surface {self.labels[i]}')
            for site in self.surface_sites[i]:
                print(f'   - Site \'{site}\' (coordination: {self.site_coordinations[i][site]})')


    def train(self, 
              samples_per_site: int=500,
              surf_mults: Sequence[tuple[int, int, int]]=[(1,1,1)],
              n_jobs: int=1
        ):
        '''Trains a random forest classifier to recognise surface sites.
        
        Arguments:
            samples_per_site: Number of adsorbate positions to sample on each surface site during training.
            surf_mults: (X,Y,Z) surface supercell multipliers to sample.
            n_jobs: Number of processes to parallelise descriptor generation and training over.
        '''
        if self.verbose:
            print('ASESurfaceFinder Training')
            print('------------------------------------')

        n_mults = len(surf_mults)
        n_samples = sum([n_mults*len(sites)*samples_per_site for sites in self.surface_sites])

        if self.verbose: print('  Constructing local descriptors for sampled systems...')
        surf_descs = np.zeros((n_samples, self.desc.get_number_of_features()))
        labels = []
        start_idx = 0
        for i, (surface, sites, label) in enumerate(zip(self.surfaces, self.surface_sites, self.labels)):
            for j, smult in enumerate(surf_mults):
                slab = surface.repeat(smult)
                slab_positions = np.zeros((len(sites)*samples_per_site, 3))

                for k, site in enumerate(sites):
                    site_abspos = get_absolute_abspos(surface, site)
                    for m in range(samples_per_site):
                        slab = surface.copy()
                        bounds = self.sample_bounds[i][site]
                        xy, z = sample_ads_pos(site_abspos, bounds.z_bounds, bounds.r_max)
                        add_adsorbate(slab, 'H', z, xy)
                        slab_positions[(k*samples_per_site)+m, :] = slab.get_positions()[-1]
                        labels.append(f'{label}_{site}')

                end_idx = start_idx + (len(sites)*samples_per_site)
                slab = surface.copy()
                if self.verbose: print(f'  Adding {len(slab_positions)} descs between idxs {start_idx} and {end_idx} ')
                surf_descs[start_idx:end_idx, :] = self.desc.create(slab, centers=slab_positions, n_jobs=n_jobs)

                start_idx = end_idx

        if self.verbose: print('  Training random forest classifier...')
        X, y = shuffle(surf_descs, labels)
        if self.clf_preconfig is None:
            clf = RandomForestClassifier(n_jobs=n_jobs)
        else:
            clf = self.clf_preconfig
            clf.n_jobs = n_jobs
        clf.fit(X, y)
        if self.verbose: print('  Training complete.\n')
        
        self.clf = clf
        return clf


    def validate(self,
                 samples_per_site: int=500,
                 surf_mults: Sequence[tuple[int, int, int]]=[(1,1,1), (2,2,1)],
                 sample_bounds: Sequence[dict]=[]
        ):
        '''Validates a random forest classifier's ability to recognise surface sites.
        
        Arguments:
            samples_per_site: Number of adsorbate positions to sample on each surface site during validation.
            surf_mults: Optional (X,Y,Z) surface supercell multipliers to sample.
            sample_bounds: Optional list of dicts that can override the `SampleBounds` used in training.
        '''
        if self.verbose: 
            print('ASESurfaceFinder Validation')
            print('------------------------------------')
        if not hasattr(self, 'clf'):
            raise AttributeError('No trained RandomForestClassifier found.')
        
        if len(sample_bounds) != 0 and len(sample_bounds) != len(self.surfaces):
            raise ValueError('Incorrect number of sample bounds dicts for trained number of surfaces.')
        
        n_mults = len(surf_mults)
        n_samples = sum([n_mults*len(sites)*samples_per_site for sites in self.surface_sites])

        if self.verbose: print('  Constructing local descriptors for sampled systems...')
        surf_descs = np.zeros((n_samples, self.desc.get_number_of_features()))
        labels = []
        smults = []
        heights = []
        displacements = []
        start_idx = 0
        for i, (surface, sites, label) in enumerate(zip(self.surfaces, self.surface_sites, self.labels)):
            for j, smult in enumerate(surf_mults):
                slab = surface.repeat(smult)
                slab_positions = np.zeros((len(sites)*samples_per_site, 3))

                for k, site in enumerate(sites):
                    site_abspos = get_absolute_abspos(surface, site)
                    if len(sample_bounds) != 0 and site in sample_bounds[i].keys():
                        bounds = sample_bounds[i][site]
                    else:
                        bounds = self.sample_bounds[i][site]

                    for l in range(samples_per_site):
                        slab = surface.copy()
                        xy, z = sample_ads_pos(site_abspos, bounds.z_bounds, bounds.r_max)
                        add_adsorbate(slab, 'H', z, xy)
                        slab_positions[(k*samples_per_site)+l, :] = slab.get_positions()[-1]
                        labels.append(f'{label}_{site}')
                        smults.append(str(smult))
                        heights.append(z)
                        displacements.append(np.linalg.norm(site_abspos-xy))

                end_idx = start_idx + (len(sites)*samples_per_site)
                slab = surface.copy()
                if self.verbose: print(f'  Adding {len(slab_positions)} descs between idxs {start_idx} and {end_idx} ')
                surf_descs[start_idx:end_idx, :] = self.desc.create(slab, centers=slab_positions, n_jobs=self.clf.n_jobs)

                start_idx = end_idx

        assert(len(labels) == n_samples)

        if self.verbose: print('  Predicting labels with random forest classifier...')
        pred_labels = self.clf.predict(surf_descs)
        score = self.clf.score(surf_descs, labels)
        if self.verbose: print('  Prediction complete.\n')

        correct_acc = 0
        incorrect_idxs = []
        for i, (yt, yp) in enumerate(zip(labels, pred_labels)):
            if yt == yp:
                correct_acc += 1
            else:
                incorrect_idxs.append(i)
        
        print(f'  {correct_acc}/{n_samples} sites classified correctly (accuracy = {score}).')

        if len(incorrect_idxs) > 0:
            stat_labels = []
            for i in incorrect_idxs:
                stat_labels.append(f'{labels[i]} {smults[i]} (h = {heights[i]:.2f}, r = {displacements[i]:.2f})')

            stat_clen = np.max([len(lab) for lab in stat_labels])
            print(f'True {" "*(stat_clen-5)} | Predicted')
            print('-'*(stat_clen+18))
            for i, idx in enumerate(incorrect_idxs):
                print(f'{stat_labels[i].ljust(stat_clen)} | {pred_labels[idx]}')

            print(f'\n  {correct_acc}/{n_samples} sites classified correctly (accuracy = {score}).')

        return True if correct_acc == n_samples else False


    def predict(self, ads_slab: Atoms, nl_cutoffs: list=None, allow_tag_guessing: bool=True, reject_wrong_coordination=False, reject_bonded_hydrogens=False):
        '''Predicts adsorption site and surface facet of adsorbed systems.

        Systems may contain multiple adsorbates, as well as non-
        adsorbed, gas-phase molecules. This method separates all
        molecules (adsorbed or otherwise) from the underlying
        surface slab and locates all atoms in these molecules
        that are bonded to the surface.

        Surface-bound atoms are used for predicting adsorption
        sites, which are then mapped back to the correct atoms 
        in the molecules they originated from.

        Returns the isolated surface slab, a list of isolated
        molecule geometries, and a matching list of adsorption
        site dicts. Each dict (one per molecule) is keyed by
        the indices of adsorbed atoms, with dict values representing
        predicted adsorption site and coordination to the surface
        at this site. In the event that a molecule was not
        bound to the surface, its dict remains empty.

        Arguments:
            ads_slab: `Atoms` object representing adsorbate(s) on surface slab.
            nl_cutoffs: List of ASE `NeighborList` cutoffs to use for identifying bonding to surface. Defaults to `ase.neighborlist.natural_cutoffs(ads_slab)`.
            allow_tag_guessing: Whether to allow surface/adsorbate layer tags to be guessed based on elemental composition if not present or otherwise malformed in input.
            reject_wrong_coordination: Whether to reject (mark as not adsorbed) atoms with the wrong coordination for their predicted site, provided they are connected to another adsorbed atom.
            reject_bonded_hydrogens: Whether to reject (mark as not adsorbed) hydrogen atoms that are directly bonded to an adsorbed atom.
        '''
        if self.verbose: 
            print('ASESurfaceFinder Prediction')
            print('------------------------------------')
            
        if not hasattr(self, 'clf'):
            raise AttributeError('No trained RandomForestClassifier found.')
        
        if (not any(ads_slab.get_pbc())) or ads_slab.cell.sum() == 0.0:
            raise NonPeriodicError('Slab-adsorbate system is missing PBCs and/or a unit cell.')
        
        # Check slab (maybe) actually has a known surface.
        if not has_elems(ads_slab, self.elements):
            raise NoSurfaceError('Slab-adsorbate system contains no known surface.')

        tags = ads_slab.get_tags()
        tag_errmsg = check_tags(tags, len(ads_slab))
        if not allow_tag_guessing:
            raise SurfaceTagError(tag_errmsg)
        
        if len(tag_errmsg) > 0:
            if self.verbose: 
                print(tag_errmsg)
                print('WARNING: Guessing surface/adsorbate separation from elements.')

            tags = guess_tags(ads_slab, self.elements)
            tag_errmsg2 = check_tags(tags, len(ads_slab))
            if len(tag_errmsg2) > 0:
                raise SurfaceTagError(tag_errmsg2)

        slabatom_slabidxs = np.argwhere(tags!=0).flatten()
        molatom_slabidxs = np.argwhere(tags==0).flatten()

        # Determine which atoms are bonded to the surface.
        cutoffs = nl_cutoffs if nl_cutoffs is not None else natural_cutoffs(ads_slab)
        if type(cutoffs) is list:
            cutoffs = np.array(cutoffs)
        ana = Analysis(ads_slab, cutoffs=cutoffs, self_interaction=False, bothways=True)
        nl = ana.nl[0]
        bonded_molatom_slabidxs = []
        for slabatom_slabidx in slabatom_slabidxs:
            slabatom_neighbors, _ = nl.get_neighbors(slabatom_slabidx)
            for molatom_slabidx in molatom_slabidxs:
                if molatom_slabidx in slabatom_neighbors:
                    bonded_molatom_slabidxs.append(molatom_slabidx)

        bonded_molatom_slabidxs, bonded_molatom_coordinations = np.unique(bonded_molatom_slabidxs, return_counts=True)
        if self.verbose: print(f'  {len(bonded_molatom_slabidxs)} adsorbed atoms found on surface at idxs {bonded_molatom_slabidxs}.')

        # Isolate molecules.
        mol_atoms = ads_slab[molatom_slabidxs]
        mol_cutoffs = cutoffs[molatom_slabidxs]
        mol_atoms.set_pbc([False, False, False])
        mol_atoms.set_cell([0.0, 0.0, 0.0])
        ana = Analysis(mol_atoms, cutoffs=mol_cutoffs)
        nl = ana.nl[0]
        cm = nl.get_connectivity_matrix()
        n_mol, molidx_to_moleculeidx = sparse.csgraph.connected_components(cm) # e.g. 2, array[0, 0, 0, 1, 1]
        if self.verbose: print(f'  {n_mol} molecule(s) found on/above surface.')
        molecules = [mol_atoms[np.argwhere(molidx_to_moleculeidx==i).flatten()] for i in range(n_mol)]
        per_mol_cutoffs = [mol_cutoffs[np.argwhere(molidx_to_moleculeidx==i).flatten()] for i in range(n_mol)]

        # Predict surface sites.
        pos = ads_slab.get_positions()
        slab = ads_slab[slabatom_slabidxs]
        if ads_slab.info.get('adsorbate_info') is None or ads_slab.info['adsorbate_info'].get('top layer atom index') is None:
            slab_max_z = slab.positions[:, 2].max()
        else:
            slab_max_z = ads_slab.positions[ads_slab.info['adsorbate_info']['top layer atom index'], 2]
        # Only predict if there are actually adsorbed atoms.
        if len(bonded_molatom_slabidxs) > 0:
            bonded_positions = pos[bonded_molatom_slabidxs]
            descs = self.desc.create(slab, bonded_positions, n_jobs=self.clf.n_jobs)
            pred_labels = self.clf.predict(descs)

        # Assign surface sites to molecules.
        slabidx_to_molidx = {int(idx): i for i, idx in enumerate(molatom_slabidxs)}
        pred_labels_per_molecule = [{} for _ in range(n_mol)]
        for i, bonded_molatom_slabidx in enumerate(bonded_molatom_slabidxs):
            bonded_molatom_molidx = slabidx_to_molidx[bonded_molatom_slabidx]
            moleculeidx = int(molidx_to_moleculeidx[bonded_molatom_molidx])
            elem = ads_slab.symbols[bonded_molatom_slabidx]
            height = ads_slab.positions[bonded_molatom_slabidx, 2] - slab_max_z

            unique, counts = np.unique(molidx_to_moleculeidx[:bonded_molatom_molidx+1], return_counts=True)
            atomidx_in_mol = int(dict(zip(unique, counts))[moleculeidx])-1

            pred_labels_per_molecule[moleculeidx][atomidx_in_mol] = {
                'site': str(pred_labels[i]), 
                'bonded_elem': elem,
                'coordination': int(bonded_molatom_coordinations[i]),
                'height': height
            }

        # Remove predicted adsorbed atoms if 
        #   a) they are undercoordinated compared to their expected coordination,
        #   b) they are connected to another adsorbed atom that is correctly coordinated.
        # This should eliminate e.g. low-hanging hydrogen atoms that aren't actually adsorbed,
        # and are just close to the surface because they are bonded to atoms actually in 
        # a surface site.
        if reject_wrong_coordination:
            for i in range(n_mol):
                if len(pred_labels_per_molecule[i]) < 2:
                    continue

                # Find atoms with incorrect coordination.
                maybe_remove_idxs = []
                bonded_atomidxs = pred_labels_per_molecule[i].keys()
                for bonded_atomidx in bonded_atomidxs:
                    surflabel_split = pred_labels_per_molecule[i][bonded_atomidx]['site'].split('_')
                    surflabel = '_'.join(surflabel_split[:-1])
                    site = surflabel_split[-1]
                    sf_surf_idx = self.labels.index(surflabel)
                    expected_coord = self.site_coordinations[sf_surf_idx][site]
                    if pred_labels_per_molecule[i][bonded_atomidx]['coordination'] != expected_coord:
                        maybe_remove_idxs.append(bonded_atomidx)

                if len(maybe_remove_idxs) == 0:
                    continue

                # Check for adsorbed neighbours of undercoordinated atoms.
                ana = Analysis(molecules[i], cutoffs=per_mol_cutoffs[i], self_interaction=False, bothways=True)
                nl = ana.nl[0]
                remove_idxs = []
                for remidx in maybe_remove_idxs:
                    neighbors = nl.get_neighbors(remidx)[0]
                    for neighbor in neighbors:
                        if neighbor in bonded_atomidxs and neighbor in maybe_remove_idxs:
                            if self.verbose: 
                                print(f'Undercoordinated adsorbed atom {remidx} detected in molecule {i+1}/{n_mol}')
                                print('Not untagging since it shares an undercoodinated neighbour.')
                        elif neighbor in bonded_atomidxs:
                            if self.verbose:
                                print(f'Untagging undercoordinated adsorbed atom {remidx} in molecule {i+1}/{n_mol}')
                            remove_idxs.append(remidx)
                        else:
                            print(f'Warning: adsorbed atom {remidx} in molecule {i+1}/{n_mol} is undercoordinated.')

                for remidx in remove_idxs:
                    pred_labels_per_molecule[i].pop(remidx)

        # Some hydrogens end up being close enough to adsorbed atoms to be
        # detected as connected to the same surface site. These will not be
        # removed by the above.
        # This is therefore a bit of a nuclear option, rejecting all hydrogens
        # directly bonded to other (non-hydrogen) adsorbed atoms.
        if reject_bonded_hydrogens:
            for i in range(n_mol):
                if len(pred_labels_per_molecule[i]) < 2:
                    continue

                # Find any adsorbed hydrogens.
                hydrogen_idxs = []
                non_hydrogen_idxs = []
                bonded_atomidxs = pred_labels_per_molecule[i].keys()
                for bonded_atomidx in bonded_atomidxs:
                    if pred_labels_per_molecule[i][bonded_atomidx]['bonded_elem'] == 'H':
                        hydrogen_idxs.append(bonded_atomidx)
                    else:
                        non_hydrogen_idxs.append(bonded_atomidx)

                if len(hydrogen_idxs) == 0:
                    continue

                # Reject if bonded to a non-hydrogen adsorbed atom.
                ana = Analysis(molecules[i], cutoffs=per_mol_cutoffs[i], self_interaction=False, bothways=True)
                nl = ana.nl[0]
                remove_idxs = []
                for hydrogen_idx in hydrogen_idxs:
                    neighbors = nl.get_neighbors(hydrogen_idx)[0]
                    if any(non_hydrogen_idx in neighbors for non_hydrogen_idx in non_hydrogen_idxs):
                        if self.verbose:
                            print(f'Untagging hydrogen {hydrogen_idx} bonded to adsorbed atom in molecule {i+1}/{n_mol}')
                        remove_idxs.append(hydrogen_idx)

                for remidx in remove_idxs:
                    pred_labels_per_molecule[i].pop(remidx)

        return slab, molecules, pred_labels_per_molecule
