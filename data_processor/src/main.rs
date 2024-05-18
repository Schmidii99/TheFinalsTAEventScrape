mod database;
use database::Database;

use std::fs;
use serde::Deserialize;
use std::error::Error;
use std::fs::File;
use std::io::BufReader;
use std::path::Path;

#[derive(Debug, Deserialize)]
struct Entry {
    r: i32, // rank
    name: String,
    k: i32, // kills
    steam: String,
    xbox: String,
    psn: String
}


#[derive(Debug, Deserialize)]
struct Dataset {
    goal: i32,
    total: i32,
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
    // let db: Database = Database::initialize();
    let paths:fs::ReadDir  = fs::read_dir("./data/").unwrap();

    for path in paths {
        let res: Dataset = read_dataset_from_file(path.unwrap().path()).unwrap();
        println!("{}", res.total)
    }
}
