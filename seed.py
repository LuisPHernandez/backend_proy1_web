import requests
from datetime import datetime

BASE_URL = "http://localhost:8000/players"

def calculate_age(birth_date_str: str) -> int:
    birth_date = datetime.fromisoformat(birth_date_str)
    today = datetime.today()
    return today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )

players = [
    {
        "name": "LeBron James",
        "team": "Los Angeles Lakers", "position": "SF", "jersey_number": 23,
        "nationality": "USA", "birth_date": "1984-12-30T00:00:00",
        "points_per_game": 20.9, "assists_per_game": 7.2, "rebounds_per_game": 6.1
    },
    {
        "name": "Luka Dončić",
        "team": "Los Angeles Lakers", "position": "PG", "jersey_number": 77,
        "nationality": "Slovenia", "birth_date": "1999-02-28T00:00:00",
        "points_per_game": 33.5, "assists_per_game": 8.3, "rebounds_per_game": 7.7
    },
    {
        "name": "Austin Reaves",
        "team": "Los Angeles Lakers", "position": "SG", "jersey_number": 15,
        "nationality": "USA", "birth_date": "1998-05-29T00:00:00",
        "points_per_game": 23.3, "assists_per_game": 5.5, "rebounds_per_game": 4.7
    },
    {
        "name": "Rui Hachimura",
        "team": "Los Angeles Lakers", "position": "PF", "jersey_number": 28,
        "nationality": "Japan", "birth_date": "1998-02-08T00:00:00",
        "points_per_game": 11.5, "assists_per_game": 0.8, "rebounds_per_game": 3.3
    },
    {
        "name": "Dalton Knecht",
        "team": "Los Angeles Lakers", "position": "SG", "jersey_number": 4,
        "nationality": "USA", "birth_date": "2001-04-19T00:00:00",
        "points_per_game": 5.3, "assists_per_game": 0.4, "rebounds_per_game": 1.7
    },
    {
        "name": "Jaxson Hayes",
        "team": "Los Angeles Lakers", "position": "C", "jersey_number": 11,
        "nationality": "USA", "birth_date": "2000-05-23T00:00:00",
        "points_per_game": 7.5, "assists_per_game": 0.9, "rebounds_per_game": 4.1
    },
    {
        "name": "Jarred Vanderbilt",
        "team": "Los Angeles Lakers", "position": "SF", "jersey_number": 2,
        "nationality": "USA", "birth_date": "1999-04-03T00:00:00",
        "points_per_game": 4.4, "assists_per_game": 1.3, "rebounds_per_game": 4.5
    },
    {
        "name": "Bronny James Jr.",
        "team": "Los Angeles Lakers", "position": "PG", "jersey_number": 9,
        "nationality": "USA", "birth_date": "2004-10-06T00:00:00",
        "points_per_game": 2.9, "assists_per_game": 1.2, "rebounds_per_game": 0.5
    },
    {
        "name": "Jake LaRavia",
        "team": "Los Angeles Lakers", "position": "PF", "jersey_number": 12,
        "nationality": "USA", "birth_date": "2001-11-03T00:00:00",
        "points_per_game": 8.2, "assists_per_game": 1.8, "rebounds_per_game": 4.0
    },
    {
        "name": "Nick Smith Jr.",
        "team": "Los Angeles Lakers", "position": "PG", "jersey_number": 3,
        "nationality": "USA", "birth_date": "2004-04-18T00:00:00",
        "points_per_game": 6.2, "assists_per_game": 1.0, "rebounds_per_game": 0.8
    },
    {
        "name": "Drew Timme",
        "team": "Los Angeles Lakers", "position": "PF", "jersey_number": 17,
        "nationality": "USA", "birth_date": "2000-09-09T00:00:00",
        "points_per_game": 3.4, "assists_per_game": 0.9, "rebounds_per_game": 1.2
    },
    {
        "name": "Marcus Smart",
        "team": "Los Angeles Lakers", "position": "PG", "jersey_number": 36,
        "nationality": "USA", "birth_date": "1994-03-06T00:00:00",
        "points_per_game": 9.3, "assists_per_game": 3.0, "rebounds_per_game": 2.8
    },
    {
        "name": "Maxi Kleber",
        "team": "Los Angeles Lakers", "position": "C", "jersey_number": 14,
        "nationality": "Germany", "birth_date": "1992-01-29T00:00:00",
        "points_per_game": 2.0, "assists_per_game": 0.6, "rebounds_per_game": 2.0
    },
    {
        "name": "Deandre Ayton",
        "team": "Los Angeles Lakers", "position": "C", "jersey_number": 5,
        "nationality": "Bahamas", "birth_date": "1998-07-23T00:00:00",
        "points_per_game": 12.5, "assists_per_game": 0.8, "rebounds_per_game": 8.0
    },
    {
        "name": "Luke Kennard",
        "team": "Los Angeles Lakers", "position": "SG", "jersey_number": 10,
        "nationality": "USA", "birth_date": "1996-06-24T00:00:00",
        "points_per_game": 8.4, "assists_per_game": 2.2, "rebounds_per_game": 2.3
    },
    {
        "name": "Adou Thiero",
        "team": "Los Angeles Lakers", "position": "SG", "jersey_number": 1,
        "nationality": "USA", "birth_date": "2004-05-08T00:00:00",
        "points_per_game": 1.9, "assists_per_game": 0.4, "rebounds_per_game": 1.1
    },
    {
        "name": "Chris Mañon",
        "team": "Los Angeles Lakers", "position": "PG", "jersey_number": 30,
        "nationality": "USA", "birth_date": "2001-12-09T00:00:00",
        "points_per_game": 0.8, "assists_per_game": 0.3, "rebounds_per_game": 1.1
    },
]

def seed():
    print("Seeding players...")
    for p in players:
        payload = {
            "name":               p["name"],
            "team":               p["team"],
            "position":           p["position"],
            "jersey_number":      p["jersey_number"],
            "age":                calculate_age(p["birth_date"]),
            "nationality":        p["nationality"],
            "points_per_game":    p["points_per_game"],
            "assists_per_game":   p["assists_per_game"],
            "rebounds_per_game":  p["rebounds_per_game"],
            "is_active":          True
        }
        response = requests.post(BASE_URL, json=payload)
        if response.status_code == 201:
            print(f"  ✓ {p['name']} — {p['points_per_game']} pts | {p['assists_per_game']} ast | {p['rebounds_per_game']} reb")
        else:
            print(f"  ✗ {p['name']} — {response.status_code}: {response.text}")
    print("Done.")

if __name__ == "__main__":
    seed()