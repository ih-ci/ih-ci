import requests
import datetime

# === Config ===
username = "ih-ci"
max_mana = 1000  # Full bar at 1000 contributions
readme_path = "README.md"
marker_start = "<!-- MANA-START -->"
marker_end = "<!-- MANA-END -->"

# === Get current year contribution count from GitHub profile page ===
response = requests.get(f"https://github.com/users/{username}/contributions")
if response.status_code != 200:
    raise Exception("Failed to fetch contribution data")

# Count number of contribution days in the current year
html = response.text
contribs = [int(s.split('data-count="')[1].split('"')[0])
            for s in html.split('<rect') if 'data-count="' in s]
total = sum(contribs)

# === Calculate Mana Bar ===
percent = min(100, int((total / max_mana) * 100))
bar = "█" * (percent // 5) + "░" * (20 - (percent // 5))

tier = "Grandmaster" if percent >= 100 else \
       "Adept" if percent >= 50 else \
       "Novice"

mana_block = f"""
{marker_start}
🧙 Mana Gauge:  
`{bar}` — {percent}%

🧪 Current Power Level: {total} contributions this year  
🔋 Mana Tier: {tier}
{marker_end}
"""

# === Update README.md ===
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

start = content.find(marker_start)
end = content.find(marker_end) + len(marker_end)
if start != -1 and end != -1:
    updated = content[:start] + mana_block + content[end:]
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated)
else:
    raise Exception("Markers not found in README.md")
