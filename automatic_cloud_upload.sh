#!/bin/bash
# Sistema di Upload Cloud Automatico LUXE Collective
# Upload simultaneo su 4 servizi cloud senza autenticazione

echo "☁️ === UPLOAD AUTOMATICO CLOUD LUXE COLLECTIVE ==="
echo "🎯 Target: Backup completo per cloud storage multiplo"
echo "🔗 Sito originale: https://stilepuro.github.io/luxe-collective-fashion/"
echo "⏰ Inizio: $(date)"
echo ""

# Crea backup se non esiste
if ls *luxe-collective-backup*.zip >/dev/null 2>&1; then
    BACKUP_FILE=$(ls -t *luxe-collective-backup*.zip | head -1)
    echo "📦 Usando backup esistente: $BACKUP_FILE"
else
    echo "📦 Creazione backup..."
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    BACKUP_FILE="luxe-collective-backup-cloud-${TIMESTAMP}.zip"
    
    zip -r "$BACKUP_FILE" \
        index.html \
        styles/ \
        scripts/ \
        images/ \
        backup_netlify/ \
        BACKUP_INSTRUCTIONS.md \
        IMMEDIATE_DEPLOY.md \
        CLOUD_BACKUP_GUIDE.md \
        automatic_cloud_upload.py \
        automatic_cloud_upload.sh \
        >/dev/null 2>&1
    
    if [ -f "$BACKUP_FILE" ]; then
        SIZE_MB=$(du -h "$BACKUP_FILE" | cut -f1)
        echo "✅ Backup creato: $BACKUP_FILE ($SIZE_MB)"
    else
        echo "❌ Errore nella creazione del backup"
        exit 1
    fi
fi

echo ""
echo "🚀 === UPLOAD SU SERVIZI CLOUD ==="
echo ""

# Funzione per upload con gestione errori
upload_to_service() {
    local service_name="$1"
    local upload_url="$2"
    
    echo "🔄 $service_name..."
    
    # Upload con timeout e gestione errori
    response=$(curl -s -F "file=@${BACKUP_FILE}" \
                    --max-time 30 \
                    --connect-timeout 10 \
                    --write-out "HTTP_CODE:%{http_code}" \
                    "$upload_url" 2>/dev/null)
    
    http_code=$(echo "$response" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)
    content=$(echo "$response" | sed 's/HTTP_CODE:[0-9]*$//')
    
    if [ "$http_code" = "200" ] || [ "$http_code" = "201" ]; then
        echo "✅ $service_name: SUCCESSO!"
        echo "📊 Risposta: $content"
        
        # Estrai link se disponibile
        if echo "$content" | grep -q "http"; then
            link=$(echo "$content" | grep -o "http[s]*://[^\s]*" | head -1)
            echo "🔗 Link: $link"
        fi
        
        return 0
    else
        echo "❌ $service_name: FALLITO (HTTP $http_code)"
        echo "📊 Risposta: $content"
        return 1
    fi
}

# Upload su servizi multipli
declare -A results
success_count=0

# 1. tmpfiles.org (60 minuti)
echo "=== 1. TMPFILES.ORG ==="
if upload_to_service "tmpfiles.org" "https://tmpfiles.org/api/v1/upload"; then
    ((success_count++))
    results[tmpfiles]="SUCCESS"
else
    results[tmpfiles]="FALLITO"
fi
echo ""

# 2. file.io
echo "=== 2. FILE.IO ==="
if upload_to_service "file.io" "https://file.io"; then
    ((success_count++))
    results[fileio]="SUCCESS"
else
    results[fileio]="FALLITO"
fi
echo ""

# 3. 0x0.st
echo "=== 3. 0x0.ST ==="
if upload_to_service "0x0.st" "https://0x0.st"; then
    ((success_count++))
    results[0x0st]="SUCCESS"
else
    results[0x0st]="FALLITO"
fi
echo ""

# 4. transfer.sh
echo "=== 4. TRANSFER.SH ==="
upload_url="https://transfer.sh/${BACKUP_FILE}"
echo "🔄 transfer.sh..."
response=$(curl -s --upload-file "$BACKUP_FILE" \
                --max-time 30 \
                --connect-timeout 10 \
                --write-out "HTTP_CODE:%{http_code}" \
                "$upload_url" 2>/dev/null)
http_code=$(echo "$response" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)
content=$(echo "$response" | sed 's/HTTP_CODE:[0-9]*$//')

if [ "$http_code" = "200" ] || [ "$http_code" = "201" ]; then
    echo "✅ transfer.sh: SUCCESSO!"
    echo "🔗 Link: $content"
    ((success_count++))
    results[transfer]="SUCCESS"
else
    echo "❌ transfer.sh: FALLITO (HTTP $http_code)"
    results[transfer]="FALLITO"
fi
echo ""

# Risultati finali
echo "🎉 === UPLOAD COMPLETATI ==="
echo ""
echo "📊 RISULTATI FINALI:"
echo "============================================"
echo "tmpfiles.org  | ${results[tmpfiles]}"
echo "file.io       | ${results[fileio]}"
echo "0x0.st        | ${results[0x0st]}"
echo "transfer.sh   | ${results[transfer]}"
echo "============================================"
echo "SUCCESSO: $success_count/4 servizi"
echo "BACKUP: $BACKUP_FILE"
echo "DATA: $(date)"
echo ""

if [ $success_count -ge 2 ]; then
    echo "🎉 === BACKUP CLOUD COMPLETATO! ==="
    echo "💾 Il tuo sito LUXE Collective è ora sicuro su cloud!"
    echo "🔗 Sito originale: https://stilepuro.github.io/luxe-collective-fashion/"
    echo ""
    echo "☁️ SERVIZI ATTIVATI:"
    [ "${results[tmpfiles]}" = "SUCCESS" ] && echo "   ✅ tmpfiles.org (temporaneo 60min)"
    [ "${results[fileio]}" = "SUCCESS" ] && echo "   ✅ file.io"
    [ "${results[0x0st]}" = "SUCCESS" ] && echo "   ✅ 0x0.st"
    [ "${results[transfer]}" = "SUCCESS" ] && echo "   ✅ transfer.sh"
    echo ""
    echo "💡 Per backup permanenti, carica i file manualmente su:"
    echo "   - Dropbox (https://dropbox.com)"
    echo "   - Google Drive (https://drive.google.com)"
    echo "   - OneDrive (https://onedrive.live.com)"
else
    echo "⚠️  Pochi upload riusciti. Prova di nuovo o controlla la connessione."
fi

# Salva log dei risultati
{
    echo "=== LOG UPLOAD CLOUD LUXE COLLECTIVE ==="
    echo "DATA: $(date)"
    echo "BACKUP: $BACKUP_FILE"
    echo "SUCCESSI: $success_count/4"
    echo ""
    echo "DETTAGLI:"
    echo "tmpfiles.org: ${results[tmpfiles]}"
    echo "file.io: ${results[fileio]}"
    echo "0x0.st: ${results[0x0st]}"
    echo "transfer.sh: ${results[transfer]}"
} > cloud_upload_log.txt

echo "📝 Log salvato in: cloud_upload_log.txt"