#!/usr/bin/env python3
"""
Alsa Master Volume for i3blocks 
"""
import re
import os 
import subprocess

if __name__ == "__main__": 
    if "relative_x" in os.environ:
        subprocess.run(["amixer", "sset", "Master", "toggle"],stdout=False) 
 
    if "[on]" in subprocess.check_output(["amixer","sget", "Master"]).decode():
        print("")
    else:
        print("")
