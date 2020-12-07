from numpy.random import choice
from numpy import unique, array, argsort, multiply, sqrt, select

class Player():
    '''
    base class for player, which takes random actions by default
    '''
    def __init__(self,home=None):
        '''
        creates a player instance
        home (bool): if the player is the home team
        '''
        self.home = home
        self.options = [1,2,3,4,5] # default options for plays
        self.name = 'Random Player'

    def update(self,inning,top,outs,home_score,away_score,diamond,play_number,home_pitch_history,home_bat_history,away_pitch_history,away_bat_history):
        '''
        method for updating a player's strategy using the state from the game
        '''
        pass

    def move(self,inning,top,outs,home_score,away_score,diamond,play_number,home_pitch_history,home_bat_history,away_pitch_history,away_bat_history):
        '''
        method for deciding a move based on the current state of the game
        '''
        chosen = choice(self.options)

        return chosen

class ConservativePlayer(Player):
    '''
    player which tends to throw out lower numbers when pitching and higher numbers when batting
    '''
    def __init__(self,home=None):
        '''
        creates an instance
        home (bool): if the player is the home team
        '''
        self.home = home
        self.options = [1,2,3,4,5] # default options for plays
        self.name = 'Conservative Player'
        self.pitching_probs = [0.35,0.25,0.2,0.15,0.05] # pick lower numbers more often when pitching
        self.batting_probs = self.pitching_probs[::-1] # reverse this distribution when batting

    def move(self,inning,top,outs,home_score,away_score,diamond,play_number,home_pitch_history,home_bat_history,away_pitch_history,away_bat_history):
        '''
        method for deciding a move based on the current state of the game
        '''

        if (self.home and top) or (not self.home and not top): # if pitching
            chosen = choice(self.options,p=self.pitching_probs)

        else: # if batting
            chosen = choice(self.options,p=self.batting_probs)

        return chosen

class CalculatedPlayer(Player):

    '''
    player that forms a distribution on moves from what the other team has done in the last (up to) 500 moves
    '''
    def __init__(self,home=None):
        '''
        creates an instance
        home (bool): if the player is the home team
        '''
        self.home = home
        self.options = [1,2,3,4,5] # default options for plays
        self.name = 'Calculated Player'

    def move(self,inning,top,outs,home_score,away_score,diamond,play_number,home_pitch_history,home_bat_history,away_pitch_history,away_bat_history):
        '''
        method for deciding a move based on forming a distribution based on the opponent's last 500 moves (or fewer if opponent has fewer than 500 moves)
        '''

        # generate actions history based on situtation, only if there is an appropriate history
        if self.home and top:
            opponent_history = away_bat_history
        elif self.home and not top:
            opponent_history = away_pitch_history
        elif not self.home and top:
            opponent_history = home_pitch_history
        else:
            opponent_history = home_bat_history

        pitching = (self.home and top) or (not self.home and not top) # true if pitching

        # note - speedup or lookback window lengthening (beyond 500 moves) could occur efficiently by not re-initializing this list every time (and only appending the newest action to a tracked history), but this would have required more game tracking overhead that would have limited readability
        # form policy only if opponent history is not empty:
        if opponent_history != []:

            arr, counts = unique(opponent_history[-500:],return_counts=True)  # get count of each opponent activity

            if not pitching:  # if batting try to match opponent
                probs = counts / sum(counts)

            else: #if pitching try to avoid opponent

                if sorted(arr) == [1,2,3,4,5]: # if all numbers considered so far, "reverse" distribution
                    probs = counts / sum(counts)
                    probs_index = argsort(probs) # get argsort of probability indices
                    probs[probs_index] = probs[probs_index[::-1]] # swap largest probability with smallest and second largest probability with second smallest

                else: # if not all numbers have been played, just randomly pick a number that hasn't been played yet and skip the rest
                    chosen = choice([i+1 for i in range(5) if i+1 not in arr])
                    return chosen

        else:
            arr = self.options
            probs = [0.2 for i in range(5)]

        # make choice of action
        chosen = choice(arr,p=probs)

        return chosen

