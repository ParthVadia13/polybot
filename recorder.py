import mss
import time
from config import calibration
from utils import reset, pressPlay, countdown

#Use already-open sct to find blue value of given pixel.
def getPixelBlue(x, y, sct):
    monitor = {"top": y, "left": x, "width": 1, "height": 1}
    img = sct.grab(monitor)
    return (img.pixel(0, 0)[2])

#Record one pixel one run of the recording.
def recordOneTrial(key, duration):
    biasCorrection = 0.017

    #Grab pixel coordinates to monitor
    if key == 'left':
        x, y = calibration["left"]
    elif key == 'right':
        x, y = calibration["right"]
    elif key == 'up':
        x, y = calibration["up"]
    elif key == 'down':
        x, y = calibration["down"]

    log = []
    start = 0

    pressPlay()

    #Open sct here so getPixelBlue doesn't need to open it repeatedly
    with mss.mss() as sct:
        #Start recording when up is pressed (that is when all races start)
        while getPixelBlue(*calibration["up"], sct) > 90:
            pass

        #Start variable acts callibrator for all other logged times
        start = time.perf_counter()

        #Since key up has already been pressed without being logged, log that. 
        if key == 'up':
            log.append(start - biasCorrection)
            oldState = True
        else:
            oldState = False

        finish = start + duration + 3
        currentTime = 0

        #Detect state changes in the pixel we are monitoring
        while currentTime < finish:
            currentTime = time.perf_counter()

            #Sleeping for 1ms lessens CPU load and makes monitoring more consistent
            time.sleep(0.001)

            state = (getPixelBlue(x, y, sct) < 90)
            if oldState != state:
                log.append(currentTime)
                oldState = state
    
    editedLog = []
    for item in log:
        editedLog.append(round(item - start + biasCorrection, 5))
    
    return editedLog

#Record depth-number of trials, calculate trimmed-mean for each event, and write to file
def recordKey(key, filename, duration, depth):
    raw = []
    for i in range(depth):
        reset()
        time.sleep(0.1)
        x = recordOneTrial(key, duration)
        raw.append(x)
    
    average = []
    for j in range(len(raw[0])):
        event = []
        for k in range(depth):
            event.append(raw[k][j])
        trimmedMean = sum(event[1:(depth - 1)])/(depth - 2)
        average.append(trimmedMean)

    #state will flip flop as it parses through recorded data
    state = 'press'

    with open(filename, "a") as f:
        for l in average:
            #Format and record piece of data (ex. 0.134 left release)
            f.write(str(round(l, 5)) + ' ' + key + ' ' + state + '\n')           
     
            #Flip-flop between press and release
            if state == 'press':
                state = 'release'
            else:
                state = 'press'

#Record all keys in a list (currently 4 directions)
def recordFourKeys(filename, duration, depth):
    directions = ['up', 'down', 'left', 'right']

    countdown(5)
    print("Recording started.")
   
    pressPlay()
    time.sleep(1)

    for arrow in directions:
        time.sleep(1)
        recordKey(arrow, filename, duration, depth)

#Order events in a recorded file into chronological order 
def chronologize(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    
    #Turn data into an array of tuples (time, key, action)
    parsed = []
    for line in lines:
        parts = line.strip().split()
        number = float(parts[0])
        parsed.append((number, parts[1], parts[2]))
    
    #Sort all the tuples chronologically
    sortedLines = sorted(parsed, key = lambda item: item[0])

    #Erase old data and write new, ordered data
    with open(filename, "w") as f:
        for line in sortedLines:
            f.write(str(round(line[0], 5)) + " " + line[1] + " " + line[2] +  "\n")