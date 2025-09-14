import pyautogui
import time
from config import calibration

#Print countdown before starting a process
def countdown(number):
    for i in range(number):
        print(number - i)
        time.sleep(1)
    
#Reset the recording by moving video progress bar
def reset():
    #Click in the middle of the progress bar
    pyautogui.moveTo(*calibration["reset1"])
    pyautogui.click()
    time.sleep(1)

    #Pause
    pyautogui.moveTo(*calibration["play"])
    pyautogui.click()
    time.sleep(1)

    #Rewind to before the race starts
    pyautogui.moveTo(*calibration["reset1"])
    pyautogui.dragTo(*calibration["reset2"], duration = 0.3, button = 'left')

#Press the play button
def pressPlay():
    pyautogui.moveTo(*calibration["play"])
    pyautogui.click()

#Write new calibrations from terminal input
def newCalibrations():
    positions = ["reset1", "reset2", "play", "up", "down", "left", "right"]
    with open('calibrate.txt', 'w') as c:
        for current in positions:
            #Input is to let user decide capture once mouse is at position
            input(current)
            x, y = pyautogui.position()
            c.write(current + " " + str(x) + " " + str(y) + "\n")    

#Load calibrations from calibrate.txt
def getCalibrations():
    with open('calibrate.txt', 'r') as c:
        positions = c.readlines()
        if positions == []:
            print("YOU NEED TO CALIBRATE")
            return

    global calibration
    for position in positions:
        i = position.strip().split()
        #Write x and y coordinate into dictionary
        calibration[i[0].lower()] = (int(i[1]), int(i[2]))