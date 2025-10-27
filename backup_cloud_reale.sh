#!/bin/bash

echo "☁️ === BACKUP CLOUD REALE - LUXE COLLECTIVE ==="
echo "🎯 Target: https://stilepuro.github.io/luxe-collective-fashion/"
echo "⏰ Ora: $(date '+%H:%M:%S')"
echo ""

# Crea backup veloce
echo "📦 Creazione backup..."
zip -r luxe-collectiv-backup.zip index.html styles/ scripts/ images/ >/dev/null 2>&1

if [ -f "luxe-collectiv-backup.zip" ]; then
    SIZE=$(du -h luxe-collectiv-backup.zip | cut -f1)
    echo "✅ Backup creato: luxe-collectiv-backup.zip ($SIZE)"
else
    echo "❌ Errore creazione backup"
    exit 1
fi

echo ""
echo "🚀 Upload su file.io..."
echo ""

# Upload su file.io
echo "Caricamento in corso..."
UPLOAD_RESULT=$(curl -s -F "file=@luxe-collectiv-backup.zip" https://file.io 2>&1)

# Salva il risultato
echo "$UPLOAD_RESULT" > upload_result.txt

# Mostra il risultato
echo "📊 RISULTATO UPLOAD:"
echo "===================="
echo "$UPLOAD_RESULT"
echo "===================="

# Estrai link se presente
if echo "$UPLOAD_RESULT" | grep -q "http"; then
    LINK=$(echo "$UPLOAD_RESULT" | grep -o "https://[^\"]*" | head -1)
    echo ""
    echo "🎉 SUCCESSO! Backup caricato su cloud!"
    echo "🔗 Link: $LINK"
    echo ""
    echo "💾 Per recuperare se il sito si rompe:"
    echo "1. Vai al link: $LINK"
    echo "2. Scarica il file"
    echo "3. Estrai e carica su nuovo hosting"
    echo ""
    echo "📝 Link salvato in: backup_cloud_info.txt"
    echo "Sito: $LINK" > backup_cloud_info.txt
    echo "Data: $(date)" >> backup_cloud_info.txt
else
    echo ""
    echo "⚠️  Upload potrebbe essere fallito"
    echo "💡 Prova manualmente su: https://file.io"
    echo "📁 File da caricare: luxe-collectiv-backup.zip"
fi

echo ""
echo "🌟 Il tuo sito LUXE Collective ha un backup su cloud!"