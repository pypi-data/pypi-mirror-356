---
title: 'easyCHEM: A Python package for calculating chemical equilibrium abundances in exoplanet atmospheres'
tags:
  - Python
  - astronomy
  - equilibrium chemistry
  - Gibbs minimization
  - exoplanets
authors:
  - name: Elise Lei
    equal-contrib: true
    affiliation: 1 # (Multiple affiliations must be quoted)
  - name: Paul Mollière
    orcid: 0000-0003-4096-7067
    equal-contrib: true # (This is how you can denote equal contributions between multiple authors)
    affiliation: 2
    corresponding: true # (This is how to denote the corresponding author)
affiliations:
 - name: Mines Paris - PSL University, Paris, France
   index: 1
 - name: Max Planck Institute for Astronomy, Heidelberg, Germany
   index: 2

date: 29 August 2024
bibliography: paper.bib

---

# Summary

For modeling the spectra of exoplanets one must know their atmospheric composition.
This is necessary because the abundance of molecules, atoms, ions and condensates
is needed to construct the total cross-section for the interaction between electro-magnetic
radiation and matter.  In addition, when solving for the temperature structure of an
atmosphere the so-called adiabatic temperature gradient must be known,
which prescribes the pressure-temperature dependence in convectively unstable regions[^1].
Depending on the planetary properties, the composition and adiabatic gradients may be well
described by equilibrium chemistry, which means that
chemical reactions occur faster than any other processes in the atmosphere, such as mixing.
What is more, the equilibrium assumption often serves as a useful starting point for
non-equilibrium calculations. Efficient and easy-to-use codes for determining equilibrium
abundances are therefore needed.

[^1]: The corresponding convective region is called "troposphere" on Earth.

# Statement of need

easyCHEM is a Python package for calculating chemical equilibrium abundances (including condensation) and adiabatic gradients by minimization of the so-called Gibbs free energy.
easyCHEM implements the equations presented in @Gordon:1994 (which details the
theory behind NASA's [CEA equilibrium code](https://www1.grc.nasa.gov/research-and-engineering/ceaweb/)) from scratch in modern Fortran,
and wraps them in Python to provide an easy-to-use package to the community.
For efficient matrix inversion, required for the Gibbs minimization,
easyCHEM incorporates the optimized `dgesv` routine of the [LAPACK library](https://netlib.org/lapack/explore-html-3.6.1/d7/d3b/group__double_g_esolve_ga5ee879032a8365897c3ba91e3dc8d512.html).
Users can interact with easyCHEM's `ExoAtmos` class to calculate atmospheric
compositions with just a few lines of code. Users have full control
over the atmospheric elemental composition and chemical reactant selection.

The CEA code itself is written in a fixed-form FORTRAN77 style
and interacted with the user via input files. In @Molliere:2017 we introduced
easyCHEM as a from-scratch implementation using the @Gordon:1994 equations
and modern Fortran, without the need for input files for run specification.
easyCHEM was benchmarked with CEA, leading to identical results. It was also
successfully benchmarked with other equilibrium chemistry codes in @Baudino:2017.
easyCHEM calculations have been used in many publications,
such as @Nasedkin:2024 and @deRegt:2024, to name a few recent ones.
Here we report on the Python-wrapped version and make all of its source code public,
to further increase its usefulness and accessibility.

We note that other open-source Python packages for computing chemical equilibrium abundances exist,
such as [TEA](https://github.com/dzesmin/TEA) [@Blecic:2016] or [FastChem](https://newstrangeworlds.github.io/FastChem/index.html) [@Kitzmann:2024].


[//]: # (# Acknowledgements)

[//]: # ()
[//]: # (We acknowledge contributions from Brigitta Sipocz, Syrtis Major, and Semyeong)

[//]: # (Oh, and support from Kathryn Johnston during the genesis of this project.)

# References