class OnesAndTwos(Player):
    '''
    player that never plays anything other than 1 and 2 when pitching, but still picks fully randomly when hitting
    '''
    def __init__(self,home=None):
        '''
        creates an instance
        home (bool): if the player is the home team
        '''
        self.home = home
        self.name = "1's & 2's Only Player"

    def move(self,inning,top,outs,home_score,away_score,diamond,play_number,home_pitch_history,home_bat_history,away_pitch_history,away_bat_history):
        '''
        method for deciding a finger chosen randomly between 1 and 2 only if pitching
        '''

        if (self.home and top) or (not self.home and not top): # if pitching
            options = [1,2]
        else:
            options = [1,2,3,4,5]

        chosen = choice(options)
        return chosen

class ExpectedValuePlayer(Player):
    '''
    player that calculates expected value of each move and acts accordingly
    '''
    def __init__(self,home=None):
        '''
        creates an instance
        home (bool): if the player is the home team
        '''
        self.home = home
        self.name = "Expected Value Player"
        self.options = [1,2,3,4,5]
        self.values = [0.25,0.5,0.75,0]

    def move(self,inning,top,outs,home_score,away_score,diamond,play_number,home_pitch_history,home_bat_history,away_pitch_history,away_bat_history):
        '''
        method for deciding a move based on expected value
        '''

        # generate actions history based on situtation, only if there is an appropriate history
        if self.home and top:
            opponent_history = away_bat_history
        elif self.home and not top:
            opponent_history = away_pitch_history
        elif not self.home and top:
            opponent_history = home_pitch_history
        else:
            opponent_history = home_bat_history

        pitching = (self.home and top) or (not self.home and not top) # true if pitching

        # note - speedup or lookback window lengthening (beyond 500 moves) could occur efficiently by not re-initializing this list every time (and only appending the newest action to a tracked history), but this would have required more game tracking overhead that would have limited readability
        # form policy only if opponent history is not empty:
        if opponent_history != []:

            arr, counts = unique(opponent_history[-500:],return_counts=True)  # get count of each opponent activity

            if not pitching:  # if batting try to match opponent
                temp_vals = select([arr==i+1 for i in range(5)],[arr*.25,arr*.5,arr*.75,arr*1,arr*4])
                values = temp_vals ** (1/2)#TODO adjust this
                probs = values / sum(values)

            else: #if pitching try to avoid opponent

                if sorted(arr) == [1,2,3,4,5]: # if all numbers considered so far, "reverse" distribution
                    '''
                    temp_vals = select([arr==i+1 for i in range(5)],[arr*.25,arr*.5,arr*.75,arr*1,arr*4])
                    temp_vals_2 = (-1) * (temp_vals ** (1/1000))
                    probs_index = argsort(probs) # get argsort of probability indices
                    probs[probs_index] = probs[probs_index[::-1]] # swap largest probability with smallest and second largest probability with second smallest
                    '''
                    temp_vals = select([arr==i+1 for i in range(5)],[arr*.25,arr*.5,arr*.75,arr*1,arr*4])
                    values = temp_vals ** (1/2) #TODO adjust this
                    probs = values / sum(values)
                    probs_index = argsort(probs) # get argsort of probability indices
                    probs[probs_index] = probs[probs_index[::-1]] # swap largest probability with smallest and second largest probability with second smallest

                else: # if not all numbers have been played, just randomly pick a number that hasn't been played yet and skip the rest
                    chosen = choice([i+1 for i in range(5) if i+1 not in arr])
                    return chosen

        else: # choose randomly
            arr = self.options
            probs = [0.2 for i in range(5)]


        # make choice of action
        chosen = choice(arr,p=probs)

        return chosen
