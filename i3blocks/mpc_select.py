#!/usr/bin/env python3
"""
Select mpc playlist via dmenu.

Button 1: Replace current playlist  
Button 2: Append to current playlist 
Button 3: Play song 
"""
import os
import subprocess
import pathlib

# TODO: factor out mpc functions into mpc module, or just use py-mpd2 

def mpc_clear(): 
    subprocess.run(["mpc", "clear", "--quiet"])

def mpc_load(playlist):
    subprocess.run(["mpc", "load", playlist], stdout=subprocess.DEVNULL)

def mpc_insert(song):
    subprocess.run(["mpc", "insert", song])

def mpc_next():
    subprocess.run(["mpc", "next"], stdout=subprocess.DEVNULL)
    
def mpc_playlists():
    return subprocess.check_output(["mpc", "lsplaylist"]).decode().splitlines()

def mpc_songs(): 
     return subprocess.check_output(["mpc", "listall"]).decode().splitlines()
    
def dmenu_select(values, prompt=""):
    dmenu = subprocess.Popen(["dmenu", "-b", "-i", "-p", prompt], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    dmenu_stdout, _ = dmenu.communicate("\n".join(sorted(values)).encode())
    return dmenu_stdout.decode().strip()
    
if __name__=='__main__':
    button = os.environ.get("button","")
    if button == "1":
        playlists = mpc_playlists()
        playlist = dmenu_select(playlists, prompt="Playlist [REPLACE]:") 
        if playlist in playlists: 
            mpc_clear()
            mpc_load(playlist) 
    elif button == "2":
        playlists = mpc_playlists()
        playlist = dmenu_select(playlists, prompt="Playlist [APPEND]:") 
        if playlist:
            mpc_load(playlist)
    # FIXME: May cause issues with large song database.
    # May need to switch to mpd queries, better tagging, and rofi 
    elif button == "3":
        songs = mpc_songs()
        s_dict = {pathlib.Path(song).stem: song for song in songs} 
        s_key = dmenu_select(s_dict.keys(), prompt="Song:")
        mpc_insert(s_dict[s_key])
        mpc_next()
    else:
        pass
    
