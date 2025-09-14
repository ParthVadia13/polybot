import pyautogui
import time
from utils import countdown

#Plays formatted, recorded file precisely.
def play(filename):
    #Turn recorded strings into tuples (time [float], key, action)
    with open(filename, "r") as f:
        data = [(float(parts[0]), parts[1], parts[2]) for parts in (line.strip().split() for line in f)]
    
    countdown(5)

    #Used to callibrate other times 
    start = time.perf_counter()

    for eventTime, key, action in data:
        #Calculate time till next event
        delay = eventTime - (time.perf_counter() - start)
        
        #Sleep till 10ms before next event (less CPU, less precise)
        if delay > 0.05:
            time.sleep(delay - 0.01)

        #Sleep 1-5ms precisely (lot of CPU, more precise)
        while time.perf_counter() - start < eventTime:
            pass
        
        #Do the appropriate action using pyautogui
        if action == 'release':
            pyautogui.keyUp(key)
        else:
            pyautogui.keyDown(key)
    
    #Reset all keys
    time.sleep(3)
    pyautogui.keyUp('up')
    pyautogui.keyUp('down')
    pyautogui.keyUp('left')
    pyautogui.keyUp('right')