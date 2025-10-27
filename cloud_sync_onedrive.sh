#!/bin/bash
# Script di Backup per OneDrive
# Esegui: ./cloud_sync_onedrive.sh

echo "🔄 Caricamento backup LUXE Collective su OneDrive..."

# Verifica OneDrive
if [ ! -d "$HOME/OneDrive" ]; then
    echo "❌ OneDrive non trovato. Installa OneDrive desktop app."
    echo "📥 Download: https://www.microsoft.com/en-us/microsoft-365/onedrive/download"
    exit 1
fi

# Crea directory di backup
BACKUP_DIR="$HOME/OneDrive/LUXE_Collective_Backup"
mkdir -p "$BACKUP_DIR"

# Copia il backup più recente
LATEST_BACKUP=$(ls -t *.zip 2>/dev/null | head -1)
if [ -n "$LATEST_BACKUP" ]; then
    cp "$LATEST_BACKUP" "$BACKUP_DIR/"
    echo "✅ Backup caricato su OneDrive: $BACKUP_DIR/$LATEST_BACKUP"
else
    echo "❌ Nessun backup trovato."
    exit 1
fi

echo "🎉 Backup completato su OneDrive!"
