
import hashlib

import os

clear = lambda: os.system('cls')

class Customer:
    
    def __init__(self): #Initialise class

        def register(): #Registration function 
            clear()
            print("REGISTER")
            print("--------")
            print()
            while True:
                userName = input("Enter Your Name: ").lower()
                if userName != '':
                    break
            userName = sanitizeName(userName) #sanitizeName makes the input more easily readable
            if userAlreadyExist(userName): #Checks to see if the name of the user is already on file.
                displayUserAlreadyExistMessage()
                #Displays error message and redirects user to create a new account or submit their details on the login page
            else: #If the user isn't already registered, system prompts for details
                while True: 
                    userPassword = input("Enter Your Password: ")
                    if userPassword != '':
                        break
                while True:
                    confirmPassword = input("Confirm Your Password: ")
                    if confirmPassword == userPassword:
                        break
                    else:
                        print("Passwords Don't Match")
                        print()
                if userAlreadyExist(userName, userPassword):
                    while True:
                        print()
                        error = input("You Are Already Registered.\n\nPress (T) To Try Again:\nPress (L) To Login: ").lower()
                        if error == 't':
                            register()
                            break
                        elif error == 'l':
                            login()
                            break
                addUserInfo([userName, hash_password(userPassword)])
                #If user registers correctly, then the system calls the addUserInfo function, which will write the userName and encrypted password into the text file to be stored for later use 

                print()
                print("Registered!")

        def login(): 
            clear()
            print("LOGIN")
            print("-----")
            print()
            usersInfo = {}
            with open('Customer.txt', 'r') as file:
                for line in file:
                    line = line.split()
                    usersInfo.update({line[0]: line[1]})

            while True:
                userName = input("Enter Your Name: ").lower()
                userName = sanitizeName(userName)
                #The sanitize name function splits and then rejoins the users name, so that full names are more easily read
                if userName not in usersInfo: 
                    print("You Are Not Registered")
                    print()
                else:
                    break 
            while True:
                userPassword = input("Enter Your Password: ")
                if not check_password_hash(userPassword, usersInfo[userName]):
                    #Checks the passwords hash code versus the one saved
                    print("Incorrect Password")
                    print()
                else:
                    break
            print()
            print("Logged In!")

        def addUserInfo(userInfo: list): #This function is called when the registration process is complete
            with open('Customer.txt', 'a') as file:
                for info in userInfo:
                    file.write(info)
                    file.write(' ')
                file.write('\n')

        def userAlreadyExist(userName, userPassword=None): #Looks directly for name
            if userPassword == None:
                with open('Customer.txt', 'r') as file:
                    for line in file:
                        line = line.split()
                        if line[0] == userName:
                            return True
                return False #Will go on to check for the password
            else:
                userPassword = hash_password(userPassword)
                usersInfo = {}
                with open('Customer.txt', 'r') as file:
                    for line in file:
                        line = line.split()
                        if line[0] == userName and line[1] == userPassword:
                            usersInfo.update({line[0]: line[1]})
                if usersInfo == {}:
                    return False
                return usersInfo[userName] == userPassword

        def displayUserAlreadyExistMessage(): #Message displayed when trying to registed when already a customer
            while True:
                print()
                error = input("You Are Already Registered.\n\nPress (T) To Try Again:\nPress (L) To Login: ").lower()
                if error == 't':
                    register()
                    break
                elif error == 'l':
                    login()
                    break

        def sanitizeName(userName): #Makes it easier to hash
            userName = userName.split()
            userName = '-'.join(userName)
            return userName

        def hash_password(password): #Turns password into a string of nonsense
            return hashlib.sha256(str.encode(password)).hexdigest()

        def check_password_hash(password, hash): #Checks to see if the recorded hash is what it should be
            return hash_password(password) == hash


