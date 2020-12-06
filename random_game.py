from util import Diamond, Game, Player
from numpy.random import choice

options = [1,2,3,4,5]

game = Game()

while not game.over:
    pitcher = choice(options)
    batter = choice(options)
    game.play(pitcher,batter)
    print(game)
