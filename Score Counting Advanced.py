
# prefixes_original = ["First","Second","Third","Forth","Fifth","Sixth"]
class Player:
    Sum_of_scores = []
    def __init__(self,name):
        self.name = name
        self.scores = []
        self.sum = 0
    def SetScore(self):
        for pre in prefixes:
            self.round_score = int(input(f"What is {self.name} Score For {pre} Round: "))
            self.scores.append(self.round_score)
            break
    
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
            print("Please Enter An integer number")


def Game():
    global Player_Names,FirstTime,restart_names
    if restart_names == True or FirstTime == True:
        Player_Names = [Player(input(f"Player{number+1} Enter Your Name: ")) for number in range(Num_of_players)]
        FirstTime = False
    global prefixes
    prefixes = prefixes_original[:]
    Player.Sum_of_scores = []
    for player in Player_Names:
        player.scores = []
    i = 0
    End_Menu = Menu()
    while i < 5:
        for player in Player_Names:
            player.SetScore()
        i += 1
        prefixes.pop(0)

    for player in Player_Names:
        player.Calculate_Sum()

    Winner_Loser()
    others_scores()
    Choice = End_Menu.Display_EndMenu()

    if Choice == 1:
        prefixes = ["First","Second","Third","Forth","Fifth","Sixth"]
        restart_names = False
        Game()
    elif Choice == 2:
        prefixes = ["First","Second","Third","Forth","Fifth","Sixth"]
        restart_names = True
        # Player_Names = [Player(input(f"Player{number+1} Enter Your Name: ")) for number in range(Num_of_players)]
        Game()

    else:
        print("Thanks For Using The APP ❤️ ❤️ ")


Num_of_players = NumberOfPlayers()


# Player_Names = [Player(input(f"Player{number+1} Enter Your Name: ")) for number in range(Num_of_players)]



def Winner_Loser():
    global Winner_index
    global Loser_index
    Winner_index = Player.Sum_of_scores.index(max(Player.Sum_of_scores))
    Loser_index = Player.Sum_of_scores.index(min(Player.Sum_of_scores))
    king_and_cooz_indecies = [Winner_index,Loser_index]
    print(f"{Player_Names[Winner_index].name} Is The KIIIING With Score Of : {Player_Names[Winner_index].sum} ")
    print(f"{Player_Names[Loser_index].name} Is The COOOOOZ With Score Of : {Player_Names[Loser_index].sum} ")
    return king_and_cooz_indecies

def others_scores():
    j = 0
    while j < len(Player_Names):
        if j == Winner_index or j == Loser_index:
            j += 1
            continue
        else:
            print(f"{Player_Names[j].name} Score Is {Player_Names[j].sum}")
        
        j += 1

if __name__ == "__main__":
    FirstTime = True
    restart_names = False
    Game()

    