class Trainer():
    
    def __init__(self):
        
        def trainerMain():
            clear()
            print("Trainer Management")
            print("1. Add Trainers to system")
            print("2. View Trainers")
            while True:
                userChoice = input("Choose an option: ")
                if userChoice == '1':
                    addTrainerToSystem()
                    break
                elif userChoice == '2':
                    viewTrainers()
                    break        
                
        def addTrainerToSystem():
            clear()
            print("Add Trainer to System")
            print()
            while True:
                user_name = input("Trainer name: ")
                if user_name != '':
                    break
            while True:
                trainer_spec = input("Trainer Speciality: ")
                if trainer_spec != '':
                    break
            addTrainerToFile({user_name: trainer_spec}, clear=False) #Adds the strings in the variables to be wrote into the text file 
            returnToMainMenu("Trainer has been added")
                    
        def viewTrainers(): #This function will produce an output of our trainers recorded
            clear()
            print("VIEW TRAINERS")
            invItems = getTrainer() #calls the getTrainer function, which makes this code look tidier
            print("TRAINERS")
            print("-----")
            print()
            for item in invItems:
                print(f"{item}: {invItems[item]}")
                
            
        def editTrainer():
            clear()
            print("EDIT TRAINERS")
            print("-------------------")
            print(" Press (B) to go back")
            print()
            print("Available Options:")
            print()
            print("1 - Edit Trainer Name")
            print("2 - Edit Trainer Experience")
            print()
            while True:
                userChoice = input("Choose an Option: ").lower()
                if userChoice in ['1', '2', 'b']:
                    break
            if userChoice == 'b': #Returns to the main menu
                quit()
            trainers = getTrainer() #calls this function so I don't have to write it out again 
            if userChoice == '1': 
                print()
                while True:
                    trainerToChange = input("Enter the name of the trainer you wish to change: ")
                    if trainerToChange in trainers:
                        break
                    else:
                        print(" That trainer does not exist")
                        print()
                while True:
                    newTrainerName = input("Enter the new trainer name: ")
                    if newTrainerName != '':
                        break 
                trainers.update({newTrainerName: trainers[trainerToChange]})
                del trainers[trainerToChange] #Deletes that initial input
                
                addTrainerToFile(trainers, clear=True)
                returnToMainMenu("Trainer has been Updated")
                
            elif userChoice == '2':
                print()
                while True:
                    trainerToChange = input("Enter the name of the Trainer you wish to change")
                    if trainerToChange in trainers:
                        break
                    else:
                        print("That trainer does not exist")
                        print()
                        
                while True:
                    newTrainerSpec = input("Please enter the skills of the trainer: ")
                    if newTrainerSpec != '':
                        break
                trainers.update({trainerToChange: newTrainerSpec})
                addTrainerToFile(trainers, clear=False)
                returnToMainMenu("Trainer Speciality changed")
            
        def deleteTrainer():
            print("Delete Trainer")
            print("---------------------")
            print()
            trainers = getTrainer()
            while True:
                trainerToDelete = input("Enter the name of the trainer to delete: ")
                if trainerToDelete in trainers:
                    break 
                else:
                    print("Trainer does not exist")
                    print()
                    
            while True:
                confirmation = input("CONFIRMATION: Are You sure you want to delete this trainer?: ").lower()
                if confirmation in ['yes', 'no']:
                    break
            if confirmation == 'yes':
                del trainers[trainerToDelete]
                addTrainerToFile(trainers, clear=True)
                returnToMainMenu("Trainer has been deleted")
            else:
                quit()
                

        def addTrainerToFile(userName: dict, clear: bool):
            if clear:
                f = open('Trainers.txt', 'w')
                f.close()
                with open('Trainers.txt', 'a') as file:
                    for item in userName:
                        file.write(f"{item}: {userName[item]}") #Take them inputs from the function that calls it and write them in here
                        file.write('\n')
                return 
            trainers = getTrainer() #Calls this function and saves it as a variable
            for item in trainers:
                #CHECK IF THE ITEM HAS ALREADY BEEN ADDED
                if item in trainers:
                    trainers[item] += userName[item]
            with open('Trainers.txt', 'a') as file:
                for item in trainers:
                    file.write(f"{item}: {trainers[item]}")
                    file.write('\n')

        def getTrainer(): #This function will produce a dictionary that can be iterated through that contains that trainers name and what it is that they specialise in
            trainers = {}
            with open('Trainers.txt', 'r') as file:
                for line in file:
                    line = line.replace('\n', '').split(':')
                    trainerName, trainerSpec = line[0], line[1].strip()
                    trainers.update({trainerName: trainerSpec})
            return trainers

        def returnToMainMenu(Message):
            while True:
                print()
                back = input(f"{Message}. Press (M) to return to main menu: ").lower()
                if back == 'm':
                    main() #wanna return to home screen
                    break 
                

class Equipment():
    
    def __init__(self):
        
