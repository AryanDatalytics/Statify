import os
import requests
import datetime

# --- CONFIGURATION ---
USERNAME = "AryanDatalytics" # Check user in image_0.png
TOKEN = os.getenv("GH_TOKEN")

def get_streak():
    query = """
    query($login:String!) {
      user(login:$login) {
        contributionsCollection {
          contributionCalendar {
            weeks {
              contributionDays { contributionCount date }
            }
          }
        }
      }
    }
    """
    headers = {"Authorization": f"Bearer {TOKEN}"}
    try:
        r = requests.post('https://api.github.com/graphql', 
                         json={'query': query, 'variables': {'login': USERNAME}}, 
                         headers=headers)
        if r.status_code != 200:
            print(f"Error: API returned {r.status_code}")
            return 0
        
        data = r.json()['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
        days = [d for w in data for d in w['contributionDays']]
        days.reverse() # Today first
        
        streak = 0
        today = datetime.datetime.now().date()
        
        for d in days:
            dt = datetime.datetime.strptime(d['date'], "%Y-%m-%d").date()
            if dt == today and d['contributionCount'] == 0:
                continue
            if d['contributionCount'] > 0:
                streak += 1
            else:
                break
        return streak
    except Exception as e:
        print(f"Error details: {e}")
        return 0

def generate_svg(streak):
    size = 220 # Slightly bigger for more impact
    
    # Modern Minimal Design with subtle glow
    svg = f"""<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3.5" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <linearGradient id="gold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FFE066;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#C29900;stop-opacity:1" />
    </linearGradient>
  </defs>

  <circle cx="110" cy="110" r="100" fill="#121212" stroke="url(#gold)" stroke-width="4"/>
  
  <circle cx="110" cy="110" r="92" fill="none" stroke="#FFE066" stroke-width="1" stroke-dasharray="6 4" opacity="0.3"/>

  <g transform="translate(72, 58) scale(3.2)">
    <path d="M12 22C16.4 22 20 18.4 20 14C20 8 12 2 12 2C12 2 4 8 4 14C4 18.4 7.6 22 12 22Z" fill="#FF5500" filter="url(#glow)">
        <animate attributeName="opacity" values="0.8;1;0.8" dur="2.5s" repeatCount="indefinite" />
    </path>
    <path d="M12 18C14.2 18 16 16.2 16 14C16 11 12 8 12 8C12 8 8 11 8 14C8 16.2 9.8 18 12 18Z" fill="#FFAA00" />
  </g>

  <text x="110" y="135" fill="white" font-family="Arial Black, Impact, sans-serif" font-size="48" font-weight="900" text-anchor="middle" filter="url(#glow)">{streak}</text>
  
  <text x="110" y="165" fill="#FFE066" font-family="'Segoe UI', Arial, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" style="letter-spacing:1.5px;">DAYS STREAK</text>

</svg>"""

    with open("aura.svg", "w") as f:
        f.write(svg)

if __name__ == "__main__":
    current_streak = get_streak()
    generate_svg(current_streak)
    print(f"✅ Design updated. Streak: {current_streak}")
