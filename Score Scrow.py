import os
class Player:
    Sum_of_scores = []
    def __init__(self,name):
        self.name = name
        self.scores = []
        self.sum = 0
    def SetScore(self):
        while True:
            try:
                self.round_score = int(input(f"What is {self.name} Score For {prefixes[0]} Round: "))
                self.scores.append(self.round_score)
                break

            except ValueError:
                print("Please Enter An Integer Value")
            
            except:
                print("Error Happend")
    
    def Calculate_Sum(self):
        self.sum = sum(self.scores)
        Player.Sum_of_scores.append(self.sum)
        return self.sum

class Menu:
    def Display_EndMenu(self):
        print("1- Restart With Same Players")
        print("2- Restart With Another Players")
        print("3- Quit Game")

        while True:

            try:

                choice = int(input("Enter Your Choice (1 or 2 or 3): "))
                break
            
            except ValueError:
                print("Please Enter an integer number (1 or 2 or 3): ")

            except :
                print("Error Happend Please Try Again")

        return choice


def NumberOfPlayers():
    while True:
        try:
            NumberOfPlayers = int(input("Enter The Number Of Players Max is 6 : "))
            if NumberOfPlayers > 6 or NumberOfPlayers < 3:
                print("Please From 3 to 6")
            else:
                return NumberOfPlayers

        except:
            print("Please Enter An integer number From 3 to 6")


def Game():
    
    global Player_Names,FirstTime,restart_names,print_other
    print_other = False
    if restart_names == True or FirstTime == True:
        Num_of_players = NumberOfPlayers()
        Player_Names = [Player(input(f"Player{number+1} Enter Your Name: ").capitalize()) for number in range(Num_of_players)]
        FirstTime = False
    global prefixes
    prefixes = prefixes_original[:]
    Player.Sum_of_scores = []
    for player in Player_Names:
        player.scores = []
    i = 0
    End_Menu = Menu()

    ClearScreen()

    while i < 5:
        for player in Player_Names:
            player.SetScore()
        i += 1
        ClearScreen()
        prefixes.pop(0)

    ClearScreen()

    for player in Player_Names:
        player.Calculate_Sum()

    Winner_Loser()
    others_scores()
    Choice = End_Menu.Display_EndMenu()

    if Choice == 1:
        prefixes = prefixes_original.copy()
        restart_names = False
        Game()
    elif Choice == 2:
        prefixes = prefixes_original.copy()
        restart_names = True
        Game()

    else:
        print("Thanks For Using The APP ❤️  ❤️ ")


def Winner_Loser():
    global Winner_index
    global Loser_index
    global king_indices
    global cooz_indices
    global print_other

    king_indices = [i for i,d in enumerate(Player.Sum_of_scores,0) if d == max(Player.Sum_of_scores)]
    cooz_indices = [i for i,d in enumerate(Player.Sum_of_scores,0) if d == min(Player.Sum_of_scores)]
    

    if len(king_indices) == 1 and len(cooz_indices) == 1:
        Loser_index = Player.Sum_of_scores.index(min(Player.Sum_of_scores))
        Winner_index = Player.Sum_of_scores.index(max(Player.Sum_of_scores))

        print(f"{Player_Names[Winner_index].name} Is The KIIIING With Score Of : {Player_Names[Winner_index].sum} ")
        print(f"{Player_Names[Loser_index].name} Is The COOOOOZ With Score Of : {Player_Names[Loser_index].sum} ")
        print_other = True

    else:
        print_other = False
        for player in Player_Names:
            print(f"{player.name} Has A Final Score Of {player.sum}")


def others_scores():
    j = 0
    while j < len(Player_Names) and print_other == True:
        if j == Winner_index or j == Loser_index:
            j += 1
            continue
        else:
            if print_other == True:
                print(f"{Player_Names[j].name} Score Is {Player_Names[j].sum}")

        j += 1

def MainMenu():
    print("#"*60)
    print(" Score Scrow App ".center(60,"#"))
    print(" This Game Was Made By Mohamed_Fouad (Fo2sh) ".center(60,"#"))
    print("#"*60)
    print("\n", end="")

def ClearScreen():
    os.system("cls")

if __name__ == "__main__":
    prefixes_original = ["First","Second","Third","Fourth","Fifth","Sixth"]
    FirstTime = True
    restart_names = False
    print_other = False
    MainMenu()
    Game()
