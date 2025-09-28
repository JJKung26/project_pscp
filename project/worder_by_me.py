#=========|ระบบที่ต้องทำ|========
#ทำระบบเลือกโหมด(ง่าย กลาง ยาก)ทำแล้ว
#เซฟคะแนนผู้เล่น ทำแล้ว
#ทำleader bord
#ทำhint ทำแล้ว
#=================

import random
import json
import os
from word  import WORDS_BY_LEVEL, ALL_TITLES  #(แยกไฟล์คลังคำศัพท์)

#=================
filename = 'leaderboard.json' #ไฟล์เก็บคะแนน
#=============
def show_leaderboard():#ฟังก์ชันแสดงอันดับผู้เล่น
    '''ฟังก์ชันแสดงคะแนนผู้เล่น'''
    # โหลดข้อมูล
with open(filename, "r", encoding="utf-8") as f:
    data = json.load(f)

# sort จากคะแนนมากไปน้อย
data.sort(key=lambda x: x["score"], reverse=True)

# print leaderboard
print("===== Leaderboard =====")
for i, player in enumerate(data, start=1):
    print(f"{i}. {player['name']} | Score: {player['score']} | Win: {player['win']} | Lose: {player['lose']}")
print("=======================")

def leader_bord(name, score, win, lose):#ฟังก์ชันบันทึกคะแนนผู้เล่น
    '''บันทึกประวัติคะแนนผู้เล่น'''
    #ถ้าไม่มีไฟล์ก็สร้างใหม่
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([], f)
    #โหลดข้อมูลเก่า
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    #เตรวจสอบผู้เล่น
    found = False
    for player in data:
        if player['name'] == name:
            player['score'] += score #ถ้ามีผู้เล่นในไฟล์ก็เพิ่มคะแนน
            player['win'] += win
            player['lose'] += lose
            latest_score = player['score']
            latest_win = player['win']
            latest_lose = player['lose']
            found = True
            break
    #ถ้าไม่มีผู้เล่นในไฟล์ก็เพิ่มผู้เล่นใหม่
    if not found:
        data.append({'name': name, 'score': score, 'win': win, 'lose': lose})
        latest_score = score
        latest_win = data[-1].get('win', 0)
        latest_lose = data[-1].get('lose', 0)
    #โชว์คะแนนสะสมและwin lose
    win_lose = 'win:{} lose:{}'.format(latest_win, latest_lose)
    #เซฟ
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return win_lose, latest_score
#=================
def game_logic(answer, random_word):#logicเช็คคำตอบของเกม
    '''ฟังก์ชันตรวจคำถูกผิดของเกม'''
    SPACE = '-'
    answer_list = ['⬜'] * len(random_word)
    charecter_list = [f'{SPACE:^2}'] * len(random_word)
    char_list = list(random_word)

    for i in range(len(random_word)):#เช็คหาตำแหน่งตัวอักษรที่ถูกต้องและตำแหน่งถูกต้อง
        if answer[i] == random_word[i]:
            answer_list[i] = '🟩'
            charecter_list[i] = f'{random_word[i]:^2}'
            char_list[i] = None #ลบตัวอักษรที่ถูกต้องออกจากanswer_list

    for i in range(len(random_word)):#เช็คหาตำแหน่งตัวอักษรที่ถูกต้องแต่ตำแหน่งไม่ถูกต้อง
        if answer_list[i] == '⬜' and answer[i] in char_list:
            answer_list[i] = '🟨'
            charecter_list[i] = f'{answer[i]:^2}'
            char_list[char_list.index(answer[i])] = None #ลบตัวอักษรที่ถูกต้องออกจากanswer_list
    return ''.join(answer_list),''.join(charecter_list)

