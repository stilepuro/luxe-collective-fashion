#!/bin/bash
# Script di Backup Automatico per Dropbox
# Esegui: ./cloud_sync_dropbox.sh

echo "🔄 Caricamento backup LUXE Collective su Dropbox..."

# Verifica se Dropbox è installato
if [ ! -d "$HOME/Dropbox" ]; then
    echo "❌ Dropbox non trovato. Installa Dropbox desktop app."
    echo "📥 Download: https://www.dropbox.com/install"
    exit 1
fi

# Crea directory di backup in Dropbox
BACKUP_DIR="$HOME/Dropbox/LUXE_Collective_Backup"
mkdir -p "$BACKUP_DIR"

# Copia il backup più recente
LATEST_BACKUP=$(ls -t *.zip 2>/dev/null | head -1)
if [ -n "$LATEST_BACKUP" ]; then
    cp "$LATEST_BACKUP" "$BACKUP_DIR/"
    echo "✅ Backup caricato su Dropbox: $BACKUP_DIR/$LATEST_BACKUP"
else
    echo "❌ Nessun backup trovato."
    exit 1
fi

echo "🎉 Backup completato su Dropbox!"
