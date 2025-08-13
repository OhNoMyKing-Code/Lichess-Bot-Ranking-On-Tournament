import requests
from tabulate import tabulate

# ==== CONFIG ====
TOURNAMENT_ID = "tWjRtmJs"  # đổi thành ID giải đấu của ông
WEBHOOK_URL = "https://discord.com/api/webhooks/..."  # đổi thành webhook Discord
# ================

def fetch_tournament_data(tid):
    url = f"https://lichess.org/api/tournament/{tid}"
    resp = requests.get(url, headers={"Accept": "application/json"})
    resp.raise_for_status()
    return resp.json()

def create_table(data):
    players = data["standing"]["players"]

    table = []
    for p in players:
        table.append([
            p["username"],
            p["rating"],
            p["score"],
            p["nbGames"],
            f"{(p['score'] / (p['nbGames'] * 2) * 100):.0f}%"  # % thắng tương đối
        ])

    return tabulate(table, headers=["PLAYER", "RATING", "POINTS", "PLAYED", "%WIN"])

def post_to_discord(msg):
    requests.post(WEBHOOK_URL, json={"content": f"```\n{msg}\n```"})

if __name__ == "__main__":
    data = fetch_tournament_data(TOURNAMENT_ID)
    table_str = create_table(data)
    print(table_str)
    if WEBHOOK_URL:
        post_to_discord(table_str)
