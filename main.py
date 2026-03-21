import os
import requests
import datetime

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
        data = r.json()['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
        days = [d for w in data for d in w['contributionDays']][::-1]
        streak = 0
        today = datetime.datetime.now().date()
        for d in days:
            dt = datetime.datetime.strptime(d['date'], "%Y-%m-%d").date()
            if dt == today and d['contributionCount'] == 0: continue
            if d['contributionCount'] > 0: streak += 1
            else: break
        return streak
    except: return 0

def generate_svg(streak):
    # NEON CIRCLE DESIGN
    size = 180
    svg = f"""<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="neon" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <circle cx="90" cy="95" r="70" stroke="#FF1E6D" stroke-width="6" fill="transparent" filter="url(#neon)"/>
  
  <g transform="translate(78, 5)" filter="url(#neon)">
    <path d="M12 22C16.4 22 20 18.4 20 14C20 8 12 2 12 2C12 2 4 8 4 14C4 18.4 7.6 22 12 22Z" fill="#FF1E6D" />
    <path d="M12 18C13.5 18 15 16.5 15 14.5C15 12.5 12 10 12 10C12 10 9 12.5 9 14.5C9 16.5 10.5 18 12 18Z" fill="#1A1A1A" />
  </g>

  <text x="90" y="115" fill="#FFD700" font-family="Arial Black, sans-serif" font-size="52" font-weight="900" text-anchor="middle" filter="url(#neon)">{streak}</text>
  
</svg>"""
    with open("aura.svg", "w") as f: f.write(svg)

if __name__ == "__main__":
    s = get_streak()
    generate_svg(s)
