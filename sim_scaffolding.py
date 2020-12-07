from util import Game
from numpy.random import choice
from numpy import cumsum, unique
import matplotlib.pyplot as plt

def play_game(p1,p2,last_game = None,first_team_home_last_game=True,echo=False):
    '''
    function that simulates a game between player1 and player 2
    p1 (Player): player 1
    p2 (Player): player 2
    last_game (Game): instance of last game to carry over
    first_team_home_last_game (bool): if player 1 was home last game (default to true)
    echo (bool): whether or not to print results of game
    '''

    # if no last game, use a default game (with no actions history) to bring in actions histories
    if last_game is None:
        last_game = Game()

    # set home team
    first_team_home = choice([True,False])

    if first_team_home:
        p1.home = True
        p2.home = False
    else:
        p1.home = False
        p2.home = True

    # initialize game, carrying over results of last game
    if first_team_home == first_team_home_last_game: # if same home team as last game
        game = Game(last_game.home_pitch_history,last_game.home_bat_history,last_game.away_pitch_history,last_game.away_bat_history)
    else: # if different home team, pull in histories in reverse, putting last
        game = Game(last_game.away_pitch_history,last_game.away_bat_history,last_game.home_pitch_history,last_game.home_bat_history)

    # play ball!
    while not game.over:

        # find out if player 1 is pitching
        p1_pitching = (p1.home and game.top) or (not p1.home and not game.top)

        # grab state of game
        state = game.state()

        # update policies of players (if necessary)
        p1.update(*state)
        p2.update(*state)

        # select actions
        pitcher = p1.move(*state) if p1_pitching else p2.move(*state)
        batter = p2.move(*state) if p1_pitching else p1.move(*state)

        game.play(pitcher,batter)

        # print game results if echo is turned on
        if echo:
            print(game)

    return game

