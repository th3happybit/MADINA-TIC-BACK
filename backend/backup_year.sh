#!/bin/sh
# cd $APP_PATH
echo "backup year starting..."
echo "backup year: $(date +"%Y")"
./manage.py dumpdata --exclude auth.permission --exclude contenttypes > backups/$(date +"%Y")_backup.json
echo "remove the $(date +"%Y") declarations, reports and announces"
cat ../remove_models.py | ./manage.py shell
echo "Done!"