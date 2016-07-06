
"""
Check the simulations finished successfully and restart ones that didn't.

"""
from __future__ import print_function
import os
import sys


slurmdir = os.getcwd()

# read the list of jobs
with open("_pan_array.in") as fh:
    lines = fh.readlines()

# loop over and check they worked
failed = []
for line in lines:
    # job details
    array = line.split()
    jobdir = array[0]
    mesh = array[3]
    model = array[2]
    csdir = array[4]
    jobargs = " ".join(array[1:])

    # switch to job directory and check it worked
    os.chdir(jobdir)
    try:
        if not os.path.exists("cR.bin"):
            # job failed
            print("Job failed in: {0}".format(jobdir))

            # copy mesh and parameter files
            os.system("cp -f " + csdir + "/meshes/" + mesh + ".msh cs.msh")
            os.system("cp -f " + csdir + "/parameters/" + model + ".dat cs.dat")

            # resubmit
            print("  Running: sbatch {0} {1}".format(os.path.join(slurmdir, "_run_sim_single.sl"), jobargs))
            os.system("sbatch {0} {1}".format(os.path.join(slurmdir, "_run_sim_single.sl"), jobargs))

            failed.append(jobdir)

    finally:
        os.chdir(slurmdir)

# output
print("{0} jobs failed".format(len(failed)))
