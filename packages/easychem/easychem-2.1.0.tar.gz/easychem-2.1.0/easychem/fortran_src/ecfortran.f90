!> ------------------------------------
!>        EASY CHEM, a CEA clone
!> ------------------------------------

module easychem_fortran_source
   implicit none
   ! private

   ! public :: SET_DATA
   ! public :: EASYCHEM

   !> Run variables
   integer     :: iter_max
   integer     :: N_atoms, N_reactants, N_gas, N_cond, N_ions
   logical     :: verbose, verbose_cond, quick, ions, remove_ions, error
   character(len=500)   :: err_msg

   !> Constants
   double precision, parameter :: R = 8.3144598d0
   double precision, parameter :: amu = 1.660538921d-24
   double precision, parameter :: kB = 1.3806488d-16
   double precision, parameter :: mol = 6.02214129d23

   !> List of atoms
   character(len=2), allocatable   :: names_atoms(:)  !(N_atoms)
   integer, allocatable            :: id_atoms(:)  !(N_atoms)

   !> List of reactants reordered with condensates at the end
   character(len=15), allocatable  :: names_reactants(:), names_reactants_orig(:)  !(N_reac)
   integer, allocatable            :: id_reactants(:,:)  !(N_reac,2)

   !> Atomic data for each reactant
   character(len=2), allocatable   :: reac_atoms_names(:,:)  !(5,N_reac)
   integer, allocatable            :: reac_atoms_id(:,:)  !(5,N_reac)
   double precision, allocatable   :: reac_stoich(:,:)  !(5,N_reac)

   !> Nature of reactant
   logical, allocatable    :: reac_condensed(:), reac_ion(:)  !(N_reac)

   !> Thermodynamic data arrays
   integer, parameter      :: N_coeffs = 10, N_temps = 10
   integer, allocatable    :: thermo_data_n_coeffs(:,:)  !(N_temps,N_reac)
   integer, allocatable    :: thermo_data_n_intervs(:)  !(N_reac)
   double precision, allocatable   :: thermo_data(:,:,:)  !(N_coeffs,N_temps,N_reac)
   double precision, allocatable   :: thermo_data_temps(:,:,:)  !(2,N_temps,N_reac)
   double precision, allocatable   :: thermo_data_T_exps(:,:,:)  !(8,N_temps,N_reac)
   double precision, allocatable   :: form_heat_Jmol_298_15_K(:)  !(N_reac)
   double precision, allocatable   :: H_0_298_15_K_m_H_0_0_K(:,:)  !(N_temps, N_reac)
   double precision, allocatable   :: mol_weight(:)  !(N_reac)

   !> Atoms & masses, from http://www.science.co.il/PTelements.asp
   integer, parameter      :: N_atoms_save = 104
   character*2, parameter  :: names_atoms_save(N_atoms_save) = &
   (/ 'E ','H ','He','Li','Be','B ','C ','N ','O ','F ','Ne','Na', &
   'Mg','Al','Si','P ','S ','Cl','Ar','K ','Ca','Sc','Ti','V ','Cr','Mn', &
   'Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr','Rb','Sr', &
   'Y ','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb', &
   'Te','I ','Xe','Cs','Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd', &
   'Tb','Dy','Ho','Er','Tm','Yb','Lu','Hf','Ta','W ','Re','Os','Ir', &
   'Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn','Fr','Ra','Ac','Th', &
   'Pa','U ','Np','Pu','Am','Cm','Bk','Cf','Es','Fm','Md','No','Lr' /)
   double precision, parameter  :: masses_atoms_save(N_atoms_save) = &
   amu*(/ 0.000548579909d0, 1.0079d0,4.0026d0,6.941d0,9.0122d0,10.811d0,12.0107d0,14.0067d0 &
   ,15.9994d0,18.9984d0,20.1797d0,22.9897d0,24.305d0,26.9815d0,28.0855d0,30.9738d0,32.065d0 &
   ,35.453d0,39.948d0,39.0983d0,40.078d0,44.9559d0,47.867d0,50.9415d0,51.9961d0,54.938d0,55.845d0 &
   ,58.9332d0,58.6934d0,63.546d0,65.39d0,69.723d0,72.64d0,74.9216d0,78.96d0,79.904d0,83.8d0,85.4678d0 &
   ,87.62d0,88.9059d0,91.224d0,92.9064d0,95.94d0,98d0,101.07d0,102.9055d0,106.42d0,107.8682d0 &
   ,112.411d0,114.818d0,118.71d0,121.76d0,127.6d0,126.9045d0,131.293d0,132.9055d0,137.327d0,138.9055d0 &
   ,140.116d0,140.9077d0,144.24d0,145d0,150.36d0,151.964d0,157.25d0,158.9253d0,162.5d0,164.9303d0 &
   ,167.259d0,168.9342d0,173.04d0,174.967d0,178.49d0,180.9479d0,183.84d0,186.207d0,190.23d0,192.217d0 &
   ,195.078d0,196.9665d0,200.59d0,204.3833d0,207.2d0,208.9804d0,209d0,210d0,222d0,223d0,226d0,227d0,232.0381d0 &
   ,231.0359d0,238.0289d0,237d0,244d0,243d0,247d0,247d0,251d0,252d0,257d0,258d0,259d0,262d0/)

   contains

   !> INITIALIZE ALL DATA
   subroutine set_data(N_atoms_in, N_reactants_in, atoms_char, reac_char, fpath)
      character, intent(in)   :: atoms_char(N_atoms_in,2), reac_char(N_reactants_in,15)
      integer, intent(in)     :: N_atoms_in, N_reactants_in
      character(len=800), intent(in) :: fpath

      interface
      subroutine chrarr_to_stringarr(chr, str)
         character, intent(in)                   :: chr(:,:)         ! row = 1 string
         character(len=size(chr,2)), intent(out) :: str(size(chr,1))
      end subroutine
      end interface

      error = .false.

      ! REACTANTS
      if (N_reactants_in /= N_reactants .and. allocated(names_reactants_orig)) then
         ! Deallocate everything if the number of reactants changed
         deallocate(names_reactants_orig)
         deallocate(names_reactants)
         deallocate(id_reactants)
         deallocate(reac_atoms_names)
         deallocate(reac_atoms_id)
         deallocate(reac_stoich)
         deallocate(reac_condensed)
         deallocate(reac_ion)
         deallocate(thermo_data_n_coeffs)
         deallocate(thermo_data_n_intervs)
         deallocate(thermo_data)
         deallocate(thermo_data_temps)
         deallocate(thermo_data_T_exps)
         deallocate(form_heat_Jmol_298_15_K)
         deallocate(H_0_298_15_K_m_H_0_0_K)
         deallocate(mol_weight)
      end if
      if (.not. allocated(names_reactants_orig)) then
         ! Allocate reactant-related arrays
         N_reactants = N_reactants_in
         allocate(names_reactants_orig(N_reactants))
         allocate(names_reactants(N_reactants))
         allocate(id_reactants(N_reactants,2))
         allocate(reac_atoms_names(5,N_reactants))
         allocate(reac_atoms_id(5,N_reactants))
         allocate(reac_stoich(5,N_reactants))
         allocate(reac_condensed(N_reactants))
         allocate(reac_ion(N_reactants))

         allocate(thermo_data_n_coeffs(N_temps,N_reactants))
         allocate(thermo_data_n_intervs(N_reactants))
         allocate(thermo_data(N_coeffs,N_temps,N_reactants))
         allocate(thermo_data_temps(2,N_temps,N_reactants))
         allocate(thermo_data_T_exps(8,N_temps,N_reactants))
         allocate(form_heat_Jmol_298_15_K(N_reactants))
         allocate(H_0_298_15_K_m_H_0_0_K(N_temps,N_reactants))
         allocate(mol_weight(N_reactants))
      end if

      ! Set names_reactants_orig with the given list of reactants
      call da_CH2STR(reac_char, names_reactants_orig)

      ! Set all thermodynamic data
      call da_READ_THERMO(fpath)
      if (error) RETURN

      ! ATOMS
      if (N_atoms_in+1 /= N_atoms .and. allocated(names_atoms)) then
         deallocate(names_atoms)
         deallocate(id_atoms)
      end if
      if (.not. allocated(names_atoms)) then
         N_atoms = N_atoms_in + 1
         allocate(names_atoms(N_atoms))
         allocate(id_atoms(N_atoms))
      end if

      call da_CH2STR(atoms_char, names_atoms(1:N_atoms_in))
      names_atoms(N_atoms) = 'E'

      call da_ATOMS_ID()
      if (error) RETURN

      call da_REAC_ATOMS_ID()

   end subroutine set_data

   !> Convert a 2-dimensional array of characters into an array of strings ; used in SET_DATA
   subroutine da_CH2STR(chr, str)

      character, intent(in)                   :: chr(:,:)  ! 1 row = 1 string
      character(len=size(chr,2)), intent(out) :: str(size(chr,1))
      integer                                 :: i, j

      str = ''
      do i = 1, size(chr,1)
         do j = 1, size(chr,2)
            str(i) = trim(str(i))//chr(i,j)
         end do
      end do
   end subroutine da_CH2STR

   !> Sets id_atoms, where the i-th cell corresponds to names_atoms(i) and contains the index of the same atom in names_atoms_save
   !> names_atoms_save(id_atoms(i)) = names_atoms(i)
   subroutine da_ATOMS_ID()

      integer           :: i_atom, i_atom_save
      logical           :: change
      character(len=2)  :: atom_upper, atom_upper_save
      character(len=3)  :: num

      do i_atom = 1, N_atoms
         if (trim(names_atoms(i_atom)) == '') then
            id_atoms(i_atom) = -1
            CYCLE
         end if
         change = .false.
         call uppercase(names_atoms(i_atom), atom_upper)
         do i_atom_save = 1, N_atoms_save
            call uppercase(names_atoms_save(i_atom_save), atom_upper_save)
            if (atom_upper == atom_upper_save) then
               id_atoms(i_atom) = i_atom_save
               change = .true.
               exit
            end if
         end do
         if (.not. change) then
            id_atoms(i_atom) = -1
            error = .true.
            write(num, '(i3.3)') i_atom
            err_msg = "READ DATA ERROR: the atom #"//num//" '"//names_atoms(i_atom)//"' was not recognised."
            RETURN
         end if
      end do
   end subroutine da_ATOMS_ID

   subroutine da_REAC_ATOMS_ID()

      integer           :: i_reac, i_atom, i_atom_save
      logical           :: change
      character(len=2)  :: atom_upper, atom_upper_save
      character(len=3)  :: num

      do i_reac = 1, N_reactants
         do i_atom = 1, 5
            if (trim(reac_atoms_names(i_atom,i_reac))=='') then
               reac_atoms_id(i_atom, i_reac) = -1
               CYCLE
            end if
            change = .false.
            call uppercase(reac_atoms_names(i_atom,i_reac), atom_upper)
            do i_atom_save = 1, N_atoms_save
               call uppercase(names_atoms_save(i_atom_save), atom_upper_save)
               if (atom_upper == atom_upper_save) then
                  reac_atoms_id(i_atom,i_reac) = i_atom_save
                  change = .true.
                  EXIT
               end if
            end do
            if (.not. change) then
               reac_atoms_id(i_atom, i_reac) = -1
               error = .true.
               write(num, '(i3.3)') i_atom
               err_msg = "READ DATA ERROR: the atom #"//num//" '"//names_atoms(i_atom)//&
               "' in reactant '"//names_reactants(i_reac)//"' was not recognised."
               RETURN
            end if
         end do
      end do
   end subroutine da_REAC_ATOMS_ID

   !> Read in provided file all thermodynamic data
   subroutine da_READ_THERMO(fpath)

      character(len=800), intent(in) :: fpath
      character(len=80)             :: file_line, file_line_up
      character(len=15)             :: name_reac_up
      integer                       :: i_reac, n_interv, i_interv, i_stoich, stoich_start, reac_found

      reac_found = 0
      thermo_data_n_intervs = -1
      N_gas = 0
      N_ions = 0

      reac_ion = .FALSE.
      ions = .FALSE.

      open(unit=17,file=fpath, action="READ", status="OLD")
      do while (1>0)
         read(17,'(A80)',end=122) file_line
         call uppercase(file_line, file_line_up)
         do i_reac = 1, N_reactants
            call uppercase(names_reactants_orig(i_reac), name_reac_up)

            if (trim(adjustl(file_line_up(1:18))) == trim(adjustl(name_reac_up))) then
               ! Recognized a reactant in file
               reac_found = reac_found+1

               ! Mark it as found
               read(17,'(A80)',end=122) file_line
               read(file_line(1:3),'(I2)') n_interv
               thermo_data_n_intervs(i_reac) = n_interv

               ! Gas or condensate ?
               if (file_line(52:52) == '0') then
                  reac_condensed(i_reac) = .FALSE.
                  N_gas = N_gas + 1
               else
                  reac_condensed(i_reac) = .TRUE.
               end if
            end if

         end do
      end do
      122 close(17)

      ! If not all reactants were found
      if (reac_found /= N_reactants) then
         error = .true.
         err_msg = 'READ DATA ERROR: For the following species no thermodynamical data was found:'
         n_interv = 0
         do i_reac = 1, N_reactants
            if (thermo_data_n_intervs(i_reac) .EQ. -1) then
               if (n_interv == 0) then
                  err_msg = trim(err_msg)//' '//trim(adjustl(names_reactants_orig(i_reac)))
               else
                  err_msg = trim(err_msg)//', '//trim(adjustl(names_reactants_orig(i_reac)))
               end if
            end if
         end do
         RETURN
      end if

      N_cond = N_reactants - N_gas

      ! Puts in names_reactants the ordered list of reactants, sets id_reactants as a link between the two
      call da_REORDER_SPECS()

      ! BASED ON THE ~RIGHT DESCRIPTION GIVEN IN GORDON 1996, page 73 AND THE APPEARANCE OF THERMO.INP.
      open(unit=17,file=fpath, action="READ", status="OLD")
      do while (1>0)
         read(17,'(A80)',end=123) file_line
         call uppercase(file_line, file_line_up)
         do i_reac = 1, N_reactants
            call uppercase(names_reactants(i_reac), name_reac_up)

            if (trim(adjustl(file_line_up(1:18))) == trim(adjustl(name_reac_up))) then
               ! Recognized a reactant in file
               read(17,'(A80)',end=123) file_line
               read(file_line(1:3),'(I2)') n_interv
               thermo_data_n_intervs(i_reac) = n_interv

               stoich_start = 11
               do i_stoich = 1, 5
                  ! Set the atoms for each reactant
                  reac_atoms_names(i_stoich,i_reac) = file_line(stoich_start:stoich_start+1)
                  ! Are there ions to be treated?
                  if (trim(adjustl(reac_atoms_names(i_stoich,i_reac))) == 'E') then
                     ions = .TRUE.
                     reac_ion(i_reac) = .TRUE.
                     N_ions = N_ions + 1
                  end if
                  read(file_line(stoich_start+2:stoich_start+7),'(F6.2)') reac_stoich(i_stoich,i_reac)
                  stoich_start = stoich_start+8
               end do

               read(file_line(53:65),'(F13.5)') mol_weight(i_reac)
               read(file_line(66:80),'(F13.5)') form_heat_Jmol_298_15_K(i_reac)

               do i_interv = 1, 3*n_interv
                  read(17,'(A80)',end=123) file_line
                  if (MOD(i_interv,3) == 1) then
                     read(file_line(2:22),'(F10.3,X,F10.3)') thermo_data_temps(1,i_interv/3+1,i_reac), &
                     thermo_data_temps(2,i_interv/3+1,i_reac)
                     read(file_line(23:23),'(I1)') thermo_data_n_coeffs(i_interv/3+1,i_reac)
                     read(file_line(24:63),'(8F5.1)') thermo_data_T_exps(1,i_interv/3+1,i_reac), &
                     thermo_data_T_exps(2,i_interv/3+1,i_reac), thermo_data_T_exps(3,i_interv/3+1,i_reac), &
                     thermo_data_T_exps(4,i_interv/3+1,i_reac), thermo_data_T_exps(5,i_interv/3+1,i_reac), &
                     thermo_data_T_exps(6,i_interv/3+1,i_reac), thermo_data_T_exps(7,i_interv/3+1,i_reac), &
                     thermo_data_T_exps(8,i_interv/3+1,i_reac)
                     read(file_line(66:80),'(F15.3)') H_0_298_15_K_m_H_0_0_K(i_interv/3+1,i_reac)
                  end if
                  if (MOD(i_interv,3) == 2) then
                     read(file_line(1:80),'(5D16.8)') thermo_data(1,i_interv/3+1,i_reac), &
                     thermo_data(2,i_interv/3+1,i_reac), thermo_data(3,i_interv/3+1,i_reac) , &
                     thermo_data(4,i_interv/3+1,i_reac), thermo_data(5,i_interv/3+1,i_reac)
                  end if
                  if (MOD(i_interv,3) == 0) then
                     read(file_line(1:80),'(5D16.8)') thermo_data(6,i_interv/3,i_reac), &
                     thermo_data(7,i_interv/3,i_reac), thermo_data(8,i_interv/3,i_reac) , &
                     thermo_data(9,i_interv/3,i_reac), thermo_data(10,i_interv/3,i_reac)
                  end if
               end do
            end if
         end do
      end do
      123 CLOSE(17)
   end subroutine da_READ_THERMO

   !> Puts every letter in strin in uppercase
   subroutine uppercase(strin,strout)

      character(len=*)  :: strin,strout
      integer           :: i

      strout = strin
      do i = 1, len(strout)
         select case(strout(i:i))
         case("a":"z")
            strout(i:i) = achar(iachar(strout(i:i))-32)
         end select
      end do
   end subroutine uppercase

   !> Puts in names_reactants the ordered list of reactants, sets id_reactants as a link between the two
   subroutine da_REORDER_SPECS()

      integer  :: i_reac, gas_offset, cond_offset

      gas_offset = 1
      cond_offset = 1
      do i_reac = 1, N_reactants
         if (reac_condensed(i_reac)) then
            names_reactants(N_gas+cond_offset) = names_reactants_orig(i_reac)
            ! 1st row = new index of the original reactant at i_reac
            id_reactants(i_reac,1) = N_gas + cond_offset
            ! 2nd row = original index of reactants in ordered list
            id_reactants(N_gas+cond_offset,2) = i_reac
            cond_offset = cond_offset + 1
         else
            names_reactants(gas_offset) = names_reactants_orig(i_reac)
            id_reactants(i_reac,1) = gas_offset
            id_reactants(gas_offset,2) = i_reac
            gas_offset = gas_offset + 1
         end if
      end do
   end subroutine da_REORDER_SPECS



   !> MAIN SUBROUTINE
   subroutine easychem(mode,verbo,N_atoms_in,N_reactants_in,molfracs_atoms, &
      molfracs_reactants,massfracs_reactants,temp,press,nabla_ad,gamma2,MMW,rho,c_pe)

      !! I/O:
      character, intent(in)            :: mode
      character(len=2), intent(in)     :: verbo
      double precision, intent(in)     :: molfracs_atoms(N_atoms_in)
      double precision, intent(out)    :: molfracs_reactants(N_reactants_in), massfracs_reactants(N_reactants_in)
      integer, intent(in)              :: N_atoms_in, N_reactants_in
      double precision, intent(in)     :: temp, press
      double precision, intent(out)    :: nabla_ad,gamma2,MMW,rho,c_pe

      !! Internal:
      double precision                 :: C_P_0(N_reactants), H_0(N_reactants), S_0(N_reactants)
      double precision                 :: molfracs_atoms_ions(N_atoms_in+1), temp_use
      integer                          :: N_atoms_use, gamma_neg_try

      error = .false.

      if (N_atoms /= N_atoms_in+1 .or. N_reactants /= N_reactants_in) then
         error = .true.
         err_msg = "VALUE ERROR: The initialized and given arrays are not of the same size..."
         RETURN
      end if

      verbose = .FALSE.
      verbose_cond = (verbo == 'vy')
      quick = (mode /= 's')
      remove_ions = .FALSE.

      call INIT_RAND_SEED()

      molfracs_atoms_ions(1:N_atoms_in) = molfracs_atoms
      molfracs_atoms_ions(N_atoms) = 0d0

      if (ions) then
         if (temp > 750) then
            N_atoms_use = N_atoms
         else
            remove_ions = .true.
            N_atoms_use = N_atoms_in
         end if
      else
         N_atoms_use = N_atoms_in
      end if

      ! CALCULATION BEGINS

      call ec_COMP_THERMO_QUANTS(temp,N_reactants,C_P_0, H_0, S_0)
      gamma2 = 0d0
      temp_use = temp
      gamma_neg_try = 0d0
      do while (gamma2 < 1d0)
         call ec_COMP_EQU_CHEM(N_atoms_use, N_reactants,  molfracs_atoms_ions(1:N_atoms_use), &
         molfracs_reactants, massfracs_reactants, &
         temp_use, press, C_P_0, H_0, S_0, &
         nabla_ad, gamma2, MMW, rho, c_pe)
         if (error) RETURN

         if (gamma2 < 1d0) then
            write(*,*) 'Gamma was < 1, redo! gamma2, temp, ', gamma2, temp
            gamma_neg_try = gamma_neg_try + 1
            if (gamma_neg_try > 10) then
               call random_number(temp_use)
               temp_use = temp*(1d0 + 0.01d0*temp_use)
               write(*,*) 'temp, temp_use', temp, temp_use
               call ec_COMP_THERMO_QUANTS(temp_use,N_reactants,C_P_0, H_0, S_0)
            end if
         end if
      end do

      c_pe = c_pe*1d7 ! J/(g K) to erg/(g K)

   end subroutine easychem

   !> Computes the values of C_P_0, H_0 and S_0
   subroutine ec_COMP_THERMO_QUANTS(temp,N_reac,C_P_0, H_0, S_0)
      !! I/O
      double precision, intent(in)  :: temp
      integer, intent(in)           :: N_reac
      double precision, intent(out) :: C_P_0(N_reac), H_0(N_reac), &
      S_0(N_reac)
      !! internal
      integer                       :: i_reac, i_tempinv, tempinv_ind

      do i_reac = 1, N_reactants

         ! Get temperature interpolation range
         if (temp < thermo_data_temps(1,1,i_reac)) then
            tempinv_ind = 1
         else if (temp >= thermo_data_temps(2,thermo_data_n_intervs(i_reac),i_reac)) then
            tempinv_ind = thermo_data_n_intervs(i_reac)
         else
            do i_tempinv = 1, thermo_data_n_intervs(i_reac)
               if ((temp >= thermo_data_temps(1,i_tempinv,i_reac)) .AND. &
               (temp < thermo_data_temps(2,i_tempinv,i_reac))) then
                  tempinv_ind = i_tempinv
                  EXIT
               end if
            end do
         end if

         ! Calculate thermodynamic quantities as explained in Gordon 1996, page 74
         C_P_0(i_reac) = (thermo_data(1,tempinv_ind,i_reac)*temp**(-2)+ &
         thermo_data(2,tempinv_ind,i_reac)*temp**(-1)+ &
         thermo_data(3,tempinv_ind,i_reac)+thermo_data(4,tempinv_ind,i_reac)* &
         temp**(1)+thermo_data(5,tempinv_ind,i_reac)*temp**(2)+ &
         thermo_data(6,tempinv_ind,i_reac)*temp**(3)+thermo_data(7,tempinv_ind,i_reac)* &
         temp**(4))*R
         H_0(i_reac) = (-thermo_data(1,tempinv_ind,i_reac)*temp**(-2)+ &
         thermo_data(2,tempinv_ind,i_reac)*temp**(-1)*log(temp)+ &
         thermo_data(3,tempinv_ind,i_reac)+thermo_data(4,tempinv_ind,i_reac)*temp**(1)/2d0+ &
         thermo_data(5,tempinv_ind,i_reac)*temp**(2)/3d0+ &
         thermo_data(6,tempinv_ind,i_reac)*temp**(3)/4d0+thermo_data(7,tempinv_ind,i_reac)* &
         temp**(4)/5d0+thermo_data(9,tempinv_ind,i_reac)/temp)* &
         R*temp
         S_0(i_reac) = (-thermo_data(1,tempinv_ind,i_reac)*temp**(-2)/2d0- &
         thermo_data(2,tempinv_ind,i_reac)*temp**(-1)+ &
         thermo_data(3,tempinv_ind,i_reac)*log(temp)+ &
         thermo_data(4,tempinv_ind,i_reac)*temp**(1)+ &
         thermo_data(5,tempinv_ind,i_reac)*temp**(2)/2d0+ &
         thermo_data(6,tempinv_ind,i_reac)*temp**(3)/3d0+thermo_data(7,tempinv_ind,i_reac)* &
         temp**(4)/4d0+thermo_data(10,tempinv_ind,i_reac))*R

      end do

   end subroutine ec_COMP_THERMO_QUANTS

   !> Computes the specie abundances (molar and mass)
   recursive subroutine ec_COMP_EQU_CHEM(N_atoms_use, N_reac, molfracs_atoms, &
      molfracs_reactants, massfracs_reactants, &
      temp, press, C_P_0, H_0, S_0, nabla_ad, gamma2, MMW, rho, c_pe)

      !use test_module
      !! I/O:
      integer, intent(in)              :: N_atoms_use, N_reac
      double precision, intent(in)     :: molfracs_atoms(N_atoms_use)
      double precision, intent(inout)  :: molfracs_reactants(N_reac), massfracs_reactants(N_reac)
      DOUBLE PRECISION, intent(in)     :: temp, press
      DOUBLE PRECISION, intent(in)     :: C_P_0(N_reac), H_0(N_reac), S_0(N_reac)
      double precision, intent(out)    :: nabla_ad, gamma2, MMW, rho, c_pe

      !! CEA McBride 1994 style variables:
      DOUBLE PRECISION  :: n ! Moles of gas particles per total mass of mixture in kg
      DOUBLE PRECISION  :: n_spec(N_reactants) ! Moles of species per total mass of mixture in kg
      DOUBLE PRECISION  :: n_spec_old(N_reactants) ! Moles of species per total mass of mixture in kg of previous iteration
      DOUBLE PRECISION  :: pi_atom(N_atoms_use) ! Lagrangian multipliers for the atomic species divided by (R*T)
      DOUBLE PRECISION  :: matrix(N_reactants+N_atoms_use+1,N_reactants+N_atoms_use+1)
      ! So the solution vector will contain the delta log(n_j) for gas, the delta n_j for condensed species, the pis and the delta log(n)
      DOUBLE PRECISION  :: vector(N_reactants+N_atoms_use+1), solution_vector(N_reactants+N_atoms_use+1)

      !! Internal:
      INTEGER           :: i_iter, i_reac, inc_next, current_solids_number, N_spec_eff, buffer_ind, i_atom
      LOGICAL           :: converged, remove_cond, slowed
      LOGICAL           :: solid_inclu(N_cond), neg_cond(N_cond)
      DOUBLE PRECISION  :: dgdnj(N_cond)
      INTEGER           :: solid_indices(N_cond), solid_indices_buff(N_cond)
      DOUBLE PRECISION  :: nsum, mu_gas(N_gas), a_gas(N_gas,N_atoms_use), mass_species, atom_mass, msum

      converged = .FALSE.
      slowed = .FALSE.
      call ec_INIT_ALL_VALS(N_atoms_use,N_reactants,n,n_spec,pi_atom)

      iter_max = 50000 + N_reactants/2
      current_solids_number = 0

      MMW = 0d0

      n_spec_old = n_spec

      ! FIRST: DO GAS ONLY!
      DO i_iter = 1, iter_max

         ! IF (quick) THEN
         call ec_PREP_MATRIX_SHORT(N_atoms_use,N_reactants, molfracs_atoms,N_gas,press,temp,&
         H_0,S_0,n,n_spec,matrix(1:N_atoms_use+1,1:N_atoms_use+1),vector(1:N_atoms_use+1),&
         (/1,1,1,1,1/),5, mu_gas,a_gas)
         call ec_INVERT_MATRIX_SHORT(N_atoms_use+1, &
         matrix(1:N_atoms_use+1,1:N_atoms_use+1),vector(1:N_atoms_use+1), &
         solution_vector(1:N_atoms_use+1))
         if (error) RETURN

         call ec_UPDATE_ABUNDS_SHORT(N_atoms_use,N_reactants,N_gas,&
         solution_vector(1:N_atoms_use+1), n_spec,pi_atom,n,converged,&
         (/1,1,1,1,1/),5,mu_gas,a_gas,temp,molfracs_atoms,n_spec_old)
         ! ELSE
         !    call ec_PREP_MATRIX_LONG(N_atoms,id_atoms,molfracs_atoms,N_gas,&
         !    press,temp,H_0,S_0,n,n_spec,&
         !    matrix(1:N_gas+N_atoms+1,1:N_gas+N_atoms+1),vector(1:N_gas+N_atoms+1),&
         !    (/1,1,1,1,1/),names_reactants,N_reactants,5)
         !    call ec_INVERT_MATRIX_LONG(N_atoms+N_gas+1, &
         !    matrix(1:N_gas+N_atoms+1,1:N_gas+N_atoms+1),vector(1:N_gas+N_atoms+1), &
         !    solution_vector(1:N_gas+N_atoms+1))
         !    call ec_UPDATE_ABUNDS_LONG(N_atoms,N_gas,solution_vector(1:N_gas+N_atoms+1), &
         !    n_spec,pi_atom,n,converged,(/1,1,1,1,1/),5,id_atoms,molfracs_atoms,N_reactants,&
         !    n_spec_old)
         ! END IF

         n_spec_old = n_spec

         IF (verbose) THEN
            write(*,*)
            write(*,*)
            write(*,*) i_iter
            DO i_reac = 1, N_reactants
               write(*,*) names_reactants(i_reac), n_spec(i_reac)/SUM(n_spec)
            END DO
         END IF

         IF (converged) THEN
            EXIT
         END IF
      END DO

      IF (.NOT. converged) THEN
         WRITE(*,*) 'EASY CHEM WARNING: One or more convergence criteria not satisfied! Press, temp', press, temp
         print *
      END IF

      converged = .FALSE.
      remove_cond = .FALSE.

      IF (N_gas .EQ. N_reactants) THEN
         call ec_COMP_ADIABATIC_GRAD(N_atoms_use, N_reactants, N_gas,  n_spec, &
         n, H_0, C_P_0, (/ 1,1,1,1,1 /), 5, temp, nabla_ad, gamma2, c_pe)
         if (error) RETURN
      END IF

      ! THEN: INCLUDE CONDENSATES!
      IF (N_cond > 0) THEN
         solid_inclu = .FALSE.
         inc_next = 0
         neg_cond = .FALSE.

         N_spec_eff = N_gas

         DO WHILE (inc_next /= -1)

            call ec_INCLUDE_WHICH_SOLID(N_atoms_use,N_reac,pi_atom,H_0,S_0,temp, &
            n_spec,solid_inclu,neg_cond,dgdnj,remove_cond,inc_next)

            if (inc_next/=-1) then

               IF (remove_cond) THEN
                  current_solids_number = current_solids_number - 1
                  solid_indices_buff = 0
                  buffer_ind = 1
                  DO i_reac = 1, N_reactants-N_gas
                     IF (solid_indices(i_reac) .NE. inc_next) THEN
                        solid_indices_buff(buffer_ind) = solid_indices(i_reac)
                        buffer_ind = buffer_ind + 1
                     END IF
                  END DO
                  solid_indices = solid_indices_buff
                  solid_inclu(inc_next-N_gas) = .FALSE.
                  neg_cond(inc_next-N_gas) = .TRUE.
                  if (verbose_cond) then
                     print *, '-   ', names_reactants(inc_next), dgdnj(inc_next-N_gas), n_spec(inc_next)
                  end if
                  n_spec(inc_next) = 0d0
               ELSE
                  current_solids_number = current_solids_number + 1
                  solid_indices(current_solids_number) = inc_next
                  solid_inclu(inc_next-N_gas) = .TRUE.
                  call ec_INIT_COND_VALS(N_atoms_use, N_reactants, molfracs_atoms, inc_next, n_spec)
                  if (verbose_cond) then
                     print *, '+   ', names_reactants(inc_next), dgdnj(inc_next-N_gas), n_spec(inc_next)
                  end if
               END IF

               N_spec_eff = N_gas+current_solids_number
               DO i_iter = 1, iter_max

                  IF (quick) THEN
                     call ec_PREP_MATRIX_SHORT(N_atoms_use, N_reactants, molfracs_atoms,N_spec_eff, &
                     press, temp, H_0, S_0, n, n_spec, &
                     matrix(1:N_atoms_use+1+N_spec_eff-N_gas,1:N_atoms_use+1+N_spec_eff-N_gas), &
                     vector(1:N_atoms_use+1+N_spec_eff-N_gas), solid_indices, &
                     N_spec_eff-N_gas, mu_gas, a_gas)
                     call ec_INVERT_MATRIX_SHORT(N_atoms_use+1+N_spec_eff-N_gas, &
                     matrix(1:N_atoms_use+1+N_spec_eff-N_gas,1:N_atoms_use+1+N_spec_eff-N_gas), &
                     vector(1:N_atoms_use+1+N_spec_eff-N_gas), &
                     solution_vector(1:N_atoms_use+1+N_spec_eff-N_gas))
                     if (error) RETURN

                     call ec_UPDATE_ABUNDS_SHORT(N_atoms_use,N_reactants,N_spec_eff,&
                     solution_vector(1:N_atoms_use+1+N_spec_eff-N_gas), &
                     n_spec,pi_atom,n,converged,&
                     solid_indices,N_spec_eff-N_gas,mu_gas,a_gas,temp,molfracs_atoms, &
                     n_spec_old)
                  ELSE
                     call ec_PREP_MATRIX_LONG(N_atoms_use,N_reactants,molfracs_atoms,N_spec_eff,&
                     press,temp,H_0,S_0,n,n_spec,&
                     matrix(1:N_spec_eff+N_atoms_use+1,1:N_spec_eff+N_atoms_use+1),&
                     vector(1:N_spec_eff+N_atoms_use+1),&
                     solid_indices,N_spec_eff-N_gas)
                     call ec_INVERT_MATRIX_LONG(N_atoms_use+N_spec_eff+1, &
                     matrix(1:N_spec_eff+N_atoms_use+1,1:N_spec_eff+N_atoms_use+1),&
                     vector(1:N_spec_eff+N_atoms_use+1), &
                     solution_vector(1:N_spec_eff+N_atoms_use+1))
                     if (error) RETURN

                     call ec_UPDATE_ABUNDS_LONG(N_atoms_use, N_reac, N_spec_eff, &
                     solution_vector(1:N_spec_eff+N_atoms_use+1), &
                     n_spec, pi_atom, n, converged, &
                     solid_indices, N_spec_eff-N_gas, molfracs_atoms, n_spec_old)
                  END IF

                  ! call writetxtall(N_reactants, n_spec)
                  n_spec_old = n_spec

                  IF (verbose) THEN
                     write(*,*)
                     write(*,*)
                     write(*,*) i_iter
                     DO i_reac = 1, N_reactants
                        write(*,*) names_reactants(i_reac), n_spec(i_reac)/SUM(n_spec)
                     END DO
                  END IF

                  DO i_reac = N_gas+1, N_reactants
                     IF ((n_spec(i_reac) < 0d0) .AND. (i_iter > 30)) THEN
                        converged = .TRUE.
                        EXIT
                     END IF
                  END DO

                  IF (converged) THEN
                     EXIT
                  END IF

               END DO

               IF (.NOT. converged) THEN
                  IF (quick) THEN
                     quick = .FALSE.
                     print *
                     print *, 'SLOW ! Press, Temp', press, temp
                     print *
                     call ec_COMP_EQU_CHEM(N_atoms_use, N_reactants, molfracs_atoms, &
                     molfracs_reactants, massfracs_reactants, &
                     temp, press, C_P_0, H_0, S_0, &
                     nabla_ad,gamma2,MMW,rho,c_pe)
                     quick = .TRUE.
                     slowed = .TRUE.
                     EXIT
                  ELSE
                     WRITE(*,*) 'EASY CHEM WARNING: One or more convergence criteria' // &
                                             'not satisfied! in cond Press, temp', press, temp
                     print *
                  END IF
               END IF

               converged = .FALSE.

            END IF

            remove_cond = .FALSE.

         END DO

         ! Calc. nabla_ad
         IF (.NOT. slowed) THEN
            call ec_COMP_ADIABATIC_GRAD(N_atoms_use, N_reactants, N_spec_eff, n_spec, &
            n,H_0,C_P_0,solid_indices,N_spec_eff-N_gas,temp, nabla_ad,gamma2,c_pe)
            if (error) RETURN
         END IF

         if (verbose_cond) then
            print *
            print *, 'Solids included:'
            do i_reac = 1, N_reactants-N_gas
               if (solid_inclu(i_reac)) then
                  print *, ' ', names_reactants(i_reac+N_gas), n_spec(i_reac+N_gas)
               end if
            end do
         end if

      END IF

      ! PREPARE FINAL OUTPUT

      IF (.NOT. slowed) THEN
         nsum = SUM(n_spec)
         DO i_reac = 1, N_reactants
            IF (n_spec(i_reac)/nsum < 1d-50) THEN
               n_spec(i_reac) = 0d0
            END IF
         END DO

         nsum = SUM(n_spec)
         do i_reac = 1, N_reactants
            molfracs_reactants(i_reac) = n_spec(id_reactants(i_reac,1))/nsum
         end do

         msum = 0d0
         DO i_reac = 1, N_reactants
            mass_species = 0d0
            DO i_atom = 1, 5
               if (reac_atoms_id(i_atom,i_reac)>0) then
                  atom_mass = masses_atoms_save(reac_atoms_id(i_atom,i_reac))
                  mass_species = mass_species+atom_mass*DBLE(reac_stoich(i_atom,i_reac))
               END IF
            END DO
            massfracs_reactants(id_reactants(i_reac,2)) = n_spec(i_reac) * mass_species
            if (i_reac <= N_gas) then
               MMW = MMW + massfracs_reactants(id_reactants(i_reac,2))/mass_species
               msum = msum + massfracs_reactants(id_reactants(i_reac,2))
            end if
         END DO
         massfracs_reactants = massfracs_reactants / SUM(massfracs_reactants)

         ! Mean molecular weight is only calculated as mean molecular gas weight per all gas species
         MMW = MMW/msum
         MMW = 1d0/MMW

         rho = (press*1d6)/kB/temp*MMW
         MMW = MMW/amu

      END IF

   end subroutine ec_COMP_EQU_CHEM

   !> Initialize all abundances with uniform abundances for gas and 0 for condensates
   subroutine ec_INIT_ALL_VALS(N_atoms_use,N_reac,n,n_spec,pi_atom)
      !! I/O:
      integer, intent(in)           :: N_atoms_use, N_reac
      DOUBLE PRECISION, intent(out) :: n ! Moles of gas particles per total mass of mixture in kg
      DOUBLE PRECISION, intent(out) :: n_spec(N_reac) ! Moles of species per total mass of mixture in kg
      DOUBLE PRECISION, intent(out) :: pi_atom(N_atoms_use) ! Lagrangian multipliers for the atomic species divided
      ! by (R*T)

      !! Internal:
      INTEGER                      :: i_reac

      n = 0.1d0
      n_spec = 0d0
      pi_atom = 0d0
      DO i_reac = 1, N_gas
         n_spec(i_reac) = n/DBLE(N_gas)
         IF (remove_ions) THEN
            IF(reac_ion(i_reac)) THEN
               n_spec(i_reac) = 0d0
            END IF
         END IF
      END DO

   end subroutine ec_INIT_ALL_VALS

   !> Selects which solid to include next
   subroutine ec_INCLUDE_WHICH_SOLID(N_atoms_use,N_reac,pi_atom,H_0,S_0,temp, &
      n_spec,solid_inclu,neg_cond,dgdnj,remove_cond,inc_next)
      !! I/O
      integer, intent(in)           :: N_atoms_use, N_reac
      DOUBLE PRECISION, intent(in)  :: pi_atom(N_atoms_use)
      DOUBLE PRECISION, intent(in)  :: H_0(N_reac), S_0(N_reac), temp
      LOGICAL, intent(in)           :: solid_inclu(N_reac-N_gas), neg_cond(N_reac-N_gas)

      double precision, intent(inout)  :: n_spec(N_reac), dgdnj(N_reac-N_gas)
      logical, intent(out)          :: remove_cond
      integer, intent(out)          :: inc_next

      !! Internal:
      DOUBLE PRECISION             :: a(N_reactants,N_atoms_use)
      DOUBLE PRECISION             :: mu(N_reactants), minval_inc
      INTEGER                      :: i_atom, i_reac, i_ratom, remove_count, remove_id

      !f2py integer, intent(aux) :: N_gas

      remove_count = 0
      remove_id = 0
      remove_cond = .false.
      DO i_reac = N_gas+1, N_reactants
         IF (n_spec(i_reac) < 0d0) THEN
            ! n_spec(i_reac) = 0d0
            remove_count = remove_count + 1
            remove_id = i_reac
            ! remove_cond = .TRUE.
         END IF
      END DO

      if (remove_count >= 2) then
         inc_next = remove_id
         remove_cond = .true.
      else

         inc_next = -1
         minval_inc = 2d0

         ! Set up a_ij
         a = 0d0
         DO i_atom = 1, N_atoms_use
            DO i_reac = 1, N_reactants
               IF (remove_ions) THEN
                  IF (reac_ion(i_reac)) THEN
                     CYCLE
                  END IF
               END IF
               DO i_ratom = 1, 5
                  IF (reac_atoms_id(i_ratom, i_reac)>0 .and. id_atoms(i_atom) == reac_atoms_id(i_ratom, i_reac)) then
                     a(i_reac,i_atom) = reac_stoich(i_ratom,i_reac)*mol
                  END IF
               END DO
            END DO
         END DO

         ! EVAL Eq. 3.7 in McBride Manual
         DO i_reac = N_gas+1, N_reactants
            mu(i_reac) = H_0(i_reac) - temp*S_0(i_reac)
            dgdnj(i_reac-N_gas) = mu(i_reac)/R/temp - SUM(a(i_reac,1:N_atoms_use)*pi_atom)
         END DO

         DO i_reac = N_gas+1, N_reactants
            IF ((dgdnj(i_reac-N_gas) < 0d0) .AND. (.NOT. solid_inclu(i_reac-N_gas))) THEN
               IF (((dgdnj(i_reac-N_gas) < minval_inc) .AND. (.NOT. neg_cond(i_reac-N_gas)) .AND. &
               temp <= thermo_data_temps(2,thermo_data_n_intervs(i_reac),i_reac)) .AND. &
               (temp >= thermo_data_temps(1,1,i_reac))) THEN
                  minval_inc = dgdnj(i_reac-N_gas)
                  inc_next = i_reac
               END IF
            END IF
         END DO

         if (inc_next==-1 .and. remove_count==1) then
            inc_next = remove_id
            remove_cond = .true.
         end if

      end if

   end subroutine ec_INCLUDE_WHICH_SOLID

   !> Initialize one condensate abundance, as if the most molecules condensed
   subroutine ec_INIT_COND_VALS(N_atoms_use, N_reac, molfracs_atoms, i_cond, n_spec)

      integer, intent(in)              :: N_atoms_use, i_cond, N_reac
      double precision, intent(in)     :: molfracs_atoms(N_atoms_use)
      double precision, intent(inout)  :: n_spec(N_reac)

      integer           :: i_ratom, i_atom
      double precision  :: min_molfrac, stoich_molfrac

      min_molfrac = -1
      do i_ratom = 1, 5
         if (reac_atoms_id(i_ratom,i_cond) > 0) then
            do i_atom = 1, N_atoms_use
               if (id_atoms(i_atom) == reac_atoms_id(i_ratom,i_cond)) then
                  stoich_molfrac = molfracs_atoms(i_atom) / reac_stoich(i_ratom,i_cond)
                  if (min_molfrac==-1 .or. stoich_molfrac < min_molfrac) then
                     min_molfrac = stoich_molfrac
                  end if
               end if
            end do
         end if
      end do

      if (min_molfrac >= 0) then
         n_spec(i_cond) = min_molfrac
      else
         print *, 'ERROR: no data found for the atoms of the given condensate'
      end if

   end subroutine ec_INIT_COND_VALS

   !> Build the small matrix
   subroutine ec_PREP_MATRIX_SHORT(N_atoms_use, N_reac, molfracs_atoms, N_species, press, temp, &
   H_0, S_0, n, n_spec, matrix, vector, solid_indices, N_solids, mu_gas, a_gas)
      !! I/O:
      INTEGER, intent(in)          :: N_atoms_use, N_reac, N_species, N_solids
      INTEGER, intent(in)          :: solid_indices(N_solids)
      DOUBLE PRECISION, intent(in) :: molfracs_atoms(N_atoms_use), press, temp
      DOUBLE PRECISION, intent(in) ::  H_0(N_reac), S_0(N_reac)
      DOUBLE PRECISION, intent(in) :: n ! Moles of gas particles per total mass of mixture in kg
      DOUBLE PRECISION, intent(inout)  :: n_spec(N_reac) ! Moles of species per total mass of mixture in kg

      DOUBLE PRECISION, intent(out):: matrix(N_atoms_use+1+(N_species-N_gas),N_atoms_use+1+(N_species-N_gas))
      ! So the solution vector will contain the delta log(n_j) for gas, the delta n_j for
      ! condensed species, the pis and the delta log(n)
      DOUBLE PRECISION, intent(out):: vector(N_atoms_use+1+(N_species-N_gas))
      DOUBLE PRECISION, intent(out):: mu_gas(N_gas), a_gas(N_gas,N_atoms_use)

      !! Internal:
      DOUBLE PRECISION             :: b_0(N_atoms_use), b_0_norm, b(N_atoms_use)
      DOUBLE PRECISION             :: a(N_species,N_atoms_use), mu(N_species)
      INTEGER                      :: i_atom, i_reac, i_ratom, i_atom2

      !f2py integer, intent(aux) :: N_gas

      ! print *, "START ec_PREP_MATRIX_SHORT"

      ! Set up b0
      ! b_0_norm = 0d0
      ! DO i_atom = 1, N_atoms_use
      !    ! call ec_ATOM_MASS(names_atoms(i_atom),mass_atom)
      !    mass_atom = masses_atoms_save(id_atoms(i_atom))
      !    b_0_norm = b_0_norm + mass_atom*molfracs_atoms(i_atom)
      ! END DO
      ! b_0 = molfracs_atoms/b_0_norm
      call ec_b_0(N_atoms_use, molfracs_atoms, b_0_norm, b_0)

      ! Set up a_ij
      a = 0d0
      DO i_atom = 1, N_atoms_use
         ! call uppercase(names_atoms(i_atom),upper_atom_name)
         DO i_reac = 1, N_gas
            IF (remove_ions) THEN
               IF (reac_ion(i_reac)) THEN
                  a(i_reac,1:N_atoms_use) = 0d0
                  CYCLE
               END IF
            END IF
            DO i_ratom = 1, 5
               IF (reac_atoms_id(i_ratom, i_reac)>0 .and. &
               id_atoms(i_atom) == reac_atoms_id(i_ratom, i_reac)) then
                  a(i_reac,i_atom) = reac_stoich(i_ratom,i_reac)*mol
               END IF
            END DO
         END DO
         DO i_reac = N_gas+1, N_species
            DO i_ratom = 1, 5
               IF (reac_atoms_id(i_ratom, solid_indices(i_reac - N_gas))>0 .and. &
               id_atoms(i_atom) == reac_atoms_id(i_ratom, solid_indices(i_reac - N_gas))) then
                  a(i_reac,i_atom) = reac_stoich(i_ratom,solid_indices(i_reac-N_gas))*mol
                  ! print *, i_ratom, i_reac, i_atom
               END IF
            END DO
         END DO
      END DO

      ! Set up mu_j
      DO i_reac = 1, N_species
         IF (remove_ions) THEN
            IF (reac_ion(i_reac)) THEN
               mu(i_reac) = 0d0
               CYCLE
            END IF
         END IF
         ! Taken from Venot et al. (2012), in comparison with McBride 1996.
         IF (i_reac <= N_gas) THEN
            mu(i_reac) = H_0(i_reac) - temp*S_0(i_reac)

            IF (n_spec(i_reac) > 1d-290) THEN
               mu(i_reac) = mu(i_reac) + R*temp*log(n_spec(i_reac)/n)+R*temp*log(press)
            ELSE
               IF (verbose) THEN
                  write(*,*) 'n_spec(i_reac) == 0 for '//trim(adjustl(names_reactants(i_reac)))// &
                  ' set to 1d-13 and try again.'
               END IF
               call RANDOM_NUMBER(n_spec(i_reac))
               n_spec(i_reac) = n_spec(i_reac)*1d-13
               mu(i_reac) = mu(i_reac) + R*temp*log(n_spec(i_reac)/n)+R*temp*log(press)
            END IF
         ELSE
            mu(i_reac) = H_0(solid_indices(i_reac-N_gas)) - temp*S_0(solid_indices(i_reac-N_gas))
         END IF
      END DO

      a_gas = a(1:N_gas,1:N_atoms_use)
      mu_gas = mu(1:N_gas)

      ! MATRIX SETUP
      matrix = 0d0

      ! Set up the matrix for the N_atoms equations (Eq. 2.24)
      DO i_atom = 1, N_atoms_use
         DO i_atom2 = 1, N_atoms_use
            DO i_reac = 1, N_gas
               ! IF (remove_ions) THEN
               !    IF (reac_ion(i_reac)) THEN
               !       CYCLE
               !    END IF
               ! END IF
               if (.not. remove_ions .or. .not. reac_ion(i_reac)) then
                  matrix(i_atom,i_atom2) = matrix(i_atom,i_atom2) + &
                  a(i_reac,i_atom)*a(i_reac,i_atom2)*n_spec(i_reac)
               end if
            END DO
         END DO

         DO i_reac = 1, N_gas
            ! IF (remove_ions) THEN
            !    IF (reac_ion(i_reac)) THEN
            !       CYCLE
            !    END IF
            ! END IF
            if (.not. remove_ions .or. .not. reac_ion(i_reac)) then
               matrix(i_atom,N_atoms_use+1) = matrix(i_atom,N_atoms_use+1) + &
               a(i_reac,i_atom)*n_spec(i_reac)
            end if
         END DO

         IF (N_gas < N_species) THEN
            DO i_reac = N_gas+1, N_species
               matrix(i_atom,N_atoms_use+1+i_reac-N_gas) = a(i_reac,i_atom)
            END DO
         END IF

      END DO

      ! Set up the matrix for the equation (Eq. 2.26)
      DO i_atom = 1, N_atoms_use
         DO i_reac = 1, N_gas
            IF (remove_ions) THEN
               IF (reac_ion(i_reac)) THEN
                  CYCLE
               END IF
            END IF
            matrix(N_atoms_use+1,i_atom) = matrix(N_atoms_use+1,i_atom) + &
            a(i_reac,i_atom)*n_spec(i_reac)
         END DO
      END DO

      DO i_reac = 1, N_gas
         IF (remove_ions) THEN
            IF (reac_ion(i_reac)) THEN
               CYCLE
            END IF
         END IF
         matrix(N_atoms_use+1,N_atoms_use+1) = matrix(N_atoms_use+1,N_atoms_use+1) + n_spec(i_reac) !!
      END DO
      matrix(N_atoms_use+1,N_atoms_use+1) = matrix(N_atoms_use+1,N_atoms_use+1) - n

      ! Set up the matrix for the (N_reactants-N_gas) equations (Eq. 2.25)

      IF (N_gas < N_species) THEN
         DO i_reac = N_gas+1, N_species
            DO i_atom = 1, N_atoms_use
               matrix(N_atoms_use+1+i_reac-N_gas,i_atom) = a(i_reac,i_atom)
            END DO
         END DO
      END IF

      ! VECTOR SETUP
      !vector(N_atoms+1+(N_reactants-N_gas))
      vector = 0d0

      ! (Eq. 2.25)
      IF (N_gas < N_species) THEN
         vector(N_atoms_use+2:N_atoms_use+1+(N_species-N_gas)) = mu(N_gas+1:N_species)/R/temp
      END IF

      ! (Eq. 2.24)
      b = 0d0
      DO i_atom = 1, N_atoms_use
         DO i_reac = 1, N_gas
            IF (remove_ions) THEN
               IF (reac_ion(i_reac)) THEN
                  CYCLE
               END IF
            END IF
            b(i_atom) = b(i_atom) + a(i_reac,i_atom)*n_spec(i_reac)
         END DO
         DO i_reac = N_gas+1, N_species
            b(i_atom) = b(i_atom) + a(i_reac,i_atom)*n_spec(solid_indices(i_reac-N_gas))
         END DO
      END DO
      vector(1:N_atoms_use) = b_0 - b
      DO i_reac = 1, N_gas
         IF (remove_ions) THEN
            IF (reac_ion(i_reac)) THEN
               CYCLE
            END IF
         END IF
         vector(1:N_atoms_use) = vector(1:N_atoms_use) + &
         a(i_reac,1:N_atoms_use)*n_spec(i_reac)*mu(i_reac)/R/temp
      END DO

      ! (Eq. 2.26)
      vector(N_atoms_use+1) = n - SUM(n_spec(1:N_gas)) + SUM(n_spec(1:N_gas)*mu(1:N_gas))/R/temp

   end subroutine ec_PREP_MATRIX_SHORT



   !> Return the result of one step of computation with small matrix(problem: AX=B)
   subroutine ec_UPDATE_ABUNDS_SHORT(N_atoms_use,N_reac,N_species,solution_vector,n_spec,pi_atom,&
   n,converged,solid_indices,N_solids,mu_gas,a_gas,temp,molfracs_atoms,n_spec_old)

      !! I/O:
      INTEGER, intent(in)          :: N_atoms_use, N_reac, N_species, N_solids
      INTEGER, intent(in)          :: solid_indices(N_solids)
      DOUBLE PRECISION, intent(in) :: solution_vector(N_atoms_use+1+(N_species-N_gas))
      DOUBLE PRECISION, intent(inout)  :: n ! Moles of gas particles per total mass of mixture in kg
      DOUBLE PRECISION, intent(inout)  :: n_spec(N_reac) ! Moles of species per total mass of mixture in kg
      DOUBLE PRECISION, intent(in) :: n_spec_old(N_reac) ! Moles of species per total mass of mixture in kg
      DOUBLE PRECISION, intent(inout)  :: pi_atom(N_atoms_use) ! Lagrangian multipliers for the atomic species divided
      ! by (R*T)
      LOGICAL, intent(out)          :: converged
      DOUBLE PRECISION, intent(in) :: mu_gas(N_gas), a_gas(N_gas,N_atoms_use), temp

      !! Internal:
      INTEGER                      :: i_reac
      INTEGER, save                :: n_done = 0
      DOUBLE PRECISION             :: lambda, lambda1, lambda2
      DOUBLE PRECISION, parameter  :: SIZE = 18.420681
      LOGICAL                      :: gas_good, solids_good, total_good
      DOUBLE PRECISION             :: delta_n_gas(N_gas)

      ! IONS
      INTEGER                      :: i_ion, i_stoich
      DOUBLE PRECISION             :: pi_ion, pi_ion_norm, mass

      ! MASS BALANCE CHECKS
      DOUBLE PRECISION             :: b_0(N_atoms_use), b_0_norm, pi_atom_old(N_atoms_use)
      DOUBLE PRECISION             :: a(N_species,N_atoms_use), mval_mass_good
      INTEGER                      :: i_atom, i_ratom
      LOGICAL                      :: mass_good, pi_good
      DOUBLE PRECISION             :: molfracs_atoms(N_atoms_use)
      DOUBLE PRECISION             :: change

      !f2py integer, intent(aux) :: N_gas

      ! print *, "START ec_UPDATE_ABUNDS_SHORT"

      ! Get delta_n_gas, following Eq. 2.18:
      DO i_reac = 1, N_gas
         IF (remove_ions) THEN
            IF (reac_ion(i_reac)) THEN
               CYCLE
            END IF
         END IF
         delta_n_gas(i_reac) = SUM(a_gas(i_reac,1:N_atoms_use)*solution_vector(1:N_atoms_use)) + &
         solution_vector(N_atoms_use+1) - mu_gas(i_reac)/R/temp
      END DO

      ! Calculate correction factors as described in Section 3.3 of the McBride Manual
      lambda1 = 9d99
      lambda2 = 9d99
      DO i_reac = 1, N_gas
         IF (remove_ions) THEN
            IF (reac_ion(i_reac)) THEN
               CYCLE
            END IF
         END IF
         IF (LOG(n_spec(i_reac)/n) > -SIZE) THEN
            lambda1 = MIN(lambda1,2d0/(MAX(5d0*ABS(solution_vector(N_atoms_use+1)), &
            ABS(delta_n_gas(i_reac)))))
         ELSE IF ((LOG(n_spec(i_reac)/n) <= -SIZE) .AND. (delta_n_gas(i_reac) >= 0d0)) THEN
            lambda2 = MIN(lambda2,ABS((-LOG(n_spec(i_reac)/n)-9.2103404)/ &
            (delta_n_gas(i_reac)-solution_vector(N_atoms_use+1))))
         END IF
      END DO
      lambda = MIN(1d0,lambda1,lambda2)

      DO i_reac = 1, N_gas
         IF (remove_ions) THEN
            IF (reac_ion(i_reac)) THEN
               CYCLE
            END IF
         END IF
         n_spec(i_reac) = n_spec(i_reac)*exp(lambda*delta_n_gas(i_reac))
      END DO

      IF (N_gas < N_species) THEN
         DO i_reac = N_gas+1, N_species
            change = lambda*solution_vector(N_atoms_use+1+i_reac-N_gas)
            ! if (2*abs(change) < n_spec(solid_indices(i_reac-N_gas)) .OR. n_spec(solid_indices(i_reac-N_gas)) < tiny(0d0)) then
            !    n_spec(solid_indices(i_reac-N_gas)) = n_spec(solid_indices(i_reac-N_gas)) + change
            ! else
            !    n_spec(solid_indices(i_reac-N_gas)) = (1d0 + sign(0.5d0,change)) * n_spec(solid_indices(i_reac-N_gas))
            ! end if
            n_spec(solid_indices(i_reac-N_gas)) = n_spec(solid_indices(i_reac-N_gas)) + change
         END DO
      END IF
      pi_atom_old = pi_atom
      pi_atom = solution_vector(1:N_atoms_use)
      n = n*exp(lambda*solution_vector(N_atoms_use+1))

      gas_good = .TRUE.
      DO i_reac = 1, N_gas
         IF (remove_ions) THEN
            IF (reac_ion(i_reac)) THEN
               CYCLE
            END IF
         END IF
         IF (n_spec(i_reac)*ABS(delta_n_gas(i_reac))/SUM(n_spec) > 0.5d-5) THEN
            gas_good = .FALSE.
         END IF
      END DO
      solids_good = .TRUE.
      IF (N_gas < N_species) THEN
         DO i_reac = N_gas+1, N_species
            IF (ABS(solution_vector(N_atoms_use+1+i_reac-N_gas))/SUM(n_spec) > 0.5d-5) THEN
               solids_good = .FALSE.
            END IF
         END DO
      END IF
      total_good = .TRUE.
      IF (n*ABS(solution_vector(N_atoms_use+1))/SUM(n_spec) > 05.d-5) THEN
         total_good = .FALSE.
      END IF

      !!!-----------------------

      mass_good = .TRUE.
      pi_good = .TRUE.

      ! Set up b0
      ! b_0_norm = 0d0
      ! DO i_atom = 1, N_atoms_use
      !    ! call ec_ATOM_MASS(names_atoms(i_atom),mass_atom)
      !    mass_atom = masses_atoms_save(id_atoms(i_atom))
      !    b_0_norm = b_0_norm + mass_atom*molfracs_atoms(i_atom)
      ! END DO
      ! b_0 = molfracs_atoms/b_0_norm
      call ec_b_0(N_atoms_use, molfracs_atoms, b_0_norm, b_0)

      ! Set up a_ij
      a = 0d0
      DO i_atom = 1, N_atoms_use
         DO i_reac = 1, N_gas
            IF (remove_ions) THEN
               IF (reac_ion(i_reac)) THEN
                  a(i_reac,1:N_atoms_use) = 0d0
                  CYCLE
               END IF
            END IF
            DO i_ratom = 1, 5
               IF (reac_atoms_id(i_ratom, i_reac)>0 .and. id_atoms(i_atom) == reac_atoms_id(i_ratom, i_reac)) then
                  a(i_reac,i_atom) = reac_stoich(i_ratom,i_reac)*mol
               END IF
            END DO
         END DO
         DO i_reac = N_gas+1, N_species
            DO i_ratom = 1, 5
               IF (reac_atoms_id(i_ratom, solid_indices(i_reac - N_gas))>0 .and. &
               id_atoms(i_atom) == reac_atoms_id(i_ratom, solid_indices(i_reac - N_gas))) then
                  a(i_reac,i_atom) = reac_stoich(i_ratom,solid_indices(i_reac-N_gas))*mol
               END IF
            END DO
         END DO
      END DO

      mval_mass_good = MAXVAL(b_0)*1d-2
      DO i_atom = 1, N_atoms_use
         mass = 0.0d0
         DO i_reac = 1, N_gas
            mass = mass + a(i_reac,i_atom)*n_spec(i_reac)
         END DO
         DO i_reac = N_gas+1, N_species
            mass = mass + a(i_reac,i_atom)*n_spec(solid_indices(i_reac-N_gas))
         END DO
         IF ((abs(b_0(i_atom) - mass) > mval_mass_good) .AND. (b_0(i_atom) > 1d-6)) THEN
            mass_good = .FALSE.
         END IF
      END DO

      DO i_atom = 1, N_atoms_use
         IF (abs((pi_atom_old(i_atom)-pi_atom(i_atom))/pi_atom(i_atom)) > 1d-3) THEN
            pi_good = .FALSE.
         END IF
      END DO

      IF ((.NOT. mass_good) .OR. (.NOT. pi_good)) THEN
         mass_good = .TRUE.
         pi_good = .TRUE.
         DO i_reac = 1, N_reactants
            IF (ABS(n_spec(i_reac)-n_spec_old(i_reac)) > 1d-10) THEN
               mass_good = .FALSE.
               pi_good = .FALSE.
            END IF
         END DO
      END IF

      !!!-------------------

      ! ION CONVERGENCE?

      IF (ions .AND. (.NOT. remove_ions)) THEN

         ! DO THE MAGIC THEY DO IN SECT. 3.7 in McBride

         pi_ion = 0d0
         pi_ion_norm = 0d0
         DO i_reac = 1, N_species
            DO i_stoich = 1, 5
               ! IF (trim(adjustl(reac_atoms_names(i_stoich,i_reac))) .EQ. 'E') THEN
               IF (reac_atoms_id(i_stoich,i_reac) == 1) THEN
                  pi_ion = pi_ion - n_spec(i_reac)*reac_stoich(i_stoich,i_reac)
                  pi_ion_norm = pi_ion_norm + n_spec(i_reac)*reac_stoich(i_stoich,i_reac)**2d0
                  EXIT
               END IF
            END DO
         END DO

         pi_ion = pi_ion / pi_ion_norm

         IF (ABS(pi_ion) > 1d-4) THEN
            DO i_ion = 1, 80
               DO i_reac = 1, N_species
                  DO i_stoich = 1, 5
                     ! IF (trim(adjustl(reac_atoms_names(i_stoich,i_reac))) .EQ. 'E') THEN
                     IF (reac_atoms_id(i_stoich,i_reac) == 1) THEN
                        n_spec(i_reac) = n_spec(i_reac)*exp(reac_stoich(i_stoich,i_reac)*pi_ion)
                        EXIT
                     END IF
                  END DO
               END DO

               pi_ion = 0d0
               pi_ion_norm = 0d0
               DO i_reac = 1, N_species
                  DO i_stoich = 1, 5
                     ! IF (trim(adjustl(reac_atoms_names(i_stoich,i_reac))) .EQ. 'E') THEN
                     IF (reac_atoms_id(i_stoich,i_reac) == 1) THEN
                        pi_ion = pi_ion - n_spec(i_reac)*reac_stoich(i_stoich,i_reac)
                        pi_ion_norm = pi_ion_norm + n_spec(i_reac)*reac_stoich(i_stoich,i_reac)**2d0
                        EXIT
                     END IF
                  END DO
               END DO

            END DO
         END IF

         IF (((gas_good .AND. solids_good) .AND. total_good) .AND. (ABS(pi_ion) <= 1d-4)) THEN
            IF (mass_good .AND. pi_good) THEN
               converged = .TRUE.
            END IF
         END IF

      ELSE

         IF ((gas_good .AND. solids_good) .AND. total_good) THEN
            IF (mass_good .AND. pi_good) THEN
               converged = .TRUE.
            END IF
         END IF

      END IF

      n_done = n_done + 1

   end subroutine ec_UPDATE_ABUNDS_SHORT

   !> Build the big matrix
   subroutine ec_PREP_MATRIX_LONG(N_atoms_use, N_reac, molfracs_atoms, N_species,press,temp, &
   H_0, S_0, n, n_spec, matrix, vector, solid_indices, N_solids)

      !! I/O:
      INTEGER, intent(in)          :: N_atoms_use, N_reac, N_species, N_solids
      INTEGER, intent(in)          :: solid_indices(N_solids)
      DOUBLE PRECISION, intent(in) :: molfracs_atoms(N_atoms_use), press, temp
      DOUBLE PRECISION, intent(in) :: H_0(N_reac), S_0(N_reac)
      DOUBLE PRECISION, intent(in) :: n ! Moles of gas particles per total mass of mixture in kg
      DOUBLE PRECISION, intent(inout)  :: n_spec(N_reac) ! Moles of species per total mass of mixture in kg
      ! DOUBLE PRECISION, intent(in) :: pi_atom(N_atoms) ! Lagrangian multipliers for the atomic species divided
      ! ! by (R*T)
      DOUBLE PRECISION, intent(out):: matrix(N_species+N_atoms_use+1,N_species+N_atoms_use+1)
      ! So the solution vector will contain the delta log(n_j) for gas, the delta n_j for
      ! condensed species, the pis and the delta log(n)
      DOUBLE PRECISION, intent(out):: vector(N_species+N_atoms_use+1)

      !! Internal:
      DOUBLE PRECISION             :: b_0(N_atoms_use), b_0_norm, b(N_atoms_use)
      DOUBLE PRECISION             :: a(N_species,N_atoms_use), mu(N_species)
      INTEGER                      :: i_atom, i_reac, i_ratom

      ! Set up b0
      ! b_0_norm = 0d0
      ! DO i_atom = 1, N_atoms_use
      !    ! call ec_ATOM_MASS(names_atoms(i_atom),mass_atom)
      !    if (id_atoms(i_atom) > 0) then
      !       mass_atom = masses_atoms_save(id_atoms(i_atom))
      !       b_0_norm = b_0_norm + mass_atom*molfracs_atoms(i_atom)
      !    end if
      ! END DO
      ! b_0 = molfracs_atoms/b_0_norm
      call ec_b_0(N_atoms_use, molfracs_atoms, b_0_norm, b_0)

      ! Set up a_ij
      a = 0d0
      DO i_atom = 1, N_atoms_use
         ! call uppercase(names_atoms(i_atom),upper_atom_name)
         DO i_reac = 1, N_gas
            IF (remove_ions) THEN
               IF (reac_ion(i_reac)) THEN
                  a(i_reac,1:N_atoms_use) = 0d0
                  CYCLE
               END IF
            END IF
            DO i_ratom = 1, 5
               ! call uppercase(reac_atoms_names(i_ratom,i_reac),upper_ratom_name)
               ! IF (trim(adjustl(upper_atom_name)) .EQ. trim(adjustl(upper_ratom_name))) THEN
               IF (reac_atoms_id(i_ratom,i_reac)>0 .and. id_atoms(i_atom) == reac_atoms_id(i_ratom, i_reac)) then
                  a(i_reac,i_atom) = reac_stoich(i_ratom,i_reac)*mol
               END IF
            END DO
         END DO
         DO i_reac = N_gas+1, N_species
            DO i_ratom = 1, 5
               ! call uppercase(reac_atoms_names(i_ratom,solid_indices(i_reac-N_gas)),upper_ratom_name)
               ! IF (trim(adjustl(upper_atom_name)) .EQ. trim(adjustl(upper_ratom_name))) THEN
               IF (reac_atoms_id(i_ratom, solid_indices(i_reac - N_gas))>0 .and.&
               id_atoms(i_atom) == reac_atoms_id(i_ratom, solid_indices(i_reac - N_gas))) then
                  a(i_reac,i_atom) = reac_stoich(i_ratom,solid_indices(i_reac-N_gas))*mol
               END IF
            END DO
         END DO
      END DO

      ! Set up mu_j
      DO i_reac = 1, N_species
         IF (remove_ions) THEN
            IF (reac_ion(i_reac)) THEN
               mu(i_reac) = 0d0
               CYCLE
            END IF
         END IF
         ! Taken from Venot et al. (2012), in comparison with McBride 1996.
         IF (i_reac <= N_gas) THEN
            mu(i_reac) = H_0(i_reac) - temp*S_0(i_reac)

            IF (n_spec(i_reac) > 1d-290) THEN
               mu(i_reac) = mu(i_reac) + R*temp*log(n_spec(i_reac)/n)+R*temp*log(press)
            ELSE
               IF (verbose) THEN
                  write(*,*) 'n_spec(i_reac) == 0 for '//trim(adjustl(names_reactants(i_reac)))// &
                  ' set to 1d-13 and try again.'
               END IF
               call RANDOM_NUMBER(n_spec(i_reac))
               n_spec(i_reac) = n_spec(i_reac)*1d-13
               mu(i_reac) = mu(i_reac) + R*temp*log(n_spec(i_reac)/n)+R*temp*log(press)
            END IF

         ELSE
            mu(i_reac) = H_0(solid_indices(i_reac-N_gas)) - temp*S_0(solid_indices(i_reac-N_gas))
         END IF
      END DO

      ! MATRIX SETUP
      matrix = 0d0
      ! Set up the matrix for the N_gas equations (Eq. 2.18)
      DO i_reac = 1, N_gas
         IF (remove_ions) THEN
            IF (reac_ion(i_reac)) THEN
               CYCLE
            END IF
         END IF
         matrix(i_reac,i_reac) = 1d0
         DO i_atom = 1, N_atoms_use
            matrix(i_reac,N_species+i_atom) = -a(i_reac,i_atom)
         END DO
         matrix(i_reac,N_species+N_atoms_use+1) = -1d0
      END DO

      ! Set up the matrix for the N_reactants-N_gas equations (Eq. 2.19)
      IF (N_gas < N_species) THEN
         DO i_reac = N_gas+1, N_species
            DO i_atom = 1, N_atoms_use
               matrix(i_reac,N_species+i_atom) = -a(i_reac,i_atom)
            END DO
         END DO
      END IF

      ! Set up the matrix for the N_atom equations (Eq. 2.20)
      DO i_atom = 1, N_atoms_use
         DO i_reac = 1, N_gas
            IF (remove_ions) THEN
               IF (reac_ion(i_reac)) THEN
                  CYCLE
               END IF
            END IF
            matrix(N_species+i_atom,i_reac) = a(i_reac,i_atom)*n_spec(i_reac)
         END DO
         IF (N_gas < N_species) THEN
            DO i_reac = N_gas+1, N_species
               matrix(N_species+i_atom,i_reac) = a(i_reac,i_atom)
            END DO
         END IF
      END DO

      ! Set up the matrix for the last equation (Eq. 2.21)
      DO i_reac = 1, N_gas
         IF (remove_ions) THEN
            IF (reac_ion(i_reac)) THEN
               CYCLE
            END IF
         END IF
         matrix(N_species+N_atoms_use+1,i_reac) = n_spec(i_reac)
      END DO
      matrix(N_species+N_atoms_use+1,N_species+N_atoms_use+1) = -n

      ! VECTOR SETUP
      !vector(N_reactants+N_atoms+1)
      vector = 0d0

      DO i_reac = 1, N_gas
         IF (remove_ions) THEN
            IF (reac_ion(i_reac)) THEN
               CYCLE
            END IF
         END IF
         vector(i_reac) = -mu(i_reac)/R/temp ! (Eq. 2.18)
      END DO

      IF (N_gas < N_species) THEN
         vector(N_gas+1:N_species) = -mu(N_gas+1:N_species)/R/temp ! (Eq. 2.19)
      END IF

      b = 0d0
      DO i_atom = 1, N_atoms_use
         DO i_reac = 1, N_gas
            IF (remove_ions) THEN
               IF (reac_ion(i_reac)) THEN
                  CYCLE
               END IF
            END IF
            b(i_atom) = b(i_atom) + a(i_reac,i_atom)*n_spec(i_reac)
         END DO
         DO i_reac = N_gas+1, N_species
            b(i_atom) = b(i_atom) + a(i_reac,i_atom)*n_spec(solid_indices(i_reac-N_gas))
         END DO
      END DO
      vector(N_species+1:N_species+N_atoms_use) = b_0 - b ! (Eq. 2.20)

      vector(N_species+N_atoms_use+1) = n - SUM(n_spec(1:N_gas)) ! (Eq. 2.21)

   end subroutine ec_PREP_MATRIX_LONG

   !> Return the result of one step of computation with big matrix(problem: AX=B)
   subroutine ec_UPDATE_ABUNDS_LONG(N_atoms_use,N_reac,N_species,solution_vector,n_spec,pi_atom,&
   n,converged,solid_indices,N_solids,molfracs_atoms,n_spec_old)

      !! I/O:
      INTEGER, intent(in)          :: N_atoms_use, N_reac, N_species, N_solids
      INTEGER , intent(in)         :: solid_indices(N_solids)
      DOUBLE PRECISION, intent(in) :: solution_vector(N_species+N_atoms_use+1)
      DOUBLE PRECISION, intent(inout)  :: n ! Moles of gas particles per total mass of mixture in kg
      DOUBLE PRECISION, intent(inout)  :: n_spec(N_reac) ! Moles of species per total mass of mixture in kg
      DOUBLE PRECISION, intent(in)     :: n_spec_old(N_reac) ! Moles of species per total mass of mixture in kg
      DOUBLE PRECISION, intent(inout)  :: pi_atom(N_atoms_use) ! Lagrangian multipliers for the atomic species divided
      ! by (R*T)
      LOGICAL , intent(out)         :: converged

      !! Internal:
      INTEGER                      :: i_reac
      INTEGER, save                :: n_done = 0
      DOUBLE PRECISION             :: lambda, lambda1, lambda2
      DOUBLE PRECISION, parameter  :: SIZE = 18.420681
      LOGICAL                      :: gas_good, solids_good, total_good

      ! IONS
      INTEGER                      :: i_ion, i_stoich
      DOUBLE PRECISION             :: pi_ion, pi_ion_norm, mass

      ! MASS BALANCE CHECKS
      DOUBLE PRECISION             :: b_0(N_atoms_use), b_0_norm, pi_atom_old(N_atoms_use)
      DOUBLE PRECISION             :: a(N_species,N_atoms_use), mval_mass_good
      INTEGER                      :: i_atom, i_ratom
      LOGICAL                      :: mass_good, pi_good
      DOUBLE PRECISION             :: molfracs_atoms(N_atoms_use)
      DOUBLE precision             :: change


      ! Calculate correction factors as described in Section 3.3 of the McBride Manual
      lambda1 = 9d99
      lambda2 = 9d99
      DO i_reac = 1, N_gas
         IF (remove_ions) THEN
            IF (reac_ion(i_reac)) THEN
               CYCLE
            END IF
         END IF
         IF (LOG(n_spec(i_reac)/n) > -SIZE) THEN
            lambda1 = MIN(lambda1,2d0/(MAX(5d0*ABS(solution_vector(N_species+N_atoms_use+1)), &
            ABS(solution_vector(i_reac)))))
         ELSE IF ((LOG(n_spec(i_reac)/n) <= -SIZE) .AND. (solution_vector(i_reac) >= 0d0)) THEN
            lambda2 = MIN(lambda2,ABS((-LOG(n_spec(i_reac)/n)-9.2103404)/ &
            (solution_vector(i_reac)-solution_vector(N_species+N_atoms_use+1))))
         END IF
      END DO
      lambda = MIN(1d0,lambda1,lambda2)

      DO i_reac = 1, N_gas
         IF (remove_ions) THEN
            IF (reac_ion(i_reac)) THEN
               CYCLE
            END IF
         END IF
         n_spec(i_reac) = n_spec(i_reac)*exp(lambda*solution_vector(i_reac))
      END DO

      IF (N_gas < N_species) THEN
         DO i_reac = N_gas+1, N_species
            change = lambda*solution_vector(N_atoms_use+1+i_reac-N_gas)
            ! if (2*abs(change) < n_spec(solid_indices(i_reac-N_gas)) .OR. n_spec(solid_indices(i_reac-N_gas)) < tiny(0d0)) then
            !    n_spec(solid_indices(i_reac-N_gas)) = n_spec(solid_indices(i_reac-N_gas)) + changepi_atom
            ! else
            !    n_spec(solid_indices(i_reac-N_gas)) = (1d0 + sign(0.5d0,change)) * n_spec(solid_indices(i_reac-N_gas))
            ! end if
            n_spec(solid_indices(i_reac-N_gas)) = n_spec(solid_indices(i_reac-N_gas)) + change
         END DO
      END IF
      pi_atom_old = pi_atom
      pi_atom = solution_vector(N_species+1:N_species+N_atoms_use)
      n = n*exp(lambda*solution_vector(N_species+N_atoms_use+1))

      gas_good = .TRUE.
      DO i_reac = 1, N_gas
         IF (remove_ions) THEN
            IF (reac_ion(i_reac)) THEN
               CYCLE
            END IF
         END IF
         IF (n_spec(i_reac)*ABS(solution_vector(i_reac))/SUM(n_spec) > 0.5d-5) THEN
            gas_good = .FALSE.
         END IF
      END DO
      solids_good = .TRUE.
      IF (N_gas < N_species) THEN
         DO i_reac = N_gas+1, N_species
            IF (ABS(solution_vector(i_reac))/SUM(n_spec) > 0.5d-5) THEN
               solids_good = .FALSE.
            END IF
         END DO
      END IF
      total_good = .TRUE.
      IF (n*ABS(solution_vector(N_species+N_atoms_use+1))/SUM(n_spec) > 05.d-5) THEN
         total_good = .FALSE.
      END IF

      !!!-----------------------

      mass_good = .TRUE.
      pi_good = .TRUE.


      ! Set up b0
      ! b_0_norm = 0d0
      ! DO i_atom = 1, N_atoms_use
      !    ! call ec_ATOM_MASS(names_atoms(i_atom),mass_atom)
      !    mass_atom = masses_atoms_save(id_atoms(i_atom))
      !    b_0_norm = b_0_norm + mass_atom*molfracs_atoms(i_atom)
      ! END DO
      ! b_0 = molfracs_atoms/b_0_norm
      call ec_b_0(N_atoms_use, molfracs_atoms, b_0_norm, b_0)

      ! Set up a_ij
      a = 0d0
      DO i_atom = 1, N_atoms_use
         ! call uppercase(names_atoms(i_atom),upper_atom_name)
         DO i_reac = 1, N_gas
            IF (remove_ions) THEN
               IF (reac_ion(i_reac)) THEN
                  a(i_reac,1:N_atoms_use) = 0d0
                  CYCLE
               END IF
            END IF
            DO i_ratom = 1, 5
               ! call uppercase(reac_atoms_names(i_ratom,i_reac),upper_ratom_name)
               ! IF (trim(adjustl(upper_atom_name)) .EQ. trim(adjustl(upper_ratom_name))) THEN
               IF (reac_atoms_id(i_ratom, i_reac)>0 .and. id_atoms(i_atom) == reac_atoms_id(i_ratom, i_reac)) then
                  a(i_reac,i_atom) = reac_stoich(i_ratom,i_reac)*mol
               END IF
            END DO
         END DO
         DO i_reac = N_gas+1, N_species
            DO i_ratom = 1, 5
               ! call uppercase(reac_atoms_names(i_ratom,solid_indices(i_reac-N_gas)),upper_ratom_name)
               ! IF (trim(adjustl(upper_atom_name)) .EQ. trim(adjustl(upper_ratom_name))) THEN
               IF (reac_atoms_id(i_ratom, solid_indices(i_reac - N_gas))>0 .and. &
               id_atoms(i_atom) == reac_atoms_id(i_ratom, solid_indices(i_reac - N_gas))) then
                  a(i_reac,i_atom) = reac_stoich(i_ratom,solid_indices(i_reac-N_gas))*mol
               END IF
            END DO
         END DO
      END DO

      mval_mass_good = MAXVAL(b_0)*1d-2
      DO i_atom = 1, N_atoms_use
         mass = 0.0d0
         DO i_reac = 1, N_gas
            mass = mass + a(i_reac,i_atom)*n_spec(i_reac)
         END DO
         DO i_reac = N_gas+1, N_species
            mass = mass + a(i_reac,i_atom)*n_spec(solid_indices(i_reac-N_gas))
         END DO
         IF ((abs(b_0(i_atom) - mass) > mval_mass_good) .AND. (b_0(i_atom) > 1d-6)) THEN
            mass_good = .FALSE.
         END IF
      END DO

      DO i_atom = 1, N_atoms_use
         IF (abs((pi_atom_old(i_atom)-pi_atom(i_atom))/pi_atom(i_atom)) > 1d-3) THEN
            pi_good = .FALSE.
         END IF
      END DO

      IF ((.NOT. mass_good) .OR. (.NOT. pi_good)) THEN
         mass_good = .TRUE.
         pi_good = .TRUE.
         DO i_reac = 1, N_reactants
            IF (ABS(n_spec(i_reac)-n_spec_old(i_reac)) > 1d-10) THEN
               mass_good = .FALSE.
               pi_good = .FALSE.
            END IF
         END DO
      END IF

      !!!-------------------

      ! ION CONVERGENCE?

      IF (ions .AND. (.NOT. remove_ions)) THEN

         ! DO THE MAGIC THEY DO IN SECT. 3.7 in McBride

         pi_ion = 0d0
         pi_ion_norm = 0d0
         DO i_reac = 1, N_species
            DO i_stoich = 1, 5
               ! IF (trim(adjustl(reac_atoms_names(i_stoich,i_reac))) .EQ. 'E') THEN
               IF (reac_atoms_id(i_stoich,i_reac) == 1) THEN
                  pi_ion = pi_ion - n_spec(i_reac)*reac_stoich(i_stoich,i_reac)
                  pi_ion_norm = pi_ion_norm + n_spec(i_reac)*reac_stoich(i_stoich,i_reac)**2d0
                  EXIT
               END IF
            END DO
         END DO

         pi_ion = pi_ion / pi_ion_norm

         IF (ABS(pi_ion) > 1d-4) THEN
            DO i_ion = 1, 80
               DO i_reac = 1, N_species
                  DO i_stoich = 1, 5
                     ! IF (trim(adjustl(reac_atoms_names(i_stoich,i_reac))) .EQ. 'E') THEN
                     IF (reac_atoms_id(i_stoich,i_reac) == 1) THEN
                        n_spec(i_reac) = n_spec(i_reac)*exp(reac_stoich(i_stoich,i_reac)*pi_ion)
                        EXIT
                     END IF
                  END DO
               END DO

               pi_ion = 0d0
               pi_ion_norm = 0d0
               DO i_reac = 1, N_species
                  DO i_stoich = 1, 5
                     ! IF (trim(adjustl(reac_atoms_names(i_stoich,i_reac))) .EQ. 'E') THEN
                     IF (reac_atoms_id(i_stoich,i_reac) == 1) THEN
                        pi_ion = pi_ion - n_spec(i_reac)*reac_stoich(i_stoich,i_reac)
                        pi_ion_norm = pi_ion_norm + n_spec(i_reac)*reac_stoich(i_stoich,i_reac)**2d0
                        EXIT
                     END IF
                  END DO
               END DO
            END DO
         END IF

         IF (((gas_good .AND. solids_good) .AND. total_good) .AND. (ABS(pi_ion) <= 1d-4)) THEN
            IF (mass_good .AND. pi_good) THEN
               converged = .TRUE.
            END IF
         END IF

      ELSE

         IF ((gas_good .AND. solids_good) .AND. total_good) THEN
            IF (mass_good .AND. pi_good) THEN
               converged = .TRUE.
            END IF
         END IF

      END IF

      n_done = n_done + 1

   end subroutine ec_UPDATE_ABUNDS_LONG

   !> Computes the adiabatic gradient
   subroutine ec_COMP_ADIABATIC_GRAD(N_atoms_use,N_reac,N_spec_eff,n_spec, &
   n,H_0,C_P_0,solid_indices,N_solids,temp,nabla_ad,gamma2,c_pe)

      !use test_module
      !! I/O:
      INTEGER, intent(in)          :: N_atoms_use, N_reac, N_spec_eff, N_solids
      INTEGER, intent(in)          :: solid_indices(N_solids)
      DOUBLE PRECISION, intent(in) :: temp
      DOUBLE PRECISION, intent(in) :: C_P_0(N_reac), H_0(N_reac)
      DOUBLE PRECISION, intent(in) :: n ! Moles of gas particles per total mass of mixture in kg
      DOUBLE PRECISION, intent(in) :: n_spec(N_reac) ! Moles of species per total mass of mixture in kg
      DOUBLE PRECISION, intent(out):: nabla_ad, gamma2, c_pe

      !! Internal:
      DOUBLE PRECISION             :: matrix(N_atoms_use+1+(N_spec_eff-N_gas),N_atoms_use+1+(N_spec_eff-N_gas))
      ! So the solution vector will contain the delta log(n_j) for gas, the delta n_j for
      ! condensed species, the pis and the delta log(n)
      DOUBLE PRECISION             :: vector(N_atoms_use+1+(N_spec_eff-N_gas)), &
      solution_vector(N_atoms_use+1+(N_spec_eff-N_gas))
      DOUBLE PRECISION             :: a(N_spec_eff,N_atoms_use)
      INTEGER                      :: i_atom, i_reac, i_ratom, i_atom2

      ! Set up a_ij
      a = 0d0
      DO i_atom = 1, N_atoms_use
         ! call uppercase(names_atoms(i_atom),upper_atom_name)
         DO i_reac = 1, N_gas
            IF (remove_ions) THEN
               IF (reac_ion(i_reac)) THEN
                  a(i_reac,i_atom) = 0d0
                  CYCLE
               END IF
            END IF
            DO i_ratom = 1, 5
               ! call uppercase(reac_atoms_names(i_ratom,i_reac),upper_ratom_name)
               ! IF (trim(adjustl(upper_atom_name)) .EQ. trim(adjustl(upper_ratom_name))) THEN
               IF (reac_atoms_id(i_ratom, i_reac)>0 .and. id_atoms(i_atom) == reac_atoms_id(i_ratom, i_reac)) then
                  a(i_reac,i_atom) = reac_stoich(i_ratom,i_reac)*mol
               END IF
            END DO
         END DO
         DO i_reac = N_gas+1, N_spec_eff
            DO i_ratom = 1, 5
               ! call uppercase(reac_atoms_names(i_ratom,solid_indices(i_reac-N_gas)),upper_ratom_name)
               ! IF (trim(adjustl(upper_atom_name)) .EQ. trim(adjustl(upper_ratom_name))) THEN
               IF (reac_atoms_id(i_ratom, solid_indices(i_reac - N_gas))>0 .and. &
               id_atoms(i_atom) == reac_atoms_id(i_ratom, solid_indices(i_reac - N_gas))) then
                  a(i_reac,i_atom) = reac_stoich(i_ratom,solid_indices(i_reac-N_gas))*mol
               END IF
            END DO
         END DO
      END DO

      matrix = 0d0
      ! Setup matrix, following Eq. 2.56
      DO i_atom = 1, N_atoms_use
         ! First term, LHS
         DO i_atom2 = 1, N_atoms_use
            DO i_reac = 1, N_gas
               IF (remove_ions) THEN
                  IF (reac_ion(i_reac)) THEN
                     CYCLE
                  END IF
               END IF
               matrix(i_atom,i_atom2) = matrix(i_atom,i_atom2) + &
               n_spec(i_reac)*a(i_reac,i_atom2)*a(i_reac,i_atom)
            END DO
         END DO
         ! Second term, LHS
         DO i_reac = N_gas+1, N_spec_eff
            matrix(i_atom,N_atoms_use+1+i_reac-N_gas) = a(i_reac,i_atom)
         END DO
         ! Third term, LHS
         DO i_reac = 1, N_gas
            IF (remove_ions) THEN
               IF (reac_ion(i_reac)) THEN
                  CYCLE
               END IF
            END IF
            matrix(i_atom,N_atoms_use+1) = matrix(i_atom,N_atoms_use+1) + &
            a(i_reac,i_atom)*n_spec(i_reac)
         END DO
      END DO

      ! Setup matrix, following Eq. 2.58
      DO i_atom = 1, N_atoms_use
         DO i_reac = 1, N_gas
            IF (remove_ions) THEN
               IF (reac_ion(i_reac)) THEN
                  CYCLE
               END IF
            END IF
            matrix(N_atoms_use+1,i_atom) = matrix(N_atoms_use+1,i_atom) + &
            a(i_reac,i_atom)*n_spec(i_reac)
         END DO
      END DO

      ! Setup matrix, following Eq. 2.57
      DO i_reac = N_gas+1, N_spec_eff
         DO i_atom = 1, N_atoms_use
            matrix(N_atoms_use+1+i_reac-N_gas,i_atom) = a(i_reac,i_atom)
         END DO
      END DO

      vector = 0d0
      ! Setup the vector, following Eq. 2.56
      DO i_atom = 1, N_atoms_use
         vector(i_atom) = -SUM(a(1:N_gas,i_atom)*n_spec(1:N_gas)*H_0(1:N_gas)) &
         /R/temp
      END DO

      ! Setup the vector, following Eq. 2.58
      vector(N_atoms_use+1) = -SUM(n_spec(1:N_gas)*H_0(1:N_gas))/R/temp

      ! Setup the vector, following Eq. 2.57
      DO i_reac = N_gas+1, N_spec_eff
         vector(N_atoms_use+1+i_reac-N_gas) = -H_0(solid_indices(i_reac-N_gas))/R/temp
      END DO

      ! Solve the system
      call ec_INVERT_MATRIX_SHORT(N_atoms_use+1+N_spec_eff-N_gas,matrix,vector,solution_vector)
      if (error) RETURN

      ! Calculate c_pe, following Eq. 2.59
      c_pe = 0d0
      DO i_atom = 1, N_atoms_use
         c_pe = c_pe + SUM(a(1:N_gas,i_atom)*n_spec(1:N_gas)*H_0(1:N_gas)/R/temp) * &
         solution_vector(i_atom)
      END DO
      DO i_reac = N_gas+1, N_spec_eff
         c_pe = c_pe + H_0(solid_indices(i_reac-N_gas))/R/temp* &
         solution_vector(N_atoms_use+1+i_reac-N_gas) + &
         n_spec(solid_indices(i_reac-N_gas))* &
         C_P_0(solid_indices(i_reac-N_gas))/R
      END DO
      c_pe = c_pe + SUM(n_spec(1:N_gas)*C_P_0(1:N_gas)/R)
      c_pe = c_pe + SUM(n_spec(1:N_gas)*H_0(1:N_gas)/R/temp)* &
      solution_vector(N_atoms_use+1)
      c_pe = c_pe + SUM(n_spec(1:N_gas)*(H_0(1:N_gas)/R/temp)**2d0)
      c_pe = c_pe*R

      ! Calculate nabla_ad, using Eq. 2.50 and Eq. 2.75
      nabla_ad = c_pe/n/R/(1d0+solution_vector(N_atoms_use+1))
      nabla_ad = 1/nabla_ad
      gamma2 = 1d0/(1d0-nabla_ad)

   end subroutine ec_COMP_ADIABATIC_GRAD

   subroutine ec_b_0(N_atoms_use, molfracs_atoms, b_0_norm, b_0)
      integer, intent(in)           :: N_atoms_use
      double precision, intent(in)  :: molfracs_atoms(N_atoms_use)
      double precision, intent(out) :: b_0_norm, b_0(N_atoms_use)

      integer                       :: i_atom
      double precision              :: mass_atom

      ! Set up b0
      b_0_norm = 0d0
      DO i_atom = 1, N_atoms_use
         ! call ec_ATOM_MASS(names_atoms(i_atom),mass_atom)
         mass_atom = masses_atoms_save(id_atoms(i_atom))
         b_0_norm = b_0_norm + mass_atom*molfracs_atoms(i_atom)
      END DO
      b_0 = molfracs_atoms/b_0_norm
   end subroutine ec_b_0


   !> Taken from http://gcc.gnu.org/onlinedocs/gfortran/RANDOM_005fSEED.html#RANDOM_005fSEED
   subroutine INIT_RAND_SEED()
      use iso_fortran_env, only: int64
      integer, allocatable :: seed(:)
      integer :: i, n, un, istat, dt(8), pid
      integer(int64) :: t

      call random_seed(size = n)
      allocate(seed(n))
      ! First try if the OS provides a random number generator
      open(newunit=un, file="/dev/urandom", access="stream", &
      form="unformatted", action="read", status="old", iostat=istat)
      if (istat == 0) then
         read(un) seed
         close(un)
      else
         ! Fallback to OR:ing the current time and pid. The PID is
         ! useful in case one launches multiple instances of the same
         ! program in parallel.
         call system_clock(t)
         if (t == 0) then
            call date_and_time(values=dt)
            t = (dt(1) - 1970) * 365_int64 * 24 * 60 * 60 * 1000 &
            + dt(2) * 31_int64 * 24 * 60 * 60 * 1000 &
            + dt(3) * 24_int64 * 60 * 60 * 1000 &
            + dt(5) * 60 * 60 * 1000 &
            + dt(6) * 60 * 1000 + dt(7) * 1000 &
            + dt(8)
         end if
         pid = getpid()
         t = ieor(t, int(pid, kind(t)))
         do i = 1, n
            seed(i) = lcg(t)
         end do
      end if
      call random_seed(put=seed)
      contains
      ! This simple PRNG might not be good enough for real work, but is
      ! sufficient for seeding a better PRNG.
      function lcg(s)
         integer :: lcg
         integer(int64) :: s
         if (s == 0) then
            s = 104729
         else
            s = mod(s, 4294967296_int64)
         end if
         s = mod(s * 279470273_int64, 4294967291_int64)
         lcg = int(mod(s, int(huge(0), int64)), kind(0))
      end function lcg
   end subroutine INIT_RAND_SEED

   !> Invert the small matrix
   subroutine ec_INVERT_MATRIX_SHORT(lens,matrix,vector,solution_vector)
      implicit none (type, external)
      !! I/O:
      INTEGER, intent(in)           :: lens
      DOUBLE PRECISION, intent(inout)  :: matrix(lens,lens)
      ! So the solution vector will contain the delta log(n_j) for gas, the delta n_j for
      ! condensed species, the pis and the delta log(n)
      DOUBLE PRECISION, intent(in)  :: vector(lens)
      double precision, intent(out) :: solution_vector(lens)
      !! Internal:
      INTEGER                      :: good, pivot(lens)

      solution_vector = vector

      call dgesv(lens, matrix, pivot, solution_vector, good)

   end subroutine ec_INVERT_MATRIX_SHORT

   !> Invert the big matrix
   subroutine ec_INVERT_MATRIX_LONG(lens,matrix,vector,solution_vector)
      implicit none (type, external)
      !! I/O:
      INTEGER, intent(in)           :: lens
      DOUBLE PRECISION, intent(inout)  :: matrix(lens,lens)
      double precision, intent(in)  :: vector(lens)
      double precision, intent(out) :: solution_vector(lens)
      ! So the solution vector will contain the delta log(n_j) for gas, the delta n_j for
      ! condensed species, the pis and the delta log(n)

      double precision              :: matrix_nions(lens-N_ions,lens-N_ions)
      DOUBLE PRECISION              :: vector_nions(lens-N_ions), &
      solution_vector_nions(lens-N_ions)

      !! Internal:
      INTEGER                       :: corrf_i, corrf_j, good_nions, good
      INTEGER                       :: i_mat, j_mat, pivot(lens), pivot_nions(lens-N_ions)

      solution_vector = vector

      IF (remove_ions) THEN
         vector_nions = 0d0
         matrix_nions = 0d0
         corrf_i = 0
         DO i_mat = 1, lens
            corrf_j = 0
            IF (i_mat <= N_gas) THEN
               IF (reac_ion(i_mat)) THEN
                  corrf_i = corrf_i + 1
                  cycle
               END IF
            END IF
            DO j_mat = 1, lens
               IF (j_mat <= N_gas) THEN
                  IF (reac_ion(j_mat)) THEN
                     corrf_j = corrf_j + 1
                     cycle
                  END IF
               END IF
               matrix_nions(j_mat-corrf_j,i_mat-corrf_i) = matrix(j_mat,i_mat)
            END DO
            vector_nions(i_mat-corrf_i) = vector(i_mat)
         END DO
         solution_vector_nions = vector_nions

         call dgesv(lens-N_ions, matrix_nions, pivot_nions, solution_vector_nions, good_nions)

         corrf_i = 0
         DO i_mat = 1, lens
            IF (i_mat <= N_gas) THEN
               IF (reac_ion(i_mat)) THEN
                  corrf_i = corrf_i + 1
                  cycle
               END IF
            END IF
            solution_vector(i_mat) = solution_vector_nions(i_mat-corrf_i)
         END DO
      ELSE

         call dgesv(lens, matrix, pivot, solution_vector, good)

      END IF

   end subroutine ec_INVERT_MATRIX_LONG

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!   (ADAPTED) LAPACK OPEN-SOURCE ROUTINES FROM HERE ON (BSD LICENSE)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!  -- LAPACK driver routine (version 3.4.0) --
!  -- LAPACK is a software package provided by Univ. of Tennessee,    --
!  -- Univ. of California Berkeley, Univ. of Colorado Denver and NAG Ltd..--
!     November 2011

