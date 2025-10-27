#!/bin/bash
# Script di Backup per Google Drive
# Esegui: ./cloud_sync_google_drive.sh

echo "🔄 Caricamento backup LUXE Collective su Google Drive..."

# Verifica rclone
if ! command -v rclone &> /dev/null; then
    echo "📥 Installazione rclone..."
    curl https://rclone.org/install.sh | sudo bash
fi

# Configura Google Drive se non già fatto
if ! rclone listremotes | grep -q "gdrive:"; then
    echo "⚙️  Configurazione Google Drive..."
    echo "Segui le istruzioni per autenticarti con Google Drive"
    rclone config create gdrive drive
fi

# Crea directory di backup
rclone mkdir gdrive:/LUXE_Collective_Backup

# Carica il backup più recente
LATEST_BACKUP=$(ls -t *.zip 2>/dev/null | head -1)
if [ -n "$LATEST_BACKUP" ]; then
    rclone copy "$LATEST_BACKUP" gdrive:/LUXE_Collective_Backup/
    echo "✅ Backup caricato su Google Drive: LUXE_Collective_Backup/$LATEST_BACKUP"
else
    echo "❌ Nessun backup trovato."
    exit 1
fi

echo "🎉 Backup completato su Google Drive!"
