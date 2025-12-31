# CRIO_SOLUTION_AND_STUB_START_MODULE_EXERCISES
# CRIO_SOLUTION_AND_STUB_END_MODULE_EXERCISES
#!/bin/bash

# Usage: ./setupDB.sh

DB_USER="assessment"
DB_PASS="redrum"
DB_NAME="test_db"
# DB_FILE="app/src/main/resources/init-schema.sql"

echo "Initializing MySQL database..."
sudo mysql -uroot -e "CREATE USER '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';"
sudo mysql -uroot -e "GRANT ALL PRIVILEGES ON *.* TO '$DB_USER'@'localhost' WITH GRANT OPTION;"
sudo mysql -uroot -e "FLUSH PRIVILEGES;"
sudo mysql -u $DB_USER -p$DB_PASS -e "DROP DATABASE IF EXISTS $DB_NAME; CREATE DATABASE $DB_NAME;"
# sudo mysql -u $DB_USER -p$DB_PASS $DB_NAME < $DB_FILE