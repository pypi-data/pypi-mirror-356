# This test goes through all relevant capailities of easychem, as demonstrated in the getting started documentation.

import numpy as np

from .context import easychem


def test_easychem_single_PT_point():

    exo = easychem.easychem.ExoAtmos()

    exo.solve(1, 1000)

    reacMass = np.load('tests/reference_files/reacMass.npy')
    reacMols = np.load('tests/reference_files/reacMols.npy')

    if not np.allclose(reacMass, exo.reacMass, rtol=1e-13, atol=0.):
        raise AssertionError("ReacMass does not match reference values.")
    if not np.allclose(reacMols, exo.reacMols, rtol=1e-13, atol=0.):
        raise AssertionError("ReacMols does not match reference values.")


def test_easychem_profile_changing_metallicity():

    exo = easychem.easychem.ExoAtmos()

    press = np.logspace(-6, 2, 100)
    temp = np.ones(100) * 1000.
    exo.metallicity = 0.5

    exo.solve(press, temp)

    reacMass = np.load('tests/reference_files/reacMass_Changing_Metallicity_profile.npy')
    reacMols = np.load('tests/reference_files/reacMols_Changing_Metallicity_profile.npy')

    if not np.allclose(reacMass, exo.reacMass, rtol=1e-13, atol=0.):
        raise AssertionError("ReacMass does not match reference values.")
    if not np.allclose(reacMols, exo.reacMols, rtol=1e-13, atol=0.):
        raise AssertionError("ReacMols does not match reference values.")


def test_easychem_profile_changing_metallicity_and_co():

    exo = easychem.easychem.ExoAtmos()

    press = np.logspace(-6, 2, 100)
    temp = np.ones(100) * 1000.
    exo.metallicity = 0.5
    exo.co = 1.2

    exo.solve(press, temp)

    reacMass = np.load('tests/reference_files/reacMass_Changing_CO_profile.npy')
    reacMols = np.load('tests/reference_files/reacMols_Changing_CO_profile.npy')

    if not np.allclose(reacMass, exo.reacMass, rtol=1e-13, atol=0.):
        raise AssertionError("ReacMass does not match reference values.")
    if not np.allclose(reacMols, exo.reacMols, rtol=1e-13, atol=0.):
        raise AssertionError("ReacMols does not match reference values.")

def test_easychem_profile_changing_abundances_manually():

    exo = easychem.easychem.ExoAtmos()

    atom_abundances_solar = exo._atomAbunds.copy()

    atom_names = exo.atoms

    def update_atom_abundances(C_H, O_H, Fe_H):
        modif_abundances = atom_abundances_solar.copy()
        for i_spec, name in enumerate(atom_names):
            if name == 'C':
                modif_abundances[i_spec] = modif_abundances[i_spec] * 10 ** C_H
            elif name == 'O':
                modif_abundances[i_spec] = modif_abundances[i_spec] * 10 ** O_H
            elif name not in ['H', 'He', 'C', 'O']:
                modif_abundances[i_spec] = modif_abundances[i_spec] * 10 ** Fe_H

        return modif_abundances

    Fe_Hs = np.linspace(-1, 1, 20)

    H2Os = np.zeros(20)
    COs = np.zeros(20)
    CH4s = np.zeros(20)
    CO2s = np.zeros(20)
    for i, Fe_H in enumerate(Fe_Hs):
        update_abunds = update_atom_abundances(Fe_H, Fe_H, Fe_H)
        exo.updateAtomAbunds(update_abunds)
        exo.solve(0.001, 1200)
        mass_fractions = exo.result_mass()
        H2Os[i] = mass_fractions['H2O']
        COs[i] = mass_fractions['CO']
        CH4s[i] = mass_fractions['CH4']
        CO2s[i] = mass_fractions['CO2']

    reference_matrix = np.load('tests/reference_files/individual_atomic_abundance_changes_mass_fractions.npy')

    if not np.allclose(H2Os, reference_matrix[:,0], rtol=1e-13, atol=0.):
        raise AssertionError("H2O mass fractions do not match reference values.")
    if not np.allclose(COs, reference_matrix[:,1], rtol=1e-13, atol=0.):
        raise AssertionError("CO mass fractions do not match reference values.")
    if not np.allclose(CH4s, reference_matrix[:,2], rtol=1e-13, atol=0.):
        raise AssertionError("CH4 mass fractions do not match reference values.")
    if not np.allclose(CO2s, reference_matrix[:,3], rtol=1e-13, atol=0.):
        raise AssertionError("CO2 mass fractions do not match reference values.")

def test_moist_adiabatic_gradient():

    earth = easychem.easychem.ExoAtmos()

    atom_names = ['N', 'O', 'H']
    atom_abundances = np.array([0.7, 0.3, 0.04])  # these are just ballpark relative number fractions
    atom_abundances = atom_abundances / np.sum(atom_abundances)  # normalizing here...
    reactants = ['N2','O2', 'N', 'O', 'H2O', 'H2O(L)', 'H2O(c)']

    earth.atoms = atom_names
    earth.updateAtomAbunds(atom_abundances)
    earth.reactants = reactants

    press = np.logspace(-6, 0, 100)  # 1 microbar to 1 bar
    temp = np.linspace(200, 280, 100)  # Some nice habitable zone temperature

    earth.solve(press, temp)

    nabla_ad_moist = (earth.gamma2 - 1.) / earth.gamma2

    if not np.allclose(nabla_ad_moist, earth.adiabaticGrad, rtol=1e-14, atol=0.):
        raise AssertionError("Moist adiabatic gradient does not match (gamma2 - 1.) / gamma2.")

    nabla_ad_moist_reference = np.load('tests/reference_files/moist_adiabatic_gradient.npy')

    if not np.allclose(nabla_ad_moist, nabla_ad_moist_reference, rtol=1e-13, atol=0.):
        raise AssertionError("Moist adiabatic gradient does not match reference values.")
