import os
import requests
import datetime

# Config
USERNAME = "AryanDatalytics"
TOKEN = os.getenv("GH_TOKEN")

def get_streak():
    # GraphQL Query to get contribution calendar
    query = """
    query($login:String!) {
      user(login:$login) {
        contributionsCollection {
          contributionCalendar {
            weeks {
              contributionDays {
                contributionCount
                date
              }
            }
          }
        }
      }
    }
    """
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.post('https://api.github.com/graphql', 
                             json={'query': query, 'variables': {'login': USERNAME}}, 
                             headers=headers)
    
    if response.status_code != 200:
        return 0

    # Flatten the weeks into a list of daily counts
    data = response.json()['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
    days = [day for week in data for day in week['contributionDays']]
    days.reverse() # Start from today and go backwards

    streak = 0
    today = datetime.datetime.now().date()
    
    for day in days:
        date = datetime.datetime.strptime(day['date'], "%Y-%m-%d").date()
        # If it's today and 0, skip to yesterday to check the continuing streak
        if date == today and day['contributionCount'] == 0:
            continue
        if day['contributionCount'] > 0:
            streak += 1
        else:
            break
    return streak

def generate_svg(streak):
    # Same aesthetic as before, but with the REAL streak number
    width = 240
    color = "#FF4500" if streak > 10 else "#70FF9D"
    
    svg = f"""<svg width="{width}" height="28" viewBox="0 0 {width} 28" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect width="{width}" height="28" fill="#1A1A1A"/>
      <rect width="6" height="28" fill="{color}"/>
      <text x="20" y="18" fill="white" style="font-family: Arial, sans-serif; font-size: 11px; font-weight: bold; text-transform: uppercase;">
        🔥 REAL-TIME STREAK: {streak} DAYS
      </text>
    </svg>"""
    
    with open("aura.svg", "w") as f:
        f.write(svg)

if __name__ == "__main__":
    current_streak = get_streak()
    generate_svg(current_streak)
