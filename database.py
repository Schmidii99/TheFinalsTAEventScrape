import sqlite3
import datetime

DB_NAME = "finals.db"


def init_db(c):
    c.execute('''CREATE TABLE IF NOT EXISTS "scrapes" (
    "id"	INTEGER NOT NULL,
    "time"	TEXT NOT NULL,
    "goal"	INTEGER NOT NULL,
    "total"	INTEGER NOT NULL,
    PRIMARY KEY("id" AUTOINCREMENT)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS "users" (
    "id"    INTEGER NOT NULL, 
    "name"  TEXT NOT NULL, 
    "steam" TEXT, 
    "xbox"  TEXT, 
    "psn"   TEXT, 
    PRIMARY KEY("id" AUTOINCREMENT)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS "users_data" (
    "id"	INTEGER NOT NULL,
    "scrapeId"	INTEGER,
    "userId"	INTEGER,
    "rank"	INTEGER NOT NULL,
    "kills"	INTEGER NOT NULL,
    PRIMARY KEY("id" AUTOINCREMENT),
    FOREIGN KEY("scrapeId") REFERENCES "scrapes"("id"),
    FOREIGN KEY("userId") REFERENCES "users"("id")
    )''')


def add_scrape(c, goal: str, total: str):
    currentDT = str(datetime.datetime.now())
    c.execute("INSERT INTO scrapes(time, goal, total) VALUES (?, ?, ?)", (currentDT, goal, total))


def does_user_exist(c, name: str) -> bool:
    c.execute("SELECT * FROM users WHERE name=?", (name,))
    result = c.fetchall()

    return len(result) > 0


def add_user(c, name, steam, xbox, psn):
    c.execute("INSERT INTO users(name, steam, xbox, psn) VALUES (?, ?, ?, ?)", (name, steam, xbox, psn))


def add_connection(c, player_name, rank, kills):
    c.execute("select seq from sqlite_sequence where name='scrapes'")
    scrape_id = c.fetchall()[0][0]
    c.execute("select id from users where name=?", (player_name,))
    user_id = c.fetchall()
    if len(user_id) == 0:
        return
    user_id = user_id[0][0]

    c.execute("INSERT INTO users_data(scrapeId, userId, rank, kills) VALUES (?, ?, ?, ?)", (scrape_id, user_id, rank,
                                                                                            kills))
