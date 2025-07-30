import os


def hpc_setup_form():
    """
    Initial setup the HPC cluster information via a form
    """
    from amaceing_toolkit.workflow import ask_for_int
    from amaceing_toolkit.workflow import ask_for_yes_no

    path_to_program = {}
    path_to_source_file = {}
    default_cluster = ask_for_yes_no('Are you using the HPC cluster of TU Ilmenau, MLU Halle-Wittenberg? (y/n)', 'n')
    if default_cluster == 'y':
        which_cluster = ask_for_int('Which cluster are you using? (1: Ilmenau, 2: MLU Halle-Wittenberg)', 1)
        if which_cluster == '1':
            cluster = 'BatchXL'
            path_to_program['cp2k'] = '/home/joha4087/programs/cp2k_easy/cp2k-2025.1/exe/local/cp2k.popt' 
            path_to_source_file['cp2k'] = '/home/joha4087/programs/cp2k_easy/source_cp2k_gcc_openmpi_by_jonas'
            path_to_program['mace'] = 'conda activate atk'                                                      # to do add the conda env name
            path_to_source_file['mace'] = input('Enter the path to the source file of your conda: [/home/..USER../anaconda3/etc/profile.d/conda.sh]')
            path_to_program['mattersim'] = 'conda activate atk_ms7n'                                            # to do add the conda env name
            path_to_source_file['mattersim'] = path_to_source_file['mace']
            workload_manager = 'lsf'
        elif which_cluster == '2':
            cluster = 'batch6'
            path_to_program['cp2k'] = '/home/haens/programs/cp2k_2025/cp2k-2025.1/exe/local/cp2k.popt'
            path_to_source_file['cp2k'] = 'source /home/haens/programs/cp2k_2025/source_cp2k_jonas'
            workload_manager = 'slurm'
        # Other hpc settings can be added here
    else:
        cluster = input('Enter the name of the HPC cluster partition: ')
        workload_manager = input('Enter the workload manager of the HPC cluster [lsf/slurm]: ')
        setup_program = ask_for_yes_no('Do you want to setup the program path of cp2k? (y/n)', 'y')
        if setup_program == 'y':
            path_to_program['cp2k'] = input('Enter the path to the program: [/path/to/cp2k.popt]')
            path_to_source_file['cp2k'] = input('Enter the path to the source file: [/path/to/source-file]')
        setup_program = ask_for_yes_no('Do you want to setup the program path of your conda env for mace-torch? (y/n)', 'y')
        if setup_program == 'y':
            path_to_program['mace'] = input('Enter the name of your conda env: [atk]')
            path_to_program['mace'] = f'conda activate {path_to_program["mace"]}'
            path_to_source_file['mace'] = input('Enter the path to the source file of your conda: [/home/..USER../anaconda3/etc/profile.d/conda.sh]')
        setup_program = ask_for_yes_no('Do you want to setup the program path of your conda env for MatterSim and SevenNet? (y/n)', 'y')
        if setup_program == 'y':
            path_to_program['mattersim'] = input('Enter the name of your conda env: [atk_ms7n]')
            path_to_program['mattersim'] = f'conda activate {path_to_program["mattersim"]}'
            path_to_source_file['mattersim'] = path_to_source_file['mace']
        


    # Get the path of the current script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Define the path for hpc_setup.txt in the same directory as the script
    hpc_setup_file = os.path.join(script_directory, 'hpc_setup.txt')

    with open(hpc_setup_file, 'w') as f:
        f.write(f"cluster:: {cluster}\n")
        f.write(f"workload_manager:: {workload_manager}\n")
        f.write(f"path_to_program:: {path_to_program}\n")
        f.write(f"path_to_source_file:: {path_to_source_file}\n")
        
    print(f"HPC cluster information has been saved to {hpc_setup_file}.")

