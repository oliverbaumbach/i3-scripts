#!/usr/bin/env python3
import subprocess
import json
import time
import sys 
from math import log
from utils import gradient_at, span, fa

GRADIENT = [("#000000", 0.0),
            ("#FFFFFF", 1.0)] 

RX_MAX = 2.5e7 # 200MB/s
TX_MAX = 1.25e6 # 10MB/s 
INTERFACE = "wlp4s0"

def xB(val):
    shift = int(log(val + 1, 10) / 3)
    digits = int(val / 10**(shift*3)) 
    return f"{digits:·>3}" + ("·","k","M","G")[shift] 

def get_rx_tx():
    ifstat = subprocess.check_output(["ifstat","-j"]).decode()
    ifstat = json.loads(ifstat)["kernel"][INTERFACE]

    return int(ifstat["rx_bytes"]), int(ifstat["tx_bytes"])

rx_last, tx_last = get_rx_tx()
time.sleep(1)

while True:
    rx_bytes, tx_bytes = get_rx_tx() 

    rx_bytes, rx_last = rx_bytes - rx_last, rx_bytes 
    tx_bytes, tx_last = tx_bytes - tx_last, tx_bytes

    rx_color = gradient_at(GRADIENT, min(log(rx_bytes + 1, 10) / log(RX_MAX, 10), 1))
    tx_color = gradient_at(GRADIENT, min(log(tx_bytes + 1, 10) / log(TX_MAX, 10), 1))
    
    #·10㎅ ··5㎆  
    print(fa("f102"), #
          span(xB(tx_bytes), fg=tx_color),
          " ", 
          fa("f103"), #
          span(xB(rx_bytes), fg=rx_color),
          sep=""
          )
    sys.stdout.flush()
    time.sleep(1)
