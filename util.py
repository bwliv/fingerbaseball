from copy import deepcopy
from numpy.random import choice

class Diamond:
    '''
    class to store state of diamond, with methods for returning runs scored
    '''
    def __init__(self):
        '''
        initialize empty baseball diamond that will update based on each action
        '''
        self.first = False #first base
        self.second = False #second base
        self.third = False #third base
        self.scores = 0 # counter for scores

    def runs(self):
        '''
        clears "scores" counter and converts to runs, which are returned
        '''
        rns = deepcopy(self.scores)
        self.scores = 0
        return rns

    def single(self):
        '''
        if a player successfully hits a single, move the runners one base (altering diamond in place) and return number of runs scored
        '''
        if self.third:
            self.scores +=1
        if self.second:
            self.third = True
            self.second = False
        if self.first:
            self.second = True
            self.first = False
        self.first = True
        return self.runs() #calculate number of runs and clear "scores" counter

    def double(self):
        '''
        if a player successfully hits a double, move the runners two bases (altering diamond in place) and return number of runs scored
        '''
        if self.third:
            self.scores += 1
            self.third = False
        if self.second:
            self.scores +=1
        if self.first:
            self.third = True
            self.first = False
        self.second = True
        return self.runs() #calculate number of runs and clear "scores" counter

    def triple(self):
        '''
        if a player successfully hits a triple, move the runners three bases (altering diamond in place) and return number of runs scored
        '''
        if self.third:
            self.scores += 1
        if self.second:
            self.scores += 1
            self.second = False
        if self.first:
            self.scores += 1
            self.second = False
        self.third = True
        return self.runs() #calculate number of runs and clear "scores" counter

    def home_run(self):
        '''
        if a player successfully hits a home run, all the runners (and the hitter) score
        '''
        self.scores = 1 + self.third + self.second + self.first
        self.third = False
        self.second = False
        self.first = False
        return self.runs()

    def grand_slam(self):
        '''
        if a player successfully hits a grand slam, all the runners (and the hitter) score, plus a bonus of three runs
        '''
        self.scores = 4 + self.third + self.second + self.first
        self.third = False
        self.second = False
        self.first = False
        return self.runs()

    def clear(self):
        '''
        clear the diamond at the end of an inning
        '''
        self.third = False
        self.second = False
        self.first = False