def lammps_rs_form():
    """
    Initial setup the LAMMPS runscripts via a form
    """
    # Preset for TU Ilmenau HPC cluster
    from amaceing_toolkit.workflow import ask_for_yes_no
    tui = ask_for_yes_no('Are you using the HPC cluster of TU Ilmenau? (y/n)', 'n')
    if tui == 'y':
        lmp_rs_template_cpu = r"""#!/bin/sh
#BSUB -J maceL_$$PROJECT_NAME$$
#BSUB -o %J.out
#BSUB -e %J.err
#BSUB -W 120:00
#BSUB -q BatchXL
#BSUB -n 16
#BSUB -R "span[hosts=1]"

INFILE=$$INPUT_FILE$$
OUTFILE=local-${INFILE}.out

source /home/joha4087/programs/cp2k_easy/source_cp2k_gcc_openmpi_by_jonas
module load intel/oneapi/mkl

# DEFINE THE NUMBER OF CORES
export OMP_NUM_THREADS=16

# CPU LAMMPS
/home/chdr3860/programs/lammps_mace_cpu/lammps/build/lmp -in $INFILE > $OUTFILE
"""
        lmp_rs_template_gpu = r"""#!/bin/sh

INFILE=$$INPUT_FILE$$
OUTFILE=local-${INFILE}.out

source /home/joha4087/programs/cp2k_easy/source_cp2k_gcc_openmpi_by_jonas
module load intel/oneapi/mkl
module load cuda/v12.2

# GPU LAMMPS with KOKKOS
/scratch/joha4087/programs/lammps/lammps_mace_gpunodes/lammps/build-batchgpu/lmp -k on g 1 -sf kk -in $INFILE > $OUTFILE
"""

        # Write the LAMMPS runscripts template to a file
        script_directory = os.path.dirname(os.path.abspath(__file__))
        lmp_rs_template = os.path.join(script_directory, 'lmp_rs_template_cpu.txt')
        with open(lmp_rs_template, 'w') as f:
            f.write(lmp_rs_template_cpu)
        lmp_rs_template = os.path.join(script_directory, 'lmp_rs_template_gpu.txt')
        with open(lmp_rs_template, 'w') as f:
            f.write(lmp_rs_template_gpu)
        print(f"LAMMPS Runscript Template has been saved to lmp_rs_template_cpu.txt and lmp_rs_template_gpu.txt in {script_directory}.")
        return None

    workload_manager = checking_hpc_setup('cp2k')[1]
    if workload_manager == 'lsf':
        wl_setup = """#!/bin/sh
#BSUB -J maceL_$$PROJECT_NAME$$
#BSUB -o %J.out
#BSUB -e %J.err
#BSUB -W 120:00
#BSUB -q $$PARTITION$$
#BSUB -n $$CORES$$
#BSUB -R "span[hosts=1]""" # LSF config
    elif workload_manager == 'slurm':
        wl_setup = """#!/bin/bash
#
#SBATCH --job-name maceL_$$PROJECT_NAME$$
#SBATCH --output output.log
#SBATCH --nodes 1
#SBATCH --ntasks-per-node $$CORES$$
#SBATCH --time 120:00:00
#SBATCH --partition=$$PARTITION$$""" # SLURM config
    else:
        raise ValueError("Unsupported workload manager. Please use 'lsf' or 'slurm'.")

    print("Please use the instructions on the MACE readthedocs to install a LAMMPS version compatible with MACE models.")
    
    # Ask for source/module commands
    source_path = input("Enter the file path to source an environment for LAMMPS/GCC/OpenMPI (e.g. '/home/user/programs/lammps/source_lammps_gcc_openmpi.sh'): ")
    cuda_command = input("Enter the command to source an environment for CUDA or load the corresponding module (e.g. 'source /home/user/programs/cuda/source_cuda.sh' or module load cuda): ")
    imkl_command = input("Enter the command to source an environment for Intel MKL or load the corresponding module (e.g. 'source /home/user/programs/intel_mkl/source_intel_mkl.sh' or module load intel/mkl): ")

    # Ask for the path to the LAMMPS executable
    lmp_path_cpu = input("Enter the path to the LAMMPS executable for CPU (e.g. '/home/user/programs/lammps/lmp'): ")
    lmp_path_gpu = input("Enter the path to the LAMMPS executable for GPU (e.g. '/home/user/programs/lammps/lmp'): ")

    # Construct the LAMMPS runscript template
    lmp_rs_template_cpu = wl_setup + r"""
INFILE=$$INPUT_FILE$$ 
OUTFILE=local-${INFILE}.out """+f"""
source {source_path}
{imkl_command}

export OMP_NUM_THREADS=$$CORES$$

{lmp_path_cpu} -in $INFILE > $OUTFILE """
    lmp_rs_template_gpu = wl_setup + r"""
INFILE=$$INPUT_FILE$$ 
OUTFILE=local-${INFILE}.out """+f"""
source {source_path}
{imkl_command}
{cuda_command}

{lmp_path_gpu} -k on g 1 -sf kk -in $INFILE > $OUTFILE """

    # Write the LAMMPS runscripts template to a file
    script_directory = os.path.dirname(os.path.abspath(__file__))
    lmp_rs_template = os.path.join(script_directory, 'lmp_rs_template_cpu.txt')
    with open(lmp_rs_template, 'w') as f:
        f.write(lmp_rs_template_cpu)
    lmp_rs_template = os.path.join(script_directory, 'lmp_rs_template_gpu.txt')
    with open(lmp_rs_template, 'w') as f:
        f.write(lmp_rs_template_gpu)

    print(f"LAMMPS Runscript Template has been saved to {lmp_rs_template_cpu} and {lmp_rs_template_gpu} in {script_directory}.")
    return None

