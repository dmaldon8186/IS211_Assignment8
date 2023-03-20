import random
from abc import ABC, abstractmethod
import time
import argparse

class Die:
    def __init__(self):
        self.value = None

    def roll(self):
        self.value = random.randint(1, 6)
        return self.value

class Game(ABC):
    def __init__(self, player1_name, player2_name, target_score=100):
        self.player1 = Player(player1_name)
        self.player2 = Player(player2_name)
        self.target_score = target_score
        self.current_player = self.player1

    @abstractmethod
    def is_game_over(self):
        pass

    def switch_current_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def play(self):
        while not self.is_game_over():
            self.current_player.turn()
            self.switch_current_player()
        self.end_game()

    def end_game(self):
        print("Game over.")
        if self.player1.score >= self.target_score:
            print(f"{self.player1.name} wins!")
        else:
            print(f"{self.player2.name} wins!")

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.turn_score = 0

class TwoPlayerGame(Game):
    def is_game_over(self):
        return self.player1.score >= self.target_score or self.player2.score >= self.target_score

    def get_current_player(self):
        return self.current_player

    def turn(self):
        print(f"{self.current_player.name}'s turn:")
        while True:
            roll = Die().roll()
            if roll == 1:
                print(f"You rolled a 1. Your turn is over.")
                self.current_player.turn_score = 0
                break
            else:
                self.current_player.turn_score += roll
                print(f"You rolled a {roll}. Current turn score: {self.current_player.turn_score}")
                print(f"Current total score: {self.current_player.score + self.current_player.turn_score}")
                decision = input("Do you want to roll again (r) or hold (h)? ")
                if decision == "h":
                    self.current_player.score += self.current_player.turn_score
                    self.current_player.turn_score = 0
                    print(f"{self.current_player.name}'s score is now {self.current_player.score}")
                    break
                elif decision != "r":
                    print("Invalid input. Please enter 'r' or 'h'.")

    def play(self):
        self.current_player = self.player1
        while not self.is_game_over():
            self.turn()
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1
        print("Game over.")
        if self.player1.score >= self.target_score:
            print(f"{self.player1.name} wins!")
        else:
            print(f"{self.player2.name} wins!")

class TimedGameProxy(Game):
    def __init__(self, player1_name, player2_name, target_score=100):
        super().__init__(player1_name, player2_name, target_score)
        self.start_time = None

    def is_game_over(self):
        return super().is_game_over() or self.is_time_up()

    def is_time_up(self):
        if not self.start_time:
            self.start_time = time.time()
        return time.time() - self.start_time > 60

    def get_current_player(self):
        return self.current_player

    def turn(self):
        print(f"{self.current_player.name}'s turn, {60 - int((time.time() - self.start_time))} seconds left:")
        while True:
            roll = Die().roll()
            if roll == 1:
                print(f"You rolled a 1. Your turn is over.")
                self.current_player.turn_score = 0
                break
            else:
                self.current_player.turn_score += roll
                print(f"You rolled a {roll}. Current turn score: {self.current_player.turn_score}")
                print(f"Current total score: {self.current_player.score + self.current_player.turn_score}")
                decision = input("Do you want to roll again (r) or hold (h)? ")
                if decision == "h":
                    self.current_player.score += self.current_player.turn_score
                    self.current_player.turn_score = 0
                    print(f"{self.current_player.name}'s score is now {self.current_player.score}")
                    break
                elif decision != "r":
                    print("Invalid input. Please enter 'r' or 'h'.")

    def play(self):
        self.current_player = self.player1
        while not self.is_game_over():
            self.turn()
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1
        if time.time() - self.start_time > 60:
            print("Time is up!")
        print("Game over.")
        if self.player1.score >= self.target_score:
            print(f"{self.player1.name} wins!")
        else:
            print(f"{self.player2.name} wins!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--timed', action='store_true', help='Start a timed game')
    args = parser.parse_args()

    if args.timed:
        game = TimedGameProxy("Player 1", "Player 2")
    else:
        game = TwoPlayerGame("Player 1", "Player 2")
    game.play()