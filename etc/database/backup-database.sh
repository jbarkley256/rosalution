#! /bin/bash
# ./backup-database.sh <docker-container> <output-path (optional)>"
usage() {
  echo "usage: $0 <docker-container> <output-path (optional)>"
  echo " "
  echo "Dumps a rosalution mongodb database archive named 'rosalution-db-<current-date-seconds>.archive'"
  echo "to the designated output path. By default, the output path is '/home/centos/rosalution/backup-db/'"
  echo "Include a second paramater to overwrite the <output-path>.  If the <output-path> does not exist"
  echo "the backup operation will be canceled"
  exit
}

if [[ $# -eq 0 ]]
then
    echo "Missing required input. Exiting script ..."
    echo ""

    usage
    exit 1
fi

DOCKER_CONTAINER=$1
TARGET_PATH=/home/centos/rosalution/backup-db/

if [[ $# -eq 2 ]]
then
    TARGET_PATH=$2
fi

if [[ ! -d "$TARGET_PATH" ]]
then
    echo "Target output file path '$TARGET_PATH' does not exist.  Canceling backup operation ..."
    echo ""

    usage
    exit 1
fi

date_stamp=$(date +"%Y-%m-%d-%s")
docker exec "$DOCKER_CONTAINER" sh -c 'exec mongodump -d rosalution_db --archive' > "$TARGET_PATH/rosalution-db-$date_stamp.archive"

