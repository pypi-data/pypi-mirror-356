# Changelog

## [1.6.0] - 13/02/2025

### Added

- Changes have been made to the handling of disorder. ``PeriodicSet`` now has the attribute ``.disorder``, a list containing disorder assemblies if any disorder is present. The PDD of a disordered structure is a concatenation of the PDDs of all disorder configurations, which retains invariance and continuity. Note that if there are too many disorder configurations (set by ``.calculate.MAX_DISORDER_CONFIGS``, default 100) then PDD and AMD will default to using the majority occupancy configuration.

- Added 'normalised' invariants `amd.PDA()` and `amd.ADA()`, which are the differences between PDD/AMD and their asymptotic curves.

- The ``PeriodicSet`` object now has the methods ``density`` and ``formula`` returning the physical density (g/cm3) and reduced formula of a crystal respectively, as well as ``to_cif_str`` and ``to_pymatgen_structure``.

- Minor improvements to the PDD algorithm.

### Changed

- Overlapping sites are no longer removed with ``CifReader``, ``CSDReader`` or any function for converting to ``PeriodicSet`` in ``amd.io``. Geometry of a structure will be as it is found in a CIF file.

- The ``disorder`` option of ``CifReader`` and ``CSDReader`` has been replaced with ``skip_disorder``. Disordered structures are skipped if True, otherwise disorder is handled in the way described above.

- ``amd.PPC`` has been moved to be a method of the periodic set, ``amd.periodicset.PeriodicSet.PPC``.

- ``amd.PeriodicSet``'s ``.types`` attribute now contains the atomic types of the asymmetric unit instead of the motif.

- Minimum Python version is now 3.9.

### Removed

- ``amd.compare`` and the corresponding cli have been temporarily removed.

- Pymatgen and ase backends for ``CifReader`` have been temporarily disabled, as well as ``periodicset_from_pymatgen_structure``, ``periodicset_from_ase_atoms``, ``periodicset_from_pymatgen_cifblock`` and ``periodicset_from_ase_cifblock``.

## [1.5.0] - 23/02/2024

### Changed

- Earth Mover's distance changed to calculate to 8 decimal places.

## [1.4.1] - 26/05/2023

### Changed

- ``nearest_neighbours_data()`` changed in line with ``nearest_neighbours()``.

- Improved docs and formatting.

## [1.4.0] - 16/05/2023

### Changed

- Core function ``nearest_neighbours()`` and other code in the ``_nearest_neighbours`` module has changed significantly. ``nearest_neighbours()`` no longer returns ``cloud`` or ``inds``; this behaviour is now given by ``nearest_neighbours_data()``. ``nearest_neighbours()`` has been fixed to not exclude the first nearest neighbours of points in the query set ``x``. Use of ``KDTree`` has been removed. Integer lattice points are stored in a cache.

- Changes to attribute names in ``amd.PeriodicSet``: ``wyckoff_multiplicities`` --> ``multiplicities`` and ``asymmetric_unit`` --> ``asym_unit``.

- Default backend reader changed to `gemmi` for faster CIF reads; removed `ase` as a dependency and added `gemmi`. Reads should be identical to before, but this may turn out to be false. The only known difference is that the `gemmi` parser cannot handle some characters (e.g. �), and does not allow cifs with repeated headers.

- Readers in the ``io`` module give attributes of ``PeriodicSet``s smaller ``dtypes`` where appropriate: ``np.int32`` for ``asym_unit`` and ``multiplicities``, ``np.uint8`` for ``types``.

- ``amd.AMD()``, ``amd.PDD()`` and other functions in ``amd.calculate`` which accept a periodic set no longer accept a tuple, only ``amd.PeriodicSet``. A tuple can be converted before passing, e.g. replace ``amd.AMD((motif, cell), k)`` with ``amd.AMD(amd.PeriodicSet(motif, cell), k)``.

## [1.3.6] - 25/02/2023

- `verbose` parameter added to `amd.CifReader()` and `amd.CSDReader()`.

## [1.3.5] - 21/02/2023

### Added

- CIF/CSD Reader internals have been improved (expanding the asymmetric unit to the full motif is ~10x faster, giving to an overall reading improvement of ~3x).

- `utils.cell_to_cellpar` and `utils.cell_to_cellpar_2D` have been improved with `numba`.

- Removed `_ETA` class and added dependency `tqdm` for progress bars.

- Changes to converter functions in the `io` module have decoupled them from depending on other packages, e.g. `periodicset_from_pymatgen_cifblock()` now has no dependency on `ase`, just `pymatgen`.

