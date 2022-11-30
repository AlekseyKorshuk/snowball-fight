from random import randint

import numpy as np
import multiprocessing as mp


def game_loop(player1, player2, initial_num_balls=100, total_num_steps=60):
    """
    Take two players as input and perform a game.

    :param player1: player1
    :param player2: player2
    :param initial_num_balls: number of balls for each player in the start of the game
    :param total_num_steps: number of steps in the game
    :return: payoffs of players in the end of the game
    """
    player1_num_balls = initial_num_balls
    player2_num_balls = initial_num_balls

    # Number of steps without player shooting
    player1_steps_no_shoot = 0
    player2_steps_no_shoot = 0

    # Number of balls which players shot to a destination on the previous step
    player1_to_player2_num_balls = 0
    player2_to_player1_num_balls = 0

    # Game loop. Last for an hour (60 minutes)
    for i in range(total_num_steps):
        # Snow generator machine generates a ball.
        player1_num_balls += 1
        player2_num_balls += 1
        # Players shoot to other fields

        # This temporary variable is required for correct simulation of the game
        # where we do not have order, i.e. players in each step move simultaneously
        player1_to_player2_num_balls_tmp = player1.shootToOpponentField(player2_to_player1_num_balls,
                                                                        player1_num_balls,
                                                                        player1_steps_no_shoot)

        player1_to_void_num_balls = player1.shootToHotField(player2_to_player1_num_balls,
                                                            player1_num_balls,
                                                            player1_steps_no_shoot)

        player2_to_player1_num_balls = player2.shootToOpponentField(player1_to_player2_num_balls,
                                                                    player2_num_balls,
                                                                    player2_steps_no_shoot)

        player2_to_void_num_balls = player2.shootToHotField(player1_to_player2_num_balls,
                                                            player2_num_balls,
                                                            player2_steps_no_shoot)

        # After we've used this variable as input to player2,
        # we reassign a new value to it
        player1_to_player2_num_balls = player1_to_player2_num_balls_tmp

        # Update amount of balls on each player's field
        player1_num_balls += player2_to_player1_num_balls - player1_to_player2_num_balls - player1_to_void_num_balls + 1
        player2_num_balls += player1_to_player2_num_balls - player2_to_player1_num_balls - player2_to_void_num_balls + 1

        # If a player shoots in this round - reset the cannon
        if player1_to_player2_num_balls != 0 or player1_to_void_num_balls != 0:
            player1_steps_no_shoot = 0
        if player2_to_player1_num_balls != 0 or player2_to_void_num_balls != 0:
            player2_steps_no_shoot = 0

        # Increment the number of steps without shooting
        player1_steps_no_shoot += 1
        player2_steps_no_shoot += 1

        # Log player choices and states
        print(
            f"Player1. to opponent: {player1_to_player2_num_balls}, to hotfield: {player1_to_void_num_balls}. Now {player1_num_balls} balls. \t")
        print(
            f"Player2. to opponent: {player2_to_player1_num_balls}, to hotfield: {player2_to_void_num_balls}. Now {player2_num_balls} balls. \t")

    return player1_num_balls, player2_num_balls


# Taken from https://www.geeksforgeeks.org/random-list-of-m-non-negative-integers-whose-sum-is-n/
def random_list_sums_to(list_size, list_sum):
    """
    Create a random list such that all elements sum to 'list_sum'.

    :param list_size: size of the list
    :param list_sum: elements of list should sum up to this number
    :return: random list
    """
    # Create an array of size m where
    # every element is initialized to 0
    arr = [0] * list_size

    # To make the sum of the final list as n
    for i in range(list_sum):
        # Increment any random element
        # from the array by 1
        arr[randint(0, list_sum) % list_size] += 1

    return arr


def replicate_each_player_n_times(player_types, player_nums):
    """
    Returns a list of players where 'player_types[i]' is replicated 'player_nums[i]' times.

    :param player_types: types of players
    :param player_nums: number of occurences of each player
    :return: list of players
    """
    players = []
    for player_num, player_type in zip(player_nums, player_types):
        players.extend([player_type() for _ in range(player_num)])

    return players


def player_pairs(players):
    """
    Return all possible pairs of players.

    :param players: list of players in all game.
    :return: (player1, player2)
    """

    for i in range(len(players)):
        for j in range(i + 1, len(players)):
            yield players[i], players[j]


def all_players_play(players, **kwargs):
    """
    Performs a play of the game between each pair of players.

    :param players: list of players
    :param kwargs: any parameters that should be passed to 'game_loop'
    :return: payoffs of players after each game
    """
    with mp.Pool(-1) as pool:
        results = pool.map(lambda x: game_loop(x[0], x[1], **kwargs), player_pairs(players))

    results = np.array(results).reshape((len(players), len(players), 2))

    return results


def generate_population(player_types: list, population_size=50):
    """
    Generate population of size 'population_size' with types of players 'player_types'.
    :param player_types:
    :param population_size:
    :return:
    """

    num_players = random_list_sums_to(len(player_types), population_size)
    players = replicate_each_player_n_times(player_types, num_players)

    return players


if __name__ == '__main__':
    player_types = []
    players = generate_population(player_types)
    results = all_players_play(players)

    print(results)
