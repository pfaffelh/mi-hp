import os
import shutil
from pathlib import Path

def find_matching_file(file_name, search_path):
    """Find a file with the same name anywhere in the given search path."""
    for file in search_path.rglob("*"):
        if file.is_file() and file.name == file_name:
            return file
    return None

def sync_folders(static_dir: str, bw_dir: str):
    static_path = Path(static_dir)
    bw_path = Path(bw_dir)
    
    for static_file in static_path.rglob("*"):
        if static_file.is_file():
            bw_file = find_matching_file(static_file.name, bw_path)
            
            if bw_file:
                if bw_file.stat().st_mtime > static_file.stat().st_mtime:
                    shutil.copy2(bw_file, static_file)
                    print(f"\033[92mNeue Version von {static_file} aus {bw_file} überspielt.")
                else:
                    print(f"\033[0m{static_file} ist bereits die neueste Version.")
            else:
                print(f"\033[91m{static_file} in {bw_path} nicht gefunden.")

if __name__ == "__main__":
    sync_folders("pdf/lehrende", "/home/pfaffelh/bwsynchandshare/Formulare")
    sync_folders("pdf/pruefungsamt", "/home/pfaffelh/bwsynchandshare/Formulare")
    sync_folders("pdf/studiengaenge/promotion", "/home/pfaffelh/bwsynchandshare/Formulare")
