#!/home/user/scripts/i3/i3env/bin/python 
"""i3rec focused window recorder 

This script is designed to let "ffmpeg x11-grab" record the contents of the currently focused window. It is intended to be bound to an i3 keybinding.  

This script requires that `i3ipc-python` and ffmpeg are installed. 

Usage: 
> i3rec output.mp4 [--draw_mouse] [--show_region] [--framerate 25] [--display 0.0] 

"""
import i3ipc
import subprocess
import os 
import signal
import argparse
from datetime import date 

PID_FILE = "/tmp/i3rec.pid"
DEFAULT_OUTPUT_DIR ="/home/user/scratch/"

def generate_default_filename(directory):
    """Generates a default filename of the form ~/2020_12_01_1.mp4"""
    today = date.today()
    output = f"{today.strftime('%Y_%m_%d')}.mp4"
    i = 0
    while os.path.isfile(os.path.join(directory,output)):
        output = f"{today.strftime('%Y_%m_%d')}_{i}.mp4"
        i += 1
    return output


if __name__ == "__main__":
    # argparse configuration 
    parser = argparse.ArgumentParser(description="Record focused i3 window")
    parser.add_argument("output_file",
                        nargs="?", 
                        help="file to write to")
    parser.add_argument("--draw_mouse",
                        action="store_true",
                        help="show mouse pointer in output")
    parser.add_argument("--show_region",
                        action="store_true",
                        help="show border around recording region")
    parser.add_argument("--framerate",
                        help="video framerate",
                        nargs="?",
                        default=25
                        ) 
    parser.add_argument("--display",
                        nargs="?",
                        help="x11 display to capture from",
                        default="0.0") 
    
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
        base, fn = os.path.split(args.output_file or "")
        if base and fn:
            output = args.output_file
        elif base:
            output = os.path.join(base, generate_default_filename(base))
        elif fn:
            output = os.path.join(DEFAULT_OUTPUT_DIR, fn)
        else:
            output = os.path.join(DEFAULT_OUTPUT_DIR,
                                  generate_default_filename(DEFAULT_OUTPUT_DIR))
                                  
        
        sp_args = ["ffmpeg",
                   "-y",
                   "-video_size", f"{focused.rect.width}x{focused.rect.height}",
                   "-framerate", f"{args.framerate}",
                   "-draw_mouse", f"{int(args.draw_mouse)}",
                   "-show_region", f"{int(args.show_region)}",
                   "-f", "x11grab",
                   "-i", f":{args.display}+{focused.rect.x},{focused.rect.y} ",
                   output 
                   ]

        
        # start ffmpeg x11grab and write its pid to temp file
        ffmpeg = subprocess.Popen(sp_args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with open(PID_FILE, 'w') as f:
            f.write(str(ffmpeg.pid))
