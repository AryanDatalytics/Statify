import datetime
import os
import requests

# GitHub Config
USERNAME = "AryanDatalytics" # Apna exact username check kar lena
GITHUB_TOKEN = os.getenv("GH_TOKEN") # Security ke liye Secret use karenge

def check_github_activity():
    url = f"https://api.github.com/users/{USERNAME}/events"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return False
        
    events = response.json()
    today = datetime.datetime.utcnow().date()
    
    for event in events:
        # Check if event happened today (UTC)
        event_date = datetime.datetime.strptime(event['created_at'], "%Y-%m-%dT%H:%M:%SZ").date()
        if event_date == today:
            # Commit, Star, PR, ya Issue creation sab count hoga
            return True
    return False

def update_streak(active_today):
    today = datetime.datetime.utcnow().date()
    streak_file = "streak.txt"
    streak = 15 # Aapka base streak yahan se shuru hoga

    if os.path.exists(streak_file):
        with open(streak_file, "r") as f:
            data = f.read().split(",")
            streak = int(data[0])
            last_date = datetime.datetime.strptime(data[1], "%Y-%m-%d").date()

        if last_date == today:
            return streak # Aaj ka update pehle hi ho gaya
            
        if active_today:
            if last_date == today - datetime.timedelta(days=1):
                streak += 1
            else:
                streak = 1 # Kal miss ho gaya tha
    
    with open(streak_file, "w") as f:
        f.write(f"{streak},{today}")
    return streak

def generate_svg(streak):
    color = "#FF4500" if streak > 10 else "#70FF9D"
    svg = f"""<svg width="250" height="28" xmlns="http://www.w3.org/2000/svg">
      <rect width="250" height="28" fill="#1A1A1A"/>
      <rect width="6" height="28" fill="{color}"/>
      <text x="20" y="18" fill="white" font-family="Arial" font-size="12" font-weight="bold">
        🔥 ACTIVITY STREAK: {streak} DAYS
      </text>
    </svg>"""
    with open("aura.svg", "w") as f:
        f.write(svg)

if __name__ == "__main__":
    is_active = check_github_activity()
    s = update_streak(is_active)
    generate_svg(s)
