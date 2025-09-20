#ทำleader bord
#ทำhint
#ทำระบบเลือกความยาก
#เซฟคะแนนผู้เล่น

#=================

import random
from word import WORDS_BY_LEVEL  #(แยกไฟล์คลังคำศัพท์)


#=============
def leader_bord():
    '''บันทึกประวัติคะแนนผู้เล่น'''
    pass


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
    round_limit = 6#จำนวนรอบสูงสุด
    player_round = 0#จำนวนรอบเริ่มต้นของผู้เล่น
    player_point = 10#คะแนนเริ่มต้นของผู้เล่น
    
    while player_round < round_limit:#ผู้เล่นทายได้ไม่เกิน6ครั้ง
        player_round += 1
        user_answer = input().upper()
        answer = game_logic(user_answer, random_word)
        print(f'ทายครั้งที่ {player_round}')
        print(answer)
        if user_answer.upper() == random_word.upper():#เช็คว่าชนะทันทีหรือชนะในรอบนั้นๆหรือยัง
            won = True
            break
        else:
            player_point -= 1#ตอบผิดลดคะแนน

        if player_round == 5:#ถ้าถึงรอบที่5แล้ว
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

    else:#ถ้าแพ้
        print('คุณแพ้รอบนี้! คำตอบคือ',end=' ')
        player_point = 0 #ถ้าแพ้คะแนนเป็น0
    print(f"{random_word} คุณได้รับคะแนน {player_point} คะแนน")

def main():#รอไปก่อนเดี๋ยวมาทำ
    '''ฟังก์ชันหลัก'''
#==========|ระบบที่ต้องทำ|========
    #เลือกโหมด
    #สุ่มคำ
    #เล่นเกม
    #บันทึกคะแนน
    #โชว์leader bord
#===============================
    while True:
        #=====สุ่มคำ=====
        ALL_CATEGORIES = ["animals","fruits","tools","instruments","colors"]
        level = 'easy'
        random_category = random.choice(ALL_CATEGORIES)
        random_word = random.choice(WORDS_BY_LEVEL[level][random_category])
        #===============
        print(random_word)#เอาใว้เช็คเฉยๆว่ามันรันได้และรันอ่ะไรมา
        
        game_play(random_word, random_category, level)
        if input("เล่นอีกไหม? (y/n) ").lower() == 'y':
            continue
        else:
            print("จบเกม ขอบคุณที่เล่น!")
            break

if __name__ == "__main__":
    main()