- Cleaned/added more documentation, docstrings, PEP8, type hints. Moved be pyproject.toml only and use a src layout instead of flat.

### Changed

- Fixed issue with ccdc reader where atoms with missing coordinates would throw a ParseError where they should have been removed.

- Fixed `molecular_centres` parameter to work correctly in `amd.compare`.

## [1.3.4] - 07/11/2022

### Added

- Parameter `nearest` added to `amd.compare`, which finds a number of nearest neighbours in one set from the other. `amd.compare` can now also be used from the command line.

- `pymatgen` and `gemmi` added as options for the backend to `CifReader`.

- Several converter functions now exist in the `io` module to get `PeriodicSet` objects from `ase`, `pymatgen`, `gemmi` or `ccdc`: , `periodicset_from_ase_cifblock`, `periodicset_from_ase_atoms`, `periodicset_from_pymatgen_cifblock`,  `periodicset_from_pymatgen_structure`, `periodicset_from_ccdc_entry`, `periodicset_from_ccdc_crystal`, and `periodicset_from_gemmi_block`. The functions involving `ccdc` no longer depend on `ase`.

### Changed

- Read option ``molecular_centres`` now yields `PeriodicSet` objects whose motif consists of the molecular centres, instead of adding an attribute ``.molecular_centres`` containing the centres. The original motif is no longer kept.

### Removed

- Removed `.entry()` and `.family()` from `CSDReader`, instead new `CSDReader` objects should be made each time.

## [1.3.2] - 01/09/2022

### Added

- Convenience function `compare` added as a flexible, easy way to compare crystals by AMD or PDD. This addition also added the dependency `pandas` to the package.

- `PDD_pdist` and `PDD_cdist` now support parallel processing with the keyword argument `n_jobs`. The argument `verbose` has changed to accept an integer which is passed to `joblib.Parallel` to control the level of verbosity.

- Comparison by molecular centres added (``csd-python-api`` only). The readers now accept ``molecular_centres`` (default ``False``), which give the yielded `PeriodicSet` objects an attribute ``.molecular_centres``, an array of the centres of molecules. The `amd.compare` function also supports the `.molecular_centres` argument, if `True` the molecular centres will be used for comparison instead of atomic centres.

- AMD/PDD and EMD speed improvements.

- Support for reader `pycodcif` (CIF v2.0) in `CifReader` through `ase`, if installed.

### Changed

- Significant changes were made to `amd.PeriodicSet`, so old versions of this object are no longer compatible with the package (versions after 1.3 are not backwards compatible). They no longer have a generic `.tags` dictionary for additional data.

- `progressbar2` is planned to be removed. It is still in use for PDD comparisons without parallel processing, otherwise `joblib.Parallel` provides its own progress bar.

### Removed

- Module `pset_io` removed in favour of just using `pickle` on a list. `h5py` has consequently been removed as a dependency.

## [1.2.2] - 25/05/2022

### Added

- Functions `PDD()` and `finite_PDD()` now accept the optional argument `return_row_groups`, default `False`. If `True`, a tuple is returned `(pdd, groups)` where `groups[i]` contains the indices of the point(s) corresponding to `pdd[i]`. Note that these indices are for the asymmetric unit of the input set, whose indices in ``.motif`` are accessible through ``.asymmetric_unit``.

### Changed

- Readers now read atomic numbers rather than symbols which are better for checking if types align with Earth mover's distance flows.

- Argument `folder` removed from `CifReader`, now whether the path is a directory is checked by `os.path.isdir`.

- Fixed issue where AMD/PDD calculations were producing a RuntimeWarning from NumPy.

## Removed

- SDDs removed for now until theory is complete.

- include_if and extract_data removed from readers.

## [1.2] - 14/04/2022

### Added

- Reconstructing periodic sets from PDDs added. Recently it was shown the PDD is complete in a general position and it is possible to reconstruct a periodic set from its PDD with large enough k. The first (inefficient) implementation of this algorithm has be added in the `reconstruct` module.
  
- Higher-order PDDs (the order parameter of `amd.PDD()` and `amd.PDD_finite()`) are removed and replaced with `amd.SDD()` (simplex-wise distance distribution). This invariant is only appropriate for finite sets, but first-order SDDs are equivalent to PDDs. Comparing SDDs is possible with `amd.compare.SDD_EMD()`.

- `CifReader` can now read a folder of .cifs or other files with the optional folder argument (True/False).

### Changed

- `amd.finite_AMD` and `amd.finite_PDD` changed to `amd.AMD_finite` and `amd.PDD_finite` for easier autocompletion.

- Function `amd.compare.neighbours_from_distance_matrix` moved to `amd.utils.neighbours_from_distance_matrix`.