!      call dgesv_mod(lens, 1, matrix, lens, pivot, solution_vector, lens, good)

   subroutine dgesv(LEN, A, IPIV, B, INFO)

      implicit none (type, external)
      integer, intent(in) :: LEN
      integer, intent(out) :: INFO, IPIV(LEN)
      double precision, intent(inout) :: A(LEN,LEN), B(LEN)

      info = 0

      ! Compute the LU factorization of A.
      CALL dgetrf(LEN, LEN, a, LEN, ipiv, info)
      IF( info.EQ.0 ) THEN
         ! Solve the system A*X = B, overwriting B with X.
         CALL dgetrs( 'No transpose', LEN, 1, a, LEN, ipiv, b, LEN, info )
      END IF
      RETURN

   end subroutine dgesv

!
!  =====================================================================
      SUBROUTINE dgetrf( M, N, A, LDA, IPIV, INFO )
!
!  -- LAPACK computational routine (version 3.7.0) --
!  -- LAPACK is a software package provided by Univ. of Tennessee,    --
!  -- Univ. of California Berkeley, Univ. of Colorado Denver and NAG Ltd..--
!     December 2016
!
      implicit none (type, external)
!     .. Scalar Arguments ..
      INTEGER            INFO, LDA, M, N
!     ..
!     .. Array Arguments ..
      INTEGER            IPIV( * )
      DOUBLE PRECISION   A( LDA, * )
