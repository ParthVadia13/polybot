import pyautogui
import time
import mss

biasCorrection = 0.017

def play(filename: str, countdown: int):
    with open(filename, "r") as f:
        data = [(float(parts[0]), parts[1], parts[2]) for parts in (line.strip().split() for line in f)]
    
    for i in range(countdown):
        time.sleep(1)
        print(countdown - i)

    start = time.perf_counter()

    for eventTime, key, action in data:
        delay = eventTime - (time.perf_counter() - start)
        
        if delay > 0.05:
            time.sleep(delay - 0.01)

        while time.perf_counter() - start < eventTime:
            pass
        
        if action == 'release':
            pyautogui.keyUp(key)
        else:
            pyautogui.keyDown(key)
    
    time.sleep(3)
    for eventTime, key, action in data:
        pyautogui.keyUp(key)

def getPixelColor(x: int, y: int, sct, color: int):
    monitor = {"top": y, "left": x, "width": 1, "height": 1}
    img = sct.grab(monitor)
    return (img.pixel(0, 0)[color])

def recordPixelColor(x: int, y: int, duration: float, filename: str, color: str, value: int, threshold: int = 0):
    global biasCorrection

    colors = {'red':0, 'blue':1, 'green':2}
    colorNum = colors[color]

    topLimit = value + threshold
    bottomLimit = value - threshold

    log = []
    start = 0

    with mss.mss() as sct:
        start = time.perf_counter()

        oldState = False

        finish = start + duration + 3
        currentTime = 0

        while currentTime < finish:
            currentTime = time.perf_counter()
            time.sleep(0.001)

            current = getPixelColor(x, y, sct, colorNum)
            state = current < topLimit and current > bottomLimit

            if oldState != state:
                log.append(currentTime)
                oldState = state
    
    editedLog = []
    for item in log:
        editedLog.append(round(item - start + biasCorrection, 5))
    
    with open(filename, "a") as f:
        state = 'true'
        f.write("---")
        for l in editedLog:
            f.write(str(round(l, 5)) + ' ' + state + '\n')           
     
            if state == 'true':
                state = 'false'
            else:
                state = 'true'

def processPixelColor(rawFilename: str, newFilename: str):
    with open(rawFilename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]  # skip empty lines

    raw = []
    currentRun = []

    for line in lines:
        if line == '---':
            raw.append(currentRun)
            currentRun = []
        else:
            currentRun.append(line.split()[1])

    raw.append(currentRun)
    
    depth = len(raw)
    average = []
    for j in range(len(raw[0])):
        event = []
        for k in range(depth):
            event.append(raw[k][j])
        trimmedMean = sum(event[1:(depth - 1)])/(depth - 2)
        average.append(trimmedMean)
    
    with open(newFilename, "a") as f:
        state = 'true'
        f.write("---")
        for l in average:
            f.write(str(round(l, 5)) + ' ' + state + '\n')           
     
            if state == 'true':
                state = 'false'
            else:
                state = 'true'