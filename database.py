import sqlite3

DB_NAME = "finals.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('''CREATE TABLE "scrapes" (
    "id"	INTEGER NOT NULL,
    "time"	TEXT NOT NULL,
    "goal"	INTEGER NOT NULL,
    "total"	INTEGER NOT NULL,
    PRIMARY KEY("id" AUTOINCREMENT)
    )''')
    c.execute('''CREATE TABLE "users" (
    "id"    INTEGER NOT NULL, 
    "name"  TEXT NOT NULL, 
    "steam" TEXT, 
    "xbox"  TEXT, 
    "psn"   TEXT, 
    PRIMARY KEY("id" AUTOINCREMENT)
    )''')
    c.execute('''CREATE TABLE "users_data" (
    "id"	INTEGER NOT NULL,
    "scrapeId"	INTEGER,
    "userId"	INTEGER,
    "rank"	INTEGER NOT NULL,
    "kills"	INTEGER NOT NULL,
    PRIMARY KEY("id" AUTOINCREMENT),
    FOREIGN KEY("scrapeId") REFERENCES "scrapes"("id"),
    FOREIGN KEY("userId") REFERENCES "users"("id")
    )''')

    # commit changes and close database connect
    conn.commit()
    conn.close()
