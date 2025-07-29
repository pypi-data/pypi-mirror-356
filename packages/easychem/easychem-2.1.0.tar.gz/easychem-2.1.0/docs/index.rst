easyCHEM documentation
======================

Welcome to the **easyCHEM** documentation. easyCHEM is a Python package for calculating chemical abundances in exoplanet atmospheres, assuming equilibrium chemistry and including condensation. Ancillary outputs are the atmospheric adiabatic temperature gradient and mean molar mass. easyCHEM is a clone of
the equilibrium chemistry part of `NASA's CEA <https://www1.grc.nasa.gov/research-and-engineering/ceaweb/>`_ code, written from scratch
and with numerical stability in mind. In particular, the code implements the
equations described in `Gordon & McBride (1994) <https://ntrs.nasa.gov/api/citations/19950013764/downloads/19950013764.pdf>`_ and makes use of `LAPACK's dgesv routine <https://netlib.org/lapack/explore-html-3.6.1/d7/d3b/group__double_g_esolve_ga5ee879032a8365897c3ba91e3dc8d512.html>`_ for fast matrix inversion. Since we incorporated the ``dgesv`` source code into easyCHEM, users do not require external math libraries.

easyCHEM's thermodynamic input data is based on the NASA Glenn thermodynamic input database, which can be accessed `here <https://cearun.grc.nasa.gov/ThermoBuild/>`_. Additional NASA polynomials have been obtained from `Lodders & Fegley (2002) <https://ui.adsabs.harvard.edu/abs/2002Icar..155..393L/abstract>`_, `Visscher et al. (2010) <https://ui.adsabs.harvard.edu/abs/2010ApJ...716.1060V/abstract>`_, or were derived from thermodynamic data in the `NIST-JANAF database <https://janaf.nist.gov>`_ and condensate data listed in `Robie et al. (1978) <https://pubs.usgs.gov/bul/1452/report.pdf>`_. The thermodynamic data of the condensates was extended to low temperatures (60 K) using the method described in Appendix A.2 of `Mollière et al. (2017) <https://ui.adsabs.harvard.edu/abs/2017A&A...600A..10M>`_.

**To get started with some examples on how to run easyCHEM, see our** `"easyCHEM tutorial" <content/notebooks/getting_started.html>`_.

easyCHEM is available under the MIT License, and its base Fortran implementation was described in
`Mollière et al. (2017) <https://ui.adsabs.harvard.edu/abs/2017A&A...600A..10M>`_. It was benchmarked against the CEA code, leading to identical results. It was also compared to the equilibrium chemistry codes used for the ATMO and Exo-REM atmospheric models, again showing excellent agreement, see `Baudino et al. (2017) <https://ui.adsabs.harvard.edu/abs/2017ApJ...850..150B/abstract>`_.

Please cite `Lei & Mollière (2024) <https://arxiv.org/abs/2410.21364>`_ when making use of easyCHEM in your research.

.. _contact: molliere@mpia.de

This documentation webpage contains an `installation guide <content/installation.html>`_, a
`tutorial <content/notebooks/getting_started.html>`_, `community guidelines for contributions  <content/contributing.html>`_, and an `API documentation <autoapi/index.html>`_.

Developers
___________

- Elise Lei and Paul Mollière

.. toctree::
   :maxdepth: 3
   :caption: Content:

   content/installation
   content/notebooks/getting_started
   content/contributing

.. toctree::
   :maxdepth: 2
   :caption: Code documentation
