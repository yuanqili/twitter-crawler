# TwitterScrapper

Directory structure

- `AppAuthClient.py`: A Client instance is used to connect to the Twitter API server and make queries.
- `db.py`: It contains both schema of the Tweet database and database connector that can create and update a database.
- `utilities.py`: It contains some useful helper functions.
- `TwitterScrapper`: `CONSUMER_KEY` and `CONSUMER_SECRET` are used to connect to the Twitter API server, and `DB_PATH` refers to which database the data should be stored. If it doesn't exist, a new database will be created.

