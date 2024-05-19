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


def add_scrape_with_name(c, name: str, goal: str, total: str):
    c.execute("INSERT INTO scrapes(time, goal, total) VALUES (?, ?, ?)", (name, goal, total))


def get_all_users(c) -> dict[str, int]:
    c.execute("select name, id from users;")
    return dict(c.fetchall())


def add_user(c, name, steam, xbox, psn):
    c.execute("INSERT INTO users(name, steam, xbox, psn) VALUES (?, ?, ?, ?)", (name, steam, xbox, psn))


def add_connections(c, data: list[tuple[int, int, int]]):
    c.execute("select seq from sqlite_sequence where name='scrapes'")
    scrape_id = c.fetchall()[0][0]
    data = [(scrape_id, *x) for x in data]

    c.executemany("INSERT INTO users_data(scrapeId, userId, rank, kills) VALUES (?, ?, ?, ?)", data)


def add_users(c, data: list[tuple[str, str, str, str]]):
    c.executemany("INSERT INTO users(name, steam, xbox, psn) VALUES (?, ?, ?, ?)", data)
