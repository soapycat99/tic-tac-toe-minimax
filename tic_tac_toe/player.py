import math
import random

class Player:
    def __init__(self,letter):
        #letter is x or o
        self.letter = letter
    def get_move(self,game):
        pass

class RandomComputerPlayer(Player):
    def __init__(self,letter):
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):

        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + " \'s turn. Input move (0-9):")
            try:
                val = int(square)
                if val not in game.available_moves():
                    print('Invalid move')
                    raise ValueError
            except ValueError:
                print('Invalid value. Try again')
            valid_square = True
        return val
class GeniusComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())
        else:
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter #yourself
        other_player = 'O' if player == 'X' else 'X' #the other player

        #first, check if the previous move is a winner
        #this is our base case
        if state.current_winner == other_player:
            #return position and socre because we need to keep strack fo the score
            #for minimax to work
            return {'position': None,
                'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                        state.num_empty_squares() + 1)
                    }
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        #initialize some dictionaries
        if player == max_player:
            best = {'position': None, 'score': -math.inf} #next score should be maximize hence it should be bigger initial score
        else:
            best = {'position': None, 'score': math.inf} #score should be minimize

        for possible_move in state.available_moves():
            #step 1: make a move, try that spot
            state.make_move(possible_move, player)
            #step 2: recurse using minimax to simulate a game after making that move
            sim_score = self.minimax(state, other_player)

            #step 3: undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            #step 4: update the dictionaries if neccesary
            if player == max_player: #maximize the max_player
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best