def game_play(random_word, random_category, level,point_rate):#ฟังก์ชันเล่นเกม
    '''ฟังก์ชันเกม'''

    won = False #ค่าเริ่มต้น
    win = 0
    lose = 0
    player_round = 0 #จำนวนรอบเริ่มต้นของผู้เล่น
    player_point = 10 #คะแนนเริ่มต้นของผู้เล่น
    if level == 'easy':#จำนวนรอบสูงสุด
        round_limit = 10
    else:
        round_limit = 6

    while player_round < round_limit:#ผู้เล่นทายได้ไม่เกิน6ครั้ง
        player_round += 1
        print(f'ทายรอบที่ {player_round}')
        user_answer = input().upper() #รับคำตอบผู้เล่น
        if len(user_answer) != len(random_word) or not user_answer.isalpha():#เช็คความยาวคำตอบ
            print(f'คำตอบต้องมีความยาว {len(random_word)} ตัวอักษร หรือ ต้องมีเป็นตัวอักษร A-Z กรุณาลองใหม่')
            player_round -= 1 #ถ้าความยาวไม่ตรงจะไม่ถูกนับเป็นรอบ
            continue
        answer, char_hint = game_logic(user_answer, random_word)
        print(answer, char_hint) #โชว์ผลการทาย
        if user_answer.upper() == random_word.upper():#เช็คว่าชนะทันทีหรือชนะในรอบนั้นๆหรือยัง
            won = True
            break
        else:
            player_point -= 1 #ตอบผิดลดคะแนน

        if player_round == 5: #ถ้าถึงรอบที่5แล้ว
            if level == 'easy':#ถ้าโหมดง่าย
                print(f'ใบ้หมวดหมู่: {random_category}')#ใบ้หมวดหมู่
            if level == 'medium':#ถ้าโหมดกลาง
                user_input = input('ต้องการใบ้หมวดหมู่ไหม? แต่แลกกับ 1 คะแนนนะ (yes/no) :')#ถามว่าต้องการใบ้ไหม
                if user_input.lower() == 'yes':#ถ้าตอบใช่
                    print(f'ใบ้หมวดหมู่: {random_category}')#ใบ้หมวดหมู่
                    player_point -= 1 #แลกกับ1คะแนน

    if won is True:#ถ้าชนะ
        print('\nคุณชนะรอบนี้! คำตอบคือ',end=' ')
        win += 1
    else:#ถ้าแพ้
        print('\nคุณแพ้รอบนี้! คำตอบคือ',end=' ')
        player_point = 0 #ถ้าแพ้คะแนนเป็น0
        lose += 1
    print(f"{random_word} คุณได้รับคะแนน {player_point * point_rate[level]} คะแนน")
    return player_point,win,lose

def main():#รอไปก่อนเดี๋ยวมาทำ
    '''ฟังก์ชันหลัก'''
    while True:
        username = input('กรุณาใส่ชื่อผู้เล่น: ')
        #=====สุ่มคำ=====
        ALL_CATEGORIES = ALL_TITLES
        LEVEL_LIST = ["easy", "medium", "hard"]
        MULTIPLIER = {"easy": 0.5, "medium": 1, "hard": 1.5}
        #===============
        while True:
            level = input('\nเลือกความยาก (easy, medium, hard): ').lower()
            if level in LEVEL_LIST:
                random_category = random.choice(ALL_CATEGORIES)
                random_word = random.choice(WORDS_BY_LEVEL[random_category])
                break
            else:
                print("ระดับความยากไม่ถูกต้อง กรุณาเลือกใหม่")
        #===============
        print(f'\nเฉลยสำหรับเช็คคือ {random_word}')#เอาใว้เช็คเฉยๆว่ามันรันได้และรันอ่ะไรมา

        userpoint, win, lose = game_play(random_word, random_category, level, MULTIPLIER)#เล่นเกม
        show_win_lose, total_point = leader_bord(username, (userpoint * MULTIPLIER[level]), win, lose)#บันทึกชื่อและคะแนนผู้เล่น
        print(f'คะแนนสะสมของคุณ {username} คือ {total_point} คะแนน ประวัติแพ้/ชนะ:{show_win_lose}')#โชว์คะแนนสะสมและ win lose
        show_leaderboard()#โชว์ตารางคะแนน
        if input("\nเล่นอีกไหม? (yes/no) ").lower() == 'yes':
            continue
        else:
            print("จบเกมแล้วคับ ขอบคุณที่เล่น!")
            break

if __name__ == "__main__":
    main()
