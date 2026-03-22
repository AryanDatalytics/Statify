import os
import requests
import datetime

# --- CONFIGURATION ---
USERNAME = "AryanDatalytics"
TOKEN = os.getenv("GH_TOKEN")

def get_github_stats():
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
        r = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': {'login': USERNAME}}, headers=headers)
        data = r.json()['data']['user']['contributionsCollection']['contributionCalendar']
        total = data['totalContributions']
        days = [d for w in data['weeks'] for d in w['contributionDays']]
        
        # Streak Logic
        curr, maxi, temp = 0, 0, 0
        today = datetime.datetime.now().date()
        for d in reversed(days):
            dt = datetime.datetime.strptime(d['date'], "%Y-%m-%d").date()
            if dt == today and d['contributionCount'] == 0: continue
            if d['contributionCount'] > 0: curr += 1
            else: break
        for d in days:
            if d['contributionCount'] > 0:
                temp += 1
                maxi = max(maxi, temp)
            else: temp = 0
        return total, curr, maxi
    except: return 0, 0, 0

def generate_svg(total, current, longest):
    # FIXED BOX DIMENSIONS (495x195 as per standard cards)
    w, h = 495, 195
    svg = f"""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="{w}" height="{h}" rx="10" fill="#0D1117" stroke="#30363D" stroke-width="2"/>
  
  <style>
    .label {{ font: 600 14px 'Segoe UI', Arial; fill: #58A6FF; }}
    .val {{ font: 800 32px 'Segoe UI', Arial; fill: #FFFFFF; }}
    .streak-val {{ font: 800 38px 'Segoe UI', Arial; fill: #FFD700; }}
    .pink {{ font: 700 13px 'Segoe UI', Arial; fill: #FF1E6D; text-transform: uppercase; }}
  </style>

  <g transform="translate(0,0)">
    <text x="82" y="85" text-anchor="middle" class="val">{total}</text>
    <text x="82" y="120" text-anchor="middle" class="label">Total Contributions</text>
  </g>

  <line x1="165" y1="40" x2="165" y2="155" stroke="#30363D" />

  <g transform="translate(165,0)">
    <circle cx="82" cy="80" r="45" stroke="#FF1E6D" stroke-width="4" opacity="0.8" />
    <text x="82" y="92" text-anchor="middle" class="streak-val">{current}</text>
    <text x="82" y="145" text-anchor="middle" class="pink">Current Streak</text>
  </g>

  <line x1="330" y1="40" x2="330" y2="155" stroke="#30363D" />

  <g transform="translate(330,0)">
    <text x="82" y="85" text-anchor="middle" class="val">{longest}</text>
    <text x="82" y="120" text-anchor="middle" class="label">Longest Streak</text>
  </g>
</svg>"""
    with open("aura.svg", "w") as f: f.write(svg)

if __name__ == "__main__":
    t, c, l = get_github_stats()
    generate_svg(t, c, l)
