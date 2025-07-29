# Change Log
All notable changes to easyCHEM will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com)
and this project adheres to [Semantic Versioning](http://semver.org).

## [2.1.0] - 2025-06-18
### Added
- Checks for temperature, C/O, and pressures to be > 0.
- API docstring comments for all necessary methods and attributes.
- Community guidelines to the docs.
- Tox testing.

### Fixed
- Bug when checking for convergence of solid species abundances (thanks Nick Wogan for spotting and repairing!).
- Installation instructions to reflect that pipy also builds from source, and that a C compiler is needed for the installation.

## [2.0.6] - 2024-09-03
### Added
- Method to print all available reactant species in thermo_easy_chem_simp_own.inp.

---
No changelog before version 2.0.5.