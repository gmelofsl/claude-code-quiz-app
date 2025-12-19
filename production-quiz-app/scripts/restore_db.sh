#!/bin/bash
# Database restore script for Production Quiz App
#
# Usage: ./restore_db.sh <backup_file>
#
# This script restores a PostgreSQL database from a backup file

set -e  # Exit on error
set -u  # Exit on undefined variable

# Check if backup file is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <backup_file>"
    echo "Example: $0 /app/backups/quiz_app_backup_20240101_120000.sql.gz"
    exit 1
fi

BACKUP_FILE="$1"

# Database connection details from environment
DB_HOST="${POSTGRES_HOST:-postgres}"
DB_PORT="${POSTGRES_PORT:-5432}"
DB_NAME="${POSTGRES_DB:-quiz_app}"
DB_USER="${POSTGRES_USER:-quiz_user}"
DB_PASSWORD="${POSTGRES_PASSWORD}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1" >&2
}

warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

# Check if backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
    error "Backup file not found: $BACKUP_FILE"
    exit 1
fi

log "=== Database Restore Script Started ==="
log "Backup file: $BACKUP_FILE"
log "Database: $DB_NAME@$DB_HOST:$DB_PORT"

# Confirmation prompt
echo ""
warning "WARNING: This will DROP and recreate the database!"
warning "All existing data will be lost!"
echo ""
read -p "Are you sure you want to continue? (type 'yes' to confirm): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    log "Restore cancelled by user"
    exit 0
fi

# Set PostgreSQL password
export PGPASSWORD="$DB_PASSWORD"

# Restore database
log "Restoring database from backup..."

if gunzip -c "$BACKUP_FILE" | psql -h "$DB_HOST" \
                                    -p "$DB_PORT" \
                                    -U "$DB_USER" \
                                    -d "$DB_NAME" \
                                    --quiet; then
    unset PGPASSWORD
    log "=== Database Restore Completed Successfully ==="
    exit 0
else
    unset PGPASSWORD
    error "=== Database Restore Failed ==="
    exit 1
fi
