# dod

Be sure to change these for your instance:
# API setup
client_id = "client_id"

client_secret = "client_secret"

access_token = "access_token"

api_base_url = "https://yourinstance.com/"


In this text-based adventure game, you play as a character who encounters a monster and must choose actions to defeat it. The game is played through Mastodon, a social networking platform. Interactions with the game are performed by mentioning the game's account in your toots (posts) and using specific commands.

To start the game, mention the game's account with the following commands to set your character's initial attributes:

!health [value]: Sets your character's health points. Replace [value] with a positive integer (e.g., !health 100).
!attack [value]: Sets your character's attack points. Replace [value] with a positive integer (e.g., !attack 30).
!defense [value]: Sets your character's defense points. Replace [value] with a positive integer (e.g., !defense 20).
Once your character's attributes are set, the game proceeds to the combat phase, where you'll encounter a monster. The game will notify you of the monster's attributes: health, attack, and defense points.

During combat, you have three action choices:

!attack: Your character attacks the monster, dealing damage equal to your attack points minus the monster's defense points (minimum of 0 damage).
!defend: Your character defends, temporarily increasing their defense points by 5.
!heal: Your character heals, increasing their health points by 10.
To take an action, mention the game's account in a toot with the corresponding command (e.g., !attack). The game will then update you on the results of your action and the current state of your character and the monster.

The combat continues until either your character's health points reach 0 or the monster's health points reach 0. The game will notify you of the outcome, declaring a winner.

To play again, simply reset your character's attributes using the !health, !attack, and !defense commands as described earlier.

Remember to always mention the game's account when issuing commands so that the game can process your actions. Enjoy battling monsters in this Mastodon-based adventure game and become a legendary hero!
