import random
import json
import os

# ----------------------- คลังคำ (หมวดคงเดิม) + จัดระดับความยาก -----------------------
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

# ----------------------- ค่าคงที่ -----------------------
ATTEMPTS_FIXED = 6
LEADERBOARD_FILE = "leaderboard.json"

# ======================= (1) โหลดลีดเดอร์บอร์ด =======================
def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return {"players": {}}
    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"players": {}}

# ======================= (2) เซฟลีดเดอร์บอร์ด =======================
def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ======================= (3) สุ่มคำตามความยาก =======================
def pick_answer(diff: str):
    cats = [c for c in ALL_CATEGORIES if len(WORDS_BY_LEVEL[diff].get(c, [])) > 0]
    if not cats:
        raise ValueError(f"No words configured for difficulty '{diff}'")
    category = random.choice(cats)
    answer = random.choice(WORDS_BY_LEVEL[diff][category]).upper()
    return answer, category

# ======================= (4) ให้สีแบบ custom =======================
def feedback(answer: str, guess: str) -> str:
    """
    กติกา custom:
    - ตรงตำแหน่ง = เขียว (🟩)
    - ไม่ตรงตำแหน่ง แต่ 'ตัวอักษรมีอยู่ในคำตอบ' = เหลือง (🟨) ไม่จำกัดจำนวน
    - ไม่อยู่ในคำตอบเลย = ขาว (⬜)
    """
    n = len(answer)
    res = [""] * n

    # pass 1: เขียวก่อน
    for i in range(n):
        if guess[i] == answer[i]:
            res[i] = "🟩"

    set_in_answer = set(answer)

    # pass 2: เหลือง/ขาว
    for i in range(n):
        if res[i] == "🟩":
            continue
        res[i] = "🟨" if guess[i] in set_in_answer else "⬜"

    return "".join(res)

# ======================= (5) เล่นหนึ่งรอบและบันทึกผล =======================
def play_one_round(diff: str, name: str, lb: dict) -> tuple[bool, int]:
    """เล่น 1 รอบ: คืนค่า (แพ้ไหม, คะแนนรอบนี้). ถ้าแพ้ = True."""
    attempts_allowed = ATTEMPTS_FIXED
    answer, category = pick_answer(diff)
    word_len = len(answer)

    print(f"\n🕹️ รอบใหม่! โหมด: {diff.upper()} | หมวด(สุ่ม): {category} | คำยาว {word_len} | โอกาส: {attempts_allowed}")
    print("🟩 ตรงตำแหน่ง | 🟨 มีตัวนี้ในคำตอบ (กี่ตัวก็เหลือง) | ⬜ ไม่มีตัวนี้")
    print("ℹ️ เดาความยาวไม่ตรง → ‘ไม่ตัดรอบ’ | เหลือ 1 ครั้งสุดท้าย → ใบ้หมวด")

    won = False
    attempts_used = 0
    used_hint = False

    while attempts_used < attempts_allowed:
        guess = input(f"\nครั้งที่ {attempts_used+1}/{attempts_allowed} - ป้อนคำ: ").upper().strip()

        if len(guess) != word_len:
            print(f"⚠️ ต้องเป็นคำ {word_len} ตัวอักษร  ลองใหม่!")
            continue

        attempts_used += 1
        print(feedback(answer, guess))

        if guess == answer:
            print("🎉 เก่งมาก! ทายถูก")
            won = True
            break

        remaining = attempts_allowed - attempts_used
        if remaining == 1 and not used_hint:
            print(f"💡 HINT: หมวดของคำนี้คือ ➜ {category.upper()}")
            used_hint = True

    if not won:
        print(f"💥 แพ้รอบนี้! คำตอบคือ: {answer}  (หมวด: {category})")

    # คิดคะแนน (คูณตามความยาก) — ไม่มีเวลา/โซนเวลา
    mult = {"easy": 1.0, "medium": 1.4, "hard": 1.8}[diff]
    score = int(((attempts_allowed - attempts_used + 1) * 10) * mult) if won else 0

    # อัปเดต leaderboard + ประวัติ (ตัด date/เวลา/last_play ออกทั้งหมด)
    p = lb["players"].get(name, {
        "best_score": 0,
        "total_score": 0,
        "games": 0,
        "history": []
    })

    p["history"].append({
        "difficulty": diff,
        "category": category,
        "answer": answer,
        "attempts_allowed": attempts_allowed,
        "attempts_used": attempts_used,
        "won": won,
        "used_hint": used_hint,
        "score": score
    })

    p["games"] += 1
    p["total_score"] += score
    p["best_score"] = max(p["best_score"], score)

    lb["players"][name] = p
    save_leaderboard(lb)

    print(f"\n📊 สรุปรอบนี้ | {'ชนะ' if won else 'แพ้'} | ใช้ {attempts_used}/{attempts_allowed} ครั้ง | แต้ม {score}")
    print(f"➡️ รวมสะสมใน leaderboard: total {p['total_score']} | best {p['best_score']}")

    return (not won), score  # แพ้ไหม, คะแนนรอบนี้

