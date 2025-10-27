#!/bin/bash
# Upload Cloud Super Semplice - LUXE Collective
# Esegui: bash upload_cloud_simple.sh

echo "☁️ === UPLOAD CLOUD SUPER SEMPLICE ==="
echo "🎯 Backup: Sito LUXE Collective"
echo "🔗 Sito: https://stilepuro.github.io/luxe-collective-fashion/"
echo ""

# Crea backup veloce
echo "📦 Creazione backup veloce..."
zip -r luxe-collective-cloud.zip index.html styles/ scripts/ images/ CLOUD_BACKUP_GUIDE.md 2>/dev/null

if [ ! -f "luxe-collective-cloud.zip" ]; then
    echo "❌ Errore creazione backup"
    exit 1
fi

SIZE=$(du -h luxe-collective-cloud.zip | cut -f1)
echo "✅ Backup creato: luxe-collective-cloud.zip ($SIZE)"
echo ""

# Upload su servizi semplici
echo "🚀 Upload automatico su servizi cloud..."
echo ""

# File.io (più affidabile)
echo "1️⃣ Caricamento su file.io..."
RESULT1=$(curl -s -F "file=@luxe-collective-cloud.zip" https://file.io 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✅ file.io: SUCCESSO!"
    echo "📊 $RESULT1"
else
    echo "❌ file.io: Fallito"
fi
echo ""

# Transfer.sh (veloce)
echo "2️⃣ Caricamento su transfer.sh..."
RESULT2=$(curl -s --upload-file luxe-collective-cloud.zip https://transfer.sh/luxe-collective-cloud.zip 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✅ transfer.sh: SUCCESSO!"
    echo "🔗 Link: $RESULT2"
else
    echo "❌ transfer.sh: Fallito"
fi
echo ""

echo "🎉 === UPLOAD SEMPLICE COMPLETATO ==="
echo "💾 Backup: luxe-collective-cloud.zip"
echo "📁 I file sono ora su cloud!"
echo ""
echo "🔗 Per backup permanenti, vai su:"
echo "   • https://dropbox.com"
echo "   • https://drive.google.com" 
echo "   • https://onedrive.live.com"