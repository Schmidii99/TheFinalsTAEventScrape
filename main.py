import database
import requests
import sqlite3


URL = "https://storage.googleapis.com/embark-discovery-leaderboard/community-event-2-8-leaderboard-discovery-live.json"

if __name__ == '__main__':
    conn = sqlite3.connect(database.DB_NAME)
    c = conn.cursor()

    database.init_db(c)
    conn.commit()

    response = requests.get(URL).json()
    database.add_scrape(c, response["goal"], response["total"])
    conn.commit()

    for entry in response["entries"]:
        if not database.does_user_exist(c, entry["name"]):
            database.add_user(c, entry["name"], entry["steam"], entry["xbox"], entry["psn"])
            conn.commit()
        database.add_connection(c, entry["name"], entry["r"], entry["k"])
        conn.commit()

    conn.close()