- Changed how the readers handle disorder to be simpler. Now, if `disorder='skip'` then any disorder means the structure is skipped, even if the disordered atom(s) would have been removed e.g. by remove_hydrogens. If `disorder='all_sites'`, no warnings are printed for any overlapping sites in the structure.

### Removed

- Higher-order PDDs (the order parameter of `amd.PDD()` and `amd.PDD_finite()`) are removed and replaced with `amd.SDD()` (simplex-wise distance distribution). This invariant is only appropriate for finite sets, but first-order SDDs are equivalent to PDDs.

- Removed several functions which were bloating the package. List of removed functions/modules: `auto`, `ccdc_utils`, `periodicset.PeriodicSet.to_dict`, `io.SetReader.extract_tags`, `compare.mst_from_distance_matrix`, `compare.filter`, `compare.AMD_mst`, `compare.PDD_mst`, `utils.extract_tags`, `utils.neighbours_df_dict`. Also removed parameter `k` in functions in `compare`, and the `verbose` parameter (instead controlled by `compare.set_verbose()`).

- `utils.ETA` is removed and replaced by the progressbar2 package which is now a dependency.

## [1.1.7] - 01/02/2022

### Added

- Higher-order PDDs added. The parameter `order` of `amd.PDD` selects the PDD order (changed from before when it controlled lexicographically sorting the rows, which has been changed to `lexsort`), it can be any int, default `order=1`, the regular PDD. This infinite sequence of invariants grow in complexity but contain more information.

- AMD and PDD functions for finite point sets, `amd.finite_AMD()` and `amd.finite_PDD()`. `amd.finite_PDD()` accepts the new `order` parameter.

