from utils import getCalibrations, newCalibrations
from recorder import recordFourKeys, chronologize
from player import play
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel

#Displays action menu as Rich table
def displayMenu():
    print()
    table = Table(title = "Action Menu", style="bold green", header_style="bold white")
    table.add_column("Option", justify="center", style="bold purple")
    table.add_column("Action", style="white")
    
    table.add_row("1", "Record key input")
    table.add_row("2", "Play from file")
    table.add_row("3", "Calibrate screen controls")
    table.add_row("4", "Exit")

    console.print(table)

console = Console()
console.print(Panel("[bold green]Welcome to PolyBot[/bold green]", width=40))

choice = 0 

while choice != 4:
    displayMenu()
    choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4"])
    console.print("")

    #Record the screen
    if choice == '1':
        getCalibrations()
        filename = Prompt.ask("Enter filename to save")
        filename = "recordings/" + filename
        duration = float(Prompt.ask("Enter duration per trial (seconds)"))
        depth = int(Prompt.ask("Enter depth (recommended 7)"))
        console.print("Total recording will take [blue]" + str(depth * duration * 4) + "[/blue] seconds to complete.")
        input("Begin recording? ")

        recordFourKeys(filename, duration, depth)  
        chronologize(filename)

        console.print("[green] Finished recording and formating. [/green]")
        console.print("Recorded on: " + filename)

    #Play a recording/file
    elif choice == '2':
        file = input('Filename? ')
        play("recordings/" + file)
        console.print("[green] Finished playing. [/green]")


    #Calibrate screen/controls
    elif choice == '3':
        #Write all data in format 'object objectX objectY' (ex. play 153 15)
        newCalibrations() 
