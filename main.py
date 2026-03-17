import datetime
import os

def update_streak():
    today = (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).date()
    streak_file = "streak.txt"
    streak = 0
    last_date = None

    # 1. Read existing streak data
    if os.path.exists(streak_file):
        with open(streak_file, "r") as f:
            data = f.read().split(",")
            streak = int(data[0])
            last_date = datetime.datetime.strptime(data[1], "%Y-%m-%d").date()

    # 2. Logic: If it's a new day, increment. If a day was missed, reset.
    if last_date == today:
        pass # Already updated today
    elif last_date == today - datetime.timedelta(days=1):
        streak += 1
    else:
        streak = 1 # Streak broken or starting new
    
    # 3. Save progress
    with open(streak_file, "w") as f:
        f.write(f"{streak},{today}")
    
    return streak

def generate_svg(streak):
    # Colors matching your aesthetic
    color = "#FFD700" if streak > 5 else "#70FF9D"
    
    svg_content = f"""
    <svg width="220" height="28" viewBox="0 0 220 28" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect width="220" height="28" fill="#1A1A1A"/> 
      <rect width="6" height="28" fill="{color}"/>
      <text x="15" y="18" fill="white" style="font-family: 'Segoe UI', sans-serif; font-size: 11px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;">
        FOCUS STREAK | {streak} DAYS 🔥
      </text>
    </svg>
    """
    with open("aura.svg", "w") as f:
        f.write(svg_content)

if __name__ == "__main__":
    current_streak = update_streak()
    generate_svg(current_streak)
