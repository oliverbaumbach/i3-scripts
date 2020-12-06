#!/usr/bin/env python3
"""
System Monitor for i3 bar

Requires mpstat, df, and Font Awesome 5
"""
import subprocess
import re
import json
from utils import fa, span, gradient_at

def battery_level():
    """
    Reads battery level from /sys/class/power_supply/BAT0/capacity
    """
    with open("/sys/class/power_supply/BAT0/capacity", "r") as f:
        return int(f.read())

def plugged_in():
    """
    Read charging status from /sys/class/power_supply/AC/online
    """
    with open("/sys/class/power_supply/AC/online", "r") as f:
        return bool(int(f.read()))

def hdd_utilisation():
    out = subprocess.check_output(["df", "-x", "tmpfs", "-x", "devtmpfs", "--total"]).decode()
    return int(re.search(r"total.*\D(?P<per>\d{1,3})%", out).group("per"))

def mem_utilisation():
    """
    Calculates memory utilisation by parsing output of free 
    """
    out = subprocess.check_output(["free"]).decode()
    match = re.search(r"Mem:\D+(?P<total>\d+)\D+" +
                      r"(?P<used>\d+)\D+" + 
                      r"(?P<free>\d+)\D+" + 
                      r"(?P<shared>\d+)\D+" + 
                      r"(?P<buffcache>\d+)\D+" + 
                      r"(?P<available>\d+)", out)
    return round((1 - (int(match.group("available")) /
                       int(match.group("total")))) * 100)  

def cpu_utilisation():
    """
    Gets average and maximum cpu utilisation via mpstat 
    """
    out = subprocess.check_output(["mpstat", "-P", "ALL", "-o", "JSON"]).decode()
    load_data = json.loads(out).get("sysstat", {}).get("hosts", [])[0].get("statistics",{})[0].get("cpu-load",[])
    avg_utilisation = 100 - next((x for x in load_data if x.get("cpu", "") == "all"), {}).get("idle", 100)
    max_utilisation = 100 - min(x.get("idle", 0) for x in load_data)
    return round(avg_utilisation), round(max_utilisation)

def battery_indicator(charge):
    """
    Returns correct charge icon for given battery percentage 
    """
    ICONS = [("f444", 12.5), # fa-battery-empty 
             ("f243", 37.5), # fa-battery-quarter
             ("f242", 62.5), # fa-battery-half
             ("f241", 87.5), # fa-battery-three-quarters
             ("f240", 100) # fa-battery-full 
    ]
    return next(icon for icon, val in ICONS if charge <= val)

def zero_just(string, length=3, color="525252"):
    return span("0" * (length - len(string)), fg=color)
                

GRADIENT = [("#F90000", 0.0),
            ("#F90000", 0.05),
            ("#EEF600", 0.20),
            ("#7CDC7A", 1.00)]

if __name__ == "__main__":
    hdd = hdd_utilisation()
    mem = mem_utilisation()
    cpu_avg, cpu_max = cpu_utilisation()
    bat = battery_level()
    is_plugged = plugged_in()

    print(
          fa("f0a0"), #
          zero_just(f"{hdd}"),
          span(f"{hdd} ",
               fg=gradient_at(GRADIENT, 1 - (hdd/100))), 
          fa("f538"), #
          zero_just(f"{mem}"),
          span(f"{mem} ",
               fg=gradient_at(GRADIENT, 1 - mem / 100 )),
          fa("f2db"), #
          "高",
          zero_just(f"{cpu_max}"),
          span(f"{cpu_max}",
               fg=gradient_at(GRADIENT, 1 - (cpu_max / 100))),
          "平",
          zero_just(f"{cpu_avg}"),
          span(f"{cpu_avg} ",
               fg=gradient_at(GRADIENT, 1 - (cpu_avg / 100))),
          fa("f1e6") if is_plugged else fa(battery_indicator(bat)), #
          zero_just(f"{bat}"), 
          span(f"{bat}",
               fg=(gradient_at(GRADIENT, bat / 100) if not is_plugged else None)),
          sep=""
          )
    
