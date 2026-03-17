import datetime

def generate_svg():
    # Get current hour in IST (UTC +5:30)
    # GitHub Actions run on UTC, so we adjust
    hour = (datetime.datetime.utcnow().hour + 5) % 24 
    
    # Determine Status and Color
    if 0 <= hour < 5:
        status, color = "Night Owl Mode", "#9D70FF"  # Purple
    elif 5 <= hour < 9:
        status, color = "Morning Ritual", "#FF9D70"  # Orange/Peach
    elif 9 <= hour < 18:
        status, color = "Deep Work", "#70FF9D"       # Green
    else:
        status, color = "Evening Flow", "#FFD700"    # Golden

    svg_content = f"""
    <svg width="200" height="40" viewBox="0 0 200 40" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect width="200" height="40" rx="20" fill="{color}" fill-opacity="0.1"/>
      <rect x="0.5" y="0.5" width="199" height="39" rx="19.5" stroke="{color}" stroke-opacity="0.3"/>
      <circle cx="20" cy="20" r="5" fill="{color}">
        <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite" />
      </circle>
      <text x="40" y="25" fill="{color}" style="font-family: Arial, sans-serif; font-size: 14px; font-weight: bold;">
        {status}
      </text>
    </svg>
    """
    
    with open("aura.svg", "w") as f:
        f.write(svg_content)

if __name__ == "__main__":
    generate_svg()