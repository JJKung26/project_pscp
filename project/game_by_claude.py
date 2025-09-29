import random
import json
import os

# คลังคำศัพท์
WORDS_BY_LEVEL = {
    "animals": ["PANDA", "SHEEP", "HORSE", "GOOSE", "EAGLE", "ZEBRA", "WHALE","HIPPO", "RHINO", "SNAIL", "HYENA", "SHARK", "SLOTH"],
    "fruits":  ["APPLE", "MANGO", "GRAPE", "LEMON", "PEACH", "MELON", "OLIVE", "BERRY", "GUAVA", "PLUMS", "COCOA"],
    "objects": ["TABLE", "CHAIR", "PHONE", "CLOCK", "KNIFE", "PENCIL", "GLASS", "PLATE", "RADIO", "SPOON", "BRUSH", "PAPER", "SOFAS"],
    "instruments": ["AUDIO", "PIANO", "MUSIC", "SOUND", "DRUMS", "STAGE", "DANCE", "ALBUM", "RHYME", "REMIX", "MIXER", "OPERA", "BANDS"],
    "colors":  ["GREEN", "BLACK", "BROWN", "WHITE", "CREAM", "LEMON", "PEACH", "BEIGE", "AZURE", "AMBER"],
    "body_parts": ["HEART", "BRAIN", "TOOTH", "KNEES", "ELBOW", "THUMB", "WRIST", "ANKLE", "LIVER", "SPINE"],
    "food": ["PIZZA", "CANDY", "SALAD", "SUSHI", "HONEY", "STEAK", "CREAM", "JUICE", "SAUCE", "PASTA", "TOAST", "SUGAR", "WATER", "BREAD"],
    "countries": ["JAPAN", "CHINA", "INDIA", "EGYPT", "PARIS", "SPAIN", "KOREA", "NEPAL", "DUBAI", "QATAR", "CHILE", "MILAN"],
    "jobs": ["NURSE", "PILOT", "GUARD", "MINER", "ACTOR", "AGENT", "COACH"],
    "sports": ["CHESS", "RUGBY", "SKATE", "SWIMS", "GOLFS", "SAILS"],
    "nature": ["RIVER", "OCEAN", "BEACH", "STORM", "CLOUD", "STONE", "RAINY", "WINDS", "FLAME", "ROCKS", "MOUNT", "FLORA"],
    "time": ["MONTH", "HOURS", "EARLY", "NIGHT", "DATES", "EVENT", "LATER"],
    "emotions": ["HAPPY", "ANGRY", "PROUD", "SCARE", "SORRY", "WORRY", "RELAX", "SHOCK", "GLORY"],
    "music": ["PIANO", "GUITAR", "SAXON", "TRUMP", "BASSO", "CELLO", "FLUTE", "DRUMS", "VOICE", "CHORD", "NOTES", "LYRIC", "SCALE", "OPERA"]
}

ALL_TITLES = list(WORDS_BY_LEVEL.keys())
filename = 'leaderboard.json'

def print_rules():
    """แสดงกฎกติกาของเกม"""
    print("\n" + "="*50)
    print("🎮 กฎกติกาเกม Wordle 🎮")
    print("="*50)
    print("🟩 สีเขียว: ตัวอักษรถูกต้องและตำแหน่งถูกต้อง")
    print("🟨 สีเหลือง: ตัวอักษรถูกต้องแต่ตำแหน่งไม่ถูกต้อง")
    print("⬜ สีขาว: ไม่มีตัวอักษรนี้ในคำตอบ")
    print("\n📊 ระดับความยาก:")
    print("• Easy: 10 รอบ, คะแนน x0.5, ใบ้หมวดหมู่รอบที่ 5")
    print("• Medium: 6 รอบ, คะแนน x1.0, ใบ้หมวดหมู่รอบที่ 5 (เสียคะแนน)")
    print("• Hard: 6 รอบ, คะแนน x1.5, ไม่มีใบ้")
    print("="*50)

def leader_board(name, score, win, lose):
    """บันทึกประวัติคะแนนผู้เล่น"""
    # สร้างไฟล์ใหม่ถ้าไม่มี
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([], f)
    
    # โหลดข้อมูลเก่า
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # ตรวจสอบผู้เล่น
    found = False
    for player in data:
        if player['name'] == name:
            player['score'] += score
            player['win'] += win
            player['lose'] += lose
            latest_score = player['score']
            latest_win = player['win']
            latest_lose = player['lose']
            found = True
            break
    
    # เพิ่มผู้เล่นใหม่ถ้าไม่มี
    if not found:
        data.append({'name': name, 'score': score, 'win': win, 'lose': lose})
        latest_score = score
        latest_win = win
        latest_lose = lose
    
    # เรียงลำดับคะแนนจากมากไปน้อย
    data.sort(key=lambda x: x["score"], reverse=True)
    
    # แสดง Leaderboard
    print("\n" + "="*60)
    print("🏆 LEADERBOARD TOP 5 🏆".center(60))
    print("="*60)
    print(f"{'อันดับ':<8} {'ชื่อ':<15} {'คะแนน':<10} {'ชนะ':<8} {'แพ้':<8}")
    print("-"*60)
    
    for i, player in enumerate(data[:5], start=1):
        win_rate = round((player['win'] / (player['win'] + player['lose']) * 100), 1) if (player['win'] + player['lose']) > 0 else 0
        print(f"{i:<8} {player['name']:<15} {player['score']:<10} {player['win']:<8} {player['lose']:<8} ({win_rate}%)")
    
    print("="*60)
    
    # บันทึกข้อมูล
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return f"W:{latest_win} L:{latest_lose}", latest_score

