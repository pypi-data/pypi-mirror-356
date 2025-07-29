========
easyCHEM
========

.. image:: https://img.shields.io/pypi/v/easychem
   :target: https://pypi.org/project/easychem/
   :alt: Pypi version

.. image:: https://img.shields.io/readthedocs/easychem
   :target: https://easychem.readthedocs.io/en/latest/
   :alt: documentation: https://easychem.readthedocs.io/en/latest/

.. image:: https://img.shields.io/gitlab/license/EliseLei/easychem
   :target: https://gitlab.com/EliseLei/easychem/-/blob/master/LICENSE
   :alt: licence: MIT
                                        
.. image:: https://img.shields.io/badge/DOI-10.1051%2F0004--6361%2F201629800-blue
   :target: https://doi.org/10.1051/0004-6361/201629800
   :alt: DOI: 10.1051/0004-6361/201629800

**easyCHEM: a Python package for calculating equilibrium chemistry abundances of exoplanet atmospheres**

Welcome to the **easyCHEM** repository. easyCHEM is a Python package for calculating chemical abundances in exoplanet atmospheres, assuming equilibrium chemistry. Ancillary outputs are the atmospheric adiabatic temperature gradient and mean molar mass. easyCHEM is a clone of
the equilibrium chemistry part of `NASA's CEA <https://www1.grc.nasa.gov/research-and-engineering/ceaweb/>`_ code, written from scratch
and with numerical stability in mind. In particular, the code implements the
equations described in `Gordon & McBride (1994) <https://ntrs.nasa.gov/api/citations/19950013764/downloads/19950013764.pdf>`_ and makes use of `LAPACK's dgesv routine <https://netlib.org/lapack/explore-html-3.6.1/d7/d3b/group__double_g_esolve_ga5ee879032a8365897c3ba91e3dc8d512.html>`_ for fast matrix inversion. Since we incorporated the ``dgesv`` source code into easyCHEM, users do not require external math libraries.

Documentation
=============
The code documentation, installation guide, and tutorial can be found at `https://easychem.readthedocs.io <https://easychem.readthedocs.io>`_.

Attribution
===========
If you use easyCHEM in your work, please cite the following articles:

- for the easyCHEM base implementation: `Mollière et al. 2017 <https://ui.adsabs.harvard.edu/abs/2017A&A...600A..10M>`_.
- The JOSS paper (Lei & Mollière) is in prep.

License
=======
Copyright 2022-2025 Elise Lei and Paul Mollière

easyCHEM is available under the MIT license.
See the LICENSE file for more information.

``dgesv``, which is part of LAPACK, and which easyCHEM is using, is available under the `BSD license <https://en.wikipedia.org/wiki/BSD_licenses>`_.