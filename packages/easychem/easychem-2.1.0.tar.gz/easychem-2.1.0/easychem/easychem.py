import numpy as np
from easychem.ecfortran import easychem_fortran_source as ecf
import os

HOME_PATH = os.path.expanduser("~")
MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATAFILE = 'thermo_easy_chem_simp_own.inp'


def _find_thermofpath():
    '''
    Returns the path to the default thermodynamic data file (which is in CEA format).

    :returns string:
    Absolute path to the default thermodynamic data file.
    '''
    return os.path.join(MODULE_PATH, DEFAULT_DATAFILE)


class ExoAtmos:
    """
    This is a class that allows to compute the abundances of chemical species in an exoplanet atmosphere for a given
    elemental composition, temperature and pressure.

    Constant attributes:
        ATOM_STR_LEN = 2    Length of the strings for atom names
        REAC_STR_LEN = 15   Length of the strings for reactant names

    Constructor method variables

        :param atoms: Names of the atoms present in the considered atmosphere.
        :type atoms: np.ndarray(str), optional

        :param reactants: Names of the reactants present in the considered atmosphere.
        :type reactants: np.ndarray(str), optional

        :param atomAbunds: Atom abundances in the considered atmosphere (default: stellar abundances).
        :type atomAbunds: np.ndarray(float) with same size as `atoms`, optional

        :param thermofpath: Path of the file containing all the thermodynamic data
        :type thermofpath: str, optional

        :param metallicity: Global metallicity of the considered atmosphere. If set, will update the atom abundances
        accordingly.
        :type metallicity: float, optional

        :param co: The overall carbon-to-oxygen ratio in the considered atmosphere. If set, will update the oxygen
        abundance accordingly.
        :type co: float, optional

        :param atmFunc: Custom function taking `self._atoms` and `self._atomAbundsOrig` as parameters to compute
        updated atom abundances stored in `self._atomAbunds`.
        :type atmFunc: function taking at least two parameters (np.ndarray(str) and np.ndarray(float) with same size)
        and returning a np.ndarray(float) of the same size, optional

        :param atmArgs: Additional arguments to provide to `atmFunc`. If provided, `atmFunc` must also be provided.
        :type atmArgs: iterative, optional
    """

    ATOM_STR_LEN = 2
    REAC_STR_LEN = 15

    def __init__(
            self,
            atoms=None,
            reactants=None,
            atomAbunds=None,
            thermofpath=None,
            metallicity=None,
            co=None,
            atmFunc=None,
            atmArgs=None
    ):
        """
        Constructor method

        :param atoms: Names of the atoms present in the considered atmosphere.
        :type atoms: np.ndarray(str), optional

        :param reactants: Names of the reactants present in the considered atmosphere.
        :type reactants: np.ndarray(str), optional

        :param atomAbunds: Atom abundances in the considered atmosphere (default: solar abundances, following
        Asplund et al. 2009).
        :type atomAbunds: np.ndarray(float) with same size as `atoms`, optional

        :param thermofpath: Path of the file containing all the thermodynamic data
        :type thermofpath: str, optional

        :param metallicity: Global metallicity of the considered atmosphere. If set, will update the atom
        abundances accordingly.
        :type metallicity: float, optional

        :param co: The overall carbon-to-oxygen ratio in the considered atmosphere. If set, will update the oxygen
        abundance accordingly, while keeping carbon fixed. This may change the overall metallicity.
        :type co: float, optional

        :param atmFunc: Custom function taking `self._atoms` and `self._atomAbundsOrig` as parameters to compute
        updated atom abundances stored in `self._atomAbunds`.
        :type atmFunc: function taking at least two parameters (np.ndarray(str) and np.ndarray(float) with same size)
        and returning a np.ndarray(float) of the same size, optional

        :param atmArgs: Additional arguments to provide to `atmFunc`. If provided, `atmFunc` must also be provided.
        atmArgs can be a single value
        or an iterable (e.g., a list, a tuple, or a numpy array).
        :type atmArgs: iterative, optional
        """

        self._initialized = False
        self._solved = False
        self._valid = True
        if atoms is None:
            self._atoms = np.array(['H', 'He', 'C', 'N', 'O', 'Na', 'Mg', 'Al', 'Si', 'P',
                                    'S', 'Cl', 'K', 'Ca', 'Ti', 'V', 'Fe', 'Ni'])
        else:
            self._atoms = np.array(atoms)

        if reactants is None:
            self._reactants = np.array(['H', 'H2', 'He', 'O', 'C', 'N', 'Mg', 'Si', 'Fe', 'S', 'Al', 'Ca', 'Na', 'Ni',
                                        'P', 'K', 'Ti', 'CO', 'OH', 'SH', 'N2', 'O2', 'SiO', 'TiO', 'SiS', 'H2O', 'C2',
                                        'CH', 'CN', 'CS', 'SiC', 'NH', 'SiH', 'NO', 'SN', 'SiN', 'SO', 'S2', 'C2H',
                                        'HCN', 'C2H2,acetylene', 'CH4', 'AlH', 'AlOH', 'Al2O', 'CaOH', 'MgH', 'MgOH',
                                        'PH3', 'CO2', 'TiO2', 'Si2C', 'SiO2', 'FeO', 'NH2', 'NH3', 'CH2', 'CH3', 'H2S',
                                        'VO', 'VO2', 'NaCl', 'KCl', 'e-', 'H+', 'H-', 'Na+', 'K+', 'PH2', 'P2', 'PS',
                                        'PO', 'P4O6', 'PH', 'V', 'FeH', 'VO(c)', 'VO(L)', 'MgSiO3(c)', 'SiC(c)',
                                        'Fe(c)', 'Al2O3(c)', 'Na2S(c)', 'KCl(c)', 'Fe(L)', 'SiC(L)',
                                        'MgSiO3(L)', 'H2O(L)', 'H2O(c)', 'TiO(c)', 'TiO(L)',
                                        'TiO2(c)', 'TiO2(L)', 'H3PO4(c)', 'H3PO4(L)'])
        else:
            self._reactants = np.array(reactants)

        if atomAbunds is None:
            self._atomAbundsOrig = np.array([0.9207539305, 0.0783688694, 0.0002478241, 6.22506056949881E-05,
                                             0.0004509658, 1.60008694353205E-06, 3.66558742055362E-05, 0.000002595,
                                             0.000029795, 2.36670201997668E-07, 1.2137900734604E-05,
                                             2.91167958499589E-07, 9.86605611925677E-08, 2.01439011429255E-06,
                                             8.20622804366359E-08, 7.83688694089992E-09, 2.91167958499589E-05,
                                             1.52807116806281E-06])
        else:
            self._atomAbundsOrig = atomAbunds
        self._atomAbunds = self._atomAbundsOrig.copy()

        assert self._atoms.size == self._atomAbunds.size, ('The arrays containing the atoms names and '
                                                           'abundances should have the same size.')

        if thermofpath is None:
            self._thermofpath = _find_thermofpath()
        else:
            self._thermofpath = thermofpath

        if atmFunc is None:
            if metallicity is not None:
                self._metallicity = metallicity
                self._updatemetallicity()
            if co is not None:
                self.check_co_value_is_valid(co)
                self._co = co
                self._updateCO()
        else:
            self._atmFunc = atmFunc
            self._atmArgs = atmArgs
            self._updadeWithFunc()

        self._normAbunds()

    #
    # PROPERTIES
    #

    # ATOMS : array of atoms present in the atmosphere
    @property
    def atoms(self):
        """
        Type: array of strings. Lists of the atom building blocks considered for the calculation.
        """
        return list(self._atoms)

    @atoms.setter
    def atoms(self, input):
        """
        Setter method for the `atoms` property

        :param input: strings representing the atoms present in the atmosphere.
        :type input: iterative of strings (list or np.ndarray for example)
        """
        tab = np.array(input) if type(input) != np.ndarray else input
        if len(tab) != len(self._atoms) or np.any(tab != self._atoms):
            self._initialized = False
            self._solved = False
            self._atoms = tab

    def updateAtoms(self, input):
        """
        Method to set the `atoms` property to `input` (i.e., change the atoms to be considered in the calculation).

        :param input: strings representing the atoms considered in the calculation.
        :type input: iterative of strings (list or np.ndarray for example)
        """
        self.atoms = input

    # REACTANTS : array of reactants present in the atmosphere
    @property
    def reactants(self):
        """
        Type: array of strings. Names of the reactants to be considered in the calculation.
        """
        return list(self._reactants)

    @reactants.setter
    def reactants(self, input):
        """
        Setter method for the `reactants` property

        :param input: strings representing the reactants considered in the calculation.
        :type input: iterative of strings (list or np.ndarray for example)
        """
        tab = np.array(input) if type(input) != np.ndarray else input
        if len(tab) != len(self._reactants) or np.any(tab != self._reactants):
            self._initialized = False
            self._solved = False
            self._reactants = tab

    def updateReactants(self, input):
        """
        Method to set the `reactants` to be considered in the calculation.

        :param input: strings representing the reactants present in the atmosphere.
        :type input: iterative of strings (list or np.ndarray for example)
        """
        self.reactants = input

    # THERMOFPATH : string containing the path to the thermodynamic data file
    @property
    def thermofpath(self):
        """
        Type: string. Path of the file containing all the thermodynamic data.
        """
        return self._thermofpath

    @thermofpath.setter
    def thermofpath(self, string):
        """
        Setter method for the `thermofpath` property

        :param string: path to the new thermodynamic data file.
        :type string: string
        """
        if self._thermofpath != string:
            self._initialized = False
            self._solved = False
            self._thermofpath = string

    def updateThermofpath(self, string):
        """
        Method to set the path to the thermodynamic input data file.

        :param string: path to the new thermodynamic data file.
        :type string: string
        """
        self.thermofpath = string

    # ATOM ABUNDS ORIG : array of floats corresponding to the elemental abundances for each atom in "atoms",
    # usually the stellar abundances
    @property
    def atomAbundsOrig(self):
        '''Array of floats => elemental abundances of the considered atmosphere, set per default to the solar abundances
         reported in Aplund+2009; This is the base array used to generate atomAbunds by adjusting to metallicity,
         co and/or atmFunc'''
        return self._atomAbundsOrig

    @atomAbundsOrig.setter
    def atomAbundsOrig(self, tab):
        self.check_atom_abundances_values_are_valid(tab)
        assert self._atoms.size == tab.size, ('The arrays containing the atoms names and abundances should have'
                                              'the same size.')
        self._solved = False
        self._atomAbundsOrig = tab
        self._atomAbunds = tab.copy()
        self._updateAtomAbunds()

    def updateAtomAbundsOrig(self, tab):
        '''
        Method to update the default atomic abundances (these will be normalized to sum to 1 after setting).

        :param tab:  array of floats, elemental abundances of the considered atoms (number fractions).
        :type tab: np.ndarray(float)
        '''
        self.atomAbundsOrig = tab

    # ATOM ABUNDS : array of floats, elemental abundances ; array used in computation
    @property
    def atomAbunds(self):
        '''Array of floats => elemental abundances of the considered atmosphere ; array used in chemistry computation'''
        return self._atomAbunds

    @atomAbunds.setter
    def atomAbunds(self, tab):
        self.check_atom_abundances_values_are_valid(tab)
        assert self._atoms.size == tab.size, ('The arrays containing the atoms names and'
                                              'abundances should have the same size.')
        self._solved = False
        self._atomAbundsOrig = tab
        self._atomAbunds = tab.copy()
        self._normAbunds()

    def updateAtomAbunds(self, tab):
        '''
        Method to update the atomic abundances (these will be normalized to sum to 1 after setting) which define the
        building blocks from which molecules can be build during the chemistry calculation.

        :param tab:  array of floats, elemental abundances of the considered atoms (number fractions).
        :type tab: np.ndarray(float)
        '''
        self.atomAbunds = tab

    # metallicity : global metallicity of atmosphere, computation considers that atomAbundsOrig
    # represents the stellar abundances
    @property
    def metallicity(self):
        '''Float => atmosphere's metallicity ; when set this automatically updates atomAbunds considering
        atomAbundsOrig as the stellar abundances (incompatible with atmFunc, if atmFunc is set,
        priority is given to atmFunc)'''
        return self._metallicity

    @metallicity.setter
    def metallicity(self, value):
        self._solved = False
        self._metallicity = value
        self._atomAbunds = self._atomAbundsOrig.copy()
        self._updateAtomAbunds()

    def updatemetallicity(self, value):
        ''' Method to update the metallicity, which will automatically update the atomAbunds.
        Alternatively, the user can set the metallicity by setting eo.metallicity = value,
        where eo is an ExoAtmos object.
        This would also automatically update the atomAbunds.

        :param value: the desired metallicity.'''
        self.metallicity = value

    @metallicity.deleter
    def metallicity(self):
        self._solved = False
        del self._metallicity
        self._atomAbunds = self._atomAbundsOrig.copy()
        self._updateAtomAbunds()

    # CO : C/O ratio
    @property
    def co(self):
        '''Float => C/O number ratio ; automatically updates atomAbunds (if atmFunc is set, atmFunc will be
        applied first)

        Note that the C/O is changed by setting the oxygen abundance to carbon abundance/(C/O). This means that this
        operation will change the overall atmospheric metallicity, since only the oxygen abundance changes, while all
        other metal abundances remain the same (but note that all atom abundances, including H/He are normalized to sum
        to unity after any update step of the atom abundances). To exercise a finer control over the composition, the
        use of updateAtomAbunds() is recommended, which allows the user to set the
        abundances of all elements independently. In that case users may renormalize the metal abundances after
        changing the oxygen (or carbon) abundance for an updated C/O ratio. Options could include conserving the
        metal atom mass or number, in comparison to H/He.

        :param value: the desired C/O ratio. Just udpdate by setting eo.co = value, where eo is an ExoAtmos object.'''

        return self._co

    @co.setter
    def co(self, value):
        '''
        Setter for the co variable, which encodes the C/O number ratio.
        Note that the C/O is changed by setting the oxygen abundance to carbon abundance/(C/O). This means that this
        operation will change the overall atmospheric metallicity, since only the oxygen abundance changes, while all
        other metal abundances remain the same (but note that all atom abundances, including H/He are normalized to sum
        to unity after any update step of the atom abundances). To exercise a finer control over the composition, the
        use of updateAtomAbunds() is recommended, which allows the user to set the
        abundances of all elements independently. In that case users may renormalize the metal abundances after
        changing the oxygen (or carbon) abundance for an updated C/O ratio. Options could include conserving the
        metal atom mass or number, in comparison to H/He.
        :param value: the desired C/O ratio. Just udpdate by setting eo.co = value, where eo is an ExoAtmos object.
        '''
        self.check_co_value_is_valid(value)
        self._solved = False
        self._co = value
        self._atomAbunds = self._atomAbundsOrig.copy()
        self._updateAtomAbunds()

    def updateCo(self, value):
        '''
        Method to update the C/O ratio, which will automatically update the atomAbunds.
        Alternatively, the user can set the C/O ratio by setting eo.co = value, where eo is an ExoAtmos object.
        This would also automatically update the atomAbunds.

        :param value: the desired C/O ratio.
        '''
        self.co = value

    @co.deleter
    def co(self):
        self._solved = False
        del self._co
        self._atomAbunds = self._atomAbundsOrig.copy()
        self._updateAtomAbunds()

    # ATMFUNC : custom function provided by user to tinker the elemental abundances in any way they like
    @property
    def atmFunc(self):
        '''Function provided by the user that takes in atomAbundsOrig to generate atomAbunds.
        The function should take at least two parameters: the first is a list of atom names (self._atoms),
        the second is the original atom abundances (self._atomAbundsOrig). If a third parameter is provided,
        it will be passed as the third argument to the function. The third optional parameter must an iterable
        (e.g., a list, a tuple, or a numpy array) if provided and can contain any parameters that the user
        wants to use to modify the atom abundances. If just a single value should be applied, make sure to package it
        as in iterable (e.g., a list or a tuple with just one element). These parameters can be updated by setting
        the atmArgs property.'''
        return self._atmFunc

    def updateAtmFunc(self, func, args=None):
        '''
        Method to update the atmFunc function and apply it to atomAbundsOrig to update atomAbunds.

        :param func: new atmFunc function.
        :param args: None or iterable => arguments to pass to atmFunc, if required.
        '''
        self._solved = False
        self._atmFunc = func
        self._atmArgs = args
        self._atomAbunds = self._atomAbundsOrig.copy()
        self._updateAtomAbunds()

    @property
    def atmArgs(self):
        '''None or iterable => arguments to pass to self._atmFunc, containing any parameters that the user
        wants to use to modify the atom abundances. If just a single value should be applied, make sure to package it
        as in iterable (e.g., a list or a tuple with just one element). Changing atmArgs will automatically
        result in applying _atmFunc to the original atom abundances (self._atomAbundsOrig) with the new atmArgs.
        '''
        return self._atmArgs

    @atmArgs.setter
    def atmArgs(self, args):
        self._solved = False
        self._atmArgs = args
        self._atomAbunds = self._atomAbundsOrig.copy()
        self._updadeWithFunc()
        self._normAbunds()

    def updateAtmArgs(self, args):
        '''
        Function to update the atmArgs, which contains the arguments to be passed to the atmFunc function.
        If atmFunc is set, this will automatically apply the atmFunc to the original atom abundances, using
        the new atmArgs.

        :param args: None or iterable => arguments to pass to atmFunc, if required.
        :return:
        '''
        self.atmArgs = args

    def delAtmFunc(self):
        self._solved = False
        del self._atmFunc
        self._atmArgs = None
        self._atomAbunds = self._atomAbundsOrig.copy()
        self._updateAtomAbunds()

    @property
    def initialized(self):
        '''Flag indicating if the Fortran side was initialized (e.g., reading the thermodynamic data
        for the requested reactants).'''
        return self._initialized

    @property
    def solved(self):
        '''Flag indicating if the system with the current given parameters is already solved, i.e., if the object
        already contains the chemical abundances.'''
        return self._solved

    @property
    def valid(self):
        '''Flag indicating if the last run was successful, i.e., no error occurred in Fortran.'''
        return self._valid

    @property
    def reacMols(self):
        '''result => reactants' number fractions after the chemistry calculation.'''
        return self._getterResults('_reacMols', "reactants' molecular abundances")

    @property
    def reacMass(self):
        '''result => reactants' mass fractions after the chemistry calculation.'''
        return self._getterResults('_reacMass', "reactants' mass fractions")

    # ADIABATIC GRAD : result => adiabatic gradient
    @property
    def adiabaticGrad(self):
        '''result => adiabatic gradient, i.e., dlogT/dlogP assuming adiabatic conditions.'''
        return self._getterResults('_adiabaticGrad', "adiabatic gradient")

    @property
    def gamma2(self):
        '''result => gamma2, i.e., the adiabatic exponent for which it holds that dlogP/dlogT = (gamma2-1) / gamma2.'''
        return self._getterResults('_gamma2', '')

    @property
    def mmw(self):
        '''result => mean molecular weight, i.e., the mean mass of a molecule in the atmosphere in the
        reactant gas mixture.'''
        return self._getterResults('_mmw', 'mean molecular weight')

    @property
    def density(self):
        '''result => mean density of the reactant gas mixture.'''
        return self._getterResults('_density', 'mean density')

    @property
    def c_pe(self):
        '''result => specific heat capacity at constant pressure of the reactant mixture.
        the e in c_pe stands for "equilibrium", denoting that it assumes that the chemical equilibrium is reached
        instantaneously when the temperature and pressure are changed adiabatically (it thus contains contributions
        from considering the current chemical abundances and how these would change under
        adiabatic changes of temperature and pressure).'''
        return self._getterResults('_c_pe', '')

    #
    # USER METHODS
    #

    def solve(self, pressure, temperature):
        """
        Method to compute the chemical abundances.

        :param pressure: pressure in the atmosphere. Can be a single value or an array of values.
        :type pressure: float, or np.ndarray of floats
        :param temperature: temperature in the atmosphere (in K). Can be a single value or an array of values.
        :type temperature: float, or np.ndarray of floats
        """

        self.check_pressure_values_are_valid(pressure)
        self.check_temperature_values_are_valid(temperature)

        if not self._initialized:
            atoms = ExoAtmos.strArr_to_bytArr(self._atoms, ExoAtmos.ATOM_STR_LEN)
            react = ExoAtmos.strArr_to_bytArr(self._reactants, ExoAtmos.REAC_STR_LEN)
            ecf.set_data(atoms, react, self.thermofpath)
            self._initialized = True

            gotError = bool(ecf.error)
            if gotError:
                msg = bytes(ecf.err_msg).decode()
                raise ValueError(msg.rstrip())

        self._valid = True
        n_reac = len(self._reactants)

        try:
            n_prof = len(pressure)
            isProfile = True
        except TypeError:
            isProfile = False

        if isProfile:
            if len(pressure) != len(temperature):
                raise ValueError("Pressure and temperature arrays aren't of the same size")
            if not self._solved or self._reacMols.shape != (n_prof, n_reac):
                self._reacMols = np.empty((n_prof, n_reac))
                self._reacMass = np.empty((n_prof, n_reac))
                self._adiabaticGrad = np.empty(n_prof)
                self._gamma2 = np.empty(n_prof)
                self._mmw = np.empty(n_prof)
                self._density = np.empty(n_prof)
                self._c_pe = np.empty(n_prof)
            for i in range(n_prof):
                mol, mass, nabla_ad, gamma2, mmw, rho, c_pe = ecf.easychem('q',
                                                                           '',
                                                                           n_reac,
                                                                           self._atomAbunds,
                                                                           temperature[i],
                                                                           pressure[i])

                gotError = bool(ecf.error)
                if gotError:
                    msg = bytes(ecf.err_msg).decode()
                    print('T={:.2e} ; P={:.2e}\t'.format(temperature[i], pressure[i]), msg.rstrip())
                    mol, mass, nabla_ad, gamma2, mmw, rho, c_pe = np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan
                    self._valid = False

                self._reacMols[i] = mol
                self._reacMass[i] = mass
                self._adiabaticGrad[i] = nabla_ad
                self._gamma2[i] = gamma2
                self._mmw[i] = mmw
                self._density[i] = rho
                self._c_pe[i] = c_pe

        else:
            mol, mass, nabla_ad, gamma2, mmw, rho, c_pe = ecf.easychem('q',
                                                                       '',
                                                                       n_reac,
                                                                       self._atomAbunds,
                                                                       temperature,
                                                                       pressure)

            gotError = bool(ecf.error)
            if gotError:
                msg = bytes(ecf.err_msg).decode()
                print(msg)
                mol, mass, nabla_ad, gamma2, mmw, rho, c_pe = np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan
                self._valid = False

            self._reacMols = mol
            self._reacMass = mass
            self._adiabaticGrad = nabla_ad
            self._gamma2 = gamma2
            self._mmw = mmw
            self._density = rho
            self._c_pe = c_pe

        self._solved = True

    def result_mol(self):
        '''
        Returns the reactants' number fractions after the chemistry calculation as a dictionary.
        The keys are the reactant names and the values are the corresponding number fractions.

        :return: dictionary with reactant names as keys and their number fractions as values.
        '''
        if self.reacMols.ndim >= 2:
            return dict(zip(self._reactants, self.reacMols.T))
        else:
            return dict(zip(self._reactants, self.reacMols))

    def result_mass(self):
        '''
        Returns the reactants' mass fractions after the chemistry calculation as a dictionary.
        The keys are the reactant names and the values are the corresponding mass fractions.

        :return: dictionary with reactant names as keys and their mass fractions as values.
        '''
        if self.reacMass.ndim >= 2:
            return dict(zip(self._reactants, self.reacMass.T))
        else:
            return dict(zip(self._reactants, self.reacMass))

    #
    # INTERNAL METHODS
    #

    def _updatemetallicity(self):
        for i in range(self._atomAbunds.size):
            if self._atoms[i].upper() != 'H' and self._atoms[i].upper() != 'HE':
                self._atomAbunds[i] = self._atomAbundsOrig[i] * 10**self._metallicity

    def _updateCO(self):
        atomsUp = np.char.upper(self._atoms)
        iC = np.nonzero(atomsUp == 'C')[0][0]
        iO = np.nonzero(atomsUp == 'O')[0][0]
        self._atomAbunds[iO] = self._atomAbunds[iC] / self._co

    def _updadeWithFunc(self):
        if self._atmArgs is None:
            buffer = self._atmFunc(self._atoms, self._atomAbundsOrig)
        else:
            buffer = self._atmFunc(self._atoms, self._atomAbundsOrig, *self._atmArgs)

        self.check_atom_abundances_values_are_valid(buffer)
        self._atomAbunds = buffer

    def _normAbunds(self):
        self._atomAbunds /= self._atomAbunds.sum()

    def _updateAtomAbunds(self):
        if hasattr(self, '_metallicity'):
            self._updatemetallicity()
        if hasattr(self, '_atmFunc'):
            self._updadeWithFunc()
        if hasattr(self, '_co'):
            self._updateCO()
        self._normAbunds()

    def _getterResults(self, attName, fullName):
        if hasattr(self, attName):
            return getattr(self, attName)
        else:
            if fullName == '':
                raise AttributeError("The wanted quantity hasn't been computed yet... Please run the 'solve' method.")
            else:
                raise AttributeError("The wanted quantity ({}) hasn't been computed yet..."
                                     "Please run the 'solve' method.".format(fullName))

    def print_available_species(self):
        f = open(self._thermofpath, 'r')
        lines = f.readlines()
        f.close()

        i = 1
        for line in lines:
            if line[0] != ' ' and line[0] != '-':
                print(f'{i}: '+line.split(' ')[0])
                i += 1

    @staticmethod
    def strToBytes(a: str):
        return np.array([*a])

    @staticmethod
    def strArr_to_bytArr(a, m):
        # m = np.amax(np.char.str_len(a))
        res = np.empty((len(a), m), dtype='S1', order='F')
        for i, c in enumerate(a):
            res[i] = ExoAtmos.strToBytes(c.ljust(m, ' '))
        return res

    @staticmethod
    def check_co_value_is_valid(co):
        """
        Check if the provided C/O value is valid.

        :param co: The C/O value to check.
        :type co: float, int or np.ndarray
        :raises ValueError: If the C/O value is below 0.
        """
        if not ExoAtmos.check_if_input_values_are_valid(co, lower_bound=0.0):
            raise ValueError("C/O ratio must be >= 0.")

    @staticmethod
    def check_temperature_values_are_valid(temperature):
        """
        Check if the provided temperature value is valid.

        :param temperature: The temperature value to check.
        :type temperature: float, int or np.ndarray
        :raises ValueError: If the temperature value is below 0. K
        """

        if not ExoAtmos.check_if_input_values_are_valid(temperature, lower_bound=0.0):
            raise ValueError("Temperature(s) must be >= 0 K.")

    @staticmethod
    def check_pressure_values_are_valid(pressure):
        """
        Check if the provided pressure value is valid.

        :param pressure: The pressure value to check.
        :type pressure: float, int or np.ndarray
        :raises ValueError: If the pressure is below 0.
        """

        if not ExoAtmos.check_if_input_values_are_valid(pressure, lower_bound=0.0):
            raise ValueError("Pressure(s) must be >= 0.")

    @staticmethod
    def check_atom_abundances_values_are_valid(atom_abunds):
        """
        Check if the provided atom abundances are valid.

        :param atom_abunds: The atom abundances to check.
        :type atom_abunds: np.ndarray
        :raises ValueError: If the atom abundances are below 0.
        """

        if not ExoAtmos.check_if_input_values_are_valid(atom_abunds, lower_bound=0.0):
            raise ValueError("Atom abundances must be >= 0.")

    @staticmethod
    def check_if_input_values_are_valid(values, lower_bound=0., upper_bound=None):
        """
        Check if the provided values are valid.

        :param values: The values to check.
        :type values: float, int or np.ndarray
        :param lower_bound: The lower bound for the values (default is 0).
        :type lower_bound: float, optional
        :param upper_bound: The upper bound for the values (default is None, meaning no upper bound).
        :type upper_bound: float, optional
        :returns bool: True if all values are within the bounds, False otherwise.
        """

        if isinstance(values, np.ndarray):
            if (np.any(values < lower_bound)
                    or (upper_bound is not None and np.any(values > upper_bound))):
                return False
        elif isinstance(values, (int, float)):
            if values < lower_bound or (upper_bound is not None and values > upper_bound):
                return False

        return True