# ======================= (6) main: คุม session ทั้งหมด =======================
def main():
    print("🎮 WORDLE+ (เล่นต่อเนื่อง; attempts = 6 | ยาวไม่ตรง ‘ไม่นับรอบ’ | รอบสุดท้ายมี HINT | สีเหลืองไม่จำกัด)")
    lb = load_leaderboard()

    name = input("ใส่ชื่อผู้เล่น (ใช้ชื่อเดิมเพื่อเก็บคะแนนต่อ/อัปเดต best): ").strip() or "Player"

    while True:
        diff = input("เลือกระดับความยาก (easy / medium / hard): ").strip().lower()
        if diff in WORDS_BY_LEVEL:
            break
        print("⚠️ พิมพ์แค่ easy / medium / hard นะ")

    # วนเล่นทีละรอบใน session เดียว
    session_round = 0
    session_points = 0
    while True:
        session_round += 1
        print(f"\n========== ROUND {session_round} | SESSION POINTS: {session_points} ==========")
        lost, got = play_one_round(diff, name, lb)
        session_points += got

        if lost:
            print(f"\n🟥 คุณแพ้รอบล่าสุด | SESSION POINTS ก่อนรีเซ็ต: {session_points}")
            cont = input("อยากเล่นต่อไหม? (y = ต่อ / n = หยุด): ").strip().lower()
            if cont == "y":
                session_points = 0
                session_round = 0
                print("🔄 เริ่ม session ใหม่! คะแนน session ถูกรีเซ็ตเป็น 0 (leaderboard ไม่เปลี่ยน)")
                continue
            else:
                print("\n🛑 จบเกม — ขอบคุณที่เล่น! (leaderboard ถูกบันทึกตามรอบที่ผ่านมาแล้ว)")
                break

        cont = input("\n✅ ชนะรอบนี้! เล่นต่อไหม? (y = ต่อ / n = หยุด): ").strip().lower()
        if cont != "y":
            print("\n🟦 จบเกมตามคำสั่ง — คะแนนใน leaderboard ถูกบันทึกตามรอบที่ผ่านมาแล้ว")
            break

    # โชว์ LEADERBOARD (ตัด last_play ออก)
    print("\n🏆 LEADER BOARD (Top 10 โดย Best Score)")
    players = []
    for name_, info in lb.get("players", {}).items():
        players.append({
            "name": name_,
            "best_score": info.get("best_score", 0),
            "total_score": info.get("total_score", 0),
            "games": info.get("games", 0),
        })
    players.sort(key=lambda x: (x["best_score"], x["total_score"]), reverse=True)
    for idx, p in enumerate(players[:10], start=1):
        print(f"{idx:>2}. {p['name']:<12} | best: {p['best_score']:>4} | total: {p['total_score']:>4} | games: {p['games']:>2}")

    print("\n💾 คะแนนถูกบันทึกใน 'leaderboard.json' — รอบหน้าพิมพ์ชื่อเดิมเพื่อเล่นต่อได้เลย 😉")

if __name__ == "__main__":
    main()