class Game:
    '''
    Tracks the state of a game
    '''
    def __init__(self,home_pitch_history = None, home_bat_history= None,away_pitch_history = None,away_bat_history= None):
        '''
        begin a game
        '''
        self.inning = 1
        self.outs = 0
        self.top = True
        self.away_score = 0
        self.home_score = 0
        self.diamond = Diamond()
        self.over = False # if game is over
        self.last_act = None
        self.play_number = 1
        self.home_pitch_history = [] if home_pitch_history is None else home_pitch_history
        self.home_bat_history = [] if home_bat_history is None else home_bat_history
        self.away_pitch_history = [] if away_pitch_history is None else away_pitch_history
        self.away_bat_history = [] if away_bat_history is None else away_bat_history

    def inning_to_string(self):
        '''
        converts inning to a string representation
        '''
        if self.inning % 10 == 1 and self.inning % 100 != 11:
            inn = str(self.inning) + 'st'
        elif self.inning % 10 == 2 and self.inning % 100 != 12:
            inn = str(self.inning) + 'nd'
        elif self.inning % 10 == 3 and self.inning % 100 != 13:
            inn = str(self.inning) + 'rd'
        else:
            inn = str(self.inning) + 'th'
        return inn

    def __str__(self):
        '''
        return string representation of state
        '''

        tp = 'Top' if self.top else 'Bottom'
        tm = 'Away Team' if self.top else 'Home Team'

        inn = self.inning_to_string()

        if self.diamond.first == self.diamond.second == self.diamond.third == False:
            runners = "with no runners on"
        else:
            runners = "with runner(s) on"
            if self.diamond.first:
                runners += ' 1st'
            if self.diamond.second:
                runners += ' 2nd'
            if self.diamond.third:
                runners += ' 3rd'

        if self.away_score > self.home_score:
            res = "{act} for {tm}! Away {aw}, Home {hs} with {outs} outs in the {tp} of the {inn}, {rnrs}".format(act=self.last_act,tm=tm,aw=self.away_score,hs=self.home_score,outs=self.outs,tp=tp,inn=inn,rnrs = runners)
        else:
            res = "{act} for {tm}! Home {hs}, Away {aw} with {outs} outs in the {tp} of the {inn}, {rnrs}".format(act=self.last_act,tm=tm,aw=self.away_score,hs=self.home_score,outs=self.outs,tp=tp,inn=inn,rnrs = runners)

        if self.over: # if game is over, show the final score too
            if self.home_score > self.away_score: # home team won
                res += '\n\nGame Over! Home team wins {}-{}'.format(self.home_score,self.away_score)
            else: # home team lost
                res += '\n\nGame Over! Away team wins {}-{}'.format(self.away_score,self.home_score)

        return res

    def state(self):
        '''
        return current state of game to inform player
        '''
        return self.inning,self.top,self.outs,self.home_score,self.away_score,self.diamond,self.play_number,self.home_pitch_history,self.home_bat_history,self.away_pitch_history,self.away_bat_history

    def play(self,pitch,bat):
        '''
        run a play of the game
        pitch (int): number flashed by pitching team
        bat (int): number flashed by batting team
        '''

        if self.top: # if top of the inning

            # append to actions histories
            self.home_pitch_history.append(pitch)
            self.away_bat_history.append(bat)

            if pitch == bat == 1:
                self.away_score += self.diamond.single()
                self.last_act = 'Single'
            elif pitch == bat == 2:
                self.away_score += self.diamond.double()
                self.last_act = 'Double'
            elif pitch == bat == 3:
                self.away_score += self.diamond.triple()
                self.last_act = 'Triple'
            elif pitch == bat == 4:
                self.away_score += self.diamond.home_run()
                self.last_act = 'Home Run'
            elif pitch == bat == 5:
                self.away_score += self.diamond.grand_slam()
                self.last_act = 'Grand Slam'

            else: # if numbers do not match
                self.last_act = 'Out'

                self.outs +=1 # record an out
                if self.outs == 3: # end the half inning
                    if self.inning == 9 and self.home_score > self.away_score: #edge case where home team is leading after top of 9th, and thus no need for bottom of ninth
                        self.over = True
                    else:
                        self.top = False
                        self.outs = 0
                        self.diamond.clear()

        else: # if bottom of the inning

            # append to actions histories
            self.home_bat_history.append(bat)
            self.away_pitch_history.append(pitch)

            if pitch == bat == 1:
                self.home_score += self.diamond.single()
                self.last_act = 'Single'
                if self.inning >= 9 and self.home_score > self.away_score: # walk off, game is over
                    self.over = True

            elif pitch == bat == 2:
                self.home_score += self.diamond.double()
                self.last_act = 'Double'

                if self.inning >= 9 and self.home_score > self.away_score: # walk off, game is over
                    self.over = True

            elif pitch == bat == 3:
                self.home_score += self.diamond.triple()
                self.last_act = 'Triple'

                if self.inning >= 9 and self.home_score > self.away_score: # walk off, game is over
                    self.over = True

            elif pitch == bat == 4:
                self.home_score += self.diamond.home_run()
                self.last_act = 'Home Run'

                if self.inning >= 9 and self.home_score > self.away_score: # walk off, game is over
                    self.over = True

            elif pitch == bat == 5:
                self.home_score += self.diamond.grand_slam()
                self.last_act = 'Grand Slam'

                if self.inning >= 9 and self.home_score > self.away_score: # walk off, game is over
                    self.over = True

            else: # if numbers do not match
                self.last_act = 'Out'
                self.outs +=1 # record an out

                if self.outs == 3: # end the half inning
                    if self.inning < 9 or self.away_score == self.home_score: # if not 9th inning or game is tied, continue game by moving to next inning

                        self.top = True
                        self.outs = 0
                        self.diamond.clear()
                        self.inning += 1

                    else: #end the game
                        self.over = True

        # increment the play number
        self.play_number += 1
