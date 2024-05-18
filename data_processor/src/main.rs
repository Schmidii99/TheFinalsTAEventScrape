mod database;
use database::Database;

fn main() {
    let db: Database = Database::initialize();
    db.add_scrape("myTime", 7000000, 1345678);
    if db.does_user_exist("testuser") {
        println!("testuser exists")
    }
    if !db.does_user_exist("testuser2") {
        println!("testuser2 does not exists")
    }
    db.add_user("name", "steam", "xbox", "psn");
    db.add_connection("testuser", 100, 876);
}