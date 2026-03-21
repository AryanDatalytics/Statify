import os
import requests
import datetime

# --- CONFIGURATION ---
USERNAME = "AryanDatalytics"
TOKEN = os.getenv("GH_TOKEN")

def get_github_stats():
    # GraphQL Query to get all contribution data
    query = """
    query($login:String!) {
      user(login:$login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
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
            return 0, 0, 0
        
        data = r.json()['data']['user']['contributionsCollection']['contributionCalendar']
        total_contributions = data['totalContributions']
        days = [d for w in data['weeks'] for d in w['contributionDays']]
        
        # 1. Current Streak Logic
        current_streak = 0
        today = datetime.datetime.now().date()
        for d in reversed(days):
            dt = datetime.datetime.strptime(d['date'], "%Y-%m-%d").date()
            if dt == today and d['contributionCount'] == 0:
                continue
            if d['contributionCount'] > 0:
                current_streak += 1
            else:
                break
        
        # 2. Longest Streak Logic
        longest_streak = 0
        temp_streak = 0
        for d in days:
            if d['contributionCount'] > 0:
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            else:
                temp_streak = 0
                
        return total_contributions, current_streak, longest_streak
    except:
        return 0, 0, 0

def generate_svg(total, current, longest):
    width = 495
    height = 195
    
    svg = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="{width}" height="{height}" rx="8" fill="#0D1117" stroke="#30363D" stroke-width="1"/>
  
  <style>
    .header {{ font: 600 14px 'Segoe UI', Arial, sans-serif; fill: #58A6FF; }}
    .stat {{ font: 800 32px 'Segoe UI', Arial, sans-serif; fill: #FFFFFF; }}
    .streak-num {{ font: 800 36px 'Segoe UI', Arial, sans-serif; fill: #FFD700; }}
    .pink-text {{ font: 600 14px 'Segoe UI', Arial, sans-serif; fill: #FF1E6D; }}
  </style>

  <g transform="translate(0, 0)">
    <text x="82.5" y="80" text-anchor="middle" class="stat">{total}</text>
    <text x="82.5" y="115" text-anchor="middle" class="header">Total Contributions</text>
    <text x="82.5" y="140" text-anchor="middle" font-size="10" fill="#8B949E" font-family="Arial">Since Joining</text>
  </g>

  <line x1="165" y1="40" x2="165" y2="155" stroke="#30363D" stroke-width="1"/>

  <g transform="translate(165, 0)">
    <circle cx="82.5" cy="85" r="45" stroke="#FF1E6D" stroke-width="5" fill="none" opacity="0.8">
        <animate attributeName="stroke-opacity" values="0.8;0.4;0.8" dur="2s" repeatCount="indefinite" />
    </circle>
    <path d="M82.5 30C82.5 30 78 36 78 40C78 42.5 80 44.5 82.5 44.5C85 44.5 87 42.5 87 40C87 36 82.5 30 82.5 30Z" fill="#FF1E6D"/>
    
    <text x="82.5" y="98" text-anchor="middle" class="streak-num">{current}</text>
    <text x="82.5" y="150" text-anchor="middle" class="pink-text" style="font-weight:bold; letter-spacing:1px;">CURRENT STREAK</text>
  </g>

  <line x1="330" y1="40" x2="330" y2="155" stroke="#30363D" stroke-width="1"/>

  <g transform="translate(330, 0)">
    <text x="82.5" y="80" text-anchor="middle" class="stat">{longest}</text>
    <text x="82.5" y="115" text-anchor="middle" class="header">Longest Streak</text>
    <text x="82.5" y="140" text-anchor="middle" font-size="10" fill="#8B949E" font-family="Arial">Personal Best</text>
  </g>
</svg>"""

    with open("aura.svg", "w", encoding='utf-8') as f:
        f.write(svg)

if __name__ == "__main__":
    t, c, l = get_github_stats()
    generate_svg(t, c, l)
    print(f"✅ Card Updated: Total={t}, Current={c}, Longest={l}")
