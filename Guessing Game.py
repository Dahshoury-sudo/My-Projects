import random
import sys

def menu():
    global printed
    printed = False
    print("#" * 60)
    print(" 🎯 guessing game ".center(60,"#"))
    print(" This Game Was Made By Mohamed_Fouad (Fo2sh) ".center(60,"#"))
    print("#" * 60)


def guessed_number():
    global printed
    if printed == False:
        print("Guess A number between 1 and 10")
        printed = True

    while(True):
        try:
            x = int(input("My Guess Is: "))
            if x in [1,2,3,4,5,6,7,8,9,10]:
                break
            else:
                print("⚠️ ⚠️ ⚠️  Wrong Input..Please From 1 To 10")

        except ValueError:
            print("⚠️  Please enter an integer number")

    return x


def game():
    secret = random.randint(1,10)
    your_tries = 0

    while your_tries < 3:
        guess = guessed_number()
        if guess == secret:
            print("🎉 Congrats you won 🎉")
            break

        elif guess != secret:
            your_tries += 1
            print("❌ Wrong Guess")
            print(f"Your Tries is {your_tries} out of 3")

            if your_tries == 1:
                if secret % 2 == 0:
                    print("The Secret Number is Even ❗️❗️❗️")

                else:
                    print("The Secret Number is Odd ❗️❗️❗️")

            elif your_tries == 2:
                if secret > 5:
                    print("The Secret Number Greater than 5")

                else:
                    print("The Secret Number is 5 or less")


    else:
        print(f"💀💀💀 You Ran Out Of Tries The Right Number was {secret}")

    outro()


def outro():
    while True:

        play = input("Do u want to play again ? y/n ").replace(" ", "").lower()
        
        if play == "y" or play == "yes":
            game()

        elif play == "n" or play == "no":
            print("Thanks For Playing My Game ❤️ ❤️ ")
            sys.exit()

        else:
            print("⚠️  Wrong Input Please try again")


menu()
game()