!     ..
!
!  =====================================================================
!
!     .. Parameters ..
      DOUBLE PRECISION   ONE
      PARAMETER          ( ONE = 1.0D+0 )
!     ..
!     .. Local Scalars ..
      INTEGER            I, IINFO, J, JB, NB
!     ..
!     .. Intrinsic Functions ..
      INTRINSIC          MAX, MIN
!     ..
!     .. Executable Statements ..
!
!     Test the input parameters.
!
      INFO = 0
      IF( M.LT.0 ) THEN
         INFO = -1
      ELSE IF( N.LT.0 ) THEN
         INFO = -2
      ELSE IF( LDA.LT.MAX( 1, M ) ) THEN
         INFO = -4
      END IF
      IF( INFO.NE.0 ) THEN
         CALL XERBLA( 'DGETRF', -INFO )
         RETURN
      END IF
!
!     Quick return if possible
!
      IF( M.EQ.0 .OR. N.EQ.0 ) &
         RETURN
!
!     Determine the block size for this environment.
!
      CALL ILAENV_RETURN( 1, 'DGETRF', ' ', M, N, -1, -1, NB)
      IF( NB.LE.1 .OR. NB.GE.MIN( M, N ) ) THEN
!
!        Use unblocked code.
!
         CALL DGETRF2( M, N, A, LDA, IPIV, INFO )
      ELSE
