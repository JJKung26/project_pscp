#=====================| worder |=====================
import random
import json
import os
from word  import WORDS_BY_LEVEL  #(แยกไฟล์คลังคำศัพท์)

#=================
filename = 'leaderboard.json' #ไฟล์เก็บคะแนน
#=================
def print_rules():#แสดงกฎกติกา
    print("\n" + "="*50)
    print("🎮 กฎกติกาเกม Worder 🎮")
    print("="*50)
    print("คุณต้องทายคำศัพท์ที่ซ่อนอยู่ให้ถูกต้อง")
    print("🟩 สีเขียว: ตัวอักษรถูกต้องและตำแหน่งถูกต้อง")
    print("🟨 สีเหลือง: ตัวอักษรถูกต้องแต่ตำแหน่งไม่ถูกต้อง")
    print("⬜ สีขาว: ไม่มีตัวอักษรนี้ในคำตอบ")
    print("\n📊 ระดับความยาก:")
    print("• Easy: ทาย 10 รอบ, เต็ม 5 คะแนน, ใบ้หมวดในหมู่รอบที่ 5")
    print("• Medium: ทาย 6 รอบ, เต็ม 10 คะแนน, ใบ้หมวดในหมู่รอบที่ 5 (เสีย 1 คะแนน)")
    print("• Hard: ทาย 6 รอบ, เต็ม 15 คะแนน, ไม่มีคำใบ้")
    print("="*50)

def leaderboard(name, score, win, lose):#ฟังก์ชันบันทึกคะแนนผู้เล่น
    '''บันทึกประวัติคะแนนผู้เล่น'''
    #ถ้าไม่มีไฟล์ก็สร้างใหม่
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([], f)

    #โหลดข้อมูลเก่า
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    #ตรวจสอบผู้เล่น
    found = False
    for player in data:
        if player['name'] == name:#อัพเดตคะแนนผู้เล่น
            player['score'] += score
            player['win'] += win
            player['lose'] += lose
            found = True
            break

    #ถ้าไม่มีผู้เล่นในไฟล์ก็เพิ่มผู้เล่นใหม่
    if not found:
        data.append({'name': name, 'score': score, 'win': win, 'lose': lose})

    # sort จากคะแนนมากไปน้อย
    data.sort(key=lambda x: x["score"], reverse=True)

    print("\n" + "=" * 60)
    # แสดง คะแนนรวมผู้เล่น
    current_player = next(p for p in data if p["name"] == name)#loopเพื่อหาข้อมูลผู้เล่นปัจจุบัน(กรณีที่เป็นผู้เล่นใหม่)
    print(f'🎯สรุปผลของ {name}: คะแนนรวม {current_player['score']} | win: {current_player['win']} | lose: {current_player['lose']}')
    print(f'🏅อันดับของคุณคือ {data.index(current_player) + 1} จาก {len(data)} คน')#แสดงอันดับของผู้เล่น

    # print leaderboard
    print("\n🏆 LEADERBOARD TOP 5 🏆".center(60))
    print("="*60)
    for i, player in enumerate(data[:5], start=1):# print top 5 ทีละคน
            print(f"{i}. {player['name']:<6} | Score: {player['score']:<6} \
| Win: {player['win']:<3} | Lose: {player['lose']:<3} | {player['win'] / (player['win'] + player['lose']) * 100 if (player['win'] + player['lose']) > 0 else 0:.1f}%")
    print('=' * 60)

    #เซฟข้อมูลกลับลงไฟล์
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def game_logic(answer, random_word):#logicเช็คคำตอบของเกม
    '''ฟังก์ชันตรวจคำถูกผิดของเกม'''
    SPACE = '-'
    answer_list = ['⬜'] * len(random_word)
    charecter_list = [f'{SPACE:^2}'] * len(random_word)
    char_list = list(random_word)

    for i in range(len(random_word)):#เช็คหาตำแหน่งตัวอักษรที่ถูกต้องและตำแหน่งถูกต้อง
        if answer[i] == random_word[i]:
            answer_list[i] = '🟩'
            charecter_list[i] = f'{random_word[i]:^2}'# แทนที่indexนั้นด้วยตัวอักษรที่ถูกต้องลงในcharecter_list
            char_list[i] = None #ลบตัวอักษรที่ถูกต้องออกจากanswer_list

    for i in range(len(random_word)):#เช็คหาตำแหน่งตัวอักษรที่ถูกต้องแต่ตำแหน่งไม่ถูกต้อง
        if answer_list[i] == '⬜' and answer[i] in char_list:
            answer_list[i] = '🟨'# แทนที่indexนั้นด้วยสีเหลือง
            charecter_list[i] = f'{answer[i]:^2}'# แทนที่indexนั้นด้วยตัวอักษรที่ถูกต้องลงในcharecter_list
            char_list[char_list.index(answer[i])] = None #ลบตัวอักษรที่ถูกต้องออกจากanswer_list

    return ''.join(answer_list),''.join(charecter_list)

