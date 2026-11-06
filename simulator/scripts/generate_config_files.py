#!/usr/bin/python
import sys
import os
import errno

# Same as `mkdir -p` on *nix, mkdir that doesn't fail on existing directory
def mkdir_p(directory):
    try:
        os.makedirs(directory)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(directory):
            pass
        else:
            raise

if(len(sys.argv) < 2):
    print("Usage python generate_config_files.py command_file [stat_dir_prefix]")
    print("command_file: benckmark,applicationm,function,command")
    exit(1)

if not os.getcwd.endswith("simulator"):
    print(f"Do not run this script from {os.getcwd()}, run from [DAMOV repo root]/simulator")
    exit(1)

mkdir_p("../workloads")
os.chdir("../workloads")
PIM_ROOT = os.getcwd() +"/"
os.chdir("../simulator") 
ROOT = os.getcwd() +"/"




if(len(sys.argv) >= 3):
    stat_prefix = sys.argv[2]
else:
    stat_prefix = f"{ROOT}zsim_stats"

if(len(sys.argv) >= 4):
    config_prefix = sys.argv[3]
else:
    config_prefix = f"{ROOT}config_files"

if(len(sys.argv) == 5):
    slurm_prefix = sys.argv[4]
else:
    slurm_prefix = f"{ROOT}slurm"

with open(sys.argv[1], "r") as command_file:
    for line in command_file:
        line = line.split(",")
        benchmark = line[0]
        application = line[1]
        function = line[2]
        command = line[3]
        print(line)
        command = command.replace('\n','')

        ### Fixed LLC Size 
        number_of_cores = [1, 4, 16, 20, 32, 40, 64, 80, 112, 128, 256]
        versions = ["inorder", "ooo", "accelerator"]
        platforms = ["host_{0}/no_prefetch", "host_{0}/prefetch", "pim_{0}"]

        for platform in platforms:
            for version in versions:
                for cores in number_of_cores:
                    mkdir_p(f"{config_prefix}/{platform.format(version)}/{benchmark}/{cores}/")
                    mkdir_p(f"{slurm_prefix}/{platform.format(version)}/{benchmark}/{cores}/")
                    mkdir_p(f"{stat_prefix}/{platform.format(version)}/{cores}/")

                fname = f"{ROOT}/templates/"
                if platform == "host_{0}/no_prefetch":
                    fname += "template_host_{0}.cfg"
                elif platform == "host_{0}/prefetch":
                    fname += "template_host_prefetch_{0}.cfg"
                else:
                    fname += "template_pim_{0}.cfg"


                with open(f"{ROOT}/templates/template_slurm.slurm", "r") as s:
                    slurm_template = s.readlines()

                with open(fname.format(version), "r") as ins:
                    print(fname.format(version))
                    conf_template = ins.readlines()

                for cores in number_of_cores:
                    config_fname = f"{config_prefix}/{platform.format(version)}/{benchmark}/{cores}/{application}_{function}.cfg"
                    job_name = f"{benchmark}.{application}.{function}.{platform.format(version)}.{cores}"
                    job_name = job_name.replace("/", "_")
                    config_file = open(config_fname,"w")
                    for line in conf_template:
                        line = line.replace("NUMBER_CORES", str(cores))
                        line = line.replace("STATS_PATH", f"{stat_prefix}/{platform.format(version)}/{cores}/{benchmark}_{application}_{function}")
                        line = line.replace("COMMAND_STRING", f"\"{command}\";")
                        line = line.replace("THREADS", str(cores))
                        line = line.replace("PIM_ROOT", PIM_ROOT)

                        config_file.write(line)
                    config_file.close()
                    with open(f"{slurm_prefix}/{platform.format(version)}/{benchmark}/{cores}/{application}_{function}.slurm", "w") as sl:
                        for line in slurm_template:
                            line = line.replace("JOBNAME", job_name)
                            line = line.replace("FILENAME", config_fname)
                            line = line.replace("THREADS", str(cores) if cores < 64 else "64")
                            line = line.replace("ROOT", ROOT)
                            sl.write(line)


                    