!
!        Use blocked code.
!
         DO 20 J = 1, MIN( M, N ), NB
            JB = MIN( MIN( M, N )-J+1, NB )
!
!           Factor diagonal and subdiagonal blocks and test for exact
!           singularity.
!
            CALL DGETRF2( M-J+1, JB, A( J, J ), LDA, IPIV( J ), IINFO )
!
!           Adjust INFO and the pivot indices.
!
            IF( INFO.EQ.0 .AND. IINFO.GT.0 ) &
               INFO = IINFO + J - 1
            DO 10 I = J, MIN( M, J+JB-1 )
               IPIV( I ) = J - 1 + IPIV( I )
   10       CONTINUE
!
!           Apply interchanges to columns 1:J-1.
!
            CALL DLASWP( J-1, A, LDA, J, J+JB-1, IPIV, 1 )
!
            IF( J+JB.LE.N ) THEN
!
!              Apply interchanges to columns J+JB:N.
!
               CALL DLASWP( N-J-JB+1, A( 1, J+JB ), LDA, J, J+JB-1, &
                                     IPIV, 1 )
!
!              Compute block row of U.
!
               CALL DTRSM( 'Left', 'Lower', 'No transpose', 'Unit', JB, &
                           N-J-JB+1, ONE, A( J, J ), LDA, A( J, J+JB ), &
                           LDA )
               IF( J+JB.LE.M ) THEN