- Documentation is now available on [readthedocs](https://average-minimum-distance.readthedocs.io/en/latest/).

### Changed

- Parameter `order` of `amd.PDD` no longer refers to lexicographically ordering the rows, this has been changed to `lexsort`. Higher-order PDDs are now implemented and `order` refers to the order of the PDD (default 1).

- Fixed/reworked the `ccdc` Reader (especially for disorder). The disorder option 'ordered_sites' now does not remove all atoms with partial occupancy; rather it essentially (for the `ccdc` reader) uses the motif of entry.molecule instead of entry.disordered_molecule (removes atoms whose label ends with ?), so the result should look like some feasible ordered structure.

## [1.1.6] - 29/11/2021

### Added

- Optional parameter low_memory added to AMD comparison functions. Uses a slower but more memory efficient method, useful for larger collections of AMDs.

- The functions `amd.utils.extract_tags()` and `SetReader.extract_tags()` return a `dict` containing the scalar (strings and numbers) tags of the PeriodicSets in the list/reader. The format of the returned dictionary is easily passable to `pandas.DataFrame()`.

- To compliment the addition of `.to_dict()`, the `CifReader` and `CSDReader` now have ways to extract additional data from `ccdc.entry.Entry` objects (later `ase` CifBlocks). The parameter `extract_data` can be passed as a dictionary with data (column) titles as keys and callable functions as values, which take the Entry object and return the data. E.g. if the custom function `get_density()` takes the entry and returns the density, use `extract_data={'Density': get_density}`, then the PeriodicSets will have the tag 'Density' with a value given by get_density(entry). This approach is flexible to any function, but some common ones are included in `amd.io.ccdc_utils`.

- `CifReader` and `CSDReader` accept `include_if` parameter, which can be `None` or a list of callable objects. This can be used to discard structures with specific properties. If `include_if` is a list, the `Entry`/`CifBlock` is passed to each callable and is skipped if any do not return `True`.

### Changed

- The main README has been simplified; the old one read more like documentation than an introduction to the package. Details in the old README have moved to dedicated documentation.

- Bug fixes: infinite recursion in `PeriodicSet.__getattr__`; undetected equivalent sites with `ase` reader.

### Removed

- Deprecated functions `amd.compare()` and the lower case versions of functions e.g. `amd.amd()`, `amd.amd_pdist()`, etc, have been removed. Also removed is the deprecated optional parameter `types=True` for the readers; atomic types are now always read.

- The option to pass a range of k values to comparison functions, along with the optional parameter `ord`, have been removed. Comparing over a range of k can be useful, but often its not if the range of distances aren't stored. No computational savings were really made in the function as opposed to a naive approach.

## [1.1.5] - 02/11/2021

### Added

- SetReader has additional convenient functions `.keys()` which generates all names (keeping order) and `.family(refcode)` which generates only items whose name starts with the string `refcode`.

- `CSDReader` has the function `.entry(refcode)` which returns a `PeriodicSet` given a `ccdc` refcode. This can be any refcode, not just those given when the reader is initialised.

### Changed

- EMD has updated internals which are 2-3x faster.

## [1.1.4] - 13/09/2021

### Added

- Major changes were made to some internals of the CIF and CSD readers, as well as AMD/PDD computation functions. Now, a `PeriodicSet` read from one of these readers will contain the tags `'asymmetric_unit'` and `'wyckoff_multiplicities'`. Since equivalent sites have the same environment, it's only necessary to compute nearest neighbour distances for atoms in the asymmetric unit, and the PDD weights can be computed from the multiplicities. For crystals with an asymmetric unit, this improves AMD/PDD computation speed, PDD size and EMD speed.

### Changed

- **Functions `amd.amd()` and `amd.pdd()` are deprecated, replaced with `amd.AMD()` and `amd.PDD()`. The 'amd' and 'pdd' in the names of all functions have been capitalized and old versions deprecated**. It was a bad idea to have a function named `amd` in a package of the same name.

- The earth mover's distance algorithm no longer incorrectly divides by 1e+6. All earth mover's distances from this update will be 1e+6 times larger than before.

- `ase` and `h5py` are no longer an optional dependencies but required. `numba` was also added to dependencies as it was missing.

- The optional keyword argument `types` is no longer used for the readers; types are read in regardless.

## [1.1.1] - 18/07/2021

### Added

- `PeriodicSet` now implements `__getattr__` to search tags for the attribute, e.g. if atomic types are in the set's tags under the name `'types'` it can now be accessed by `set.types`.

- The function `neighbours_from_distance_matrix(n, dm)` takes an integer and a distance matrix and returns information on the `n` nearest neighbours.

### Changed

- Readers no longer 'normalise' the output by rounding and lexicographically sorting. Sorting the motif means the list of types must be sorted as well, so it's now left in the order it appears in the .CIF (sans symops).

- Fixed bug reading .CIFs whose symmetric operators don't start with the identity.

## [1.1.0] - 01/07/2021

### Added

- Several functions for comparison:
  - `amd_pdist` and `pdd_pdist` compare one collection pairwise by AMD/PDD respectively
  - `amd_cdist` and `pdd_cdist` compare one collection vs another by AMD/PDD respectively
  - `filter` takes PDDs. It gets the n closest items to every item by AMDs, then calculates PDD distances for these comparisons only. This does `n * len(input)` PDD comparisons instead of `len(input)` choose 2 for `pdist`, or `len(input_1) * len(input_2)` for `cdist`.
  - `amd_mst` and `pdd_mst` take a collection of AMDs/PDDs respectively and return edges of a minimum spanning tree.

  All of these functions support a range of metrics, any integer k (less than the input's max k) or range of k. The PDD functions include a verbose argument which prints an ETA to the terminal.

- The `SetWriter` and `SetReader` objects write and read `PeriodicSet`s as compressed .hdf5 files (requires `h5py`). Optionally accepts any keyword arguments, stored alongside the sets (intended to store AMDs and PDDs).

- `CifReader` and `CSDReader` no longer take the optional Boolean parameter `allow_disorder`, but instead the parameter `disorder` which can be any out of {`'skip'`, `'ordered_sites'`, `'all_sites'`}. `allow_disorder=False` is now `disorder='skip'` (default: skip disordered structures), `allow_disorder=True` is now `disorder='all_sites'` (take all sites ignoring any disorder) and newly added `disorder='ordered_sites'` reads in the set but removes disordered sites.

- `PeriodicSet`s now have an attribute `.tags`, a dictionary storing any additional information. This data is saved with the `PeriodicSet` if written with `SetWriter`.

- `CifReader` and `CSDReader` include a parameter `types` (default `False`) which includes a list of atomic types of atoms in the `.tags` dictionary (with key `'types'`) of the `PeriodicSet`s yielded. Access with `set.tags['types']`.

- Requirements now includes version requirements (NumPy>=1.20.1, SciPy>=1.6.1).

### Changed

- The `ase` reader backend has been cleaned up. It no longer handles `ase` `Atoms` or `Spacegroup` objects, which were throwing errors/warnings in some cases. Instead it deals with the tags directly.

- With the `ccdc` reader, if `crystal.molecule.all_atoms_have_sites` is `False` the structure is no longer automatically skipped but a warning is still printed.

- `PeriodicSet` is no longer a wrapped `namedtuple`. A `tuple` (motif, cell) is still accepted by the calculate functions, which dispatch to another function handling each case.

### Removed

- `compare()` has been removed and replaced with `amd_cdist()`.
