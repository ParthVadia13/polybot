    
# polybot

**This is a bot which plays the racing game, Polytrack.**

It records live-pixel data, refines it using calibrated center-finding algorithms, and replays the keystroles with millisecond precision.

Read more about how I made it here: https://medium.com/@parthvadia13/polybot-devlog-47e93b5f3fed


**This repo includes a 'solo.py' which has extracted and made some important features from this project stand-alone:**
- play(textFile: str) plays a text file with lines in the format 'key action time' (ex. enter press 0.5). It will do the action on the specified key when the time after the function has been called matches the time stamp on the line. Very precise.
- recordPixelColor(x: int, y: int, duration: float, filename: str, color: str, value: int, threshold: int = 0). Records a time stamp every time a specified pixel cross a threshold RGB value. Can be used to detect button presses and other GUI automation.

**Thank you to:**
- Kodub for making Polytrack (https://kodub.itch.io/polytrack)
- Documentators for the mss library (https://python-mss.readthedocs.io/)
- ABBA for making awesome coding music