!
!                 Update trailing submatrix.
!
                  CALL DGEMM( 'No transpose', 'No transpose', M-J-JB+1, &
                              N-J-JB+1, JB, -ONE, A( J+JB, J ), LDA, &
                              A( J, J+JB ), LDA, ONE, A( J+JB, J+JB ), &
                              LDA )
               END IF
            END IF
   20    CONTINUE
      END IF
      RETURN
!
!     End of DGETRF
!
      END

      RECURSIVE SUBROUTINE DGETRF2( M, N, A, LDA, IPIV, INFO )
!
!  -- LAPACK computational routine (version 3.7.0) --
!  -- LAPACK is a software package provided by Univ. of Tennessee,    --
!  -- Univ. of California Berkeley, Univ. of Colorado Denver and NAG Ltd..--
!     June 2016
      implicit none (type, external)
!     .. Scalar Arguments ..
      INTEGER            INFO, LDA, M, N
!     ..
!     .. Array Arguments ..
      INTEGER            IPIV( * )
      DOUBLE PRECISION   A( LDA, * )
!     ..
!
!  =====================================================================
!
!     .. Parameters ..
      DOUBLE PRECISION   ONE, ZERO
      PARAMETER          ( ONE = 1.0D+0, ZERO = 0.0D+0 )
