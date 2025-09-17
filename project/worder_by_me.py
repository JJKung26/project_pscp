import random
#=================
WORDS_BY_LEVEL = {
    "easy": {
        "animals": ["PANDA", "SHEEP", "HORSE", "GOOSE", "EAGLE", "ZEBRA", "WHALE"],
        "fruits":  ["APPLE", "MANGO", "GRAPE", "LEMON", "PEACH"],
        "tools":   ["RULER", "PHONE", "BOOKS", "TABLE"],
        "instruments": ["AUDIO", "PIANO", "MUSIC", "SOUND", "DRUMS"],
        "colors":  ["GREEN", "BLACK", "BROWN", "WHITE"]
    },
    "medium": {
        "animals": ["HIPPO", "RHINO", "SNAIL"],
        "fruits":  ["MELON", "OLIVE", "BERRY", "GUAVA"],
        "tools":   ["PAPER", "SPOON", "CLOCK"],
        "instruments": ["STAGE", "DANCE", "ALBUM"],
        "colors":  ["CREAM", "LEMON", "PEACH"]
    },
    "hard": {
        "animals": ["HYENA", "SHARK", "SLOTH"],
        "fruits":  ["PLUMS", "COCOA"],
        "tools":   ["BRUSH", "PLATE", "DOLLS"],
        "instruments": ["RHYME", "REMIX", "MIXER", "OPERA", "BANDS"],
        "colors":  ["BEIGE", "AZURE", "AMBER"]
    }
}

ALL_CATEGORIES = ["animals","fruits","tools","instruments","colors"]
#========|random word|=========
level = 'easy'
random_category = random.choice(ALL_CATEGORIES)
random_word = random.choice(WORDS_BY_LEVEL[level][random_category])
#=============
print(random_word)




def game_logic(answer, random_word):
    '''ฟังก์ชันตรวจคำถูกผิดของเกม'''
    answer_liist = []
    for i in range(len(random_word)):
        if answer[i] == random_word[i]:
            answer_liist.append('🟩')
        elif answer[i] in random_word:
            answer_liist.append('🟨')
        else:
            answer_liist.append('⬜')
    return ''.join(answer_liist)

def one_play():
    '''ฟังก์ชันเกมในหนึ่งรอบ'''
    won = False
    round_limit = 6
    player_round = 0
    while player_round < round_limit:
        player_round += 1
        user_answer = input().upper()
        answer = game_logic(user_answer, random_word)
        print(f'ทายครั้งที่ {player_round}')
        print(answer)
        if user_answer.upper() == random_word.upper():
            won = True
            break

    if won is True:
        print(f'คุณชนะรอบนี้! คำตอบคือ',end=' ')
    else:
        print('คุณแพ้รอบนี้! คำตอบคือ',end=' ')
    print(random_word)

def main():
    '''ฟังก์ชันหลัก'''
    pass

if __name__ == "__main__":
    one_play()
