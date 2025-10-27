#!/bin/bash
# Scheduler Automatico di Backup
# Esegue backup automatici ogni 24 ore

BACKUP_DIR="./cloud_backup_packages"
LOG_FILE="$BACKUP_DIR/backup_log.txt"

# Crea directory se non esiste
mkdir -p "$BACKUP_DIR"

echo "=== Backup automatico LUXE Collective ===" >> "$LOG_FILE"
echo "Data: $(date)" >> "$LOG_FILE"

# Esegui il backup
python3 cloud-backup-automation.py >> "$LOG_FILE" 2>&1

# Esegui sincronizzazione con tutti i servizi cloud
echo "🔄 Sincronizzazione con servizi cloud..." >> "$LOG_FILE"

# Dropbox
if [ -d "$HOME/Dropbox" ]; then
    ./cloud_sync_dropbox.sh >> "$LOG_FILE" 2>&1
    echo "✅ Dropbox sincronizzato" >> "$LOG_FILE"
fi

# Google Drive
if command -v rclone &> /dev/null; then
    ./cloud_sync_google_drive.sh >> "$LOG_FILE" 2>&1
    echo "✅ Google Drive sincronizzato" >> "$LOG_FILE"
fi

# OneDrive
if [ -d "$HOME/OneDrive" ]; then
    ./cloud_sync_onedrive.sh >> "$LOG_FILE" 2>&1
    echo "✅ OneDrive sincronizzato" >> "$LOG_FILE"
fi

echo "=== Backup completato ===" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

echo "🎉 Backup automatico completato!"