!     ..
!     .. Local Scalars ..
      DOUBLE PRECISION   SFMIN, TEMP
      INTEGER            I, IINFO, N1, N2
!     ..
!     .. Intrinsic Functions ..
      INTRINSIC          MAX, MIN
!     ..
!     .. Executable Statements ..
!
!     Test the input parameters
!
      INFO = 0
      IF( M.LT.0 ) THEN
         INFO = -1
      ELSE IF( N.LT.0 ) THEN
         INFO = -2
      ELSE IF( LDA.LT.MAX( 1, M ) ) THEN
         INFO = -4
      END IF
      IF( INFO.NE.0 ) THEN
         CALL XERBLA( 'DGETRF2', -INFO )
         RETURN
      END IF
!
!     Quick return if possible
!
      IF( M.EQ.0 .OR. N.EQ.0 ) &
         RETURN

      IF ( M.EQ.1 ) THEN
!
!        Use unblocked code for one row case
!        Just need to handle IPIV and INFO
!
         IPIV( 1 ) = 1
         IF ( A(1,1).EQ.ZERO ) &
            INFO = 1
!
      ELSE IF( N.EQ.1 ) THEN
!
!        Use unblocked code for one column case
!
!
!        Compute machine safe minimum
!
         CALL DLAMCH_RETURN('S', SFMIN)
!
!        Find pivot and test for singularity
!
         CALL IDAMAX_RETURN( M, A( 1, 1 ), 1 , I)
         IPIV( 1 ) = I
         IF( A( I, 1 ).NE.ZERO ) THEN
!
!           Apply the interchange
!
            IF( I.NE.1 ) THEN
               TEMP = A( 1, 1 )
               A( 1, 1 ) = A( I, 1 )
               A( I, 1 ) = TEMP
            END IF
!
!           Compute elements 2:M of the column
!
            IF( ABS(A( 1, 1 )) .GE. SFMIN ) THEN
               CALL DSCAL( M-1, ONE / A( 1, 1 ), A( 2, 1 ), 1 )
            ELSE
               DO 10 I = 1, M-1
                  A( 1+I, 1 ) = A( 1+I, 1 ) / A( 1, 1 )
   10          CONTINUE
            END IF
!
         ELSE
            INFO = 1
         END IF
!
      ELSE
!
!        Use recursive code
!
         N1 = MIN( M, N ) / 2
         N2 = N-N1
!
!               [ A11 ]
!        Factor [ --- ]
!               [ A21 ]
!
         CALL DGETRF2( M, N1, A, LDA, IPIV, IINFO )

         IF ( INFO.EQ.0 .AND. IINFO.GT.0 ) &
            INFO = IINFO
!
!                              [ A12 ]
!        Apply interchanges to [ --- ]
!                              [ A22 ]
!
         CALL DLASWP( N2, A( 1, N1+1 ), LDA, 1, N1, IPIV, 1 )
!
!        Solve A12
!
         CALL DTRSM( 'L', 'L', 'N', 'U', N1, N2, ONE, A, LDA, &
                     A( 1, N1+1 ), LDA )
!
!        Update A22
!
         CALL DGEMM( 'N', 'N', M-N1, N2, N1, -ONE, A( N1+1, 1 ), LDA, &
                     A( 1, N1+1 ), LDA, ONE, A( N1+1, N1+1 ), LDA )
!
!        Factor A22
!
         CALL DGETRF2( M-N1, N2, A( N1+1, N1+1 ), LDA, IPIV( N1+1 ), &
                       IINFO )
!
!        Adjust INFO and the pivot indices
!
         IF ( INFO.EQ.0 .AND. IINFO.GT.0 ) &
            INFO = IINFO + N1
         DO 20 I = N1+1, MIN( M, N )
            IPIV( I ) = IPIV( I ) + N1
   20    CONTINUE
!
!        Apply interchanges to A21
!
         CALL DLASWP( N1, A( 1, 1 ), LDA, N1+1, MIN( M, N), IPIV, 1 )
!
      END IF
      RETURN
!
!     End of DGETRF2
!
      END

      SUBROUTINE DGETRS( TRANS, N, NRHS, A, LDA, IPIV, B, LDB, INFO )
!
!  -- LAPACK computational routine (version 3.7.0) --
!  -- LAPACK is a software package provided by Univ. of Tennessee,    --
!  -- Univ. of California Berkeley, Univ. of Colorado Denver and NAG Ltd..--
!     December 2016
!
      implicit none (type, external)
!     .. Scalar Arguments ..
      CHARACTER          TRANS
      INTEGER            INFO, LDA, LDB, N, NRHS
!     ..
!     .. Array Arguments ..
      INTEGER            IPIV( * )
      DOUBLE PRECISION   A( LDA, * ), B( LDB, * )
!     ..
!
!  =====================================================================
!
!     .. Parameters ..
      DOUBLE PRECISION   ONE
      PARAMETER          ( ONE = 1.0D+0 )
!     ..
!     .. Local Scalars ..
      LOGICAL            NOTRAN, BUFFER1, BUFFER2
!     ..
!     .. Intrinsic Functions ..
      INTRINSIC          MAX
!     ..
!     .. Executable Statements ..
!
!     Test the input parameters.
!
      INFO = 0
      CALL LSAME_RETURN( TRANS, 'N', NOTRAN)
      CALL LSAME_RETURN( TRANS, 'T', BUFFER1)
      CALL LSAME_RETURN( TRANS, 'C', BUFFER2)
      IF( .NOT.NOTRAN .AND. .NOT.BUFFER1 .AND. .NOT. &
          BUFFER2 ) THEN
         INFO = -1
      ELSE IF( N.LT.0 ) THEN
         INFO = -2
      ELSE IF( NRHS.LT.0 ) THEN
         INFO = -3
      ELSE IF( LDA.LT.MAX( 1, N ) ) THEN
         INFO = -5
      ELSE IF( LDB.LT.MAX( 1, N ) ) THEN
         INFO = -8
      END IF
      IF( INFO.NE.0 ) THEN
         CALL XERBLA( 'DGETRS', -INFO )
         RETURN
      END IF
!
!     Quick return if possible
!
      IF( N.EQ.0 .OR. NRHS.EQ.0 ) &
         RETURN
!
      IF( NOTRAN ) THEN
!
!        Solve A * X = B.
!
!        Apply row interchanges to the right hand sides.
!
         CALL DLASWP( NRHS, B, LDB, 1, N, IPIV, 1 )
!
!        Solve L*X = B, overwriting B with X.
!
         CALL DTRSM( 'Left', 'Lower', 'No transpose', 'Unit', N, NRHS, &
                     ONE, A, LDA, B, LDB )
!
!        Solve U*X = B, overwriting B with X.
!
         CALL DTRSM( 'Left', 'Upper', 'No transpose', 'Non-unit', N, &
                     NRHS, ONE, A, LDA, B, LDB )
      ELSE
!
!        Solve A**T * X = B.
!
!        Solve U**T *X = B, overwriting B with X.
!
         CALL DTRSM( 'Left', 'Upper', 'Transpose', 'Non-unit', N, NRHS, &
                     ONE, A, LDA, B, LDB )
!
!        Solve L**T *X = B, overwriting B with X.
!
         CALL DTRSM( 'Left', 'Lower', 'Transpose', 'Unit', N, NRHS, ONE, &
                     A, LDA, B, LDB )
!
!        Apply row interchanges to the solution vectors.
!
         CALL DLASWP( NRHS, B, LDB, 1, N, IPIV, -1 )
      END IF
!
      RETURN
!
!     End of DGETRS
!
      END

      SUBROUTINE DGEMM(TRANSA,TRANSB,M,N,K,ALPHA,A,LDA,B,LDB,BETA,C,LDC)
!
!  -- Reference BLAS level3 routine (version 3.7.0) --
!  -- Reference BLAS is a software package provided by Univ. of Tennessee,    --
!  -- Univ. of California Berkeley, Univ. of Colorado Denver and NAG Ltd..--
!     December 2016
!
      implicit none (type, external)
!     .. Scalar Arguments ..
      DOUBLE PRECISION ALPHA,BETA
      INTEGER K,LDA,LDB,LDC,M,N
      CHARACTER TRANSA,TRANSB
!     ..
!     .. Array Arguments ..
      DOUBLE PRECISION A(LDA,*),B(LDB,*),C(LDC,*)
!     ..
!
!  =====================================================================
!
!     .. Intrinsic Functions ..
      INTRINSIC MAX
!     ..
!     .. Local Scalars ..
      DOUBLE PRECISION TEMP
      INTEGER I,INFO,J,L,NCOLA,NROWA,NROWB
      LOGICAL NOTA,NOTB, BUFFER1, BUFFER2, BUFFER3, BUFFER4
!     ..
!     .. Parameters ..
      DOUBLE PRECISION ONE,ZERO
      PARAMETER (ONE=1.0D+0,ZERO=0.0D+0)
!     ..
!
!     Set  NOTA  and  NOTB  as  true if  A  and  B  respectively are not
!     transposed and set  NROWA, NCOLA and  NROWB  as the number of rows
!     and  columns of  A  and the  number of  rows  of  B  respectively.
!
      CALL LSAME_RETURN(TRANSA,'N', NOTA)
      CALL LSAME_RETURN(TRANSB,'N', NOTB)
      IF (NOTA) THEN
          NROWA = M
          NCOLA = K
      ELSE
          NROWA = K
          NCOLA = M
      END IF
      IF (NOTB) THEN
          NROWB = K
      ELSE
          NROWB = N
      END IF
!
!     Test the input parameters.
!
      INFO = 0
      CALL LSAME_RETURN(TRANSA,'C', BUFFER1)
      CALL LSAME_RETURN(TRANSA,'T', BUFFER2)
      CALL LSAME_RETURN(TRANSB,'C', BUFFER3)
      CALL LSAME_RETURN(TRANSB,'T', BUFFER4)
      IF ((.NOT.NOTA) .AND. (.NOT.BUFFER1) .AND. &
          (.NOT.BUFFER2)) THEN
          INFO = 1
      ELSE IF ((.NOT.NOTB) .AND. (.NOT.BUFFER3) .AND. &
               (.NOT.BUFFER4)) THEN
          INFO = 2
      ELSE IF (M.LT.0) THEN
          INFO = 3
      ELSE IF (N.LT.0) THEN
          INFO = 4
      ELSE IF (K.LT.0) THEN
          INFO = 5
      ELSE IF (LDA.LT.MAX(1,NROWA)) THEN
          INFO = 8
      ELSE IF (LDB.LT.MAX(1,NROWB)) THEN
          INFO = 10
      ELSE IF (LDC.LT.MAX(1,M)) THEN
          INFO = 13
      END IF
      IF (INFO.NE.0) THEN
          CALL XERBLA('DGEMM ',INFO)
          RETURN
      END IF
!
!     Quick return if possible.
!
      IF ((M.EQ.0) .OR. (N.EQ.0) .OR. &
          (((ALPHA.EQ.ZERO).OR. (K.EQ.0)).AND. (BETA.EQ.ONE))) RETURN
!
!     And if  alpha.eq.zero.
!
      IF (ALPHA.EQ.ZERO) THEN
          IF (BETA.EQ.ZERO) THEN
              DO 20 J = 1,N
                  DO 10 I = 1,M
                      C(I,J) = ZERO
   10             CONTINUE
   20         CONTINUE
          ELSE
              DO 40 J = 1,N
                  DO 30 I = 1,M
                      C(I,J) = BETA*C(I,J)
   30             CONTINUE
   40         CONTINUE
          END IF
          RETURN
      END IF
!
!     Start the operations.
!
      IF (NOTB) THEN
          IF (NOTA) THEN
!
!           Form  C := alpha*A*B + beta*C.
!
              DO 90 J = 1,N
                  IF (BETA.EQ.ZERO) THEN
                      DO 50 I = 1,M
                          C(I,J) = ZERO
   50                 CONTINUE
                  ELSE IF (BETA.NE.ONE) THEN
                      DO 60 I = 1,M
                          C(I,J) = BETA*C(I,J)
   60                 CONTINUE
                  END IF
                  DO 80 L = 1,K
                      TEMP = ALPHA*B(L,J)
                      DO 70 I = 1,M
                          C(I,J) = C(I,J) + TEMP*A(I,L)
   70                 CONTINUE
   80             CONTINUE
   90         CONTINUE
          ELSE
!
!           Form  C := alpha*A**T*B + beta*C
!
              DO 120 J = 1,N
                  DO 110 I = 1,M
                      TEMP = ZERO
                      DO 100 L = 1,K
                          TEMP = TEMP + A(L,I)*B(L,J)
  100                 CONTINUE
                      IF (BETA.EQ.ZERO) THEN
                          C(I,J) = ALPHA*TEMP
                      ELSE
                          C(I,J) = ALPHA*TEMP + BETA*C(I,J)
                      END IF
  110             CONTINUE
  120         CONTINUE
          END IF
      ELSE
          IF (NOTA) THEN
!
!           Form  C := alpha*A*B**T + beta*C
!
              DO 170 J = 1,N
                  IF (BETA.EQ.ZERO) THEN
                      DO 130 I = 1,M
                          C(I,J) = ZERO
  130                 CONTINUE
                  ELSE IF (BETA.NE.ONE) THEN
                      DO 140 I = 1,M
                          C(I,J) = BETA*C(I,J)
  140                 CONTINUE
                  END IF
                  DO 160 L = 1,K
                      TEMP = ALPHA*B(J,L)
                      DO 150 I = 1,M
                          C(I,J) = C(I,J) + TEMP*A(I,L)
  150                 CONTINUE
  160             CONTINUE
  170         CONTINUE
          ELSE
!
!           Form  C := alpha*A**T*B**T + beta*C
!
              DO 200 J = 1,N
                  DO 190 I = 1,M
                      TEMP = ZERO
                      DO 180 L = 1,K
                          TEMP = TEMP + A(L,I)*B(J,L)
  180                 CONTINUE
                      IF (BETA.EQ.ZERO) THEN
                          C(I,J) = ALPHA*TEMP
                      ELSE
                          C(I,J) = ALPHA*TEMP + BETA*C(I,J)
                      END IF
  190             CONTINUE
  200         CONTINUE
          END IF
      END IF
!
      RETURN
!
!     End of DGEMM .
!
      END

     SUBROUTINE DLASWP( N, A, LDA, K1, K2, IPIV, INCX )
!
!  -- LAPACK auxiliary routine (version 3.7.1) --
!  -- LAPACK is a software package provided by Univ. of Tennessee,    --
!  -- Univ. of California Berkeley, Univ. of Colorado Denver and NAG Ltd..--
!     June 2017
      implicit none (type, external)
!     .. Scalar Arguments ..
      INTEGER            INCX, K1, K2, LDA, N
!     ..
!     .. Array Arguments ..
      INTEGER            IPIV(*)
      DOUBLE PRECISION   A( LDA, * )
!     ..
!
! =====================================================================
!
!     .. Local Scalars ..
      INTEGER            I, I1, I2, INC, IP, IX, IX0, J, K, N32
      DOUBLE PRECISION   TEMP
!     ..
!     .. Executable Statements ..
!
!     Interchange row I with row IPIV(K1+(I-K1)*abs(INCX)) for each of rows
!     K1 through K2.
!
      IF( INCX.GT.0 ) THEN
         IX0 = K1
         I1 = K1
         I2 = K2
         INC = 1
      ELSE IF( INCX.LT.0 ) THEN
         IX0 = K1 + ( K1-K2 )*INCX
         I1 = K2
         I2 = K1
         INC = -1
      ELSE
         RETURN
      END IF
!
      N32 = ( N / 32 )*32
      IF( N32.NE.0 ) THEN
         DO 30 J = 1, N32, 32
            IX = IX0
            DO 20 I = I1, I2, INC
               IP = IPIV( IX )
               IF( IP.NE.I ) THEN
                  DO 10 K = J, J + 31
                     TEMP = A( I, K )
                     A( I, K ) = A( IP, K )
                     A( IP, K ) = TEMP
   10             CONTINUE
               END IF
               IX = IX + INCX
   20       CONTINUE
   30    CONTINUE
      END IF
      IF( N32.NE.N ) THEN
         N32 = N32 + 1
         IX = IX0
         DO 50 I = I1, I2, INC
            IP = IPIV( IX )
            IF( IP.NE.I ) THEN
               DO 40 K = N32, N
                  TEMP = A( I, K )
                  A( I, K ) = A( IP, K )
                  A( IP, K ) = TEMP
   40          CONTINUE
            END IF
            IX = IX + INCX
   50    CONTINUE
      END IF
!
      RETURN
!
!     End of DLASWP
!
      END

      SUBROUTINE DTRSM(SIDE,UPLO,TRANSA,DIAG,M,N,ALPHA,A,LDA,B,LDB)
!
!  -- Reference BLAS level3 routine (version 3.7.0) --
!  -- Reference BLAS is a software package provided by Univ. of Tennessee,    --
!  -- Univ. of California Berkeley, Univ. of Colorado Denver and NAG Ltd..--
!     December 2016
      implicit none (type, external)
!     .. Scalar Arguments ..
      DOUBLE PRECISION ALPHA
      INTEGER LDA,LDB,M,N
      CHARACTER DIAG,SIDE,TRANSA,UPLO
!     ..
!     .. Array Arguments ..
      DOUBLE PRECISION A(LDA,*),B(LDB,*)
!     ..
!
!  =====================================================================
!
!     .. Intrinsic Functions ..
      INTRINSIC MAX
!     ..
!     .. Local Scalars ..
      DOUBLE PRECISION TEMP
      INTEGER I,INFO,J,K,NROWA
      LOGICAL BUFFER1,BUFFER2,BUFFER3,BUFFER4,BUFFER5, &
              BUFFER6,BUFFER7,BUFFER8,BUFFER9
      LOGICAL LSIDE,NOUNIT,UPPER
!     ..
!     .. Parameters ..
      DOUBLE PRECISION ONE,ZERO
      PARAMETER (ONE=1.0D+0,ZERO=0.0D+0)
!     ..
!
!     Test the input parameters.
!
      CALL LSAME_RETURN(SIDE,'L', LSIDE)
      IF (LSIDE) THEN
          NROWA = M
      ELSE
          NROWA = N
      END IF
      CALL LSAME_RETURN(DIAG,'N',NOUNIT)
      CALL LSAME_RETURN(UPLO,'U',UPPER)
!
      CALL LSAME_RETURN(SIDE,'R', BUFFER1)
      CALL LSAME_RETURN(UPLO,'L', BUFFER2)
      CALL LSAME_RETURN(TRANSA,'N', BUFFER3)
      CALL LSAME_RETURN(TRANSA,'T', BUFFER4)
      CALL LSAME_RETURN(TRANSA,'C', BUFFER5)
      CALL LSAME_RETURN(DIAG,'U', BUFFER6)
      CALL LSAME_RETURN(DIAG,'N', BUFFER7)

      INFO = 0
      IF ((.NOT.LSIDE) .AND. (.NOT.BUFFER1)) THEN
          INFO = 1
      ELSE IF ((.NOT.UPPER) .AND. (.NOT.BUFFER2)) THEN
          INFO = 2
      ELSE IF ((.NOT.BUFFER3) .AND. &
               (.NOT.BUFFER4) .AND. &
               (.NOT.BUFFER5)) THEN
          INFO = 3
      ELSE IF ((.NOT.BUFFER6) .AND. (.NOT.BUFFER7)) THEN
          INFO = 4
      ELSE IF (M.LT.0) THEN
          INFO = 5
      ELSE IF (N.LT.0) THEN
          INFO = 6
      ELSE IF (LDA.LT.MAX(1,NROWA)) THEN
          INFO = 9
      ELSE IF (LDB.LT.MAX(1,M)) THEN
          INFO = 11
      END IF
      IF (INFO.NE.0) THEN
          CALL XERBLA('DTRSM ',INFO)
          RETURN
      END IF