def game_logic(answer, random_word):
    """ตรวจสอบคำตอบและแสดงผลแบบ Wordle"""
    SPACE = '-'
    answer_list = ['⬜'] * len(random_word)
    character_list = [f'{SPACE:^3}'] * len(random_word)
    char_list = list(random_word)
    
    # เช็คตำแหน่งที่ถูกต้อง (เขียว)
    for i in range(len(random_word)):
        if answer[i] == random_word[i]:
            answer_list[i] = '🟩'
            character_list[i] = f'{random_word[i]:^3}'
            char_list[i] = None
    
    # เช็คตัวอักษรที่มีแต่ตำแหน่งผิด (เหลือง)
    for i in range(len(random_word)):
        if answer_list[i] == '⬜' and answer[i] in char_list:
            answer_list[i] = '🟨'
            character_list[i] = f'{answer[i]:^3}'
            char_list[char_list.index(answer[i])] = None
    
    return ''.join(answer_list), ''.join(character_list)

def game_play(random_word, random_category, level, point_rate):
    """ฟังก์ชันเกมหลัก"""
    won = False
    win = 0
    lose = 0
    player_round = 0
    player_point = 10
    
    # กำหนดจำนวนรอบตามระดับ
    round_limit = 10 if level == 'easy' else 6
    
    print(f"\n🎯 เริ่มเกม! ทายคำ {len(random_word)} ตัวอักษร")
    print(f"📝 คุณมี {round_limit} รอบในการทาย")
    print(f"💎 ระดับ: {level.upper()}")
    
    # แสดงตาราง header
    print(f"\n{'รอบ':<5} {'คำตอบ':<15} {'ผลลัพธ์'}")
    print("-" * 40)
    
    while player_round < round_limit:
        player_round += 1
        user_answer = input(f"{player_round:>2}. > ").upper().strip()
        
        # ตรวจสอบความถูกต้องของ input
        if len(user_answer) != len(random_word):
            print(f"❌ คำตอบต้องมี {len(random_word)} ตัวอักษร กรุณาลองใหม่")
            player_round -= 1
            continue
            
        if not user_answer.isalpha():
            print("❌ ต้องเป็นตัวอักษร A-Z เท่านั้น กรุณาลองใหม่")
            player_round -= 1
            continue
        
        # ตรวจสอบคำตอบ
        answer, char_hint = game_logic(user_answer, random_word)
        print(f"    {user_answer:<15} {answer}")
        print(f"    {char_hint}")
        
        if user_answer == random_word:
            won = True
            break
        else:
            player_point -= 1
        
        # ให้คำใบ้ในรอบที่ 5
        if player_round == 5:
            if level == 'easy':
                print(f"💡 ใบ้: หมวดหมู่ '{random_category}'")
            elif level == 'medium':
                hint_choice = input("💡 ต้องการใบ้หมวดหมู่ไหม? (แลกกับ 1 คะแนน) [y/n]: ").lower()
                if hint_choice in ['y', 'yes']:
                    print(f"💡 ใบ้: หมวดหมู่ '{random_category}'")
                    player_point = max(0, player_point - 1)
    
    # แสดงผลลัพธ์
    print("\n" + "="*50)
    if won:
        print("🎉 ยินดีด้วย! คุณทายถูก! 🎉")
        win = 1
        final_score = int(player_point * point_rate[level])
    else:
        print("😔 เสียใจด้วย คุณทายไม่ถูก")
        lose = 1
        player_point = 0
        final_score = 0
    
    print(f"✅ คำตอบคือ: {random_word}")
    print(f"📂 หมวดหมู่: {random_category}")
    print(f"🎯 รอบที่ทาย: {player_round}/{round_limit}")
    print(f"💰 คะแนนที่ได้: {final_score}")
    print("="*50)
    
    return player_point, win, lose

def main():
    """ฟังก์ชันหลัก"""
    print("🎮 ยินดีต้อนรับสู่เกม WORDLE 🎮")
    
    while True:
        print_rules()
        username = input("\n👤 กรุณาใส่ชื่อผู้เล่น: ").strip()
        
        if not username:
            print("❌ กรุณาใส่ชื่อผู้เล่น")
            continue
        
        # ตั้งค่าเกม
        LEVEL_LIST = ["easy", "medium", "hard"]
        MULTIPLIER = {"easy": 0.5, "medium": 1, "hard": 1.5}
        
        # เลือกระดับความยาก
        while True:
            level = input('\n⚡ เลือกความยาก (easy/medium/hard): ').lower().strip()
            if level in LEVEL_LIST:
                break
            else:
                print("❌ กรุณาเลือก easy, medium หรือ hard")
        
        # สุ่มคำและหมวดหมู่
        random_category = random.choice(ALL_TITLES)
        random_word = random.choice(WORDS_BY_LEVEL[random_category])
        
        # เล่นเกม
        userpoint, win, lose = game_play(random_word, random_category, level, MULTIPLIER)
        
        # บันทึกคะแนน
        win_lose_record, total_point = leader_board(username, int(userpoint * MULTIPLIER[level]), win, lose)
        
        print(f"\n📊 สถิติของ {username}:")
        print(f"💎 คะแนนสะสม: {total_point} คะแนน")
        print(f"📈 สถิติ: {win_lose_record}")
        
        # ถามเล่นต่อ
        if input("\n🔄 เล่นอีกรอบไหม? [y/n]: ").lower() not in ['y', 'yes']:
            print("\n🙏 ขอบคุณที่เล่น! แล้วเจอกันใหม่! 🎮")
            break

if __name__ == "__main__":
    main()
