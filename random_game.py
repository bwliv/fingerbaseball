# initial run of a random game
from util import Diamond, Game
from numpy.random import choice

options = [1,2,3,4,5]

game = Game()

print('Running sample game between a Home Team and an Away Teams...\n')

# run sample game
while not game.over:
    pitcher = choice(options)
    batter = choice(options)
    game.play(pitcher,batter)
    print(game)

n = 5000 # number of times to sample

print('\n\nSimulating {} games between Team A and Team B, randomly assigning home/away teams...\n'.format(n))

A_wins = 0
B_wins = 0

# simulate 10000 sample games
for i in range(n):

    # print game number if 10th of the way there:
    if i == 0 or (i+1) % (n//10) == 0 or i+1 == n:
        print('Simulating Game #' + str(i+1))

    # initialize and simulate game
    game = Game()
    A_home = choice([True,False]) # randomly choose if A is home team
    while not game.over:
        pitcher = choice(options)
        batter = choice(options)
        game.play(pitcher,batter)
    if A_home:
        if game.home_score > game.away_score: # if A won
            A_wins += 1
        else:
            B_wins += 1
    else:
        if game.away_score > game.home_score: # if A won
            A_wins += 1
        else:
            B_wins += 1

# show result
if A_wins > B_wins:
    print('\nA wins, {} to {}'.format(A_wins,B_wins))
elif B_wins > A_wins:
    print('\nB wins, {} to {}'.format(B_wins,A_wins))
else:
    print('\nTie at {}!'.format(A_wins))
