#!/bin/bash
# Script Maestro per Backup Cloud Completo
# Esegui: chmod +x master_cloud_backup.sh && ./master_cloud_backup.sh

echo "☁️ === MASTER BACKUP CLOUD LUXE COLLECTIVE ==="
echo "🎯 Target: https://stilepuro.github.io/luxe-collective-fashion/"
echo "⏰ Data: $(date)"
echo ""

# Funzione per verificare servizi cloud
check_cloud_service() {
    local service_name="$1"
    local service_path="$2"
    
    if [ -d "$service_path" ]; then
        echo "✅ $service_name: Disponibile"
        return 0
    else
        echo "⚠️  $service_name: Non trovato"
        return 1
    fi
}

# Funzione per creare backup
create_backup() {
    echo "📦 Creazione backup aggiornato..."
    
    BACKUP_FILE="luxe-collective-backup-cloud-$(date +%Y%m%d_%H%M%S).zip"
    
    zip -r "$BACKUP_FILE" \
        index.html \
        styles/ \
        scripts/ \
        images/ \
        backup_netlify/ \
        BACKUP_INSTRUCTIONS.md \
        IMMEDIATE_DEPLOY.md \
        CLOUD_BACKUP_GUIDE.md \
        2>/dev/null
    
    if [ -f "$BACKUP_FILE" ]; then
        echo "✅ Backup creato: $BACKUP_FILE"
        echo "📊 Dimensione: $(du -h "$BACKUP_FILE" | cut -f1)"
        echo "$BACKUP_FILE"
    else
        echo "❌ Errore nella creazione del backup"
        exit 1
    fi
}

# Funzione per caricare su servizi cloud
upload_to_cloud() {
    local backup_file="$1"
    local service="$2"
    local service_path="$3"
    
    if [ -d "$service_path" ]; then
        BACKUP_DIR="$service_path/LUXE_Collective_Backup"
        mkdir -p "$BACKUP_DIR"
        
        cp "$backup_file" "$BACKUP_DIR/"
        echo "📤 Caricato su $service: $BACKUP_DIR/$backup_file"
    else
        echo "📝 $service: Caricamento manuale richiesto"
    fi
}

echo "🔍 Verifica servizi cloud disponibili..."
echo ""

# Verifica servizi cloud
DROPBOX_AVAILABLE=false
ONEDRIVE_AVAILABLE=false
GOOGLE_DRIVE_AVAILABLE=false

if check_cloud_service "Dropbox" "$HOME/Dropbox"; then
    DROPBOX_AVAILABLE=true
fi

if check_cloud_service "OneDrive" "$HOME/OneDrive"; then
    ONEDRIVE_AVAILABLE=true
fi

echo ""

# Crea backup
BACKUP_FILE=$(create_backup)
echo ""

# Carica sui servizi disponibili
echo "☁️ Caricamento sui servizi cloud..."
echo ""

if [ "$DROPBOX_AVAILABLE" = true ]; then
    upload_to_cloud "$BACKUP_FILE" "Dropbox" "$HOME/Dropbox"
fi

if [ "$ONEDRIVE_AVAILABLE" = true ]; then
    upload_to_cloud "$BACKUP_FILE" "OneDrive" "$HOME/OneDrive"
fi

echo ""
echo "🎉 === BACKUP CLOUD COMPLETATO ==="
echo ""
echo "📦 Backup file: $BACKUP_FILE"
echo "🔗 Sito online: https://stilepuro.github.io/luxe-collective-fashion/"
echo ""
echo "📋 SERVIZI CLOUD CONFIGURATI:"
[ "$DROPBOX_AVAILABLE" = true ] && echo "   ✅ Dropbox: Caricato automaticamente"
[ "$DROPBOX_AVAILABLE" = false ] && echo "   📝 Dropbox: Carica manualmente su dropbox.com"

[ "$ONEDRIVE_AVAILABLE" = true ] && echo "   ✅ OneDrive: Caricato automaticamente"  
[ "$ONEDRIVE_AVAILABLE" = false ] && echo "   📝 OneDrive: Carica manualmente su onedrive.live.com"

echo ""
echo "📖 Leggi CLOUD_BACKUP_GUIDE.md per istruzioni dettagliate"
echo "🔄 Per backup automatici, configura un cron job"
echo ""
echo "🌟 Il tuo sito LUXE Collective è ora protetto su cloud!"