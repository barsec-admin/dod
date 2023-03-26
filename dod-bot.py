import time
import random
import re
from mastodon import Mastodon
from mastodon.errors import MastodonNotFoundError
import os

def load_since_id():
    if os.path.exists('since_id.txt'):
        with open('since_id.txt', 'r') as file:
            return int(file.read())
    else:
        return None

def save_since_id(since_id):
    with open('since_id.txt', 'w') as file:
        file.write(str(since_id))

# API setup
client_id = "client_id"
client_secret = "client_secret"
access_token = "access_token"
api_base_url = "api_base_url"

mastodon = Mastodon(
    client_id=client_id,
    client_secret=client_secret,
    access_token=access_token,
    api_base_url=api_base_url
)

# Game entities
class Character:
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense

class Monster:
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense

# Game mechanics
def create_character(name):
    health = 100
    attack = 10
    defense = 10
    return Character(name, health, attack, defense)

# Reset Player
def reset_player(player):
    player.health = 100
    player.attack = 10
    player.defense = 10

def combat(player, monster):
    player_damage = max(player.attack - monster.defense, 0)
    monster_damage = max(monster.attack - player.defense, 0)

    player.health -= monster_damage
    monster.health -= player_damage

    return player_damage, monster_damage

def set_attributes(player, content, user_acct, status):
    attributes = re.findall(r'!(\w+)\s+(\d+)', content)
    for attribute, value in attributes:
        value = int(value)
        if attribute.lower() == "health":
            player.health = value
        elif attribute.lower() == "attack":
            player.attack = value
        elif attribute.lower() == "defense":
            player.defense = value

    response = f"@{user_acct} Your character's attributes have been set to Health: {player.health}, Attack: {player.attack}, Defense: {player.defense}."
    mastodon.status_post(response, in_reply_to_id=status["id"], visibility=status["visibility"])

def perform_fight(player, monster, user_acct, status):
    player_damage, monster_damage = combat(player, monster)

    if player.health <= 0:
        response = f"@{user_acct} You have been defeated by the {monster.name}."
        mastodon.status_post(response, in_reply_to_id=status["id"], visibility=status["visibility"])
        reset_player(player)
    elif monster.health <= 0:
        response = f"@{user_acct} You have defeated the {monster.name}!"
        mastodon.status_post(response, in_reply_to_id=status["id"], visibility=status["visibility"])
        reset_player(player)
    else:
        response = f"@{user_acct} You dealt {player_damage} damage to the {monster.name}. The {monster.name} dealt {monster_damage} damage to you. Your health: {player.health}. Monster's health: {monster.health}."
        mastodon.status_post(response, in_reply_to_id=status["id"], visibility=status["visibility"])

def handle_mentions(active_players, monster):
    print("Checking for mentions...")
    since_id = load_since_id()
    last_processed_mention = {}
    while True:
        mentions = mastodon.notifications(since_id=since_id, limit=5, exclude_types=["follow", "favourite", "reblog"])

        if mentions:
            new_since_id = mentions[0]["id"]
            if since_id != new_since_id:
                since_id = new_since_id
                save_since_id(since_id)
                start_processed = False
                for mention in mentions:
                    user_acct = mention["status"]["account"]["acct"]
                    if user_acct not in last_processed_mention or mention["id"] != last_processed_mention[user_acct]:
                        last_processed_mention[user_acct] = mention["id"]
                        process_command(mention["status"], active_players, monster)

        time.sleep(45)

def process_command(status, active_players, monster):
    content = status["content"]
    user_acct = status["account"]["acct"]

    if user_acct not in active_players and "!start" not in content:
        return

    if "!start" in content:
        print("Start command detected")
        if user_acct not in active_players:
            active_players[user_acct] = create_character("Player")
            response = f"@{user_acct} Welcome to the game! Please choose your character's attributes by tooting: !health, !attack, and !defense followed by a number."
            print(f"Preparing to send response: {response}")
            try:
                mastodon.status_post(response, in_reply_to_id=status["id"], visibility=status["visibility"])
            except MastodonNotFoundError:
                print(f"Error: Status not found (ID: {status['id']})")
        return

    player = active_players[user_acct]

    commands_processed = set()
    # Process other commands here
    if "!health" in content or "!attack" in content or "!defense" in content:
        print("Attributes command detected")
        if "attributes" not in commands_processed:
            set_attributes(player, content, user_acct, status)
            commands_processed.add("attributes")
    if "!fight" in content:
        print("Fight command detected")
        if "fight" not in commands_processed:
            perform_fight(player, monster, user_acct, status)
            commands_processed.add("fight")
    if "!stop" in content:
        print("Stop command detected")
        if "stop" not in commands_processed:
            del active_players[user_acct]
            response = f"@{user_acct} You have been removed from the game."
            mastodon.status_post(response, in_reply_to_id=status["id"], visibility=status["visibility"])
            commands_processed.add("stop")

# Main game loop
if __name__ == "__main__":
    monster = Monster("Monster", 50, 8, 5)
    active_players = {}
    handle_mentions(active_players, monster)

