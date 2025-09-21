#=========|ระบบที่ต้องทำ|========
#ทำระบบเลือกโหมด(ง่าย กลาง ยาก)
#เซฟคะแนนผู้เล่น
#ทำleader bord
#ทำhint
#ทำระบบเลือกความยาก
#เซฟคะแนนผู้เล่น

#=================

import random
import json
import os
from word import WORDS_BY_LEVEL  #(แยกไฟล์คลังคำศัพท์)
#=================
filename = 'leaderboard.json' #ไฟล์เก็บคะแนน
#=============
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
    #โชว์คะแนนสะสมและwin lose
    win_lose = 'win:{} lose:{}'.format(latest_win, latest_lose)
    #เซฟ
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return win_lose, latest_score
#=================
def game_logic(answer, random_word):#logicเช็คคำตอบของเกม
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

def game_play(random_word, random_category, level):
    '''ฟังก์ชันเกม'''

    won = False #ค่าเริ่มต้น
    win = 0
    lose = 0
    round_limit = 6 #จำนวนรอบสูงสุด
    player_round = 0 #จำนวนรอบเริ่มต้นของผู้เล่น
    player_point = 10 #คะแนนเริ่มต้นของผู้เล่น
    
    while player_round < round_limit:#ผู้เล่นทายได้ไม่เกิน6ครั้ง
        player_round += 1
        print(f'ทายรอบที่ {player_round} หากทายถูกในรอบนี้จะได้รับ {player_point} คะแนน')
        user_answer = input().upper()
        answer = game_logic(user_answer, random_word)
        print(f'ทายครั้งที่ {player_round}')
        print(answer)
        if user_answer.upper() == random_word.upper():#เช็คว่าชนะทันทีหรือชนะในรอบนั้นๆหรือยัง
            won = True
            break
        else:
            player_point -= 1 #ตอบผิดลดคะแนน

        if player_round == 5: #ถ้าถึงรอบที่5แล้ว
            if level == 'easy':#ถ้าโหมดง่าย
                print(f'ใบ้หมวดหมู่: {random_category}')#ใบ้หมวดหมู่
            if level == 'medium':#ถ้าโหมดกลาง
                user_input = input('ต้องการใบ้หมวดหมู่ไหม? แต่แลกกับ 1 คะแนนนะ (y/n)')#ถามว่าต้องการใบ้ไหม
                if user_input.lower() == 'y':#ถ้าตอบใช่
                    print(f'ใบ้หมวดหมู่: {random_category}')#ใบ้หมวดหมู่
                else:
                    pass

    if won is True:#ถ้าชนะ
        print(f'คุณชนะรอบนี้! คำตอบคือ',end=' ')
        win += 1
    else:#ถ้าแพ้
        print('คุณแพ้รอบนี้! คำตอบคือ',end=' ')
        player_point = 0 #ถ้าแพ้คะแนนเป็น0
        lose += 1
    print(f"{random_word} คุณได้รับคะแนน {player_point} คะแนน")
    return player_point,win,lose

def main():#รอไปก่อนเดี๋ยวมาทำ
    '''ฟังก์ชันหลัก'''
    while True:
        username = input('กรุณาใส่ชื่อผู้เล่น: ')
        #=====สุ่มคำ=====
        ALL_CATEGORIES = ["animals","fruits","tools","instruments","colors"]
        level = input('เลือกความยาก (easy, medium, hard): ').lower()
        random_category = random.choice(ALL_CATEGORIES)
        random_word = random.choice(WORDS_BY_LEVEL[level][random_category])
        #===============
        print(f'เฉลยสำหรับเช็คคือ {random_word}')#เอาใว้เช็คเฉยๆว่ามันรันได้และรันอ่ะไรมา

        userpoint, win, lose = game_play(random_word, random_category, level)
        show_win_lose, total_point = leader_bord(username, userpoint, win, lose)#บันทึกชื่อและคะแนนผู้เล่น
        print(f'คะแนนสะสมของคุณ {username} คือ {total_point} คะแนน ประวัติแพ้/ชนะ:{show_win_lose}')#โชว์คะแนนสะสมและ win lose
        if input("เล่นอีกไหม? (y/n) ").lower() == 'y':
            continue
        else:
            print("จบเกม ขอบคุณที่เล่น!")
            break

if __name__ == "__main__":
    main()