def checking_hpc_setup(program):
    """
    Check if the HPC cluster information has been set up
    """
    from amaceing_toolkit.workflow import string_to_dict

    try:
        # Get the path of the current script
        script_directory = os.path.dirname(os.path.abspath(__file__))
        
        # Define the path for hpc_setup.txt in the same directory as the script
        hpc_setup_file = os.path.join(script_directory, 'hpc_setup.txt')

        if not os.path.isfile(hpc_setup_file):
            raise FileNotFoundError
    
    except FileNotFoundError:
        print("HPC cluster information has not been set up yet.")
        hpc_setup_form()
    
    # Open the hpc_setup.txt file in the same directory as the script
    with open(hpc_setup_file, 'r') as f:
        lines = f.readlines()
        cluster = lines[0].split(':: ')[1].strip()
        workload_manager = lines[1].split(':: ')[1].strip()
        path_to_program = string_to_dict(lines[2].split(':: ')[1])
        path_to_source_file = lines[3].split(':: ')[1]
        path_to_source_file = string_to_dict(path_to_source_file)


    return cluster, workload_manager, path_to_program[program], path_to_source_file[program]

def lammps_runscript():
    """
    Generate the runscript for LAMMPS
    """
    try: 
        # Get the path of the current script
        script_directory = os.path.dirname(os.path.abspath(__file__))
        
        # Define the path for hpc_setup.txt in the same directory as the script
        lmp_rs_template = os.path.join(script_directory, 'lmp_rs_template_cpu.txt')
        if not os.path.isfile(lmp_rs_template):
            raise FileNotFoundError
    
    except FileNotFoundError:
        print("LAMMPS Runscript Template has not been set up yet.")
        lammps_rs_form()

    # Load the LAMMPS runscripts template content and return it
    with open(lmp_rs_template, 'r') as f:
        lmp_rs_cpu_template = f.read()
    lmp_rs_template = os.path.join(script_directory, 'lmp_rs_template_gpu.txt')
    with open(lmp_rs_template, 'r') as f:
        lmp_rs_gpu_template = f.read()
    return lmp_rs_cpu_template, lmp_rs_gpu_template

def resource_setup_cp2k(level):
    """
    Set the resources for the HPC cluster
    """
    resources = {'intermediate': [32, 96], 'heavy' : [64, 240], 'light' : [16, 48]}
    return resources[level]


def cp2k_runscript(project_name, input_file_name):
    """
    Generate the runscript for CP2K
    """

    # Load the HPC cluster information and set resources
    cluster, workload_manager, path_to_program, path_to_source_file = checking_hpc_setup('cp2k')
    resources = resource_setup_cp2k('intermediate')

    if workload_manager == 'lsf':
        return f"""#!/bin/sh
#BSUB -J {project_name}
#BSUB -o %J.out
#BSUB -e %J.err
#BSUB -W {resources[1]}:00
#BSUB -q {cluster}
#BSUB -n {resources[0]}
#BSUB -R "span[hosts=1]"
export OMP_NUM_THREADS=1
""" + r"""
if [ ! -f ./seq ];  then echo "01" > seq ; fi
export seq=`cat seq`
awk 'BEGIN{printf "%2.2d\n",ENVIRON["seq"]+1}' > seq
""" + f"""
# Check if {project_name}-1.restart exists:
if [ -f {project_name}-1.restart ]; then
    INFILE={project_name}-1.restart
else 
    INFILE={input_file_name}
fi

""" + """
OUTFILE=local-${INFILE}.${seq}.out
""" + f"""
source {path_to_source_file}
mpirun -np {resources[0]} {path_to_program} $INFILE > $OUTFILE
""", "Start the calculation with 'bsub < runscript.sh'"
    
    elif workload_manager == 'slurm':
        return f"""#!/bin/bash
#
#SBATCH --job-name {project_name}
#SBATCH --output output.log
#SBATCH --nodes 1
#SBATCH --ntasks-per-node {resources[0]}
#SBATCH --time {resources[1]}:00:00
#SBATCH --partition={cluster}
export OMP_NUM_THREADS=1
""" + r"""
if [ ! -f ./seq ];  then echo "01" > seq ; fi
export seq=`cat seq`
awk 'BEGIN{printf "%2.2d\n",ENVIRON["seq"]+1}' > seq
""" + f"""
# Check if {project_name}-1.restart exists:
if [ -f {project_name}-1.restart ]; then
    INFILE={project_name}-1.restart
else 
    INFILE={input_file_name}
fi
""" + """
OUTFILE=local-${INFILE}.${seq}.out
""" + f"""
source {path_to_source_file}
mpirun -bind-to none {path_to_program} $INFILE > $OUTFILE
""", "Start the calculation with 'sbatch runscript.sh'"


