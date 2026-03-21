import os
import requests
import datetime

# --- CONFIGURATION ---
USERNAME = "AryanDatalytics"
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
            return 0
        
        data = r.json()['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
        days = [d for w in data for d in w['contributionDays']]
        days.reverse() # Start from today and go back
        
        streak = 0
        today = datetime.datetime.now().date()
        
        for d in days:
            dt = datetime.datetime.strptime(d['date'], "%Y-%m-%d").date()
            # If today has 0, check from yesterday to keep streak alive
            if dt == today and d['contributionCount'] == 0:
                continue
            if d['contributionCount'] > 0:
                streak += 1
            else:
                break
        return streak
    except Exception as e:
        print(f"Error: {e}")
        return 0

def generate_svg(streak):
    size = 200
    # Aesthetic Design with Phoenix/Fire theme
    svg = f"""<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <linearGradient id="fireGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FF8C00;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#FF4500;stop-opacity:1" />
    </linearGradient>
  </defs>

  <circle cx="100" cy="100" r="90" fill="#0D0D0D" stroke="#FFD700" stroke-width="3" filter="url(#glow)"/>
  <circle cx="100" cy="100" r="82" fill="none" stroke="#FFD700" stroke-width="1" stroke-dasharray="5 3" opacity="0.4"/>

  <g transform="translate(65, 50) scale(3)">
    <path d="M12 22C16.4183 22 20 18.4183 20 14C20 8 12 2 12 2C12 2 4 8 4 14C4 18.4183 7.58172 22 12 22Z" fill="url(#fireGrad)">
        <animate attributeName="opacity" values="0.7;1;0.7" dur="2s" repeatCount="indefinite" />
    </path>
  </g>

  <text x="100" y="125" fill="white" font-family="Arial Black, sans-serif" font-size="42" font-weight="900" text-anchor="middle" filter="url(#glow)">{streak}</text>
  
  <text x="100" y="155" fill="#FFD700" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" style="letter-spacing:1px;">DAYS STREAK</text>
  
  <path id="curvePath" d="M 50,100 A 50,50 0 0,1 150,100" fill="transparent"/>
  <text style="font-family:Arial; font-size:10px; font-weight:bold; fill:#FFD700; text-transform:uppercase;">
    <textPath href="#curvePath" startOffset="50%" text-anchor="middle">GitHub Activity</textPath>
  </text>
</svg>"""

    with open("aura.svg", "w") as f:
        f.write(svg)

if __name__ == "__main__":
    current_streak = get_streak()
    generate_svg(current_streak)
    print(f"✅ Success! Streak: {current_streak}")
