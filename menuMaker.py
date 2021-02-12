"""
Main Files for the Menu Maker Program.

Author: Valentino Lugli, 2021.
"""

# Packages
#   SQLite interface for the database
import sqlite3
from sqlite3 import Error

#   Get parameters from the command line.   
import sys

#   Get hash functions
import hashlib


# Functions
def addPlates(conn):
    """
    Lmao gottem
    """

    cursor = conn.cursor()

    foodList = []
    print("---- ADDING A PLATE ----")
    foodName = input(">Plate name: ")

    foodID = hashlib.sha256(foodName.encode())

    foodList.append(foodID.hexdigest())
    foodList.append(foodName)

    uniqueAns = input(">Can this plate be eaten alonside another one? (Y/N): ")

    if(uniqueAns == 'Y' or uniqueAns == 'y'):
        foodList.append(True)
    else:
        foodList.append(False)
    
    timeOfDay = input(">A what times of day can this be eaten? (Breakfast, Lunch, Dinner)")
    foodList.append(int(str(timeOfDay), 2))

    cursor.execute('INSERT INTO food VALUES (?, ?, ?, ?, 0)', foodList)

    ingrNumber = input(">How many ingredients does it have? ")


    for i in range(0, int(ingrNumber)):
        igrList = []
        print("\t Ingredient ["+str(i+1)+"/"+str(ingrNumber)+"]")
        igrName = input(">Ingredient name: ")
        igrID = hashlib.sha256(igrName.encode())

        igrList.append(igrID.hexdigest())
        igrList.append(igrName)

        cursor.execute('INSERT INTO ingredient VALUES (?, ?, 0)', igrList)

        madeUpList = []
        madeUpList.append(foodID)
        madeUpList.append(igrID)
        quantity = input(">How much quantity is used for the food? ")
        madeUpList.append(input(">Measurement unit? (ml, gr, kg, ...)"))

        cursor.execute('INSERT INTO madeup VALUES (?, ?, ?, ?)', (foodID.hexdigest(), igrID.hexdigest(), quantity, ' '))

        igrList.clear()
        madeUpList.clear()
    
    conn.commit()
    print("INSERTION DONE.")


def genMenu():
    print("...here....")

#   MAIN FUNCTION
def main():

    # Connecting to the database.
    conn = None
    try:
        conn = sqlite3.connect("food.db")
    except Error as e:
        print(e)

    if conn is not None:
        conn.execute('PRAGMA foreign_keys = ON')
        print(">DATABASE CONNECTION ESTABLISHED")
        running = True

        while(running):
            print("---MENU MAKER---")
            print("1- Add plate\n"+
            "2- Generate menu\n"+
            "0- Exit")
            case = int(input("> "))

            if case == 1:
                addPlates(conn)
            elif case == 2:
                genMenu()
            elif case == 0:
                running = False
                conn.close()
            else:
                print("Input Error")
    else:
        print(">DATABASE CONNECTION FAILED")



# Setting up the script enviroment
if __name__ == '__main__':
    main()