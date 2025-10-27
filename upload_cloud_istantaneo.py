#!/usr/bin/env python3
"""
Sistema di Upload Cloud Istantaneo
Caricamento immediato su cloud senza dipendenze complesse
"""

import os
import requests
import time

def create_simple_backup():
    """Crea backup semplificato"""
    print("📦 Creazione backup semplice...")
    
    # Import per creazione ZIP
    import zipfile
    
    files_to_zip = [
        "index.html",
        "styles/main.css", 
        "scripts/main.js",
        "CLOUD_BACKUP_GUIDE.md"
    ]
    
    backup_name = f"luxe-collective-backup-{int(time.time())}.zip"
    
    with zipfile.ZipFile(backup_name, 'w') as zipf:
        for file_path in files_to_zip:
            if os.path.exists(file_path):
                zipf.write(file_path)
                print(f"✅ Aggiunto: {file_path}")
    
    print(f"📦 Backup creato: {backup_name}")
    return backup_name

def upload_to_fileio(file_path):
    """Upload su file.io"""
    print("\n🔄 Upload su file.io...")
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post('https://file.io', files=files, timeout=30)
            
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                link = data.get('link', 'N/A')
                print(f"✅ file.io: SUCCESSO!")
                print(f"🔗 Link: {link}")
                return True, link
            else:
                print(f"❌ file.io: Fallito - {data}")
                return False, str(data)
        else:
            print(f"❌ file.io: Errore HTTP {response.status_code}")
            return False, f"HTTP {response.status_code}"
            
    except Exception as e:
        print(f"❌ file.io: Eccezione - {str(e)}")
        return False, str(e)

def upload_to_transfer(file_path):
    """Upload su transfer.sh"""
    print("\n🔄 Upload su transfer.sh...")
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f)}
            response = requests.post(f'https://transfer.sh/{file_path}', files=files, timeout=30)
            
        if response.status_code == 200:
            link = response.text.strip()
            print(f"✅ transfer.sh: SUCCESSO!")
            print(f"🔗 Link: {link}")
            return True, link
        else:
            print(f"❌ transfer.sh: Errore HTTP {response.status_code}")
            return False, f"HTTP {response.status_code}"
            
    except Exception as e:
        print(f"❌ transfer.sh: Eccezione - {str(e)}")
        return False, str(e)

def main():
    """Funzione principale"""
    print("☁️ === UPLOAD CLOUD ISTANTANEO ===")
    print("🎯 Target: LUXE Collective Website")
    print("🔗 Sito: https://stilepuro.github.io/luxe-collective-fashion/")
    print(f"⏰ Inizio: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Crea backup
    backup_file = create_simple_backup()
    
    print("\n" + "="*50)
    print("🚀 UPLOAD SU SERVIZI CLOUD")
    print("="*50)
    
    results = {}
    
    # Upload su file.io
    success1, link1 = upload_to_fileio(backup_file)
    results['file.io'] = {'success': success1, 'link': link1}
    
    # Upload su transfer.sh  
    success2, link2 = upload_to_transfer(backup_file)
    results['transfer.sh'] = {'success': success2, 'link': link2}
    
    # Risultati
    print("\n" + "="*50)
    print("🎉 === RISULTATI FINALI ===")
    print("="*50)
    
    for service, result in results.items():
        status = "✅ SUCCESSO" if result['success'] else "❌ FALLITO"
        print(f"{service:15} | {status}")
        if result['success'] and result['link'] != 'N/A':
            print(f"{'':15} | 🔗 {result['link']}")
        print("-" * 40)
    
    successful = sum(1 for r in results.values() if r['success'])
    print(f"\n📊 SUCCESSO: {successful}/2 servizi")
    
    if successful >= 1:
        print("\n🎉 === BACKUP CLOUD RIUSCITO! ===")
        print("💾 Il tuo sito LUXE Collective è ora su cloud!")
        print("🔗 Sito originale: https://stilepuro.github.io/luxe-collective-fashion/")
        
        # Salva risultati
        with open('cloud_results_simple.txt', 'w') as f:
            f.write(f"UPLOAD CLOUD LUXE COLLECTIVE\n")
            f.write(f"Data: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Backup: {backup_file}\n")
            f.write(f"Risultati: {results}\n")
        
        print("📝 Risultati salvati in: cloud_results_simple.txt")
    else:
        print("\n⚠️  Upload falliti. Prova:")
        print("1. Controlla connessione internet")
        print("2. Esegui: bash upload_cloud_simple.sh")
        print("3. Upload manuale su https://file.io o https://transfer.sh")

if __name__ == "__main__":
    main()