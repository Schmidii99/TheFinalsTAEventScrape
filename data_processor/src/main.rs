mod database;
use database::Database;

use std::fs;
use serde::Deserialize;
use std::error::Error;
use std::fs::File;
use std::io::BufReader;
use std::path::Path;
use std::time::Instant;

#[derive(Debug, Deserialize)]
struct Entry {
    r: u32, // rank
    name: String,
    k: u32, // kills
    steam: String,
    xbox: String,
    psn: String
}


#[derive(Debug, Deserialize)]
struct Dataset {
    goal: u32,
    total: u32,
    entries: Vec<Entry>,
}

fn read_dataset_from_file<P: AsRef<Path>>(path: P) -> Result<Dataset, Box<dyn Error>>{
    // Open the file in read-only mode with buffer.
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    // Read the JSON contents of the file as an instance of `Dataset`.
    let u: Dataset = serde_json::from_reader(reader)?;

    // Return the `Dataset`.
    Ok(u)
}

fn main() {
    let now = Instant::now();

    let db: Database = Database::initialize();

    let mut users = db.get_user_hashmap();

    let paths:fs::ReadDir  = fs::read_dir("./data1/").unwrap();

    for path in paths {
        let set: Dataset = read_dataset_from_file(&path.as_ref().unwrap().path()).unwrap();
        _ = db.add_scrape(&path.as_ref().unwrap().file_name().into_string().unwrap()[..26].replace("_", ":"), set.goal, set.total);
        for entry in set.entries {
            if users.get(&entry.name) == None {
                _ = db.add_user(&entry.name, &entry.steam, &entry.xbox, &entry.psn);
                users.insert(entry.name.to_string(), users.len() as i32);
            }
            _ = db.add_connection(&entry.name, entry.k, entry.r);
        }
    }

    println!("Time took: {}ms", now.elapsed().as_millis());
}


