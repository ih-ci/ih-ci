import requests
import datetime

# Config
username = "ih-ci"
max_mana = 1000  # Max yearly contribution = full mana
readme_path = "README.md"
marker_start = "<!-- MANA-START -->"
marker_end = "<!-- MANA-END -->"

# Get current year contributions
year = datetime.datetime.now().year
url = f"https://github-contributions-api.jogruber.de/v4/{username}?y={year}"
contrib = requests.get(url).json()

total = sum(day['count'] for week in contrib['contributions'] for day in week['contributionDays'])
percent = min(100, int((total / max_mana) * 100))
bar = "█" * (percent // 5) + "░" * (20 - (percent // 5))

mana_block = f"""
{marker_start}
🧙 Mana Gauge:  
`{bar}` — {percent}%

🧪 Current Power Level: {total} contributions this year  
🔋 Mana Tier: {"Grandmaster" if percent >= 100 else "Adept" if percent >= 50 else "Novice"}
{marker_end}
"""

# Inject into README
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

start = content.find(marker_start)
end = content.find(marker_end) + len(marker_end)
updated = content[:start] + mana_block + content[end:]

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(updated)
