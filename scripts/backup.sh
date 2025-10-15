#!/bin/bash
# scripts/backup.sh
# Backup database and files

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups"
DB_NAME="dojo_launchpad"

mkdir -p $BACKUP_DIR

echo "📦 Creating backup: $TIMESTAMP"

# Backup database
echo "💾 Backing up database..."
pg_dump -U dojo_user -h localhost $DB_NAME > $BACKUP_DIR/db_backup_$TIMESTAMP.sql

# Backup uploads
echo "📁 Backing up uploads..."
tar -czf $BACKUP_DIR/uploads_$TIMESTAMP.tar.gz uploads/

# Backup docs
echo "📚 Backing up docs..."
tar -czf $BACKUP_DIR/docs_$TIMESTAMP.tar.gz docs/

# Clean old backups (keep 7 days)
echo "🧹 Cleaning old backups..."
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "✅ Backup completed: $TIMESTAMP"
