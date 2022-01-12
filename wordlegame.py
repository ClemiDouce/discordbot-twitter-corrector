from randomwordfr import RandomWordFr
rw = RandomWordFr()


game_list = []

class WordleGame:
    secret_word = ""
    found_letters = set()
    searched_letters = set()
    try_count = 0
    max_try = 3
    actual_state = ""
    ended = False

    def __init__(self):
        self.secret_word = self.get_random_word()
        self.actual_state = ''.join(["⬜️" for char in self.secret_word])

    def get_random_word(self):
        return rw.get()["word"]

    async def try_word(self, message, user_input):
        result = ""
        temp_char = self.secret_word
        for index, char in enumerate(user_input):
            if char == temp_char[index]:
                result += "🟩"
                # self.found_letters.add(char)
            elif temp_char.count(char) > 0:
                result += "🟨"
                temp_char = temp_char.replace(char, '.', 1)
            else:
                result += "⬜️"
                # self.searched_letters.add(char)
        if user_input == self.secret_word:
            result += "\n Bravo, vous avez trouvé le mot !"
            self.ended = True
        else:
            self.actual_state = result
            self.try_count += 1
            if self.try_count == self.max_try:
                result += f"\n C'était votre dernier essais, DOMMAGE. Le mot secret était {self.secret_word} "
                self.ended = True
            else:
                result += f"\nDommage, il vous reste {self.max_try - self.try_count} essais pour trouver le bon mot"
        await message.channel.send(result)

async def start_game(message):
    game = WordleGame()
    game_list.append(game)
    await message.channel.send(f"Une nouvelle partie a été commencé par {message.author.name}")

async def list_game(message):
    active_games = [game for game in game_list if game.ended == False]
    response = f"Il y a actuellement {len(active_games)} parties en cours :\n"
    for index, game in enumerate(active_games):
        response += f"[{index+1}] - {game.actual_state}\n"
    await message.channel.send(response)

async def play_game(message, index, user_input):
    if index <= 0 or index > len(game_list):
        await message.channel.send("Index incorrect")
        return
    game = game_list[index-1]
    if len(user_input) != len(game.secret_word):
        await message.channel.send(f"Votre mot a une taille incorrect. Le mot secret de ce jeu est de {len(game.secret_word)}")
    else:
        await game.try_word(message, user_input)
