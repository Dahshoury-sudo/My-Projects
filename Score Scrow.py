import os

class Player:
    def __init__(self, name):
        self.name = name
        self.scores = []
        self.total_score = 0

    def set_score(self, round_name):
        while True:
            try:
                score = int(input(f"What is {self.name}'s score for the {round_name} round: "))
                if round_name in ["Fourth", "Fifth"]:
                    self.scores.append(score * 2)
                else:
                    self.scores.append(score)
                break
            except ValueError:
                print("Please enter an integer value.")
            except Exception as e:
                print(f"An error occurred: {e}")

    def calculate_total_score(self):
        self.total_score = sum(self.scores)
        return self.total_score


class Game:
    def __init__(self):
        self.players = []
        self.rounds = ["First", "Second", "Third", "Fourth", "Fifth"]
        self.first_time = True

    def setup_players(self):
        num_players = self.get_number_of_players()
        self.players = [Player(input(f"Player {i + 1}, enter your name: ").capitalize()) for i in range(num_players)]
        self.first_time = False

    @staticmethod
    def get_number_of_players():
        while True:
            try:
                num_players = int(input("Enter the number of players (3 to 12): "))
                if 3 <= num_players <= 12:
                    return num_players
                print("Please enter a number between 3 and 12.")
            except ValueError:
                print("Please enter an integer.")

    def play_rounds(self):
        for round_name in self.rounds:
            self.clear_screen()
            for player in self.players:
                player.set_score(round_name)
        self.clear_screen()

    def calculate_scores(self):
        for player in self.players:
            player.calculate_total_score()

    def determine_winners(self):
        scores = [player.total_score for player in self.players]
        min_score = min(scores)
        max_score = max(scores)
        winners = [player for player in self.players if player.total_score == min_score]
        losers = [player for player in self.players if player.total_score == max_score]

        if len(winners) == 1 and len(losers) == 1:
            print(f"{winners[0].name} is the KING with a score of {winners[0].total_score}!")
            print(f"{losers[0].name} is the COOZ with a score of {losers[0].total_score}!")
            self.display_other_scores(winners[0], losers[0])
        else:
            for player in self.players:
                print(f"{player.name} has a final score of {player.total_score}.")

    def display_other_scores(self, winner, loser):
        for player in self.players:
            if player not in [winner, loser]:
                print(f"{player.name}'s score is {player.total_score}.")

    @staticmethod
    def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")

    def start(self):
        if self.first_time:
            self.setup_players()
        self.play_rounds()
        self.calculate_scores()
        self.determine_winners()
        self.end_menu()

    def end_menu(self):
        while True:
            print("#" * 34)
            print("1. Restart with the same players")
            print("2. Restart with new players")
            print("3. Quit game")
            print("4. Show all rounds' scores for all players")
            try:
                choice = int(input("Enter your choice (1-4): "))
                if choice == 1:
                    self.first_time = False
                    self.start()
                elif choice == 2:
                    self.first_time = True
                    self.start()
                elif choice == 3:
                    print("Thanks for using the app! ❤️❤️")
                    break
                elif choice == 4:
                    self.clear_screen()
                    for player in self.players:
                        print(f"{player.name}'s round scores: {player.scores}")
                    input("Press Enter to continue...")
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid integer.")


def main():
    print("#" * 60)
    print(" Score Scrow App ".center(60, "#"))
    print(" This app was made by Mohamed_Fouad (Fo2sh) ".center(60, "#"))
    print("#" * 60)
    print()

    game = Game()
    game.start()


if __name__ == "__main__":
    main()