def local_run_cp2k():
    """
    Return the command to run CP2K locally:  source command and run command
    """
    # Load the HPC cluster information and set resources
    cluster, workload_manager, path_to_program, path_to_source_file = checking_hpc_setup('cp2k')

    return f"""source {path_to_source_file}""", f""" mpirun -np 4 {path_to_program}"""


def resource_setup_pyML(level):
    """
    Set the resources for the HPC cluster
    """
    resources = {'intermediate': [8, 96], 'light' : [4, 96], 'gpu' : [1]}
    return resources[level]

def mace_runscript(project_name, input_file_name, run_type):
    """
    Generate the runscript for MACE: gpu and cpu
    """

    # Load the HPC cluster information and set resources
    cluster, workload_manager, path_to_program, path_to_source_file = checking_hpc_setup('mace')
    resources_cpu = resource_setup_pyML('intermediate')
    resources_gpu = resource_setup_pyML('gpu')

    if workload_manager == 'lsf':
        return f"""#!/bin/sh
# GPU runscript

source {path_to_source_file}
{path_to_program}

python {input_file_name} > {project_name}.out
""", f"Start the calculation with 'batch.{resources_gpu[0]}gpu gpu_script.job'", f"""#!/bin/sh
# CPU runscript

#BSUB -J {project_name}
#BSUB -o %J.out
#BSUB -e %J.err
#BSUB -W {resources_cpu[1]}:00
#BSUB -q {cluster}
#BSUB -n {resources_cpu[0]}
#BSUB -R "span[hosts=1]"

source {path_to_source_file}
{path_to_program}

python {input_file_name} > {project_name}.out
""", "Start the calculation with 'bsub < runscript.sh'"
    
    elif workload_manager == 'slurm':           # WIP please check the slurm script for your hpc
        return f"""#!/bin/bash
# GPU runscript

#SBATCH --job-name {project_name}
#SBATCH --output output.log
#SBATCH --nodes 1
#SBATCH --ntasks-per-node {resources_gpu[0]}
#SBATCH --time 24:00:00
#SBATCH --partition={cluster}

source {path_to_source_file}
{path_to_program}

python {input_file_name} > {project_name}.out
source {path_to_source_file}
""", f"Start the calculation with 'sbatch runscript.sh'", f"""#!/bin/bash
# CPU runscript

#SBATCH --job-name {project_name}
#SBATCH --output output.log
#SBATCH --nodes 1
#SBATCH --ntasks-per-node {resources_cpu[0]}
#SBATCH --time {resources_cpu[1]}:00:00
#SBATCH --partition={cluster}   

source {path_to_source_file}
{path_to_program}

python {input_file_name} > {project_name}.out
""", "Start the calculation with 'sbatch runscript.sh'"
    
