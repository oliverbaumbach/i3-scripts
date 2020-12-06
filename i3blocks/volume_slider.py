#!/usr/bin/env python3
"""
Interactive ALSA volume slider of i3blocks 
"""
import os
import sys
import re 
import subprocess
from utils import gradient_at, span

BLOCKS = [" ","▏","▎","▍","▌","▊","▉","█"] 
def bar(length, fraction):
    """
    Creates Unicode Bargraph (left to right)
    """
    return (BLOCKS[7] * int(length * fraction) +
            BLOCKS[int(length * 8 * fraction) % 8]).ljust(length)[:length]

if "relative_x" in os.environ:
    percentage = round(int(os.getenv("relative_x", 0)) / int(os.getenv("width", 1)) * 100)
    subprocess.run(["amixer", "sset", "Master", f"{int(percentage)}%", "-q"])
else:
    query = subprocess.check_output(["amixer", "sget", "Master"]).decode()
    percentage = int(re.search(r"\[(\d+)%\]", query).groups()[0])

length = 30
GRADIENT = [("#4b4b4b", 0.0),
            ("#dfdfdf", 0.8),
            ("#dfdfdf", 1.0)]

if __name__ == "__main__":
    _, length = sys.argv
    length = int(length)
    print("<span font='4'>", 
          *[span(cha, fg=gradient_at(GRADIENT, i/length))
            for i, cha in
            enumerate(bar(length, percentage / 100))],
          "</span>",
          sep="")
