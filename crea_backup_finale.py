import zipfile
import os
from pathlib import Path

print("☁️ === CREAZIONE BACKUP COMPLETO LUXE COLLECTIVE ===")
print("🎯 Target: https://stilepuro.github.io/luxe-collective-fashion/")
print("💾 Backup: Workspace MiniMax (Sicuro e Locale)")
print()

# Crea backup completo
backup_name = "luxe-collective-backup-completo.zip"

with zipfile.ZipFile(backup_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # File principali del sito
    files_to_include = [
        "index.html",
        "styles/main.css", 
        "scripts/main.js"
    ]
    
    print("📦 Aggiungendo file del sito...")
    for file in files_to_include:
        if os.path.exists(file):
            zipf.write(file)
            print(f"✅ Aggiunto: {file}")
    
    # Directory images
    if os.path.exists("images"):
        print("📸 Aggiungendo immagini...")
        for img in os.listdir("images"):
            if img.lower().endswith(('.jpg', '.png', '.jpeg', '.webp')):
                img_path = f"images/{img}"
                zipf.write(img_path)
                print(f"✅ Aggiunto: {img_path}")
    
    # Backup configuration files
    config_files = [
        "CLOUD_BACKUP_GUIDE.md",
        "BACKUP_INSTRUCTIONS.md", 
        "IMMEDIATE_DEPLOY.md",
        "backup_netlify/index.html",
        "backup_netlify/netlify.toml"
    ]
    
    print("📋 Aggiungendo configurazioni...")
    for config in config_files:
        if os.path.exists(config):
            zipf.write(config)
            print(f"✅ Aggiunto: {config}")
    
    # Carica i backup esistenti se presenti
    backup_dir = Path("backup_netlify")
    if backup_dir.exists():
        print("☁️ Aggiungendo configurazioni cloud...")
        for file in backup_dir.rglob("*"):
            if file.is_file():
                zipf.write(str(file))
                print(f"✅ Aggiunto: {file}")

# Verifica dimensione
if os.path.exists(backup_name):
    size_mb = os.path.getsize(backup_name) / (1024*1024)
    print(f"📊 Backup creato: {backup_name}")
    print(f"📏 Dimensione: {size_mb:.1f} MB")
    print()
    print("✅ SUCCESSO! Il backup è pronto nel workspace MiniMax!")
else:
    print("❌ Errore nella creazione del backup")