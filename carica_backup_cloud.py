#!/usr/bin/env python3
"""
CARICAMENTO CLOUD IMMEDIATO - LUXE COLLECTIVE
Esecuzione reale dell'upload su servizi cloud
"""

import requests
import zipfile
import os
import time

def create_and_upload():
    """Crea backup e carica immediatamente"""
    
    print("☁️ === BACKUP CLOUD IMMEDIATO LUXE COLLECTIVE ===")
    print("🔗 Sito originale: https://stilepuro.github.io/luxe-collective-fashion/")
    print(f"⏰ Inizio: {time.strftime('%H:%M:%S')}")
    print()
    
    # 1. Crea backup completo
    print("📦 Creazione backup completo...")
    backup_name = f"luxe-backup-{int(time.time())}.zip"
    
    with zipfile.ZipFile(backup_name, 'w') as zipf:
        # File principali del sito
        files = ["index.html", "styles/main.css", "scripts/main.js"]
        for file in files:
            if os.path.exists(file):
                zipf.write(file)
                print(f"✅ Aggiunto: {file}")
        
        # Directory images
        if os.path.exists("images"):
            for file in os.listdir("images"):
                if file.endswith(('.jpg', '.png', '.jpeg')):
                    zipf.write(f"images/{file}")
                    print(f"✅ Aggiunto: images/{file}")
        
        # Documentazione
        docs = ["CLOUD_BACKUP_GUIDE.md", "BACKUP_INSTRUCTIONS.md"]
        for doc in docs:
            if os.path.exists(doc):
                zipf.write(doc)
                print(f"✅ Aggiunto: {doc}")
    
    size_mb = os.path.getsize(backup_name) / (1024*1024)
    print(f"📊 Backup creato: {backup_name} ({size_mb:.1f} MB)")
    print()
    
    # 2. Upload su file.io (servizio più affidabile)
    print("🌐 Upload su file.io...")
    try:
        with open(backup_name, 'rb') as f:
            response = requests.post('https://file.io', files={'file': f}, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                link = data.get('link')
                print("✅ FILE.IO: SUCCESSO!")
                print(f"🔗 Link backup: {link}")
                
                # Salva il link
                with open('backup_cloud_links.txt', 'w') as file:
                    file.write(f"BACKUP LUXE COLLECTIVE\n")
                    file.write(f"Data: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    file.write(f"File: {backup_name}\n")
                    file.write(f"File.io: {link}\n")
                
                print("💾 Link salvato in: backup_cloud_links.txt")
                return True, link, backup_name
            else:
                print(f"❌ FILE.IO: Errore - {data}")
                return False, "Errore upload", backup_name
        else:
            print(f"❌ FILE.IO: HTTP Error {response.status_code}")
            return False, f"HTTP {response.status_code}", backup_name
            
    except Exception as e:
        print(f"❌ FILE.IO: Errore di connessione - {str(e)}")
        return False, str(e), backup_name

def main():
    """Funzione principale"""
    success, link, backup_file = create_and_upload()
    
    print()
    print("🎉 === RISULTATO FINALE ===")
    if success:
        print("✅ BACKUP CLOUD COMPLETATO!")
        print(f"📦 File: {backup_file}")
        print(f"🔗 Link: {link}")
        print()
        print("💡 Se il sito si rompe:")
        print("1. Scarica: " + link)
        print("2. Estrai il ZIP")
        print("3. Ricarica su hosting")
        print()
        print("🌟 Il tuo sito LUXE Collective è ora al sicuro su cloud!")
    else:
        print("❌ Upload fallito, ma backup locale creato")
        print(f"📦 Backup locale: {backup_file}")
        print("💡 Per backup cloud manuale:")
        print("1. Vai su https://file.io")
        print(f"2. Carica il file: {backup_file}")

if __name__ == "__main__":
    main()