#LOTS OF THIS IS JUST REPEATED CODE
        def equipmentMain():
            clear()
            print("Equipment menu")
            print("1. Add equipment to system")
            print("2. View equipment")
            while True:
                userChoice = input("Choose an option: ")
                if userChoice == '1':
                    addEquipmentToInventory()
                    break
                elif userChoice == '2':
                    printEquipment()
                    break
                
        def addEquipmentToInventory():
            clear()
            print("Add Equipment to inventory")
            print("Available options:")
            print("1 - Add Multiple Items")
            print("2 - Add a Single Item")
            while True:
                userChoice = input("Choose an option")
                if userChoice in ['1', '2']:
                    break
            if userChoice == '1':
                print()
                while True:
                    numItems = input("Enter the number of items to be added ")
                    if numItems.isdigit():
                        break
                numItems = int(numItems)
                userItems = {}
                for i in range(1, numItems+1):
                    while True:
                        print()
                        user_item = input("Equipment name")
                        if user_item != '':
                            break
                    while True:
                        item_amount = input("Equipment Amount: ")
                        if item_amount.isdigit():
                            break
                    userItems.update({user_item: int(item_amount)})
                    addEquipmentToFile(userItems, clear=False)
                    returnToMainMenu("Equipment added")
                
            if userChoice == '2':
                print()
                while True:
                    user_item = input("Equipment name: ")
                    if user_item != '':
                        break
                while True:
                    item_amount = input("Equipment Amount: ")
                    if item_amount.isdigit():
                        break
                addEquipmentToFile({user_item: int(item_amount)}, clear=False)
                returnToMainMenu("Item has been added")

        def printEquipment(): #THis function is another way to call the inventory
            equipmentFile = open("Equipment.txt", 'r')
            print("Our Trainers")
            while equipment_description != '':
                equipment_description = equipmentFile.readline()
                equipment_quantity = equipmentFile.readline()
                equipment_description = equipment_description.rstrip('\n')
                equipment_quantity = equipment_quantity.rstrip('\n')
                print('Equipment:   ', equipment_description)
                print('Number in the gym:    ', equipment_quantity)
                print('--------------------') 
                equipment_description = equipmentFile.readline()
            equipmentFile.close()

        def editEquipment():
            clear()
            print("Edit Equptment Inventory ")
            print("-------------------")
            print(" Press (B) to go back")
            print()
            print("Available Options:")
            print()
            print("1 - Delete Equipment")
            print("2 - Edit Equipment")
            print()
            while True:
                userChoice = input("Choose an Option: ").lower()
                if userChoice in ['1', '2', 'b']:
                    break
            if userChoice == 'b':
                main()

            if userChoice == '1':
                deleteEquipment()

        def deleteEquipment():
            print("Delete Equipment")
            print("---------------------")
            print()
            equipment = getEquipment()
            while True:
                equipmentToDelete = input("Enter the name of the equipment to delete: ")
                if equipmentToDelete in equipment:
                    break 
                else:
                    print("Equipment does not exist")
                    print()
                
            while True:
                confirmation = input("CONFIRMATION: Are You sure you want to delete this item?: ").lower()
                if confirmation in ['yes', 'no']:
                    break
            if confirmation == 'yes':
                del equipment[equipmentToDelete]
                addEquipmentToFile(equipment, clear=True)
                returnToMainMenu("Item has been deleted")
            else:
                pass 
            
        def addEquipmentToFile(userItems: dict, clear: bool):
            if clear:
                f = open('Equipment.txt', 'w')
                f.close()
                with open('Equipment.txt', 'a') as file:
                    for item in userItems:
                        file.write(f"{item}: {userItems[item]}")
                        file.write('\n')
                return 
            invItems = getEquipment()
            for item in userItems:
                if item in invItems:
                    invItems[item] += userItems[item]
            with open('Equipment.txt', 'a') as file:
                for item in invItems:
                    file.write(f"{item}: {invItems[item]}")
                    file.write('\n')
                    
        def getEquipment():
            equipment = {}
            with open('Equipment.txt', 'r') as file:
                for line in file:
                    line = line.replace('\n', '').split(':')
                    equipmentName, equipmentAmount = line[0], line[1].strip()
                    equipment.update({equipmentName: int(equipmentAmount)})
            return equipment

        def returnToMainMenu(Message):
            while True:
                print()
                back = input(f"{Message}. Press (M) to return to main menu: ").lower()
                if back == 'm':
                    pass
                    break 
    
class ExercisePlan():

    def __init__(self):

#Prints out a nice table to display to the person who calls this function
        def viewExercisePlan():
            print("Exercise Plan")
            trainer_file = open("Trainers.txt",'r')
            trainer_input = input("Please enter the name of the trainer that you have selected").lower()
            if trainer_input in trainer_file:
                print("Your workout routine")
                data = open('ExercisePlan', 'r')
                items = data.readlines()
                for item in items:
                    exercise, machine, repetitions, sets = item.split(',')
                    print()
                    print('{0}\t\t{1}\t{2}\t{3}'.format(exercise, machine, repetitions, sets))
                    print()
                

        def addExercise(): #Add exercises
            ExerciseFile = open('ExercisePlan.txt', 'a')
            print('Adding Exercise')
            exerciseName = input("Enter Name: ")
            machineName = input("Machine Name: ")
            repetitions = input("Number of repetitions: ")
            sets = input("Number of sets: ")
            ExerciseFile.write(exerciseName + '\n')
            ExerciseFile.write(machineName + '\n')
            ExerciseFile.write(repetitions + '\n')
            ExerciseFile.write(sets + '\n')
            ExerciseFile.close
            CHOICE = input('Do you wish to continue? y/n')
            if CHOICE == 'y':
                addExercise()
                pass
            else:
                exit()

        def deleteRegimen(): #If you wanted to make a whole new workout plan, this would be called
            with open('ExercisePlan.txt', 'w') as r:
                r.close()

        
