Installation
============

Prerequisites for installation
------------------------------
To install easyCHEM, you need the following:

- Python 3.9+,
- a Fortran compiler, for example ``gfortran``,
- a C compiler, for example ``gcc``.

Linux
~~~~~
On Linux, install Python, the Fortran and the C compiler with:

.. code-block:: bash

    sudo apt-get install python python-pip gfortran gcc

On some distributions, ``python`` may need to be replaced with ``python3``.

.. Note:: A general Python recommendation is to use a Python virtual environment such as `venv <https://docs.python.org/3/library/venv.html>`_, `conda <https://docs.anaconda.com/free/anaconda/install/index.html>`_ or or `conda-forge <https://conda-forge.org/download/>`_, to prevent potential conflicts.

Mac OS
~~~~~~

.. important:: On Mac, it is highly recommended to use a Python virtual environment such as `venv <https://docs.python.org/3/library/venv.html>`_ or `conda <https://docs.anaconda.com/free/anaconda/install/index.html>`_ or `conda-forge <https://conda-forge.org/download/>`_ to prevent potential conflicts.

Recommended: using homebrew
^^^^^^^^^^^^^^^^^^^^^^^^^^^

On Mac OS, it is highly recommended to use `homebrew <https://brew.sh/>`_ to install ``gfortran``. Homebrew is able to manage external libraries dependencies and can help you fix broken setups. Other installation methods are more risky by making setup-related errors frequent, difficult to identify and to fix.

To ensure a safe installation, execute first:

.. code-block:: bash

    brew update
    brew upgrade
    brew doctor

A list of suggestions and fixes may be displayed when executing `brew doctor`. It is highly recommended to go through all of them before proceeding.

Then, install the `gfortran` and `gcc` compiler with (on Homebrew the C and Fortran compilers are bundled):

.. code-block:: bash

    brew install gcc

.. note:: In general, ``brew install`` is highly recommended to install all the dependencies (including conda), as this minimizes the risk of conflicts and issues.

Using gfortran disk images
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. warning:: While using **homebrew is the preferred method** for installing external libraries on Mac, alternative methods exist. Use them at your own risk.

François-Xavier Coudert's `github repository <https://github.com/fxcoudert/gfortran-for-macOS>`_ provides gfortran disk images (.dmg) with which you can install gfortran like any other program for Mac, through an installation wizard. Both Apple Silicon (M1, M2, M3) and Intel chip versions are available.

Windows
~~~~~~~

Recommended: using WSL
^^^^^^^^^^^^^^^^^^^^^^
To make the most out of easyCHEM on Windows, it is recommended to use the `Windows Subsystem for Linux <https://learn.microsoft.com/en-us/windows/wsl/install>`_ (WSL).

Follow the WSL installation instructions from the previous link, then install pRT from the WSL terminal, following the same steps as in the Linux case.

Native installation prerequisites
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. Get a Fortran compiler through, for example, `MSYS2 <https://www.msys2.org/>`_ or `Visual Studio <https://visualstudio.microsoft.com/>`_.
2. Go to the `Python website <https://www.python.org/>`_, then download and execute the Python installer.

WSL-native dual installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
easyCHEM can be installed both on the Windows and WSL sides. Files on WSL can be accessed from the Windows side using the path ``\\wsl.localhost\``, and files on Windows can be accessed from the WSL side using ``/mnt`` (e.g., to get into "C:\\Users" from WSL: ``cd /mnt/c/Users``). Note however than accessing files across sides is `slow <https://learn.microsoft.com/en-us/windows/wsl/setup/environment#file-storage>`_.

Pre-installation packages
-------------------------
Before starting the installation of easyCHEM, make sure to install the following Python packages with:

.. code-block:: bash

    pip install numpy meson-python ninja

On some distributions, ``pip`` may need to be replaced with ``pip3``.

easyCHEM Installation
---------------------

Installation from PyPI (using `pip`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To install easyCHEM via pip install just type

.. code-block:: bash

   pip install easychem --no-build-isolation

Be sure to add the ``--no-build-isolation`` flag.

Installation from Gitlab
~~~~~~~~~~~~~~~~~~~~~~~~

Download easyCHEM from `Gitlab <https://gitlab.com/EliseLei/easychem>`_, or clone it from GitLab via

.. code-block:: bash
		
   git clone https://gitlab.com/EliseLei/easychem.git

- In the terminal, enter the easyCHEM folder
- Type the following in the terminal ``pip install .  --no-build-isolation``, and press
  Enter.

Testing the installation
------------------------

Open a new terminal window. Then open python and type:

.. code-block:: python

    import easychem.easychem as ec
    exo = ec.ExoAtmos()
    exo.solve(1, 1000)