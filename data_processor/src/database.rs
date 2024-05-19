use std::{collections::HashMap, fs::File};
use std::path::Path;
use rusqlite::{named_params, Connection};

const DB_PATH: &str = "./database.sqlite";

pub struct Database {
    conn: Connection,
}

impl Database {
    pub fn initialize() -> Database {
        if !Path::new(DB_PATH).try_exists().unwrap() {
            _ = File::create(DB_PATH);
        }
    
        let conn: Connection = Connection::open(DB_PATH).unwrap();

        _ = conn.execute_batch("
            BEGIN;
            CREATE TABLE IF NOT EXISTS 'scrapes' (
                'id'	INTEGER NOT NULL,
                'time'	TEXT NOT NULL,
                'goal'	INTEGER NOT NULL,
                'total'	INTEGER NOT NULL,
                PRIMARY KEY('id' AUTOINCREMENT)
            );
            CREATE TABLE IF NOT EXISTS 'users' (
                'id'    INTEGER NOT NULL, 
                'name'  TEXT NOT NULL, 
                'steam' TEXT, 
                'xbox'  TEXT, 
                'psn'   TEXT, 
                PRIMARY KEY('id' AUTOINCREMENT)
            );
            CREATE TABLE IF NOT EXISTS 'users_data' (
                'id'	INTEGER NOT NULL,
                'scrapeId'	INTEGER,
                'userId'	INTEGER,
                'rank'	INTEGER NOT NULL,
                'kills'	INTEGER NOT NULL,
                PRIMARY KEY('id' AUTOINCREMENT),
                FOREIGN KEY('scrapeId') REFERENCES 'scrapes'('id'),
                FOREIGN KEY('userId') REFERENCES 'users'('id')
            );
            CREATE INDEX IF NOT EXISTS 'userIndex' ON 'users' (
                'name',
                'id'
            );
            COMMIT;");

        Database{conn: conn}
    }

    pub fn add_scrape(&self, time: &str, goal: u32, total: u32) {
        _ = self.conn.execute("INSERT INTO scrapes(time, goal, total) VALUES (@time, @goal, @total );", named_params! {
            "@time": time,
            "@goal": goal,
            "@total": total
        });
    }

    pub fn does_user_exist(&self, user_name: &str) -> bool {
        let res: Result<(), rusqlite::Error> = self.conn.query_row("SELECT id FROM users WHERE name=@name;", named_params! {"@name": user_name
        }, |_row| Ok(()));
        match res {
            Ok(_o) => true,
            Err(_e) => false,
        }
    }

    pub fn add_user(&self, name: &str, steam: &str, xbox: &str, psn: &str) {
        _ = self.conn.execute("INSERT INTO users(name, steam, xbox, psn) VALUES (@name, @steam, @xbox, @psn);", named_params! {
            "@name": name,
            "@steam": steam,
            "@xbox": xbox,
            "@psn": psn
        });
    }

    pub fn add_connection(&self, user_name: &str, kills: u32, rank: u32) {
        let scrape_id: i32 = self.conn.query_row("select seq from sqlite_sequence where name='scrapes';", [], |row| row.get(0),).unwrap();
        let user_id: i32 = self.conn.query_row("select id from users where name=@name;", named_params! { "@name": user_name }, |row| row.get(0)).unwrap();
        _ = self.conn.execute("INSERT INTO users_data(scrapeId, userId, rank, kills) VALUES (@scrape_id, @user_id, @rank, @kills);", named_params! {
            "@scrape_id": scrape_id,
            "@user_id": user_id,
            "@rank": rank,
            "@kills": kills
        })
    }

    fn get_all_users(&self) -> Result<Vec<User>, rusqlite::Error> {
        let mut statement = self.conn.prepare("SELECT name, id FROM users;").unwrap();

        let res = statement.query_map([], |row| {
            Ok(User {
                name: row.get(0)?,
                id: row.get(1)?,
            })
        });

        match res {
            Ok(res) => {
                res.collect()
            },
            Err(_) => Err(rusqlite::Error::QueryReturnedNoRows)
        }
    }

    pub fn get_user_hashmap(&self) -> HashMap<String, i32> {
        let users = self.get_all_users().unwrap();

        let mut map: HashMap<String, i32> = HashMap::new();

        for u in users {
            map.insert(u.name, u.id);
        }
        map
    }
}

struct User {
    name: String,
    id: i32
}