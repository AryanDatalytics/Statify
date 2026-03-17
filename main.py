import datetime

def generate_svg():
    # 1. Handle Timezone (GitHub Actions use UTC, so we add 5.5 hours for IST)
    # 5 hours + 30 mins = 330 minutes
    now_utc = datetime.datetime.utcnow()
    ist_offset = datetime.timedelta(hours=5, minutes=30)
    now_ist = now_utc + ist_offset
    hour = now_ist.hour
    
    # 2. Define Status, Colors, and Labels based on your routine
    if 0 <= hour < 5:
        status, color = "NIGHT OWL", "#9D70FF"  # Deep Purple
    elif 5 <= hour < 9:
        status, color = "MORNING RITUAL", "#FF9D70"  # Soft Orange
    elif 9 <= hour < 18:
        status, color = "DEEP WORK", "#70FF9D"  # Neon Green
    elif 18 <= hour < 22:
        status, color = "EVENING FLOW", "#FFD700"  # Golden Hour
    else:
        status, color = "WINDING DOWN", "#FF4500"  # Sunset Red

    # 3. Create the SVG (Matches your sharp-edged Tech Stack badges)
    svg_content = f"""
    <svg width="180" height="28" viewBox="0 0 180 28" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect width="180" height="28" fill="#1A1A1A"/> 
      
      <rect width="6" height="28" fill="{color}"/>
      
      <circle cx="22" cy="14" r="4" fill="{color}">
        <animate attributeName="opacity" values="1;0.2;1" dur="1.5s" repeatCount="indefinite" />
      </circle>

      <text x="36" y="18" fill="white" style="font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 11px; font-weight: bold; text-transform: uppercase; letter-spacing: 1.2px;">
        AURA | {status}
      </text>
      
      <rect x="0.5" y="0.5" width="179" height="27" stroke="white" stroke-opacity="0.1"/>
    </svg>
    """
    
    # 4. Save the file
    with open("aura.svg", "w") as f:
        f.write(svg_content)
    print(f"Successfully generated aura.svg with status: {status}")

if __name__ == "__main__":
    generate_svg()
