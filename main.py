import database
import requests
import sqlite3
import os
import datetime
import json

URL = "https://storage.googleapis.com/embark-discovery-leaderboard/community-event-2-8-leaderboard-discovery-live.json"


def save_json_file():
    response = requests.get(URL)

    if not os.path.exists("./data"):
        os.makedirs("./data")

    with open("./data/" + str(datetime.datetime.now()).replace(" ", "_").replace(":", "_") + ".json", "wb") as f:
        f.write(response.content)


def save_in_db():
    conn = sqlite3.connect(database.DB_NAME)
    c = conn.cursor()

    database.init_db(c)
    conn.commit()

    all_users: dict[str, int] = database.get_all_users(c)

    response = requests.get(URL).json()
    database.add_scrape(c, response["goal"], response["total"])
    conn.commit()

    connections: list[tuple[int, int, int]] = []

    for entry in response["entries"]:
        if not entry["name"] in all_users:
            database.add_user(c, entry["name"], entry["steam"], entry["xbox"], entry["psn"])
            all_users[entry["name"]] = len(all_users)

        connections.append((all_users[entry["name"]], entry["r"], entry["k"]))

    database.add_connections(c, connections)
    conn.commit()

    conn.close()


DATA_DIR = "./data/"


def process_files():
    conn = sqlite3.connect(database.DB_NAME)
    c = conn.cursor()

    database.init_db(c)
    conn.commit()

    all_users: dict[str, int] = database.get_all_users(c)
    users_to_add: list[tuple[str, str, str, str]] = []
    connections: list[tuple[int, int, int]] = []

    for file in os.listdir(DATA_DIR):
        f = open(DATA_DIR + file, encoding='utf-8')
        js = json.load(f)
        date = datetime.datetime.strptime(file.split(".j")[0].replace("_", ":"), "%Y-%m-%d:%H:%M:%S.%f")
        # dates were shifted by one hour
        date = date + datetime.timedelta(hours=1)

        database.add_scrape_with_name(c, date.strftime("%Y-%m-%d:%H:%M:%S.%ms"), js["goal"], js["total"])
        conn.commit()

        for entry in js["entries"]:
            if not entry["name"] in all_users:
                users_to_add.append((entry["name"], entry["steam"], entry["xbox"], entry["psn"]))
                all_users[entry["name"]] = len(all_users)

            connections.append((all_users[entry["name"]], entry["r"], entry["k"]))

    database.add_connections(c, connections)
    database.add_users(c, users_to_add)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    start = datetime.datetime.now()
    process_files()
    print(datetime.datetime.now() - start)
