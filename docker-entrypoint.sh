#!/bin/sh
cd $APP_PATH
# check if the database is ready
echo "Waiting for Postgres DB"
while ! pg_isready -h $PG_HOSTNAME > /dev/null 2>&1;
do
  echo -n "."
  sleep 1
done
echo "Postgres DB is ready"

# create tables
echo "Updating Database Tables"
./manage.py makemigrations
./manage.py migrate
echo "The Database has been updated"

# create admin user
echo "Superuser..."
cat /create_superuser.py | ./manage.py shell
cat /create_groups.py | ./manage.py shell
# cat /setup_perms.py | ./manage.py shell
# collect static files
./manage.py collectstatic --no-input

# Setup a cron schedule for end of year backup
mkdir -p backups
echo "59 23 31 12 * /backup_year.sh >> $(pwd)/backups/cron.log 2>&1
# This extra line makes it a valid cron" > scheduler.txt
crontab scheduler.txt
cron -f

# run the server
echo "Starting the server..."
gunicorn backend.wsgi --bind 0.0.0.0:8000