def game_play(random_word, random_category, level,point_rate):#ฟังก์ชันเล่นเกม
    '''ฟังก์ชันเกม'''
    won = False #ค่าเริ่มต้น
    win = 0
    lose = 0
    player_round = 0 #จำนวนรอบเริ่มต้นของผู้เล่น
    player_point = 10 #คะแนนเริ่มต้นของผู้เล่น
    round_limit = 10 if level == 'easy' else 6 #กำหนดจำนวนรอบตามระดับความยาก

    print(f"\n🎯 เริ่มเกม! ทายคำ {len(random_word)} ตัวอักษร")
    print(f"📝 คุณมี {round_limit} รอบในการทาย")
    print(f"💎 ระดับ: {level.upper()}")

    # แสดงheaderของตาราง
    print(f"\n{'รอบ':<5} {'คำตอบ':<13} {'ผลลัพธ์'}")
    print("-" * 40)

    while player_round < round_limit:#ผู้เล่นทายได้ไม่เกิน6ครั้ง
        player_round += 1
        user_answer = input('ทายครั้งที่ {}: '.format(player_round)).upper() #รับคำตอบผู้เล่น
        if len(user_answer) != len(random_word) or not user_answer.isalpha():#เช็คความยาวคำตอบ
            print(f'❌ คำตอบต้องมีความยาว {len(random_word)} ตัวอักษร และต้องเป็นตัวอักษร A-Z เท่านั้น')
            player_round -= 1 #ถ้าไม่ตรงเงื่อนไขจะไม่ถูกนับเป็นรอบ
            continue
        answer, char_hint = game_logic(user_answer, random_word)
        print(f'{player_round:<6}|{user_answer:<13} | {answer} | {char_hint} |') #โชว์ผลการทาย
        if user_answer.upper() == random_word.upper():#เช็คว่าชนะทันทีหรือชนะในรอบนั้นๆหรือยัง
            won = True
            break#ถ้าชนะ ออกจากloop
        else:
            player_point = max(0, player_point - 1)  # ตอบผิดหัก 1 คะแนน กันไม่ให้ติดลบ

        if player_round == 5: #ถ้าถึงรอบที่5แล้ว
            print('-' * 40)
            if level == 'easy':#ถ้าโหมดง่าย
                print(f"💡 ใบ้: หมวดหมู่ '{random_category}'")#ใบ้หมวดหมู่
            if level == 'medium':
                while True:
                    user_input = input("💡 ต้องการใบ้หมวดหมู่ไหม? (แลกกับ 1 คะแนน) [yes/no]: ").lower()
                    if user_input not in ['yes', 'no']:
                        print("❌ กรุณาตอบ 'yes' หรือ 'no' เท่านั้น")
                        continue
                    if user_input == 'yes':
                        print(f'💡 ใบ้หมวดหมู่: {random_category}')
                        player_point = max(0, player_point - 1)  # แก้ไม่ให้ติดลบ
                    break  # ออกจากลูปไม่ว่าจะตอบ yes หรือ no
            print('-' * 40)

    print("-" * 40)
    if won is True:#ถ้าชนะ
        print('🎉 ยินดีด้วย! คุณทายถูก! 🎉')
        win += 1
    else:#ถ้าแพ้
        print('😔 เสียใจด้วย คุณทายไม่ถูก! 😔')
        player_point = 0 #ถ้าแพ้คะแนนเป็น0
        lose += 1

    print(f"🎯 เฉลยคือ: {random_word}")
    print(f"📂 หมวดหมู่: {random_category}")
    print(f"🎲 จำนวนรอบที่ทาย: {player_round}/{round_limit} รอบ")
    print(f"💰 คะแนนที่ได้: {player_point * point_rate[level]} คะแนน")

    return player_point,win,lose

def main():#รอไปก่อนเดี๋ยวมาทำ
    '''ฟังก์ชันหลัก'''
    print_rules()#เรียกใช้ฟังก์ชันแสดงกฎกติกา
    while True:
        while True:
            username = input("\n👤 กรุณาใส่ชื่อผู้เล่น: ").strip()
            if not username:
                print("❌ กรุณาใส่ชื่อผู้เล่น")
                continue
            break
        #=====สุ่มคำ=====
        ALL_CATEGORIES = list(WORDS_BY_LEVEL.keys())
        LEVEL_LIST = ["easy", "medium", "hard"]
        MULTIPLIER = {"easy": 0.5, "medium": 1, "hard": 1.5}
        #===============
        while True:
            level = input('\n⚡เลือกความยาก [easy, medium, hard] : ').lower()
            if level in LEVEL_LIST:
                random_category = random.choice(ALL_CATEGORIES)
                random_word = random.choice(WORDS_BY_LEVEL[random_category])
                break
            else:
                print("❌ ระดับความยากไม่ถูกต้อง กรุณาเลือกใหม่")

        userpoint, win, lose = game_play(random_word, random_category, level, MULTIPLIER)#เล่นเกม
        leaderboard(username, (userpoint * MULTIPLIER[level]), win, lose)#บันทึกชื่อและคะแนนผู้เล่น
        while True:
            again = input("\nอยากเล่นต่อมั้ย? [yes/no] : ").lower()
            if again in ['yes', 'no']:
                break
            else:
                print("❌ กรุณาตอบ 'yes' หรือ 'no' เท่านั้น")
        if again.lower() == 'yes':
            continue
        else:
            print("\n🙏จบเกมแล้วคับ ขอบคุณที่เล่น!🎮")
            break

if __name__ == "__main__":
    main()
