# fingerbaseball

A simulator of the classic summer camp game "Finger Baseball", primed for machine learning

Finger Baseball closely follows the rules of baseball, with some simplifications.

At each point in the game, there is a batter and a pitcher, just like baseball. The batter and the pitcher each declare the four syllables "fin-ger-base-ball!", then flash a number of fingers between 1 and 5 (similar to Rock-Paper-Scissors).

If the numbers do not match, an out is recorded.

If the numbers do match, the batter gets a hit according to the numbers that were flashed. 1 means a single (batter and all runners advance one base), 2 a double (two bases), 3 a triple (three bases), 4 a home run (batter and all runners score), and 5 a grand slam (batter and all runners score, plus a bonus of three runs).

Other than that, the game follows the exact same structure of a baseball game: three outs per inning, nine innings per game (unless there is a tie).

Of course, there is strategy involved. The hitter wants to match numbers, and the pitcher wants to avoid matching numbers. If the numbers match, the hitter hopes the number if higher. The pitcher hopes it is lower.

Players want to remain unpredictable, but make an optimal play. The pitcher will naturally want to flash lower numbers more often, but may want to flash higher numbers on occasion to maintain unpredictability. The batter may want to play higher numbers more frequently, but may find that playing lower numbers with more frequency leads to more success of matching the pitcher's number (since the pitcher will, presumably, tend to play lower numbers).

This repo will start with a random initiation, laying the ground for future machine learning strategies. 