def simulate_games(p1,p2,n_games = 1000,echo_first_game = False,plot=False):
    '''
    simulate games
    p1 (Player): player 1
    p2 (Player): player 2
    n_games (int): number of games to play
    echo_first_game (bool): show results of first game
    plot (bool): plot game results over time
    '''

    # initialize first game and counters

    p1_wins = []
    p2_wins = []
    p1_runs = []
    p2_runs = []
    innings = []

    print('{} vs. {}'.format(p1.name,p2.name))

    # simulate games
    for i in range(n_games):

        if i == 0 and echo_first_game: # first game with echo
            if p1.home:
                if p1.name != p2.name:
                    print(p1.name + ' is home team in first game. Showing first game then simulating the rest...\n')
                else:
                    print('First {} is home team in first game. Showing first game then simulating the rest...\n'.format(p1.name))
            else:
                if p1.name != p2.name:
                    print(p2.name + ' is home team in first game. Showing first game then simulating the rest...\n')
                else:
                    print('Second {} is home team in first game. Showing first game then simulating the rest...\n'.format(p1.name))
            game = play_game(p1,p2,last_game = Game(),echo=True)

        elif i == 0: # first game without echo
            print('Simulating games...')
            game = play_game(p1,p2,last_game = Game(),echo=False)

        else: # the rest of the games
            first_team_home_last = p1.home
            game = play_game(p1,p2,first_team_home_last_game=first_team_home_last,last_game=game)

        # summarize results of game
        if p1.home:
            if game.home_score > game.away_score:
                p1_wins.append(1)
                p2_wins.append(0)
            else:
                p2_wins.append(1)
                p1_wins.append(0)
            p1_runs.append(game.home_score)
            p2_runs.append(game.away_score)

        if p2.home:
            if game.home_score > game.away_score:
                p2_wins.append(1)
                p1_wins.append(0)
            else:
                p1_wins.append(1)
                p2_wins.append(0)
            p2_runs.append(game.home_score)
            p1_runs.append(game.away_score)

    # get full slate of actions for each actor
    p1_pitch_history = game.home_pitch_history if p1.home else game.away_pitch_history
    p1_bat_history = game.home_bat_history if p1.home else game.away_bat_history
    p2_pitch_history = game.home_pitch_history if p2.home else game.away_pitch_history
    p2_bat_history = game.home_bat_history if p2.home else game.away_bat_history

    p1_runs_history = cumsum(p1_runs)
    p2_runs_history = cumsum(p2_runs)
    p1_wins_history = cumsum(p1_wins)
    p2_wins_history = cumsum(p2_wins)

    if plot: # plot if outlined

        figsize = (14,4)
        xlab = 18
        ylab = 18
        title = 24
        xticks = 16
        yticks = 14

        # plot runs over time
        plt.figure(figsize=figsize)
        plt.xlabel('Game Number',size=xlab)
        plt.ylabel('Runs',size=ylab)
        if p1.name == p2.name:
            plt.title('{} vs. {}: Runs'.format(p1.name+' 1',p2.name+ ' 2'),size=title)
            plt.plot(p1_runs_history,label=p1.name + ' 1')
            plt.plot(p2_runs_history,label=p2.name + ' 2')
        else:
            plt.title('{} vs. {}: Runs'.format(p1.name,p2.name),size=title)
            plt.plot(p1_runs_history,label=p1.name)
            plt.plot(p2_runs_history,label=p2.name)
        plt.xticks(fontsize=xticks)
        plt.yticks(fontsize=yticks)
        plt.legend(fontsize='large')
        plt.show()

        # plot wins over time
        plt.figure(figsize=figsize)
        plt.xlabel('Game Number',size=xlab)
        plt.ylabel('Wins',size=ylab)
        if p1.name == p2.name:
            plt.title('{} vs. {}: Wins'.format(p1.name + ' 1',p2.name + ' 2'),size=title)
            plt.plot(p1_wins_history,label=p1.name + ' 1')
            plt.plot(p2_wins_history,label=p2.name + ' 2')
        else:
            plt.title('{} vs. {}: Wins'.format(p1.name,p2.name),size=title)
            plt.plot(p1_wins_history,label=p1.name)
            plt.plot(p2_wins_history,label=p2.name)
        plt.xticks(fontsize=xticks)
        plt.yticks(fontsize=yticks)
        plt.legend(fontsize='large')
        plt.show()

        # plot pitches for player 1
        plt.figure(figsize=figsize)
        arr, counts = unique(p1_pitch_history,return_counts=True)
        freqs = counts/sum(counts)
        plt.bar(arr,freqs)
        plt.xlabel('Finger Choice',size=xlab)
        plt.ylabel('Frequency',size=ylab)
        if p1.name == p2.name:
            plt.title('{} 1: Pitch Finger Frequency vs. {} 2'.format(p1.name,p2.name),size=title)
        else:
            plt.title('{}: Pitch Finger Frequency vs. {}'.format(p1.name,p2.name),size=title)
        plt.xticks(fontsize=xticks)
        plt.yticks(fontsize=yticks)
        plt.show()

        # plot hits for player 2
        plt.figure(figsize=figsize)
        arr, counts = unique(p2_bat_history,return_counts=True)
        freqs = counts/sum(counts)
        plt.bar(arr,freqs)
        plt.xlabel('Finger Choice',size=xlab)
        plt.ylabel('Frequency',size=ylab)
        if p1.name == p2.name:
            plt.title('{} 2: Bat Finger Frequency vs. {} 1'.format(p2.name, p1.name),size=title)
        else:
            plt.title('{}: Bat Finger Frequency vs. {}'.format(p2.name, p1.name),size=title)
        plt.xticks(fontsize=xticks)
        plt.yticks(fontsize=yticks)
        plt.show()

        # plot pitches for player 2
        plt.figure(figsize=figsize)
        arr, counts = unique(p2_pitch_history,return_counts=True)
        freqs = counts/sum(counts)
        plt.bar(arr,freqs)
        plt.xlabel('Finger Choice',size=xlab)
        plt.ylabel('Frequency',size=ylab)
        if p1.name == p2.name:
            plt.title('{} 2: Pitch Finger Frequency vs. {} 1'.format(p2.name,p1.name),size=title)
        else:
            plt.title('{}: Pitch Finger Frequency vs. {}'.format(p2.name,p1.name),size=title)
        plt.xticks(fontsize=xticks)
        plt.yticks(fontsize=yticks)
        plt.show()

        # plot hits for player 1
        plt.figure(figsize=figsize)
        arr, counts = unique(p1_bat_history,return_counts=True)
        freqs = counts/sum(counts)
        plt.bar(arr,freqs)
        plt.xlabel('Finger Choice',size=xlab)
        plt.ylabel('Frequency',size=ylab)
        if p1.name == p2.name:
            plt.title('{} 1: Bat Finger Frequency vs. {} 2'.format(p1.name,p2.name),size=title)
        else:
            plt.title('{}: Bat Finger Frequency vs. {}'.format(p1.name,p2.name),size=title)
        plt.xticks(fontsize=xticks)
        plt.yticks(fontsize=yticks)
        plt.show()


    return # can carry over these results to something else later
