import datetime
import os

def update_streak():
    # IST is UTC + 5.5
    today = (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).date()
    streak_file = "streak.txt"
    streak = 1
    
    if os.path.exists(streak_file):
        try:
            with open(streak_file, "r") as f:
                data = f.read().split(",")
                last_streak = int(data[0])
                last_date = datetime.datetime.strptime(data[1], "%Y-%m-%d").date()
                
                if last_date == today:
                    streak = last_streak
                elif last_date == today - datetime.timedelta(days=1):
                    streak = last_streak + 1
        except:
            streak = 1

    with open(streak_file, "w") as f:
        f.write(f"{streak},{today}")
    return streak

def generate_svg(streak):
    # Wider width (250) ensures text like "10 DAYS 🔥" never hits the wall
    width = 250
    color = "#70FF9D" # Neon Green
    
    svg_content = f"""<svg width="{width}" height="28" viewBox="0 0 {width} 28" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="{width}" height="28" fill="#1A1A1A"/> 
  <rect width="6" height="28" fill="{color}"/>
  <text x="20" y="18" fill="white" style="font-family: Arial, sans-serif; font-size: 12px; font-weight: bold; text-transform: uppercase;">
    STREAK: {streak} DAYS 🔥
  </text>
  <rect x="0.5" y="0.5" width="{width-1}" height="27" stroke="white" stroke-opacity="0.1"/>
</svg>"""

    with open("aura.svg", "w") as f:
        f.write(svg_content)

if __name__ == "__main__":
    s = update_streak()
    generate_svg(s)