!
!     Quick return if possible.
!
      IF (M.EQ.0 .OR. N.EQ.0) RETURN
!
!     And when  alpha.eq.zero.
!
      IF (ALPHA.EQ.ZERO) THEN
          DO 20 J = 1,N
              DO 10 I = 1,M
                  B(I,J) = ZERO
   10         CONTINUE
   20     CONTINUE
          RETURN
      END IF
!
!     Start the operations.
!
      CALL LSAME_RETURN(TRANSA,'N', BUFFER8)
      IF (LSIDE) THEN
          IF (BUFFER8) THEN
!
!           Form  B := alpha*inv( A )*B.
!
              IF (UPPER) THEN
                  DO 60 J = 1,N
                      IF (ALPHA.NE.ONE) THEN
                          DO 30 I = 1,M
                              B(I,J) = ALPHA*B(I,J)
   30                     CONTINUE
                      END IF
                      DO 50 K = M,1,-1
                          IF (B(K,J).NE.ZERO) THEN
                              IF (NOUNIT) B(K,J) = B(K,J)/A(K,K)
                              DO 40 I = 1,K - 1
                                  B(I,J) = B(I,J) - B(K,J)*A(I,K)
   40                         CONTINUE
                          END IF
   50                 CONTINUE
   60             CONTINUE
              ELSE
                  DO 100 J = 1,N
                      IF (ALPHA.NE.ONE) THEN
                          DO 70 I = 1,M
                              B(I,J) = ALPHA*B(I,J)
   70                     CONTINUE
                      END IF
                      DO 90 K = 1,M
                          IF (B(K,J).NE.ZERO) THEN
                              IF (NOUNIT) B(K,J) = B(K,J)/A(K,K)
                              DO 80 I = K + 1,M
                                  B(I,J) = B(I,J) - B(K,J)*A(I,K)
   80                         CONTINUE
                          END IF
   90                 CONTINUE
  100             CONTINUE
              END IF
          ELSE
!
!           Form  B := alpha*inv( A**T )*B.
!
              IF (UPPER) THEN
                  DO 130 J = 1,N
                      DO 120 I = 1,M
                          TEMP = ALPHA*B(I,J)
                          DO 110 K = 1,I - 1
                              TEMP = TEMP - A(K,I)*B(K,J)
  110                     CONTINUE
                          IF (NOUNIT) TEMP = TEMP/A(I,I)
                          B(I,J) = TEMP
  120                 CONTINUE
  130             CONTINUE
              ELSE
                  DO 160 J = 1,N
                      DO 150 I = M,1,-1
                          TEMP = ALPHA*B(I,J)
                          DO 140 K = I + 1,M
                              TEMP = TEMP - A(K,I)*B(K,J)
  140                     CONTINUE
                          IF (NOUNIT) TEMP = TEMP/A(I,I)
                          B(I,J) = TEMP
  150                 CONTINUE
  160             CONTINUE
              END IF
          END IF
      ELSE
         CALL LSAME_RETURN(TRANSA,'N', BUFFER9)
          IF (BUFFER9) THEN
!
!           Form  B := alpha*B*inv( A ).
!
              IF (UPPER) THEN
                  DO 210 J = 1,N
                      IF (ALPHA.NE.ONE) THEN
                          DO 170 I = 1,M
                              B(I,J) = ALPHA*B(I,J)
  170                     CONTINUE
                      END IF
                      DO 190 K = 1,J - 1
                          IF (A(K,J).NE.ZERO) THEN
                              DO 180 I = 1,M
                                  B(I,J) = B(I,J) - A(K,J)*B(I,K)
  180                         CONTINUE
                          END IF
  190                 CONTINUE
                      IF (NOUNIT) THEN
                          TEMP = ONE/A(J,J)
                          DO 200 I = 1,M
                              B(I,J) = TEMP*B(I,J)
  200                     CONTINUE
                      END IF
  210             CONTINUE
              ELSE
                  DO 260 J = N,1,-1
                      IF (ALPHA.NE.ONE) THEN
                          DO 220 I = 1,M
                              B(I,J) = ALPHA*B(I,J)
  220                     CONTINUE
                      END IF
                      DO 240 K = J + 1,N
                          IF (A(K,J).NE.ZERO) THEN
                              DO 230 I = 1,M
                                  B(I,J) = B(I,J) - A(K,J)*B(I,K)
  230                         CONTINUE
                          END IF
  240                 CONTINUE
                      IF (NOUNIT) THEN
                          TEMP = ONE/A(J,J)
                          DO 250 I = 1,M
                              B(I,J) = TEMP*B(I,J)
  250                     CONTINUE
                      END IF
  260             CONTINUE
              END IF
          ELSE
!
!           Form  B := alpha*B*inv( A**T ).
!
              IF (UPPER) THEN
                  DO 310 K = N,1,-1
                      IF (NOUNIT) THEN
                          TEMP = ONE/A(K,K)
                          DO 270 I = 1,M
                              B(I,K) = TEMP*B(I,K)
  270                     CONTINUE
                      END IF
                      DO 290 J = 1,K - 1
                          IF (A(J,K).NE.ZERO) THEN
                              TEMP = A(J,K)
                              DO 280 I = 1,M
                                  B(I,J) = B(I,J) - TEMP*B(I,K)
  280                         CONTINUE
                          END IF
  290                 CONTINUE
                      IF (ALPHA.NE.ONE) THEN
                          DO 300 I = 1,M
                              B(I,K) = ALPHA*B(I,K)
  300                     CONTINUE
                      END IF
  310             CONTINUE
              ELSE
                  DO 360 K = 1,N
                      IF (NOUNIT) THEN
                          TEMP = ONE/A(K,K)
                          DO 320 I = 1,M
                              B(I,K) = TEMP*B(I,K)
  320                     CONTINUE
                      END IF
                      DO 340 J = K + 1,N
                          IF (A(J,K).NE.ZERO) THEN
                              TEMP = A(J,K)
                              DO 330 I = 1,M
                                  B(I,J) = B(I,J) - TEMP*B(I,K)
  330                         CONTINUE
                          END IF
  340                 CONTINUE
                      IF (ALPHA.NE.ONE) THEN
                          DO 350 I = 1,M
                              B(I,K) = ALPHA*B(I,K)
  350                     CONTINUE
                      END IF
  360             CONTINUE
              END IF
          END IF
      END IF
!
      RETURN
!
!     End of DTRSM .
!
      END



      SUBROUTINE XERBLA( SRNAME, INFO )
!
!  -- Reference BLAS level1 routine (version 3.7.0) --
!  -- Reference BLAS is a software package provided by Univ. of Tennessee,    --
!  -- Univ. of California Berkeley, Univ. of Colorado Denver and NAG Ltd..--
!     December 2016
      implicit none (type, external)
!     .. Scalar Arguments ..
      CHARACTER*(*)      SRNAME
      INTEGER            INFO
!     ..
!
! =====================================================================
!
!     .. Intrinsic Functions ..
      INTRINSIC          LEN_TRIM
!     ..
!     .. Executable Statements ..
!
      WRITE( *, FMT = 9999 )SRNAME( 1:LEN_TRIM( SRNAME ) ), INFO
!
      STOP
!
 9999 FORMAT( ' !! On entry to ', A, ' parameter number ', I2, ' had ', &
            'an illegal value' )
!
!     End of XERBLA
!
      END

      SUBROUTINE DSCAL(N,DA,DX,INCX)
!
!  -- Reference BLAS level1 routine (version 3.8.0) --
!  -- Reference BLAS is a software package provided by Univ. of Tennessee,    --
!  -- Univ. of California Berkeley, Univ. of Colorado Denver and NAG Ltd..--
!     November 2017
      implicit none (type, external)
!     .. Scalar Arguments ..
      DOUBLE PRECISION DA
      INTEGER INCX,N
!     ..
!     .. Array Arguments ..
      DOUBLE PRECISION DX(*)
!     ..
!
!  =====================================================================
!
!     .. Local Scalars ..
      INTEGER I,M,MP1,NINCX
!     ..
!     .. Intrinsic Functions ..
      INTRINSIC MOD
!     ..
      IF (N.LE.0 .OR. INCX.LE.0) RETURN
      IF (INCX.EQ.1) THEN
!
!        code for increment equal to 1
!
!
!        clean-up loop
!
         M = MOD(N,5)
         IF (M.NE.0) THEN
            DO I = 1,M
               DX(I) = DA*DX(I)
            END DO
            IF (N.LT.5) RETURN
         END IF
         MP1 = M + 1
         DO I = MP1,N,5
            DX(I) = DA*DX(I)
            DX(I+1) = DA*DX(I+1)
            DX(I+2) = DA*DX(I+2)
            DX(I+3) = DA*DX(I+3)
            DX(I+4) = DA*DX(I+4)
         END DO
      ELSE
!
!        code for increment not equal to 1
!
         NINCX = N*INCX
         DO I = 1,NINCX,INCX
            DX(I) = DA*DX(I)
         END DO
      END IF
      RETURN
      END

      SUBROUTINE ILAENV_RETURN( ISPEC, NAME, OPTS, N1, N2, N3, N4, ILAENV)
!
!  -- LAPACK auxiliary routine (version 3.9.0) --
!  -- LAPACK is a software package provided by Univ. of Tennessee,    --
!  -- Univ. of California Berkeley, Univ. of Colorado Denver and NAG Ltd..--
!     November 2019
      implicit none (type, external)
!     .. Scalar Arguments ..
      CHARACTER*( * )    NAME, OPTS
      INTEGER            ISPEC, N1, N2, N3, N4, ILAENV
!     ..
!
!  =====================================================================
!
!     .. Local Scalars ..
      INTEGER            I, IC, IZ, NB, NBMIN, NX
      LOGICAL            CNAME, SNAME, TWOSTAGE
      CHARACTER          C1*1, C2*2, C4*2, C3*3, SUBNAM*16
!     ..
!     .. Intrinsic Functions ..
      INTRINSIC          CHAR, ICHAR, INT, MIN, REAL
!     ..
!     .. Executable Statements ..
!
      GO TO ( 10, 10, 10, 80, 90, 100, 110, 120, &
              130, 140, 150, 160, 160, 160, 160, 160)ISPEC
!
!     Invalid value for ISPEC
!
      ILAENV = -1
      RETURN
!
   10 CONTINUE
!
!     Convert NAME to upper case if the first character is lower case.
!
      ILAENV = 1
      SUBNAM = NAME
      IC = ICHAR( SUBNAM( 1: 1 ) )
      IZ = ICHAR( 'Z' )
      IF( IZ.EQ.90 .OR. IZ.EQ.122 ) THEN
!
!        ASCII character set
!
         IF( IC.GE.97 .AND. IC.LE.122 ) THEN
            SUBNAM( 1: 1 ) = CHAR( IC-32 )
            DO 20 I = 2, 6
               IC = ICHAR( SUBNAM( I: I ) )
               IF( IC.GE.97 .AND. IC.LE.122 ) &
                  SUBNAM( I: I ) = CHAR( IC-32 )
   20       CONTINUE
         END IF
!
      ELSE IF( IZ.EQ.233 .OR. IZ.EQ.169 ) THEN
!
!        EBCDIC character set
!
         IF( ( IC.GE.129 .AND. IC.LE.137 ) .OR. &
             ( IC.GE.145 .AND. IC.LE.153 ) .OR. &
             ( IC.GE.162 .AND. IC.LE.169 ) ) THEN
            SUBNAM( 1: 1 ) = CHAR( IC+64 )
            DO 30 I = 2, 6
               IC = ICHAR( SUBNAM( I: I ) )
               IF( ( IC.GE.129 .AND. IC.LE.137 ) .OR. &
                   ( IC.GE.145 .AND. IC.LE.153 ) .OR. &
                   ( IC.GE.162 .AND. IC.LE.169 ) )SUBNAM( I: &
                   I ) = CHAR( IC+64 )
   30       CONTINUE
         END IF
!
      ELSE IF( IZ.EQ.218 .OR. IZ.EQ.250 ) THEN
!
!        Prime machines:  ASCII+128
!
         IF( IC.GE.225 .AND. IC.LE.250 ) THEN
            SUBNAM( 1: 1 ) = CHAR( IC-32 )
            DO 40 I = 2, 6
               IC = ICHAR( SUBNAM( I: I ) )
               IF( IC.GE.225 .AND. IC.LE.250 ) &
                  SUBNAM( I: I ) = CHAR( IC-32 )
   40       CONTINUE
         END IF
      END IF
!
      C1 = SUBNAM( 1: 1 )
      SNAME = C1.EQ.'S' .OR. C1.EQ.'D'
      CNAME = C1.EQ.'C' .OR. C1.EQ.'Z'
      IF( .NOT.( CNAME .OR. SNAME ) ) &
         RETURN
      C2 = SUBNAM( 2: 3 )
      C3 = SUBNAM( 4: 6 )
      C4 = C3( 2: 3 )
      TWOSTAGE = LEN( SUBNAM ).GE.11 &
                 .AND. SUBNAM( 11: 11 ).EQ.'2'
!
      GO TO ( 50, 60, 70 )ISPEC
!
   50 CONTINUE
!
!     ISPEC = 1:  block size
!
!     In these examples, separate code is provided for setting NB for
!     real and complex.  We assume that NB will take the same value in
!     single or double precision.
!
      NB = 1
!
      IF( SUBNAM(2:6).EQ.'LAORH' ) THEN
!
!        This is for *LAORHR_GETRFNP routine
!
         IF( SNAME ) THEN
             NB = 32
         ELSE
             NB = 32
         END IF
      ELSE IF( C2.EQ.'GE' ) THEN
         IF( C3.EQ.'TRF' ) THEN
            IF( SNAME ) THEN
               NB = 64
            ELSE
               NB = 64
            END IF
         ELSE IF( C3.EQ.'QRF' .OR. C3.EQ.'RQF' .OR. C3.EQ.'LQF' .OR. &
                  C3.EQ.'QLF' ) THEN
            IF( SNAME ) THEN
               NB = 32
            ELSE
               NB = 32
            END IF
         ELSE IF( C3.EQ.'QR ') THEN
            IF( N3 .EQ. 1) THEN
               IF( SNAME ) THEN
!     M*N
                  IF ((N1*N2.LE.131072).OR.(N1.LE.8192)) THEN
                     NB = N1
                  ELSE
                     NB = 32768/N2
                  END IF
               ELSE
                  IF ((N1*N2.LE.131072).OR.(N1.LE.8192)) THEN
                     NB = N1
                  ELSE
                     NB = 32768/N2
                  END IF
               END IF
            ELSE
               IF( SNAME ) THEN
                  NB = 1
               ELSE
                  NB = 1
               END IF
            END IF
         ELSE IF( C3.EQ.'LQ ') THEN
            IF( N3 .EQ. 2) THEN
               IF( SNAME ) THEN
!     M*N
                  IF ((N1*N2.LE.131072).OR.(N1.LE.8192)) THEN
                     NB = N1
                  ELSE
                     NB = 32768/N2
                  END IF
               ELSE
                  IF ((N1*N2.LE.131072).OR.(N1.LE.8192)) THEN
                     NB = N1
                  ELSE
                     NB = 32768/N2
                  END IF
               END IF
            ELSE
               IF( SNAME ) THEN
                  NB = 1
               ELSE
                  NB = 1
               END IF
            END IF
         ELSE IF( C3.EQ.'HRD' ) THEN
            IF( SNAME ) THEN
               NB = 32
            ELSE
               NB = 32
            END IF
         ELSE IF( C3.EQ.'BRD' ) THEN
            IF( SNAME ) THEN
               NB = 32
            ELSE
               NB = 32
            END IF
         ELSE IF( C3.EQ.'TRI' ) THEN
            IF( SNAME ) THEN
               NB = 64
            ELSE
               NB = 64
            END IF
         END IF
      ELSE IF( C2.EQ.'PO' ) THEN
         IF( C3.EQ.'TRF' ) THEN
            IF( SNAME ) THEN
               NB = 64
            ELSE
               NB = 64
            END IF
         END IF
      ELSE IF( C2.EQ.'SY' ) THEN
         IF( C3.EQ.'TRF' ) THEN
            IF( SNAME ) THEN
               IF( TWOSTAGE ) THEN
                  NB = 192
               ELSE
                  NB = 64
               END IF
            ELSE
               IF( TWOSTAGE ) THEN
                  NB = 192
               ELSE
                  NB = 64
               END IF
            END IF
         ELSE IF( SNAME .AND. C3.EQ.'TRD' ) THEN
            NB = 32
         ELSE IF( SNAME .AND. C3.EQ.'GST' ) THEN
            NB = 64
         END IF
      ELSE IF( CNAME .AND. C2.EQ.'HE' ) THEN
         IF( C3.EQ.'TRF' ) THEN
            IF( TWOSTAGE ) THEN
               NB = 192
            ELSE
               NB = 64
            END IF
         ELSE IF( C3.EQ.'TRD' ) THEN
            NB = 32
         ELSE IF( C3.EQ.'GST' ) THEN
            NB = 64
         END IF
      ELSE IF( SNAME .AND. C2.EQ.'OR' ) THEN
         IF( C3( 1: 1 ).EQ.'G' ) THEN
            IF( C4.EQ.'QR' .OR. C4.EQ.'RQ' .OR. C4.EQ.'LQ' .OR. C4.EQ. &
                'QL' .OR. C4.EQ.'HR' .OR. C4.EQ.'TR' .OR. C4.EQ.'BR' ) &
                 THEN
               NB = 32
            END IF
         ELSE IF( C3( 1: 1 ).EQ.'M' ) THEN
            IF( C4.EQ.'QR' .OR. C4.EQ.'RQ' .OR. C4.EQ.'LQ' .OR. C4.EQ. &
                'QL' .OR. C4.EQ.'HR' .OR. C4.EQ.'TR' .OR. C4.EQ.'BR' ) &
                 THEN
               NB = 32
            END IF
         END IF
      ELSE IF( CNAME .AND. C2.EQ.'UN' ) THEN
         IF( C3( 1: 1 ).EQ.'G' ) THEN
            IF( C4.EQ.'QR' .OR. C4.EQ.'RQ' .OR. C4.EQ.'LQ' .OR. C4.EQ. &
                'QL' .OR. C4.EQ.'HR' .OR. C4.EQ.'TR' .OR. C4.EQ.'BR' ) &
                 THEN
               NB = 32
            END IF
         ELSE IF( C3( 1: 1 ).EQ.'M' ) THEN
            IF( C4.EQ.'QR' .OR. C4.EQ.'RQ' .OR. C4.EQ.'LQ' .OR. C4.EQ. &
                'QL' .OR. C4.EQ.'HR' .OR. C4.EQ.'TR' .OR. C4.EQ.'BR' ) &
                 THEN
               NB = 32
            END IF
         END IF
      ELSE IF( C2.EQ.'GB' ) THEN
         IF( C3.EQ.'TRF' ) THEN
            IF( SNAME ) THEN
               IF( N4.LE.64 ) THEN
                  NB = 1
               ELSE
                  NB = 32
               END IF
            ELSE
               IF( N4.LE.64 ) THEN
                  NB = 1
               ELSE
                  NB = 32
               END IF
            END IF
         END IF
      ELSE IF( C2.EQ.'PB' ) THEN
         IF( C3.EQ.'TRF' ) THEN
            IF( SNAME ) THEN
               IF( N2.LE.64 ) THEN
                  NB = 1
               ELSE
                  NB = 32
               END IF
            ELSE
               IF( N2.LE.64 ) THEN
                  NB = 1
               ELSE
                  NB = 32
               END IF
            END IF
         END IF
      ELSE IF( C2.EQ.'TR' ) THEN
         IF( C3.EQ.'TRI' ) THEN
            IF( SNAME ) THEN
               NB = 64
            ELSE
               NB = 64
            END IF
         ELSE IF ( C3.EQ.'EVC' ) THEN
            IF( SNAME ) THEN
               NB = 64
            ELSE
               NB = 64
            END IF
         END IF
      ELSE IF( C2.EQ.'LA' ) THEN
         IF( C3.EQ.'UUM' ) THEN
            IF( SNAME ) THEN
               NB = 64
            ELSE
               NB = 64
            END IF
         END IF
      ELSE IF( SNAME .AND. C2.EQ.'ST' ) THEN
         IF( C3.EQ.'EBZ' ) THEN
            NB = 1
         END IF
      ELSE IF( C2.EQ.'GG' ) THEN
         NB = 32
         IF( C3.EQ.'HD3' ) THEN
            IF( SNAME ) THEN
               NB = 32
            ELSE
               NB = 32
            END IF
         END IF
      END IF
      ILAENV = NB
      RETURN
