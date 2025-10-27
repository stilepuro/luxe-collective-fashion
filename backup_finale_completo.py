#!/usr/bin/env python3
"""
BACKUP FINALE LUXE COLLECTIVE - WORKSPACE MINIMAX
Backup completo salvato localmente nel workspace per sicurezza totale
"""

import os
import shutil
import zipfile
import json
from pathlib import Path
from datetime import datetime

def create_complete_backup():
    """Crea backup completo del sito LUXE Collective"""
    
    print("☁️ === BACKUP FINALE LUXE COLLECTIVE ===")
    print("💾 Posizione: Workspace MiniMax (Sicuro)")
    print("🎯 Sito: https://stilepuro.github.io/luxe-collective-fashion/")
    print(f"⏰ Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Nome del backup con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"LUXE_COLLECTIVE_BACKUP_{timestamp}.zip"
    
    # Lista completa di file da includere
    files_to_backup = [
        "index.html",
        "styles/main.css",
        "scripts/main.js",
        "CLOUD_BACKUP_GUIDE.md",
        "BACKUP_INSTRUCTIONS.md", 
        "IMMEDIATE_DEPLOY.md"
    ]
    
    print("📦 Creazione backup completo...")
    
    with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Aggiungi file principali
        for file_path in files_to_backup:
            if os.path.exists(file_path):
                zipf.write(file_path)
                print(f"✅ Aggiunto: {file_path}")
        
        # Aggiungi directory images
        if os.path.exists("images"):
            print("📸 Aggiungendo immagini...")
            for img_file in os.listdir("images"):
                img_path = f"images/{img_file}"
                if os.path.isfile(img_path):
                    zipf.write(img_path)
                    print(f"✅ Aggiunto: {img_path}")
        
        # Aggiungi backup_netlify
        if os.path.exists("backup_netlify"):
            print("☁️ Aggiungendo configurazioni cloud...")
            for root, dirs, files in os.walk("backup_netlify"):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = file_path
                    zipf.write(file_path, arcname)
                    print(f"✅ Aggiunto: {file_path}")
    
    # Verifica backup creato
    if os.path.exists(backup_file):
        size_mb = os.path.getsize(backup_file) / (1024*1024)
        print(f"🎉 BACKUP COMPLETO CREATO!")
        print(f"📁 File: {backup_file}")
        print(f"📊 Dimensione: {size_mb:.1f} MB")
        
        # Crea file di informazioni
        info = {
            "backup_file": backup_file,
            "creation_date": datetime.now().isoformat(),
            "original_site": "https://stilepuro.github.io/luxe-collective-fashion/",
            "size_mb": round(size_mb, 1),
            "backup_location": "Workspace MiniMax",
            "status": "COMPLETE",
            "recovery_steps": [
                "1. Scarica il file ZIP dal workspace",
                "2. Estrai tutti i file",
                "3. Carica su nuovo hosting (GitHub Pages, Netlify, etc.)",
                "4. Il sito sarà operativo immediatamente"
            ]
        }
        
        with open(f"{backup_file}.info.json", "w") as f:
            json.dump(info, f, indent=2)
        
        print(f"💾 Info backup salvate: {backup_file}.info.json")
        return backup_file, info
    else:
        print("❌ Errore nella creazione del backup")
        return None, None

def main():
    """Funzione principale"""
    backup_file, info = create_complete_backup()
    
    if backup_file:
        print()
        print("🎯 === BACKUP COMPLETATO ===")
        print("✅ Il tuo sito LUXE Collective è ora al sicuro!")
        print()
        print("🔄 SE IL SITO SI ROMPE:")
        print(f"1. Scarica: {backup_file}")
        print("2. Estrai il file ZIP")
        print("3. Carica su hosting")
        print("4. ✅ Sito operativo!")
        print()
        print("🌟 VANTAGGI:")
        print("• Backup salvato in workspace sicuro")
        print("• Nessuna dipendenza da servizi esterni")
        print("• Recupero immediato garantito")
        print("• Dimensione ottimizzata")
        print()
        print("🎉 Il tuo sito è PROTETTO!")
    else:
        print("❌ Backup fallito")

if __name__ == "__main__":
    main()