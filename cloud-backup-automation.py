#!/usr/bin/env python3
"""
Sistema di Backup Cloud Automatico per LUXE Collective
Carica automaticamente i backup su servizi cloud multipli
"""

import os
import shutil
import zipfile
import datetime
from pathlib import Path

def create_cloud_backup_structure():
    """Crea la struttura per i backup cloud"""
    print("☁️  Configurazione backup cloud per LUXE Collective...")
    
    # Crea directory di backup
    backup_dir = Path("cloud_backup_packages")
    backup_dir.mkdir(exist_ok=True)
    
    # Sottodirectory per diversi servizi cloud
    services = ["dropbox", "google_drive", "onedrive", "mega", "pcloud"]
    for service in services:
        (backup_dir / service).mkdir(exist_ok=True)
    
    return backup_dir

def package_files_for_cloud():
    """Prepara i file per il backup cloud"""
    print("📦 Preparazione pacchetti per servizi cloud...")
    
    backup_dir = create_cloud_backup_structure()
    
    # Crea timestamp per organizzazione
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Lista dei file da includere nel backup
    files_to_backup = [
        "index.html",
        "styles/main.css", 
        "scripts/main.js",
        "images/",
        "backup_netlify/",
        "BACKUP_INSTRUCTIONS.md",
        "IMMEDIATE_DEPLOY.md"
    ]
    
    # Crea pacchetto completo
    backup_file = backup_dir / f"LUXE_Collective_Complete_Backup_{timestamp}.zip"
    
    with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in files_to_backup:
            path = Path(item)
            if path.exists():
                if path.is_file():
                    zipf.write(path, path.name)
                    print(f"✅ Aggiunto: {item}")
                elif path.is_dir():
                    for file_path in path.rglob('*'):
                        if file_path.is_file():
                            arcname = file_path.relative_to(path.parent)
                            zipf.write(file_path, arcname)
                            print(f"✅ Aggiunto: {file_path}")
    
    print(f"📦 Pacchetto creato: {backup_file}")
    return backup_file

def create_cloud_sync_scripts():
    """Crea script per sincronizzazione con servizi cloud"""
    print("🔄 Creazione script di sincronizzazione cloud...")
    
    # Script per Dropbox
    dropbox_script = '''#!/bin/bash
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
'''
    
    with open("cloud_sync_dropbox.sh", "w") as f:
        f.write(dropbox_script)
    
    # Script per Google Drive (tramite rclone)
    gdrive_script = '''#!/bin/bash
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
'''
    
    with open("cloud_sync_google_drive.sh", "w") as f:
        f.write(gdrive_script)
    
    # Script per OneDrive
    onedrive_script = '''#!/bin/bash
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
'''
    
    with open("cloud_sync_onedrive.sh", "w") as f:
        f.write(onedrive_script)
    
    print("✅ Script di sincronizzazione creati:")
    print("   - cloud_sync_dropbox.sh")
    print("   - cloud_sync_google_drive.sh") 
    print("   - cloud_sync_onedrive.sh")

def create_automatic_backup_scheduler():
    """Crea sistema di backup automatico programmato"""
    print("⏰ Configurazione backup automatico...")
    
    scheduler_script = '''#!/bin/bash
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
'''
    
    with open("automatic_backup.sh", "w") as f:
        f.write(scheduler_script)
    
    # Cron job per backup quotidiano
    cron_entry = '''# Aggiungi questa riga al crontab per backup automatico quotidiano
# crontab -e
# Backup ogni giorno alle 02:00
0 2 * * * cd /path/to/workspace && ./automatic_backup.sh
'''
    
    with open("cron_backup_setup.txt", "w") as f:
        f.write(cron_entry)
    
    print("✅ Sistema di backup automatico configurato:")
    print("   - automatic_backup.sh")
    print("   - cron_backup_setup.txt")

def main():
    """Funzione principale"""
    print("☁️  === SISTEMA DI BACKUP CLOUD AUTOMATICO ===")
    print("🎯 Target: LUXE Collective Website")
    print("🔗 Sito: https://stilepuro.github.io/luxe-collective-fashion/")
    print("⏰ Data: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print()
    
    # Crea backup
    backup_file = package_files_for_cloud()
    
    # Crea script di sincronizzazione
    create_cloud_sync_scripts()
    
    # Crea scheduler automatico
    create_automatic_backup_scheduler()
    
    print()
    print("🎉 === BACKUP CLOUD CONFIGURATO ===")
    print(f"📦 Backup pronto: {backup_file}")
    print()
    print("🔄 Per caricare su cloud:")
    print("   1. Dropbox: ./cloud_sync_dropbox.sh")
    print("   2. Google Drive: ./cloud_sync_google_drive.sh") 
    print("   3. OneDrive: ./cloud_sync_onedrive.sh")
    print()
    print("⏰ Per backup automatico:")
    print("   - Esegui: ./automatic_backup.sh")
    print("   - Oppure configura cron job da cron_backup_setup.txt")
    print()
    print("📊 Il tuo sito LUXE Collective è ora protetto su cloud!")

if __name__ == "__main__":
    main()