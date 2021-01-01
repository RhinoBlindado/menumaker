"""
Main Files for the Menu Maker Program.

Author: Valentino Lugli, 2021.
"""

# Packages
import sqlite3
from sqlite3 import Error


# Functions
def addPlates():
    print("..here..")

def genMenu():
    print("...here....")

# Main
def main():

    # Connecting to the database.
    conn = None
    try:
        conn = sqlite3.connect(r"food.db")
    except Error as e:
        print(e)

    if conn is not None:
        print(">DATABASE CONNECTION ESTABLISHED")
        running = True

        while(running):
            print("---MENU MAKER---")
            print("1- Add plate\n"+
            "2- Generate menu\n"+
            "0- Exit")
            case = int(input("> "))

            if case == 1:
                addPlates()
            elif case == 2:
                genMenu()
            elif case == 0:
                running = False
            else:
                print("Input Error")
    else:
        print(">DATABASE CONNECTION FAILED")


if __name__ == '__main__':
    main()