!
   60 CONTINUE
!
!     ISPEC = 2:  minimum block size
!
      NBMIN = 2
      IF( C2.EQ.'GE' ) THEN
         IF( C3.EQ.'QRF' .OR. C3.EQ.'RQF' .OR. C3.EQ.'LQF' .OR. C3.EQ. &
             'QLF' ) THEN
            IF( SNAME ) THEN
               NBMIN = 2
            ELSE
               NBMIN = 2
            END IF
         ELSE IF( C3.EQ.'HRD' ) THEN
            IF( SNAME ) THEN
               NBMIN = 2
            ELSE
               NBMIN = 2
            END IF
         ELSE IF( C3.EQ.'BRD' ) THEN
            IF( SNAME ) THEN
               NBMIN = 2
            ELSE
               NBMIN = 2
            END IF
         ELSE IF( C3.EQ.'TRI' ) THEN
            IF( SNAME ) THEN
               NBMIN = 2
            ELSE
               NBMIN = 2
            END IF
         END IF
      ELSE IF( C2.EQ.'SY' ) THEN
         IF( C3.EQ.'TRF' ) THEN
            IF( SNAME ) THEN
               NBMIN = 8
            ELSE
               NBMIN = 8
            END IF
         ELSE IF( SNAME .AND. C3.EQ.'TRD' ) THEN
            NBMIN = 2
         END IF
      ELSE IF( CNAME .AND. C2.EQ.'HE' ) THEN
         IF( C3.EQ.'TRD' ) THEN
            NBMIN = 2
         END IF
      ELSE IF( SNAME .AND. C2.EQ.'OR' ) THEN
         IF( C3( 1: 1 ).EQ.'G' ) THEN
            IF( C4.EQ.'QR' .OR. C4.EQ.'RQ' .OR. C4.EQ.'LQ' .OR. C4.EQ. &
                'QL' .OR. C4.EQ.'HR' .OR. C4.EQ.'TR' .OR. C4.EQ.'BR' ) &
                 THEN
               NBMIN = 2
            END IF
         ELSE IF( C3( 1: 1 ).EQ.'M' ) THEN
            IF( C4.EQ.'QR' .OR. C4.EQ.'RQ' .OR. C4.EQ.'LQ' .OR. C4.EQ. &
                'QL' .OR. C4.EQ.'HR' .OR. C4.EQ.'TR' .OR. C4.EQ.'BR' ) &
                 THEN
               NBMIN = 2
            END IF
         END IF
      ELSE IF( CNAME .AND. C2.EQ.'UN' ) THEN
         IF( C3( 1: 1 ).EQ.'G' ) THEN
            IF( C4.EQ.'QR' .OR. C4.EQ.'RQ' .OR. C4.EQ.'LQ' .OR. C4.EQ. &
                'QL' .OR. C4.EQ.'HR' .OR. C4.EQ.'TR' .OR. C4.EQ.'BR' ) &
                 THEN
               NBMIN = 2
            END IF
         ELSE IF( C3( 1: 1 ).EQ.'M' ) THEN
            IF( C4.EQ.'QR' .OR. C4.EQ.'RQ' .OR. C4.EQ.'LQ' .OR. C4.EQ. &
                'QL' .OR. C4.EQ.'HR' .OR. C4.EQ.'TR' .OR. C4.EQ.'BR' ) &
                 THEN
               NBMIN = 2
            END IF
         END IF
      ELSE IF( C2.EQ.'GG' ) THEN
         NBMIN = 2
         IF( C3.EQ.'HD3' ) THEN
            NBMIN = 2
         END IF
      END IF
      ILAENV = NBMIN
      RETURN
!
   70 CONTINUE
!
!     ISPEC = 3:  crossover point
!
      NX = 0
      IF( C2.EQ.'GE' ) THEN
         IF( C3.EQ.'QRF' .OR. C3.EQ.'RQF' .OR. C3.EQ.'LQF' .OR. C3.EQ. &
             'QLF' ) THEN
            IF( SNAME ) THEN
               NX = 128
            ELSE
               NX = 128
            END IF
         ELSE IF( C3.EQ.'HRD' ) THEN
            IF( SNAME ) THEN
               NX = 128
            ELSE
               NX = 128
            END IF
         ELSE IF( C3.EQ.'BRD' ) THEN
            IF( SNAME ) THEN
               NX = 128
            ELSE
               NX = 128
            END IF
         END IF
      ELSE IF( C2.EQ.'SY' ) THEN
         IF( SNAME .AND. C3.EQ.'TRD' ) THEN
            NX = 32
         END IF
      ELSE IF( CNAME .AND. C2.EQ.'HE' ) THEN
         IF( C3.EQ.'TRD' ) THEN
            NX = 32
         END IF
      ELSE IF( SNAME .AND. C2.EQ.'OR' ) THEN
         IF( C3( 1: 1 ).EQ.'G' ) THEN
            IF( C4.EQ.'QR' .OR. C4.EQ.'RQ' .OR. C4.EQ.'LQ' .OR. C4.EQ. &
                'QL' .OR. C4.EQ.'HR' .OR. C4.EQ.'TR' .OR. C4.EQ.'BR' ) &
                 THEN
               NX = 128
            END IF
         END IF
      ELSE IF( CNAME .AND. C2.EQ.'UN' ) THEN
         IF( C3( 1: 1 ).EQ.'G' ) THEN
            IF( C4.EQ.'QR' .OR. C4.EQ.'RQ' .OR. C4.EQ.'LQ' .OR. C4.EQ. &
                'QL' .OR. C4.EQ.'HR' .OR. C4.EQ.'TR' .OR. C4.EQ.'BR' ) &
                 THEN
               NX = 128
            END IF
         END IF
      ELSE IF( C2.EQ.'GG' ) THEN
         NX = 128
         IF( C3.EQ.'HD3' ) THEN
            NX = 128
         END IF
      END IF
      ILAENV = NX
      RETURN
!
   80 CONTINUE
!
!     ISPEC = 4:  number of shifts (used by xHSEQR)
!
      ILAENV = 6
      RETURN
!
   90 CONTINUE
!
!     ISPEC = 5:  minimum column dimension (not used)
!
      ILAENV = 2
      RETURN
!
  100 CONTINUE
!
!     ISPEC = 6:  crossover point for SVD (used by xGELSS and xGESVD)
!
      ILAENV = INT( REAL( MIN( N1, N2 ) )*1.6E0 )
      RETURN
!
  110 CONTINUE
!
!     ISPEC = 7:  number of processors (not used)
!
      ILAENV = 1
      RETURN
!
  120 CONTINUE
!
!     ISPEC = 8:  crossover point for multishift (used by xHSEQR)
!
      ILAENV = 50
      RETURN
!
  130 CONTINUE
!
!     ISPEC = 9:  maximum size of the subproblems at the bottom of the
!                 computation tree in the divide-and-conquer algorithm
!                 (used by xGELSD and xGESDD)
!
      ILAENV = 25
      RETURN
!
  140 CONTINUE
!
!     ISPEC = 10: ieee NaN arithmetic can be trusted not to trap
!
!     ILAENV = 0
      ILAENV = 1
      IF( ILAENV.EQ.1 ) THEN
         CALL IEEECK_RETURN( 1, 0.0, 1.0, ILAENV)
      END IF
      RETURN
!
  150 CONTINUE
!
!     ISPEC = 11: infinity arithmetic can be trusted not to trap
!
!     ILAENV = 0
      ILAENV = 1
      IF( ILAENV.EQ.1 ) THEN
         CALL IEEECK_RETURN( 0, 0.0, 1.0, ILAENV )
      END IF
      RETURN
!
  160 CONTINUE
!
!     12 <= ISPEC <= 16: xHSEQR or related subroutines.
!
!      CALL IPARMQ_RETURN( ISPEC, NAME, OPTS, N1, N2, N3, N4, ILAENV)
      RETURN
!
!     End of ILAENV_RETURN
!
      END

      SUBROUTINE IEEECK_RETURN( ISPEC, ZERO, ONE, IEEECK )
!
!  -- LAPACK auxiliary routine (version 3.7.0) --
!  -- LAPACK is a software package provided by Univ. of Tennessee,    --
!  -- Univ. of California Berkeley, Univ. of Colorado Denver and NAG Ltd..--
!     December 2016
      implicit none (type, external)
!     .. Scalar Arguments ..
      INTEGER            ISPEC, IEEECK
      REAL               ONE, ZERO
!     ..
!
!  =====================================================================
!
!     .. Local Scalars ..
      REAL               NAN1, NAN2, NAN3, NAN4, NAN5, NAN6, NEGINF, &
                         NEGZRO, NEWZRO, POSINF
!     ..
!     .. Executable Statements ..
      IEEECK = 1
!
      POSINF = ONE / ZERO
      IF( POSINF.LE.ONE ) THEN
         IEEECK = 0
         RETURN
      END IF
!
      NEGINF = -ONE / ZERO
      IF( NEGINF.GE.ZERO ) THEN
         IEEECK = 0
         RETURN
      END IF
!
      NEGZRO = ONE / ( NEGINF+ONE )
      IF( NEGZRO.NE.ZERO ) THEN
         IEEECK = 0
         RETURN
      END IF
!
      NEGINF = ONE / NEGZRO
      IF( NEGINF.GE.ZERO ) THEN
         IEEECK = 0
         RETURN
      END IF
!
      NEWZRO = NEGZRO + ZERO
      IF( NEWZRO.NE.ZERO ) THEN
         IEEECK = 0
         RETURN
      END IF
!
      POSINF = ONE / NEWZRO
      IF( POSINF.LE.ONE ) THEN
         IEEECK = 0
         RETURN
      END IF
!
      NEGINF = NEGINF*POSINF
      IF( NEGINF.GE.ZERO ) THEN
         IEEECK = 0
         RETURN
      END IF
!
      POSINF = POSINF*POSINF
      IF( POSINF.LE.ONE ) THEN
         IEEECK = 0
         RETURN
      END IF
!
!
!
!
!     Return if we were only asked to check infinity arithmetic
!
      IF( ISPEC.EQ.0 ) &
         RETURN
!
      NAN1 = POSINF + NEGINF
!
      NAN2 = POSINF / NEGINF
!
      NAN3 = POSINF / POSINF
!
      NAN4 = POSINF*ZERO
!
      NAN5 = NEGINF*NEGZRO
!
      NAN6 = NAN5*ZERO
!
      IF( NAN1.EQ.NAN1 ) THEN
         IEEECK = 0
         RETURN
      END IF
!
      IF( NAN2.EQ.NAN2 ) THEN
         IEEECK = 0
         RETURN
      END IF
!
      IF( NAN3.EQ.NAN3 ) THEN
         IEEECK = 0
         RETURN
      END IF
!
      IF( NAN4.EQ.NAN4 ) THEN
         IEEECK = 0
         RETURN
      END IF
!
      IF( NAN5.EQ.NAN5 ) THEN
         IEEECK = 0
         RETURN
      END IF
!
      IF( NAN6.EQ.NAN6 ) THEN
         IEEECK = 0
         RETURN
      END IF
!
      RETURN
      END

      SUBROUTINE LSAME_RETURN(CA,CB,LSAME)
!
!  -- Reference BLAS level1 routine (version 3.1) --
!  -- Reference BLAS is a software package provided by Univ. of Tennessee,    --
!  -- Univ. of California Berkeley, Univ. of Colorado Denver and NAG Ltd..--
!     December 2016
!
!     .. Scalar Arguments ..
      CHARACTER CA,CB
      LOGICAL LSAME
!     ..
!
! =====================================================================
!
!     .. Intrinsic Functions ..
      INTRINSIC ICHAR
!     ..
!     .. Local Scalars ..
      INTEGER INTA,INTB,ZCODE
!     ..
!
!     Test if the characters are equal
!
      LSAME = CA .EQ. CB
      IF (LSAME) RETURN
!
!     Now test for equivalence if both characters are alphabetic.
!
      ZCODE = ICHAR('Z')
!
!     Use 'Z' rather than 'A' so that ASCII can be detected on Prime
!     machines, on which ICHAR returns a value with bit 8 set.
!     ICHAR('A') on Prime machines returns 193 which is the same as
!     ICHAR('A') on an EBCDIC machine.
!
      INTA = ICHAR(CA)
      INTB = ICHAR(CB)
!
      IF (ZCODE.EQ.90 .OR. ZCODE.EQ.122) THEN
!
!        ASCII is assumed - ZCODE is the ASCII code of either lower or
!        upper case 'Z'.
!
          IF (INTA.GE.97 .AND. INTA.LE.122) INTA = INTA - 32
          IF (INTB.GE.97 .AND. INTB.LE.122) INTB = INTB - 32
!
      ELSE IF (ZCODE.EQ.233 .OR. ZCODE.EQ.169) THEN
!
!        EBCDIC is assumed - ZCODE is the EBCDIC code of either lower or
!        upper case 'Z'.
!
          IF (INTA.GE.129 .AND. INTA.LE.137 .OR. &
              INTA.GE.145 .AND. INTA.LE.153 .OR. &
              INTA.GE.162 .AND. INTA.LE.169) INTA = INTA + 64
          IF (INTB.GE.129 .AND. INTB.LE.137 .OR. &
              INTB.GE.145 .AND. INTB.LE.153 .OR. &
              INTB.GE.162 .AND. INTB.LE.169) INTB = INTB + 64
!
      ELSE IF (ZCODE.EQ.218 .OR. ZCODE.EQ.250) THEN
!
!        ASCII is assumed, on Prime machines - ZCODE is the ASCII code
!        plus 128 of either lower or upper case 'Z'.
!
          IF (INTA.GE.225 .AND. INTA.LE.250) INTA = INTA - 32
          IF (INTB.GE.225 .AND. INTB.LE.250) INTB = INTB - 32
      END IF
      LSAME = INTA .EQ. INTB
!
!     RETURN
!
!     End of LSAME
!
      END

      SUBROUTINE DLAMCH_RETURN( CMACH, DLAMCH )
!
!  -- LAPACK auxiliary routine (version 3.7.0) --
!  -- LAPACK is a software package provided by Univ. of Tennessee,    --
!  -- Univ. of California Berkeley, Univ. of Colorado Denver and NAG Ltd..--
!     December 2016
      implicit none (type, external)
!     .. Scalar Arguments ..
      CHARACTER          CMACH
      DOUBLE PRECISION   DLAMCH
!     ..
!
! =====================================================================
!
!     .. Parameters ..
      DOUBLE PRECISION   ONE, ZERO
      PARAMETER          ( ONE = 1.0D+0, ZERO = 0.0D+0 )
!     ..
!     .. Local Scalars ..
      DOUBLE PRECISION   RND, EPS, SFMIN, SMALL, RMACH
!     ..
!     .. Intrinsic Functions ..
      INTRINSIC          DIGITS, EPSILON, HUGE, MAXEXPONENT, &
                         MINEXPONENT, RADIX, TINY
      LOGICAL            BUFFER1, BUFFER2, BUFFER3, BUFFER4, BUFFER5, &
                         BUFFER6, BUFFER7, BUFFER8, BUFFER9, BUFFER10
!     ..
!     .. Executable Statements ..
!
!
!     Assume rounding, not chopping. Always.
!
      RND = ONE
!
      IF( ONE.EQ.RND ) THEN
         EPS = EPSILON(ZERO) * 0.5
      ELSE
         EPS = EPSILON(ZERO)
      END IF
!
      CALL LSAME_RETURN( CMACH, 'E', BUFFER1 )
      CALL LSAME_RETURN( CMACH, 'S', BUFFER2 )
      CALL LSAME_RETURN( CMACH, 'B', BUFFER3 )
      CALL LSAME_RETURN( CMACH, 'P', BUFFER4 )
      CALL LSAME_RETURN( CMACH, 'N', BUFFER5 )
      CALL LSAME_RETURN( CMACH, 'R', BUFFER6 )
      CALL LSAME_RETURN( CMACH, 'M', BUFFER7 )
      CALL LSAME_RETURN( CMACH, 'U', BUFFER8 )
      CALL LSAME_RETURN( CMACH, 'L', BUFFER9 )
      CALL LSAME_RETURN( CMACH, 'O', BUFFER10 )

      IF( BUFFER1 ) THEN
         RMACH = EPS
      ELSE IF( BUFFER2 ) THEN
         SFMIN = TINY(ZERO)
         SMALL = ONE / HUGE(ZERO)
         IF( SMALL.GE.SFMIN ) THEN
!
!           Use SMALL plus a bit, to avoid the possibility of rounding
!           causing overflow when computing  1/sfmin.
!
            SFMIN = SMALL*( ONE+EPS )
         END IF
         RMACH = SFMIN
      ELSE IF( BUFFER3 ) THEN
         RMACH = RADIX(ZERO)
      ELSE IF( BUFFER4 ) THEN
         RMACH = EPS * RADIX(ZERO)
      ELSE IF( BUFFER5 ) THEN
         RMACH = DIGITS(ZERO)
      ELSE IF( BUFFER6 ) THEN
         RMACH = RND
      ELSE IF( BUFFER7 ) THEN
         RMACH = MINEXPONENT(ZERO)
      ELSE IF( BUFFER8 ) THEN
         RMACH = tiny(zero)
      ELSE IF( BUFFER9 ) THEN
         RMACH = MAXEXPONENT(ZERO)
      ELSE IF( BUFFER10 ) THEN
         RMACH = HUGE(ZERO)
      ELSE
         RMACH = ZERO
      END IF
!
      DLAMCH = RMACH
      RETURN
!
!     End of DLAMCH
!
      END
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!> \brief \b DLAMC3
!> \details
!> \b Purpose:
!> \verbatim
!> DLAMC3  is intended to force  A  and  B  to be stored prior to doing
!> the addition of  A  and  B ,  for use in situations where optimizers
!> might hold one of these in a register.
!> \endverbatim
!> \author LAPACK is a software package provided by Univ. of Tennessee, Univ. of California Berkeley, Univ. of Colorado Denver and NAG Ltd..
!> \date December 2016
!> \ingroup auxOTHERauxiliary
!>
!> \param[in] A
!> \verbatim
!>          A is a DOUBLE PRECISION
!> \endverbatim
!>
!> \param[in] B
!> \verbatim
!>          B is a DOUBLE PRECISION
!>          The values A and B.
!> \endverbatim
!>
      DOUBLE PRECISION FUNCTION DLAMC3( A, B )
!
!  -- LAPACK auxiliary routine (version 3.7.0) --
!     Univ. of Tennessee, Univ. of California Berkeley and NAG Ltd..
!     November 2010
!
!     .. Scalar Arguments ..
      DOUBLE PRECISION   A, B
!     ..
! =====================================================================
!
!     .. Executable Statements ..
!
      DLAMC3 = A + B
!
      RETURN
!
!     End of DLAMC3
!
      END
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

      SUBROUTINE IDAMAX_RETURN(N,DX,INCX, IDAMAX)
!
!  -- Reference BLAS level1 routine (version 3.8.0) --
!  -- Reference BLAS is a software package provided by Univ. of Tennessee,    --
!  -- Univ. of California Berkeley, Univ. of Colorado Denver and NAG Ltd..--
!     November 2017
!
!     .. Scalar Arguments ..
      implicit none (type, external)
      INTEGER INCX,N
      INTEGER IDAMAX
!     ..
!     .. Array Arguments ..
      DOUBLE PRECISION DX(*)
!     ..
!
!  =====================================================================
!
!     .. Local Scalars ..
      DOUBLE PRECISION DMAX
      INTEGER I,IX
!     ..
!     .. Intrinsic Functions ..
      INTRINSIC DABS
!     ..
      IDAMAX = 0
      IF (N.LT.1 .OR. INCX.LE.0) RETURN
      IDAMAX = 1
      IF (N.EQ.1) RETURN
      IF (INCX.EQ.1) THEN
!
!        code for increment equal to 1
!
         DMAX = DABS(DX(1))
         DO I = 2,N
            IF (DABS(DX(I)).GT.DMAX) THEN
               IDAMAX = I
               DMAX = DABS(DX(I))
            END IF
         END DO
      ELSE
!
!        code for increment not equal to 1
!
         IX = 1
         DMAX = DABS(DX(1))
         IX = IX + INCX
         DO I = 2,N
            IF (DABS(DX(IX)).GT.DMAX) THEN
               IDAMAX = I
               DMAX = DABS(DX(IX))
            END IF
            IX = IX + INCX
         END DO
      END IF
      RETURN
      END


end module easychem_fortran_source