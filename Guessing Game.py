import random


x = random.randint(1,10)
yourtries = 0
dumb = False

print("Guessing Game !!!")
print ("Guess A Number between 1 to 10 ...... You Have 3 Tries ")
while yourtries < 4:
    guess = int(input("My Guess is : "))

    if guess not in [1,2,3,4,5,6,7,8,9,10]:
        if dumb == True:
            
            yourtries += 1
            print("Again ???? i Said from 1 to 10 you fucking stupid asshole monkey Get the fuck out of my game")
            break

        if dumb == False:
            yourtries += 1
            dumb = True
            print("I Said From 1 To 10 You dumbass")
            print(f"Your Tries is {yourtries} out of 3")
            if yourtries == 3:
                print("Go Fuck Yourself iam not telling you what the right number was")
                break

            continue
       

    if guess == x:
        yourtries+= 1
        print("Congrats You Won " ,end="")
        if yourtries == 1:
            print ("From the First Time!!!!")
            print("Run The Code Again if You Want To Play Again !!!!!!!")
        break

    elif guess != x:
        yourtries += 1
        if yourtries == 1:
            print(f"Sorry Your Guess is Wrong Your Tries is {yourtries} out of 3")
            if x % 2 == 0:
                print("Hint1: The Right number is even")
            else:
                print("Hint1: The Right Number is odd")

        elif yourtries == 2:
            print(f"Sorry Your Guess is Wrong Your Tries is {yourtries} out of 3")
            if x >= 5:
                print("The Right Number is 5 Or More")
            else:
                print("The Right Number is 5 Or Less")
    
    if yourtries == 3:
        print(f"You Ran Out Of Tries The Right Num is {x}")
        print("Run The Code Again if You Want To Play Again !!!!!!!")
        break
    
