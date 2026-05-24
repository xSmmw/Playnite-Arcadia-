import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

PLATFORM_MAP = {
    '.bin': 'PlayStation 1',
    '.cue': 'PlayStation 1', 
    '.iso': 'PlayStation 2',
    '.pkg': 'PlayStation 3',
    '.rpcs3': 'PlayStation 3',
    '.nsp': 'Nintendo Switch',
    '.xci': 'Nintendo Switch',
    '.nes': 'Nintendo NES',
    '.cia': 'Nintendo 3DS',
}

def refresh_arcadia():
     # This function talks to Arcadia in real time using PowerShell
    # It sends a command to Playnite to update the library immediately
    try:
        subprocess.run([
            "powershell", "-Command",
            "Start-Process 'playnite://playnite/updatelibrary'"
        ], timeout=5)
        print("🔄 Arcadia library refresh requested!")
    except Exception as e:
        print(f"⚠️ Could not refresh Arcadia: {e}")

class GameDetector(FileSystemEventHandler):
    
    def on_created(self, event):
        if event.is_directory:
            return
        
        file_path = event.src_path
        file_extension = os.path.splitext(file_path)[1].lower()
        file_name = os.path.basename(file_path)
        
        if file_extension in PLATFORM_MAP:
            platform = PLATFORM_MAP[file_extension]
            print(f"✅ New game detected!")
            print(f"   File: {file_name}")
            print(f"   Platform: {platform}")
            print(f"   Path: {file_path}")
            print("-" * 40)
            
            # Tell Arcadia to refresh immediately
            refresh_arcadia()
        else:
            print(f"⚠️ Unknown file type: {file_extension} — skipping")

WATCH_FOLDER = "F:\\Shhh\\Game"

if not os.path.exists(WATCH_FOLDER):
    os.makedirs(WATCH_FOLDER)
    print(f"📁 Games folder: {WATCH_FOLDER}")

print(f"👀 Arcadia Nexus watching: {WATCH_FOLDER}")
print("Drop a game file in the folder to test...")
print("-" * 40)

observer = Observer()
observer.schedule(GameDetector(), WATCH_FOLDER, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
    print("\n🛑 Arcadia Nexus stopped")

observer.join()