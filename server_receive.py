import random
import server_send
import pdb

# Rate at which move requests are dropped
REQUEST_DROP_RATE = 0.1
def create_request(conn, body, game, client_to_player):
    """Processes request to create a new player.

    Args: 
        conn: connection on which to send the message
        body: Encoded version of username.
        game: Game state to send to player. 
        client_to_player: Dictionary containing connections as
            keys and player objects as values.
    """
    username = body.decode('utf-8').strip()

    if username in game.players:
        server_send.general_failure(conn, 'This user already exists')
        return

    # Create new player
    player = game.spawn_player(username)
    client_to_player[conn] = player
    server_send.create_success(conn, username, game)
    print('New player successfully created')

def restart_request(conn, body, game, client_to_player):
    """Processes request to restart the game.

    Args: 
        conn: connection on which to send the message
        body: Not used. Argument left to keep consistency across
            server message handlers.
        game: Game state to send to player. 
        client_to_player: Dictionary containing connections as
            keys and player objects as values.
    """
    # Use username to double-check
    username = body.decode('utf-8')
    player = client_to_player[conn]
    assert player.username == username
    game.restart_player(player)


def move_request(conn, body, game, client_to_player):
    """Processes request to change a player's direction.

    Args: 
        conn: connection on which to send the message
        body: Encoded (utf-8) version of the player's move (char)
        game: Game state to send to player. 
        client_to_player: Dictionary containing connections as
            keys and player objects as values.
    """

    if random.random() < REQUEST_DROP_RATE:
        return
    move = body.decode('utf-8')
    player = client_to_player[conn]
    player.change_direction(move)
