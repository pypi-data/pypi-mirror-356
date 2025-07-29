# MongoDB Migrations

## Overview
This project includes a CLI tool for managing MongoDB database migrations.

Migration scripts should utilize the `pymongo` library to interact with the database.

Migrations are performed in a transactional manner, 
meaning that if an error occurs during the execution of a migration, 
the migration will be rolled back and the database will be left in the state 
it was in before the migration was attempted.
To support this functionality MongoDB requires a replica set to be configured.


## Installation
```bash
pip install starsol-mongo-migrate
```

## Usage

### Python API
You can use the migration system programmatically in your Python scripts:

```python
from starsol_mongo_migrate import MigrationManager

# Create a migration manager
with MigrationManager('mongodb://localhost:27017/mydb', 'versions') as manager:
    # Initialize migration system
    manager.init()

    # Generate new migration
    revision = manager.generate('add_user_collection')

    # List migrations
    migrations = manager.list_migrations()
    for rev, name in migrations:
        print(f'{rev}: {name}')

    # Check current revision
    current = manager.current_revision()
    print(f'Current: {current}')

    # Upgrade to latest
    manager.upgrade()

    # Upgrade to specific revision
    manager.upgrade(target_revision='20250216000109')

    # Downgrade
    manager.downgrade(target_revision='20250216000109')

    # Use without transactions (for non-replica set)
    manager.upgrade(use_transactions=False)
```

### CLI Commands
This project also offers CLI commands to manage MongoDB migrations.

#### Initialize
Initialize the migration directory and the database version collection:
```bash
python3 -m starsol_mongo_migrate.cli --dir=versions init <your_mongo_uri>
```

#### Generate Migrations
Generate a new migration:
```bash
python3 -m starsol_mongo_migrate.cli --dir=versions generate migration_name
```

#### List Migrations
List all migrations:
```bash
python3 -m starsol_mongo_migrate.cli --dir=versions list
```

#### Upgrade Database
Upgrade the database to a specific revision:
```bash
python3 -m starsol_mongo_migrate.cli --dir=versions upgrade <your_mongo_uri> <target_revision>
```
Upgrade the database to the latest revision:
```bash
python3 -m starsol_mongo_migrate.cli --dir=versions upgrade <your_mongo_uri>
```
Upgrade without using transactions:
```bash
python3 -m starsol_mongo_migrate.cli --dir=versions upgrade --no-transaction <your_mongo_uri>
```

#### Downgrade Database
Downgrade the database to a specific revision:
```bash
python3 -m starsol_mongo_migrate.cli --dir=versions downgrade <your_mongo_uri> <target_revision>
```
Downgrade without using transactions:
```bash
python3 -m starsol_mongo_migrate.cli --dir=versions downgrade --no-transaction <your_mongo_uri> <target_revision>
```

#### Show Current Revision
Display the current database revision:
```bash
python3 -m starsol_mongo_migrate.cli --dir=versions current <your_mongo_uri>
```
