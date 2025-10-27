#!/usr/bin/env python3
"""
Upload Automatico LUXE Collective su Cloud Multiplo
Carica automaticamente su 4 servizi cloud in parallelo
"""

import subprocess
import json
import os
import time
from pathlib import Path

def upload_to_tmpfiles(backup_file):
    """Carica su tmpfiles.org (60 minuti)"""
    print("🔄 Caricamento su tmpfiles.org...")
    try:
        cmd = [
            "curl", "-F", f"file=@{backup_file}",
            "https://tmpfiles.org/api/v1/upload"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ tmpfiles.org: Upload riuscito!")
            print(f"📊 Risposta: {result.stdout.strip()}")
            return True, result.stdout.strip()
        else:
            print(f"❌ tmpfiles.org: Errore - {result.stderr}")
            return False, result.stderr
    except Exception as e:
        print(f"❌ tmpfiles.org: Eccezione - {str(e)}")
        return False, str(e)

def upload_to_fileio(backup_file):
    """Carica su file.io"""
    print("🔄 Caricamento su file.io...")
    try:
        cmd = [
            "curl", "-F", f"file=@{backup_file}",
            "https://file.io"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ file.io: Upload riuscito!")
            try:
                data = json.loads(result.stdout)
                if data.get('success'):
                    link = data.get('link', 'N/A')
                    print(f"🔗 Link: {link}")
                    return True, link
                else:
                    print(f"❌ file.io: Upload fallito - {result.stdout}")
                    return False, result.stdout
            except json.JSONDecodeError:
                print(f"📊 Risposta file.io: {result.stdout.strip()}")
                return True, result.stdout.strip()
        else:
            print(f"❌ file.io: Errore - {result.stderr}")
            return False, result.stderr
    except Exception as e:
        print(f"❌ file.io: Eccezione - {str(e)}")
        return False, str(e)

def upload_to_0x0st(backup_file):
    """Carica su 0x0.st"""
    print("🔄 Caricamento su 0x0.st...")
    try:
        cmd = [
            "curl", "-F", f"file=@{backup_file}",
            "https://0x0.st"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 0x0.st: Upload riuscito!")
            link = result.stdout.strip()
            print(f"🔗 Link: {link}")
            return True, link
        else:
            print(f"❌ 0x0.st: Errore - {result.stderr}")
            return False, result.stderr
    except Exception as e:
        print(f"❌ 0x0.st: Eccezione - {str(e)}")
        return False, str(e)

def upload_to_transfer_sh(backup_file):
    """Carica su transfer.sh"""
    print("🔄 Caricamento su transfer.sh...")
    try:
        cmd = [
            "curl", "--upload-file", backup_file,
            f"https://transfer.sh/{backup_file.name}"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ transfer.sh: Upload riuscito!")
            link = result.stdout.strip()
            print(f"🔗 Link: {link}")
            return True, link
        else:
            print(f"❌ transfer.sh: Errore - {result.stderr}")
            return False, result.stderr
    except Exception as e:
        print(f"❌ transfer.sh: Eccezione - {str(e)}")
        return False, str(e)

def create_backup_if_not_exists():
    """Crea backup se non esiste"""
    backup_files = list(Path(".").glob("luxe-collective-backup-cloud-*.zip"))
    
    if backup_files:
        # Trova il più recente
        latest_backup = max(backup_files, key=lambda x: x.stat().st_mtime)
        print(f"📦 Usando backup esistente: {latest_backup.name}")
        return latest_backup
    
    # Crea nuovo backup
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_file = f"luxe-collective-backup-cloud-{timestamp}.zip"
    
    print("📦 Creazione nuovo backup...")
    files_to_include = [
        "index.html",
        "styles/",
        "scripts/", 
        "images/",
        "backup_netlify/",
        "BACKUP_INSTRUCTIONS.md",
        "IMMEDIATE_DEPLOY.md",
        "CLOUD_BACKUP_GUIDE.md"
    ]
    
    # Usa zip system command per massima compatibilità
    import zipfile
    with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in files_to_include:
            path = Path(item)
            if path.exists():
                if path.is_file():
                    zipf.write(path)
                elif path.is_dir():
                    for file_path in path.rglob('*'):
                        if file_path.is_file():
                            arcname = file_path.relative_to(path.parent)
                            zipf.write(file_path, arcname)
    
    size_mb = Path(backup_file).stat().st_size / (1024*1024)
    print(f"✅ Backup creato: {backup_file} ({size_mb:.1f} MB)")
    return Path(backup_file)

def main():
    """Funzione principale"""
    print("☁️ === UPLOAD AUTOMATICO LUXE COLLECTIVE ===")
    print("🎯 Target: Backup completo per cloud storage")
    print("🔗 Sito originale: https://stilepuro.github.io/luxe-collective-fashion/")
    print(f"⏰ Inizio: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Crea o trova backup
    backup_file = create_backup_if_not_exists()
    print()
    
    # Lista dei servizi e risultati
    services = [
        ("tmpfiles.org", upload_to_tmpfiles),
        ("file.io", upload_to_fileio), 
        ("0x0.st", upload_to_0x0st),
        ("transfer.sh", upload_to_transfer_sh)
    ]
    
    results = {}
    
    print("🚀 === UPLOAD SU SERVIZI CLOUD ===")
    print()
    
    # Upload su ogni servizio
    for service_name, upload_func in services:
        print(f"🔄 === {service_name.upper()} ===")
        success, link = upload_func(backup_file)
        results[service_name] = {"success": success, "link": link}
        print()
        
        # Piccola pausa tra upload
        time.sleep(2)
    
    # Risultati finali
    print("🎉 === UPLOAD COMPLETATI ===")
    print()
    print("📊 RISULTATI:")
    print("="*50)
    
    successful_uploads = 0
    for service, result in results.items():
        status = "✅ SUCCESSO" if result["success"] else "❌ FALLITO"
        print(f"{service:15} | {status}")
        if result["success"]:
            successful_uploads += 1
            if result["link"] != "N/A" and "http" in result["link"]:
                print(f"{'':15} | 🔗 {result['link']}")
        print("-" * 50)
    
    print()
    print(f"📈 SUCCESSO: {successful_uploads}/4 servizi")
    print(f"📦 Backup: {backup_file.name}")
    print(f"⏰ Completato: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if successful_uploads >= 2:
        print()
        print("🎉 === BACKUP CLOUD COMPLETATO CON SUCCESSO! ===")
        print("💾 Il tuo sito LUXE Collective è ora sicuro su cloud!")
        print("🔗 Sito originale: https://stilepuro.github.io/luxe-collective-fashion/")
        
        # Salva risultati per riferimento futuro
        with open("cloud_upload_results.json", "w") as f:
            json.dump({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "backup_file": str(backup_file),
                "results": results,
                "successful_uploads": successful_uploads,
                "total_services": len(services)
            }, f, indent=2)
        
        print("💾 Risultati salvati in: cloud_upload_results.json")
    else:
        print("⚠️  Pochi upload riusciti. Riprova o controlla la connessione.")

if __name__ == "__main__":
    main()