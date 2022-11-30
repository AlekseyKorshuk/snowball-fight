def game_loop(player1, player2, initial_num_balls=100, total_num_steps=60):
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

if __name__ == '__main__':
    pass
