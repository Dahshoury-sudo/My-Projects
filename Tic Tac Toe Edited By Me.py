import os
import sys

def clear_screen():
    os.system("cls")

class Player:
    def __init__(self):
        self.name = ""
        self.symbol = ""

    def choose_name(self):
        name = input("Enter Your Name: ").capitalize()
        self.name = name


    def choose_symbol(self):
        while True:

            symbol = input(f"{self.name}, Choose Your Symbol (X or O): ").upper()
            if symbol in ("X","O") and len(symbol) == 1:
                self.symbol = symbol
                break
            else:
                print("Invalid Symbol Please Choose From (X or O) Only")


class Board:
    def __init__(self):
        self.board = [str(x) for x in range(1,10)]

    
    def display_board(self):
        print(f" {self.board[0]} | {self.board[1]} | {self.board[2]} ")
        print("---+---+---")
        print(f" {self.board[3]} | {self.board[4]} | {self.board[5]} ")
        print("---+---+---")
        print(f" {self.board[6]} | {self.board[7]} | {self.board[8]} ")

    def update_board(self,choice,symbol):

        if self.is_valid_move(choice) == True:
            self.board[choice - 1] = symbol
            return True
        else:
            return False
    
    def is_valid_move(self,choice):
        return self.board[choice - 1].isdigit()
    
    def reset_board(self):
        self.board = [str(x) for x in range(1,10)]


class Game:
    def __init__(self):
        self.players = [Player(),Player()]
        self.board = Board()
        self.menu = Menu()
        self.current_player_index = 0

    def start_game(self):
        choice = self.menu.display_main_menu()
        if choice == 1:
            self.setup_players()
            self.play_game()

        else:
            self.quit_game()

    def setup_players(self):
        for number, player in enumerate(self.players, start = 1):
            print(f"Player {number} Enter Your Details:")
            player.choose_name()
            player.choose_symbol()
            clear_screen()


    def play_game(self):
        while True:
            self.play_turn()
            if self.check_win():
                self.board.display_board()
                self.switch_player()
                print(f"{self.players[self.current_player_index].name} ({self.players[self.current_player_index].symbol}) Has Won")
                self.switch_player()
                choice = self.menu.display_endgame_menu()
                if choice == 1:
                    self.restart_game()
                else:
                    self.quit_game()
                    break

            elif self.check_draw():
                self.board.display_board()
                self.switch_player()
                print("It's a Tie. ⚔️  ⚔️ ")
                choice = self.menu.display_endgame_menu()
                if choice == 1:
                    self.restart_game()
                else:
                    self.quit_game()
                    break


    def restart_game(self):
        self.board.reset_board()
        self.play_game()
    
    def check_draw(self):
        return all(not cell.isdigit() for cell in self.board.board)


    def check_win(self): 
        win_combinations = [ 
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6], 
    [1, 4, 7], 
    [2, 5, 8], 
    [0, 4, 8],  
    [2, 4, 6]   
]
        for combo in win_combinations:
            if(self.board.board[combo[0]] == self.board.board[combo[1]] == self.board.board[combo[2]]) :
                return True
        return False


    
    def play_turn(self):
        player = self.players[self.current_player_index]
        self.board.display_board()
        print(f"{player.name}'s Turn ({player.symbol})")
        while True:
            try:
                cell_choice = int(input("Choose The Cell Number (1-9): "))
                if 1 <= cell_choice <= 9 and self.board.update_board(cell_choice,player.symbol):
                    break
                elif cell_choice > 9 or cell_choice < 1:
                    print("Enter a Proper cell number From 1 To 9")

                else:
                    print("This Place Is Already Taken")

        
            except ValueError:
                print("Please Choose Integer")

        clear_screen()
        self.switch_player()

    
    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index


    def quit_game(self):
        print("Thanks For Playing My Game ❤️ ❤️ ")
        sys.exit()


class Menu:

    def display_main_menu(self):
        print("#"*60)
        print(" Tic Tac Toe Game ❌ ⭕️ ".center(60,"#"))
        print(" This Game Was Made By Mohamed_Fouad (Fo2sh) ".center(60,"#"))
        print("#"*60)
        print("1- Start Game")
        print("2- Quit Game")
        while True:
            try:

                choice = int(input("Enter Your Choice (1 or 2): "))
                break
            
            except ValueError:
                print("Please Enter an integer number (1 or 2): ")

            except :
                print("Error Happend Please Try Again")

        return choice

    def display_endgame_menu(self):

        print("1- Restart Game")
        print("2- Quit Game")

        while True:

            try:

                choice = int(input("Enter Your Choice (1 or 2): "))
                break
            
            except ValueError:
                print("Please Enter an integer number (1 or 2): ")

            except :
                print("Error Happend Please Try Again")

        return choice


game = Game()
game.start_game()