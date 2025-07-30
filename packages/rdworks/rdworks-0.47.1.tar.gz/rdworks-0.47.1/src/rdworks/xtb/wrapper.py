import os
import resource
import subprocess
import json
import tempfile
import logging
import shutil
import re

from pathlib import Path
from types import SimpleNamespace

from rdkit import Chem
from rdkit.Geometry import Point3D


logger = logging.getLogger()

# In ASE, the default energy unit is eV (electron volt).
# It will be converted to kcal/mol
# CODATA 2018 energy conversion factor
hartree2ev = 27.211386245988
hartree2kcalpermol = 627.50947337481
ev2kcalpermol = 23.060547830619026


class GFN2xTB:
    def __init__(self, molecule: Chem.Mol, ncores: int = 8):
        assert isinstance(molecule, Chem.Mol), "molecule is not rdkit.Chem.Mol type"
        assert molecule.GetConformer().Is3D(), "molecule is not a 3D conformer"
        assert self.is_xtb_ready(), "xtb is not accessible"

        self.rdmol = molecule
        self.natoms = molecule.GetNumAtoms()
        self.symbols = [ atom.GetSymbol() for atom in molecule.GetAtoms() ]
        self.positions = molecule.GetConformer().GetPositions().tolist()

        # Parallelisation
        os.environ['OMP_STACKSIZE'] = '4G'
        os.environ['OMP_NUM_THREADS'] = f'{ncores},1'
        os.environ['OMP_MAX_ACTIVE_LEVELS'] = '1'
        os.environ['MKL_NUM_THREADS'] = f'{ncores}'
        
        # unlimit the system stack
        resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))


    @staticmethod
    def is_xtb_ready() -> bool:
        """Check if xtb is available.

        Returns:
            bool: True if `xtb` is available, False otherwise.
        """
        return shutil.which('xtb') is not None


    @staticmethod
    def is_cpx_ready() -> bool:
        """Checks if the CPCM-X command-line tool, `cpx`, is accessible in the system.

        Returns:
            bool: True if the cpx is found, False otherwise.
        """
        return shutil.which('cpx') is not None
    

    @staticmethod
    def is_cpcmx_option_ready() -> bool:
        """Checks if xtb works with the `--cpcmx` option.

        xtb distributed by the conda does not include CPCM-X function (as of June 17, 2025). 
        xtb installed from the github source codes by using meson and ninja includes it.

        Returns:
            bool: True if the --cpcmx option is working, False otherwise.
        """
        if GFN2xTB.is_xtb_ready():
            cmd = ['xtb', '--cpcmx']
            proc = subprocess.run(cmd, capture_output=True, text=True)
            # we are expecting an error because no input file is given
            assert proc.returncode != 0
            for line in proc.stdout.split('\n'):
                line = line.strip()
                if 'CPCM-X library was not included' in line:
                    return False
        
        return True


    @staticmethod
    def is_ready() -> bool:
        """Check if `xtb` and `cpx` are accessible and `xtb --cpcmx` are available.

        Returns:
            bool: True if both `xtb` and `cpx` are accessible, False otherwise.
        """
        return all([GFN2xTB.is_xtb_ready(),
                    GFN2xTB.is_cpx_ready(),
                    GFN2xTB.is_cpcmx_option_ready()])
    

    @staticmethod
    def version() -> str | None:
        """Check xtb version.

        Returns:
            str | None: version statement.
        """
        if GFN2xTB.is_ready():
            cmd = ['xtb', '--version']
            proc = subprocess.run(cmd, capture_output=True, text=True)
            assert proc.returncode == 0, "GFN2xTB() Error: xtb not available"
            for line in proc.stdout.split('\n'):
                line = line.strip()
                if 'version' in line:
                    return line
            
        return None
    

    def to_xyz(self) -> str:
        """Export to XYZ formatted string.

        Returns:
            str: XYZ formatted string
        """
        lines = [f'{self.natoms}', ' ']
        for e, (x, y, z) in zip(self.symbols, self.positions):
            lines.append(f'{e:5} {x:23.14f} {y:23.14f} {z:23.14f}')
        
        return '\n'.join(lines)


    def to_turbomole_coord(self, bohr: bool = False) -> str:
        """Returns TURBOMOLE coord file formatted strings.

        Turbomole coord file format:

            - It starts with the keyword `$coord`.
            - Each line after the $coord line specifies an atom, consisting of:
                - Three real numbers representing the Cartesian coordinates (x, y, z).
                - A string for the element name.
                - Optional: an "f" label at the end to indicate that the atom's coordinates are frozen during optimization.
            - Coordinates can be given in Bohr (default), Ångström (`$coord angs`), or fractional coordinates (`$coord frac`).
            - Optional data groups like periodicity (`$periodic`), lattice parameters (`$lattice`), and cell parameters (`$cell`) can also be included. 
            - Regarding precision:
                The precision of the coordinates is crucial for accurate calculations, especially geometry optimizations.
                Tools like the TURBOMOLEOptimizer might check for differences in atomic positions with a tolerance of 1e-13. 

        Args:
            bohr (bool): whether to use Bohr units of the coordinates. Defaults to False.
                Otherwise, Angstrom units will be used.
        
        Returns:
            str: TURBOMOLE coord formatted file.
        """
        if bohr:
            lines = ["$coord"]
        else:
            lines = ["$coord angs"]

        for (x, y, z), e in zip(self.positions, self.symbols):
            lines.append(f"{x:20.15f} {y:20.15f} {z:20.15f} {e}")
        
        lines.append("$end")

        return '\n'.join(lines)


    def load_xyz(self, geometry_input_path: Path) -> Chem.Mol:
        """Load geometry.

        Args:
            geometry_input_path (Path): pathlib.Path to the xyz 

        Returns:
            Chem.Mol: rdkit Chem.Mol object.
        """
        rdmol_opt = Chem.Mol(self.rdmol)
        with open(geometry_input_path, 'r') as f:
            for lineno, line in enumerate(f):
                if lineno == 0:
                    assert int(line.strip()) == self.natoms
                    continue
                elif lineno == 1: # comment or title
                    continue
                (symbol, x, y, z) = line.strip().split()
                x, y, z = float(x), float(y), float(z)
                atom = rdmol_opt.GetAtomWithIdx(lineno-2)
                assert symbol == atom.GetSymbol()
                rdmol_opt.GetConformer().SetAtomPosition(atom.GetIdx(), Point3D(x, y, z))
        
        return rdmol_opt


    def load_wbo(self, wbo_path: Path) -> dict[tuple[int, int], float]:
        """Load Wiberg bond order.

        singlepoint() creates a wbo output file.

        Args:
            wbo_path (Path): path to the wbo file.

        Returns:
            dict(tuple[int, int], float): { (i, j) : wbo, ... } where i and j are atom indices for a bond.
        """

        with open(wbo_path, 'r') as f:
            # Wiberg bond order (WBO)
            Wiberg_bond_orders = {}
            for line in f:
                line = line.strip()
                if line:
                    # wbo output has 1-based indices
                    (i, j, wbo) = line.split()
                    # changes to 0-based indices
                    i = int(i) - 1
                    j = int(j) - 1
                    # wbo ouput indices are ascending order
                    ij = (i, j) if i < j else (j, i)
                    Wiberg_bond_orders[ij] = float(wbo)

            return Wiberg_bond_orders


    def cpx(self, verbose: bool = False) -> float | None:
        """Runs cpx and returns Gsolv (kcal/mol)

        Warning: 
            Solvation energy obtained from `xtb --cpcmx water` differs from
            `cpx --solvent water` (difference between gas.out and solv.out in terms of total energy).
            There are other correction terms not clearly defined in the output files.
            So, this method is not reliable and should be discarded

        Returns:
            float or None: Gsolv energy in kcal/mol or None.
        """
        with tempfile.TemporaryDirectory() as temp_dir: # tmpdir is a string
            workdir = Path(temp_dir)
            if verbose:
                logger.info(f'xtb.cpx workdir= {temp_dir}')
            
            geometry_input_path = workdir / 'coord'
            geometry_output_path = workdir / 'xtbtopo.mol'
            gas_out_path = workdir / 'gas.out'
            solv_out_path = workdir / 'solv.out'
            wbo_path = workdir / 'wbo'
         
            with open(geometry_input_path, 'w') as f:
                f.write(self.to_turbomole_coord())
        
            cmd = ['cpx']
            options = ['--solvent', 'water']
            
            proc = subprocess.run(cmd + options, cwd=temp_dir, capture_output=True, text=True)
            # cpx creates the following files:
            # charges  gas.energy    solute_sigma.txt   solvent_sigma.txt   xtbtopo.mol
            # coord    gas.out       solute_sigma3.txt  solvent_sigma3.txt
            # error    solute.cosmo  solv.out           wbo

            # example of solv.out
            #  :::::::::::::::::::::::::::::::::::::::::::::::::::::
            #  ::                     SUMMARY                     ::
            #  :::::::::::::::::::::::::::::::::::::::::::::::::::::
            #  :: total energy            -119.507131639760 Eh    ::
            #  :: w/o Gsasa/hb/shift      -119.494560363045 Eh    ::
            #  :: gradient norm              0.084154442395 Eh/a0 ::
            #  :: HOMO-LUMO gap              2.966157362876 eV    ::
            #  ::.................................................::
            #  :: SCC energy              -121.121278922798 Eh    ::
            #  :: -> isotropic ES            0.180705208303 Eh    ::
            #  :: -> anisotropic ES          0.003924951393 Eh    ::
            #  :: -> anisotropic XC          0.040710819025 Eh    ::
            #  :: -> dispersion             -0.088336282215 Eh    ::
            #  :: -> Gsolv                  -0.039236762590 Eh    ::
            #  ::    -> Gelec               -0.026665485874 Eh    ::
            #  ::    -> Gsasa               -0.012571276716 Eh    ::
            #  ::    -> Ghb                  0.000000000000 Eh    ::
            #  ::    -> Gshift               0.000000000000 Eh    ::
            #  :: repulsion energy           1.614147283037 Eh    ::
            #  :: add. restraining           0.000000000000 Eh    ::
            #  :: total charge              -0.000000000000 e     ::
            #  :::::::::::::::::::::::::::::::::::::::::::::::::::::

            # example gas.out
            # :::::::::::::::::::::::::::::::::::::::::::::::::::::
            #  ::                     SUMMARY                     ::
            #  :::::::::::::::::::::::::::::::::::::::::::::::::::::
            #  :: total energy            -119.473726280382 Eh    ::
            #  :: gradient norm              0.085445002241 Eh/a0 ::
            #  :: HOMO-LUMO gap              2.562893747102 eV    ::
            #  ::.................................................::
            #  :: SCC energy              -121.087873563419 Eh    ::
            #  :: -> isotropic ES            0.152557320965 Eh    ::
            #  :: -> anisotropic ES          0.007343156635 Eh    ::
            #  :: -> anisotropic XC          0.039625076440 Eh    ::
            #  :: -> dispersion             -0.088605122696 Eh    ::
            #  :: repulsion energy           1.614147283037 Eh    ::
            #  :: add. restraining           0.000000000000 Eh    ::
            #  :: total charge              -0.000000000000 e     ::
            #  :::::::::::::::::::::::::::::::::::::::::::::::::::::

            if proc.returncode == 0:
                total_energy_solv = None
                total_energy_gas = None
                
                with open(solv_out_path, 'r') as f:
                    for line in f:
                        if 'total energy' in line:
                            m = re.search(r"total energy\s+(?P<solv>[-+]?\d*\.?\d+)\s+Eh", line)
                            total_energy_solv = float(m.group('solv'))
                with open(gas_out_path, 'r') as f:
                    for line in f:
                        if 'total energy' in line:
                            m = re.search(r"total energy\s+(?P<gas>[-+]?\d*.?\d+)\s+Eh", line)
                            total_energy_gas = float(m.group('gas'))
                
                if total_energy_solv and total_energy_gas:
                    return (total_energy_solv - total_energy_gas) * hartree2kcalpermol
        
        return None


    def singlepoint(self, water: str | None = None, verbose: bool = False) -> SimpleNamespace:
        """Calculate single point energy.
        
        Total energy from xtb output in atomic units (Eh, hartree) is converted to kcal/mol.

        Args:
            water (str, optional) : water solvation model (choose 'gbsa' or 'alpb')
                alpb: ALPB solvation model (Analytical Linearized Poisson-Boltzmann).
                gbsa: generalized Born (GB) model with Surface Area contributions.

        Returns:
            SimpleNamespace(PE(total energy in kcal/mol), charges, wbo) 
        """

        with tempfile.TemporaryDirectory() as temp_dir: # tmpdir is a string
            workdir = Path(temp_dir)
            if verbose:
                logger.info(f'xtb.singlepoint workdir= {temp_dir}')
            
            geometry_input_path = workdir / 'geometry.xyz'
            xtbout_path = workdir / 'xtbout.json'
            stdout_path = workdir / 'fort.6'
            wbo_path = workdir / 'wbo'
            geometry_output_path = workdir / 'xtbtopo.mol'
            
            with open(geometry_input_path, 'w') as geometry:
                geometry.write(self.to_xyz())
            
            cmd = ['xtb', geometry_input_path.as_posix()]
            
            options = ['--gfn', '2', '--json']
            
            Gsolv = None
            
            if water is not None and isinstance(water, str):
                if water == 'gbsa':
                    options += ['--gbsa', 'H2O']
                    # it does not provide Gsolv contribution to the total energy
                elif water == 'alpb':
                    options += ['--alpb', 'water']
                    # it does not provide Gsolv contribution to the total energy
                elif water == 'cpcmx' and self.is_cpcmx_option_ready():
                    options += ['--cpcmx', 'water']

            # 'xtbout.json', 'xtbrestart', 'xtbtopo.mol', 'charges', and 'wbo' files will be 
            # created in the current working directory.
            proc = subprocess.run(cmd + options, cwd=temp_dir, capture_output=True, text=True)

            # if proc.returncode == 0:
            #     print("Standard Output:")
            #     print(proc.stdout)
            # else:
            #     print("Error:")
            #     print(proc.stderr)
            
            if proc.returncode == 0:
                if xtbout_path.is_file():
                    with open(xtbout_path, 'r') as f:
                        datadict = json.load(f) # takes the file object as input
                                 
                if (water is not None) and (Gsolv is None) and stdout_path.is_file():
                    #  Free Energy contributions:                       [Eh]        [kcal/mol]
                    # -------------------------------------------------------------------------
                    #  solvation free energy (dG_solv):             -0.92587E-03    -0.58099
                    #  gas phase energy (E)                         -0.52068E+01
                    # -------------------------------------------------------------------------
                    #  total free energy (dG)                       -0.52077E+01
                    with open(stdout_path, 'r') as f:
                        for line in f:
                            if 'solvation free energy' in line:
                                m = re.search(r"solvation free energy \(dG_solv\)\:\s+[-+]?\d*\.?\d+E[-+]?\d*\s+(?P<kcalpermol>[-+]?\d*\.?\d+)", line)
                                Gsolv = float(m.group('kcalpermol'))
                
                Wiberg_bond_orders = self.load_wbo(wbo_path)

                return SimpleNamespace(
                    PE = datadict['total energy'] * hartree2kcalpermol,
                    Gsolv = Gsolv, 
                    charges = datadict['partial charges'], 
                    wbo = Wiberg_bond_orders,
                    ) 
        
        # something went wrong if it reaches here          
        return SimpleNamespace()
                        


    def optimize(self, water: str | None = None, verbose: bool = False) -> SimpleNamespace:
        """Optimize geometry.

        Fortran runtime errror:
            At line 852 of file ../src/optimizer.f90 (unit = 6, file = 'stdout')
            Fortran runtime error: Missing comma between descriptors
            (1x,"("f7.2"%)")
                        ^
            Error termination.

        Args:
            water (str, optional) : water solvation model (choose 'gbsa' or 'alpb')
                alpb: ALPB solvation model (Analytical Linearized Poisson-Boltzmann).
                gbsa: generalized Born (GB) model with Surface Area contributions.

        Returns:
            (total energy in kcal/mol, optimized geometry)
        """
        with tempfile.TemporaryDirectory() as temp_dir: # tmpdir is a string
            workdir = Path(temp_dir)
            if verbose:
                logger.info(f'xtb.optimize workdir= {temp_dir}')
            
            geometry_input_path = workdir / 'geometry.xyz'
            xtbout_path = workdir / 'xtbout.json'
            geometry_output_path = workdir / 'xtbopt.xyz'
            wbo_path = workdir / 'wbo'
            
            with open(geometry_input_path, 'w') as geometry:
                geometry.write(self.to_xyz())

            cmd = ['xtb', geometry_input_path.as_posix()]

            options = ['--opt', '--gfn', '2', '--json']

            if water is not None and isinstance(water, str):
                if water == 'gbsa':
                    options += ['--gbsa', 'H2O']
                elif water == 'alpb':
                    options += ['--alpb', 'water']
                elif water == 'cpcmx':
                    logger.warning('optimize with --cpcmx option is not implemented in xtb yet')

            proc = subprocess.run(cmd + options, cwd=temp_dir, capture_output=True, text=True)

            if proc.returncode == 0 and xtbout_path.is_file():
                with open(xtbout_path, 'r') as f:
                    datadict = json.load(f) # takes the file object as input
                
                Wiberg_bond_orders = self.load_wbo(wbo_path)
                rdmol_opt = self.load_xyz(geometry_output_path)
            
                return SimpleNamespace(
                        PE = datadict['total energy'] * hartree2kcalpermol,
                        charges = datadict['partial charges'],
                        wbo = Wiberg_bond_orders,
                        geometry = rdmol_opt,
                )

        # something went wrong if it reaches here
        return SimpleNamespace()
    

    def esp(self, water: str | None = None, verbose: bool = False) -> None:
        """Calculate electrostatic potential
        
        Example:
            v = py3Dmol.view()
            v.addVolumetricData(dt,
                                "cube.gz", {
                                    'isoval': 0.005,
                                    'smoothness': 2,
                                    'opacity':.9,
                                    'voldata': esp,
                                    'volformat': 'cube.gz',
                                    'volscheme': {
                                        'gradient':'rwb',
                                        'min':-.1,
                                        'max':.1,
                                        }
                                    });
            v.addModel(dt,'cube')
            v.setStyle({'stick':{}})
            v.zoomTo()
            v.show()
        """
        with tempfile.TemporaryDirectory() as temp_dir: # tmpdir is a string
            workdir = Path(temp_dir)
            if verbose:
                logger.info(f'xtb.optimize workdir= {temp_dir}')
            
            geometry_input_path = workdir / 'geometry.xyz'
            xtb_esp_dat = workdir / 'xtb_esp_dat'

            with open(geometry_input_path, 'w') as geometry:
                geometry.write(self.to_xyz())

            cmd = ['xtb', geometry_input_path.as_posix()]

            options = ['--esp', '--gfn', '2']

            if water is not None and isinstance(water, str):
                if water == 'gbsa':
                    options += ['--gbsa', 'H2O']
                elif water == 'alpb':
                    options += ['--alpb', 'water']

            proc = subprocess.run(cmd + options, cwd=temp_dir, capture_output=True, text=True)
            # output files: xtb_esp.cosmo, xtb_esp.dat, xtb_esp_profile.dat

            if proc.returncode == 0 and xtb_esp_dat.is_file():
                with open(xtb_esp_dat, 'r') as f:
                    pass
        
        return None