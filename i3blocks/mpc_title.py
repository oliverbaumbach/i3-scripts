#!/usr/bin/env python3
"""
Persistent mpc song title scroller for i3blocks 
"""
import subprocess
import time
from pathlib import Path 
import sys
import html 

def scroll_song(length, speed=0.4):
    """
    Query mpc for current song title, and marquee scroll through it 
    """
    # Get initial title from mpc 
    mpc = subprocess.check_output(["mpc", "current"]) 
    title = Path(mpc.decode()).stem + " "

    # mpc call constructor 
    query = lambda: subprocess.Popen(["mpc", "current", "--wait"],
                                     stdout=subprocess.PIPE)
    i = 0 
    mpc = query()
    color = '' 
    while True:
        # check if mpc call has exited, set title if yes
        while "[paused]" in subprocess.check_output(["mpc"]).decode():
            time.sleep(1)

        if mpc.poll() == 0:
            title = Path(mpc.stdout.read().decode()).stem + " "
            mpc = query()
            i = 0
            color = "#FFFFFF" 

        if not title:
            time.sleep(1)
            continue
        
        # title fits 
        if length >= len(title):
            print(" <span font='8'>", 
                  html.escape(title.center(length)),
                  "</span>", sep="")
            sys.stdout.flush()
            mpc.wait()
        # segment within bounds 
        elif i + length <= len(title):
            print(" <span font='8'>",
                  html.escape(title[i:i+length]),
                  "</span>", sep="")
            sys.stdout.flush()
        # wrap around edges  
        else:
            print(" <span font='8'>",
                  html.escape(title[i:]),
                  html.escape(title[0: (i+length) % len(title)]),
                  "</span>", sep="")
            sys.stdout.flush()
        color = ''
        i = (i + 1) % len(title)
        time.sleep(speed)

if __name__ == "__main__":
    _, length = sys.argv 
    scroll_song(int(length))
