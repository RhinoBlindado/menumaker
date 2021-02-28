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

#   YAML Parser
import yaml

#   RNG
import random


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


def genMenuRand(conn):
    print("---- GENERATING MENU ----")

    cursor = conn.cursor()

    breakfast = []
    lunch = []
    dinner =[]

    foodQuery = "SELECT nameFood FROM food WHERE "

    cursor.execute(foodQuery + " breakfast = 1")
    breakfast = cursor.fetchall()

    cursor.execute(foodQuery + " lunch = 1")
    lunch = cursor.fetchall()

    cursor.execute(foodQuery + " dinner = 1")
    dinner = cursor.fetchall()

    menuBreakfast = []
    menuLunch = []
    menuDinner = []

    for i in range(0, 6):
        menuBreakfast.append( breakfast[ random.randint(0, len(breakfast)-1) ][0] )
        menuLunch.append( lunch[ random.randint(0, len(lunch)-1) ] [0])
        menuDinner.append( dinner[ random.randint(0, len(dinner)-1) ] [0])

    week = ['MON','TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']

    for i in range(0, 6):
        print(week[i], menuBreakfast[i], menuLunch[i], menuDinner[i], sep='\t')



def loadPlates(conn):
    print("---- LOADING PLATES FROM FILE ----")

    cursor = conn.cursor()

    path = input(">YAML file path: ")

    with open(path,'r') as file:
        food = yaml.full_load(file)

    for item in food:

        # Get the name from the key of the dictionary, by casting it to a list.
        actFoodName = list(item)[0]

        # Generate the ID by hashing the name.
        actFoodID = hashlib.sha256(actFoodName.encode())


        cursor.execute('SELECT idFood FROM food WHERE idFood = ?', (actFoodID.hexdigest(),))

        if(not cursor.fetchone()):
            # The rest of the items for this particular item are on a nested dictionary.
            itemDetails = item.get(actFoodName)

            actUniqueFood = itemDetails.get('isUnique')

            schedule = itemDetails.get('schedule')
            
            # Get the values of the schedule as booleans.
            breakBit = schedule[0].get('b')
            lunchBit = schedule[1].get('l')
            dinneBit = schedule[2].get('d')

            cursor.execute('INSERT INTO food VALUES (?, ?, ?, ?, ?, ?, 0)', (actFoodID.hexdigest(), actFoodName, actUniqueFood, breakBit, lunchBit, dinneBit))

            print("Food [", actFoodName, "] added.")

            # Add the ingredients to the database if not already there.
            ingr = itemDetails.get('ingr')
            for i in ingr:
                igrName = list(i.keys())[0]
                igrID = hashlib.sha256(igrName.encode())

                cursor.execute('SELECT idIngr FROM ingredient WHERE idIngr = ?', (igrID.hexdigest(),))

                if(not cursor.fetchone()):
                    cursor.execute('INSERT INTO ingredient VALUES (?, ?, 0)', (igrID.hexdigest(), igrName))
                    print("\tIngredient [", igrName, "] added.")
                else:
                    print("\tIngredient [", igrName,"] already exists on database. Skipped.")

                auxList = (str(list(i.values())[0])).split()

                igrQuantity = auxList[0]

                if(len(auxList) > 1):
                    igrUnit = auxList[1]
                else:
                    igrUnit = ''

                cursor.execute('INSERT INTO madeup VALUES (?, ?, ?, ?)', (actFoodID.hexdigest(), igrID.hexdigest(), igrQuantity, igrUnit))

        else:
            print("Food [", actFoodName, "] already exists on database. Skipped.")

    conn.commit()


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
            "2- Load plates from file\n"+
            "3- Generate a menu (Random Generation)\n"
            "0- Exit")
            case = int(input("> "))

            if case == 1:
               # addPlates(conn)
               pass
            elif case == 2:
                loadPlates(conn)
            elif case == 3:
                genMenuRand(conn)
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