def mattersim_runscript(project_name, input_file_name, run_type, finetune_config=""):
    """
    Generate the runscript for MatterSim: gpu and cpu
    """

    # Load the HPC cluster information and set resources
    cluster, workload_manager, path_to_program, path_to_source_file = checking_hpc_setup('mattersim')
    resources_cpu = resource_setup_pyML('intermediate') 
    resources_gpu = resource_setup_pyML('gpu')

    conda_sitepackage_dir = path_to_source_file.split("/etc/profile.d/conda.sh")[0]
    conda_sitepackage_dir = conda_sitepackage_dir + "/envs/atk_ms7n/lib/python3.9/site-packages/mattersim"

    if run_type == 'FINETUNE':
        if workload_manager == 'lsf':
            return f"""#!/bin/bash
# GPU runscript
source {path_to_source_file}
{path_to_program}

torchrun --nproc_per_node={resources_gpu[0]} {conda_sitepackage_dir}/training/finetune_mattersim.py {finetune_config} > {project_name}.out

""", f"Start the calculation with 'batch.{resources_gpu[0]}gpu gpu_script.job'", f"""#!/bin/sh
# CPU runscript

#BSUB -J {project_name}
#BSUB -o %J.out
#BSUB -e %J.err
#BSUB -W {resources_cpu[1]}:00
#BSUB -q {cluster}
#BSUB -n {resources_cpu[0]}
#BSUB -R "span[hosts=1]"

source {path_to_source_file}
{path_to_program}

torchrun --nproc_per_node={resources_cpu[0]} {conda_sitepackage_dir}/training/finetune_mattersim.py {finetune_config} > {project_name}.out
""", "Start the calculation with 'bsub < runscript.sh'"
    
        elif workload_manager == 'slurm':           # WIP please check the slurm script for your hpc
            return f"""#!/bin/bash
# GPU runscript

#SBATCH --job-name {project_name}
#SBATCH --output output.log
#SBATCH --nodes 1
#SBATCH --ntasks-per-node {resources_gpu}
#SBATCH --time 24:00:00
#SBATCH --partition={cluster}

source {path_to_source_file}
{path_to_program}

torchrun --nproc_per_node={resources_gpu[0]} {conda_sitepackage_dir}/training/finetune_mattersim.py {finetune_config} > {project_name}.out
source {path_to_source_file}
""", f"Start the calculation with 'sbatch runscript.sh'", f"""#!/bin/bash
# CPU runscript

#SBATCH --job-name {project_name}
#SBATCH --output output.log
#SBATCH --nodes 1
#SBATCH --ntasks-per-node {resources_cpu[0]}
#SBATCH --time {resources_cpu[1]}:00:00
#SBATCH --partition={cluster}   

source {path_to_source_file}
{path_to_program}

torchrun --nproc_per_node={resources_cpu[0]} {conda_sitepackage_dir}/training/finetune_mattersim.py {finetune_config} > {project_name}.out
""", "Start the calculation with 'sbatch runscript.sh'"
        
    
    else:
        if workload_manager == 'lsf':
            return f"""#!/bin/sh
# GPU runscript

source {path_to_source_file}
{path_to_program}

python {input_file_name} > {project_name}.out
""", f"Start the calculation with 'batch.{resources_gpu[0]}gpu gpu_script.job'", f"""#!/bin/sh
# CPU runscript

#BSUB -J {project_name}
#BSUB -o %J.out
#BSUB -e %J.err
#BSUB -W {resources_cpu[1]}:00
#BSUB -q {cluster}
#BSUB -n {resources_cpu[0]}
#BSUB -R "span[hosts=1]"

source {path_to_source_file}
{path_to_program}

python {input_file_name} > {project_name}.out
""", "Start the calculation with 'bsub < runscript.sh'"
    
        elif workload_manager == 'slurm':           # WIP please check the slurm script for your hpc
            return f"""#!/bin/bash
# GPU runscript

#SBATCH --job-name {project_name}
#SBATCH --output output.log
#SBATCH --nodes 1
#SBATCH --ntasks-per-node {resources_gpu[0]}
#SBATCH --time 24:00:00
#SBATCH --partition={cluster}

source {path_to_source_file}
{path_to_program}

python {input_file_name} > {project_name}.out
source {path_to_source_file}
""", f"Start the calculation with 'sbatch runscript.sh'", f"""#!/bin/bash
# CPU runscript

#SBATCH --job-name {project_name}
#SBATCH --output output.log
#SBATCH --nodes 1
#SBATCH --ntasks-per-node {resources_cpu[0]}
#SBATCH --time {resources_cpu[1]}:00:00
#SBATCH --partition={cluster}   

source {path_to_source_file}
{path_to_program}

python {input_file_name} > {project_name}.out
""", "Start the calculation with 'sbatch runscript.sh'"


# to do add a runscript directory where templates of other hpc clusters can be added these should be loaded in the runscript function

# Question functions
def ask_for_int(question, default):
    """
    Ask user for an integer value
    """
    value = ' '
    value = input(question + " [" + str(default) + "]: ")
    if value == '':
        value = str(default)
    while not value.isnumeric():
        value = input(question + " [" + str(default) + "]: ")
        if value == '':
            value = str(default)
        elif value.isnumeric() == False:
            print("Invalid input. Please enter an integer.")
    return value

def ask_for_yes_no(question, default):
    """
    Ask user for a yes or no answer
    """
    value = ' '
    while value != 'y' and value != 'n':
        value = input(question + " [" + default + "]: ")
        if value == '':
            value = default
        elif value != 'y' and value != 'n':
            print("Invalid input. Please enter 'y' or 'n'.")
    return value