class Subscription(Customer):
        
    def __init__(self):
        Customer.__init__(self)
    
        def purchaseSubscription():
            customers = open('Customers.txt', 'r') 
            user = input("Please enter your name: ").lower()
            if user in customers:
                print("What subscriptions would you like to purchase?: ")
                print("1. One month: ")
                print("2. Three month: ")
                print("3. Six month: ")
                print("4. One year: ")
                userChoice = input("Please select an option: ")

                if userChoice == 1:
                    with open("Subscriptions.txt", 'a') as p:
                        p.write(f'{user}\n has subscribed for 1 month')


                if userChoice == 2:
                    with open("Subscriptions.txt", 'a') as p:
                        p.write(f'{user}\n has subscribed for 3 months: ')

                if userChoice == 3:
                    with open("Subscriptions.txt", 'a') as p:
                        p.write(f'{user}\n has subscribed for 6 months: ')

                if userChoice == 4:
                    with open("Subscriptions.txt", 'a') as p:
                        p.write(f'{user}\n has subscribed for 1 year: ')

        def printEquipment(): #Nicely prints out the member and their subsrciption duration. It will also print out if they've updated
            subFile = open("Subscriptions.txt", 'r')
            print("Our Trainers")
            while member_description != '':
                member_description = subFile.readline()
                member_duration = subFile.readline()
                member_description = member_description.rstrip('\n')
                member_duration = member_duration.rstrip('\n')
                print('Member:   ', member_description)
                print('Duration of membership:    ', member_duration)
                print('--------------------') 
                member_description = subFile.readline()
            subFile.close()


        def updateSubscription():
            with open('Subscriptions.txt', 'a') as q:
                print("Please choose what subscription you would like to change to: ")
                print("1. Three month: ")
                print("2. Six month: ")
                print("3. One year: ")
                userChoice = input("Please select an option: ")
                userName = input("Please enter you first name")

                if userChoice == 1:
                    with open("Subscriptions.txt", 'a') as q:
                        q.write(f'{userName} has updated their subscription to a 3 month subscription')

                if userChoice == 2:
                    with open("Subscriptions.txt", 'a') as q:
                        q.write(f'{userName} has updated their subscription to a 6 month')

                if userChoice == 3:
                    with open("Subscriptions.txt", 'a') as q:
                        q.write(f'{userName} has updated their subscription to a 1 year subscription')

        def deleteMember(): #This deletes any record of their subscription
            cin = open("Customer.txt", "r+")
            fin = open("Subscriptions.txt", 'r+')
            couth = open("Temp.txt", "a")
            out = open("Temp2.txt", 'a')
            ch = ' '
            fh = ' '
            input = input("Enter Customer For Deletion\n")
            while ch:
                ch = cin.readline()
                fh = fin.readline()
                val = ch.split("~")
                var = fh.split("~")
                if len(ch) > 0 and len(fh) > 0:
                    if input != int(val[1]) and input != int(var[1]):
                        couth.write(ch)
                        out.write(fh)
            couth.close()
            out.close()
            cin.close()
            fin.close()
            os.remove("Customer.txt")
            os.remove("Subscription.txt")
            os.rename("Temp.txt", "Customers.txt")
            os.rename("Temp2.txt", "Subscriptions.txt")
        
        
if __name__ == "__main__":
        
    Customer_object = Customer()
    Trainer_object = Trainer()
    Equipment_object = Equipment()
    ExercisePlan_object = ExercisePlan()
    Subscription_object = Subscription()
    
  
    print("Welcome to my gym")
    print("1. Login") 
    print("2. Create a new Account")
    print("3. View our Trainers")
    print("4. View our Membership subscriptions available")
    print("5. View our luxury equipment")
    print("6. Trainer login")
    user = int(input("Make decision: "))

    if user == 1:
        Customer_object.login()
            
    if user == 2:
        Customer_object.register()

    if user == 3:
        Trainer_object.printTrainers()

    if user == 4:
        Subscription_object.purchaseSubscription()

    if user == 5:
        Equipment_object.equipmentMain()
        
    if user == 6:
        Trainer_object.trainerMain()
        