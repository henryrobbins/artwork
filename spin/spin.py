import os
import sys
import time

speed = float(sys.argv[1])
states = ["|", "/", "-", "\\", "|", "/", "-", "\\"]

while 1 > 0:
    for state in states:
        print(state)
        time.sleep(speed)
        os.system('printf "\033[1A"')
        os.system('printf "\033[K"')
