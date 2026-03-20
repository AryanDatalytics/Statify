import os
import requests
import datetime
import xml.etree.ElementTree as ET

# --- CONFIGURATION ---
USERNAME = "AryanDatalytics" # Apna exact username check kar lena
GITHUB_TOKEN = os.getenv("GH_TOKEN") # Security ke liye Secret use karenge

# --- DATA FETCHING (GraphQL) ---
def get_streak_from_history():
    # GraphQL Query to get contribution calendar for the last year
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
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    try:
        response = requests.post('https://api.github.com/graphql', 
                                 json={'query': query, 'variables': {'login': USERNAME}}, 
                                 headers=headers)
        
        if response.status_code != 200:
            print(f"❌ Error fetching data: {response.status_code}")
            return 0

        # Flatten the weeks into a list of daily counts
        data = response.json()['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
        days = [day for week in data for day in week['contributionDays']]
        days.reverse() # Start backwards from today

        streak = 0
        today = datetime.datetime.now().date()
        
        # Calculate current streak
        for day in days:
            date = datetime.datetime.strptime(day['date'], "%Y-%m-%d").date()
            
            # If it's today and 0 contributions, skip to yesterday to check if streak is alive
            if date == today and day['contributionCount'] == 0:
                continue
                
            if day['contributionCount'] > 0:
                streak += 1
            else:
                # Streak broken
                break
        
        return streak
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        return 0

# --- SVG DESIGN (Fire Icon with Streak Inside) ---
def generate_fire_streak_badge(streak):
    # Badge dimensions
    width = 250
    height = 35
    icon_size = 30 # Fire icon is slightly larger for impact

    # Colors: Deep orange/red for the fire theme
    fire_color = "#FF4500" 
    text_color = "white"

    # Minimalist fire icon path data (simplified flame shape)
    fire_path = "M12 2C10.9 2 10 2.9 10 4C10 4.6 10.2 5.1 10.5 5.5C8.9 6.2 8 7.9 8 10C8 12.2 9.8 14 12 14C14.2 14 16 12.2 16 10C16 7.9 15.1 6.2 13.5 5.5C13.8 5.1 14 4.6 14 4C14 2.9 13.1 2 12 2ZM12 4C12 4 12 4.1 12 4.1C12 4.1 12 4 12 4ZM12 8C13.1 8 14 8.9 14 10C14 11.1 13.1 12 12 12C10.9 12 10 11.1 10 10C10 8.9 10.9 8 12 8Z"

    # SVG string with embedded styles and animations
    svg_content = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="{width}" height="{height}" rx="4" fill="#1A1A1A"/>
  
  <g transform="translate(10, {(height - icon_size) / 2}) scale({icon_size / 24})">
    <path d="{fire_path}" fill="{fire_color}">
      <animate attributeName="opacity" values="1;0.6;1" dur="2s" repeatCount="indefinite" />
    </path>
    
    <text x="12" y="11" fill="white" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="6" font-weight="bold">
        {streak}
    </text>
  </g>
  
  <text x="45" y="22" fill="{text_color}" font-family="'Segoe UI', Arial, sans-serif" font-size="11" font-weight="bold" text-transform="uppercase">
    DAY FOCUS STREAK
  </text>
  
  <rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="3.5" stroke="white" stroke-opacity="0.05"/>
</svg>"""
    
    with open("aura.svg", "w", encoding='utf-8') as f:
        f.write(svg_content)

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    current_streak = get_streak_from_history()
    print(f"🔥 Current streak detected: {current_streak} days")
    generate_fire_streak_badge(current_streak)
    print("✅ Successfully generated fire streak badge (aura.svg)")
