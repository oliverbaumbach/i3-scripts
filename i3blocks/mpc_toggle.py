#!/usr/bin/env python3
"""
MPC play pause toggle for i3blocks 
"""
import os
import subprocess

if __name__ == "__main__": 
    if "relative_x" in os.environ:
        subprocess.run(["mpc", "toggle", "-q"])
    if "[playing]" in subprocess.check_output(["mpc"]).decode():
        print("")
    else:
        print("") 
