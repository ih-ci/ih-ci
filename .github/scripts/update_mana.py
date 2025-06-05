import requests
import os
from datetime import datetime

# === Config ===
token = os.environ['GH_TOKEN']
username = "ih-ci"
max_mana = 1000
readme_path = "README.md"
marker_start = "<!-- MANA-START -->"
marker_end = "<!-- MANA-END -->"

# === GraphQL Query ===
query = """
query($userName:String!) {
  user(login: $userName) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
      }
    }
  }
}
"""

headers = {"Authorization": f"Bearer {token}"}
variables = {"userName": username}
res = requests.post(
    "https://api.github.com/graphql",
    json={"query": query, "variables": variables},
    headers=headers
)

data = res.json()
total = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]

# === Mana Bar Logic ===
percent = min(100, int((total / max_mana) * 100))
bar = "█" * (percent // 5) + "░" * (20 - (percent // 5))

tier = "🪄 Grandmaster" if percent >= 100 else \
       "🔋 Arcane Adept" if percent >= 50 else \
       "💧 Novice"

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
