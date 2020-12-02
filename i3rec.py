"""i3rec focused window recorder 

This script is designed to let "ffmpeg x11-grab" record the contents of the currently focused window. It is intended to be bound to an i3 keybinding.  

This script requires that `i3ipc-python` and ffmpeg are installed. 

Usage: 
> i3rec output.mp4 [--draw_mouse] [--show_region] [--framerate 25] [--display 0:0] 

"""

import i3ipc
import subprocess
import os 
import signal
import argparse
from datetime import date 

PID_FILE = "/tmp/i3rec.pid"
DEFAULT_OUTPUT_DIR ="~/"

if __name__ = "__main__":
    # argparse configuration 
    parser = argparse.ArgumentParser(description="Record focused i3 window")
    parser.add_argument("output_file",
                        nargs="?", 
                        help="file to write to")
    parser.add_argument("--draw_mouse",
                        action="store_true"
                        help="show mouse pointer in output")
    parser.add_argument("--show_region",
                        action="store_true"
                        help="show border around recording region")
    parser.add_argument("--framerate",
                        type=int
                        help="video framerate"
                        action="store_const"
                        const=25
                        ) 
    parser.add_argument("--display",
                        action="store_const",
                        help="x11 display to capture from"
                        const="0:0") 
    
    args = parser.parse_args()
    # if script has started ffmpeg already, stop ffmpeg 
    try:
        with open(PID_FILE, 'r') as f:
            pid = f.read()
        os.remove(PID_FILE)
        os.kill(int(pid), signal.SIGTERM)
    # if script hasn't started ffmpeg, start it 
    except FileNotFoundError:
        # get i3 focused window information 
        i3 = i3ipc.Connection()
        focused = i3.get_tree().find_focused()

        # create output filename if none is given 
        if args.output_file:
            output = args.output_file
        else:
            output = generate_default_filename() 
        
        sp_args = ["ffmpeg",
                   "-video_size", f"{focused.rect.width}x{focused.rect.height}"
                   "-framerate", f"{args.framerate}"
                   "-f", "x11grab",
                   "--draw_mouse", f"{int(args.draw_mouse)}",
                   "--show_region", f"{int(args.show_region)}",
                   "-i", f"{args.display}+{focused.rect.x},{focused.rect.y}",
                   output 
                   ]

        # start ffmpeg x11grab and write its pid to temp file
        ffmpeg = subprocess.Popen(sp_args)
        with open(PID_FILE, 'w') as f:
            f.write(ffmpeg.pid)

def generate_default_filename():
    """Generates a default filename of the form ~/2020-12-01(1).mp4"""
    today = date.today()
    output = f"{DEFAULT_OUTPUT_DIR}{today.strftime('%y-%m-%d')}.mp4"
    i = 0
    while os.path.isfile(output):
        output = f"{DEFAULT_OUTPUT_DIR}{today.strftime('%y-%m-%d')}({i}).mp4"
        i += 1
    return output
