import subprocess
import utils
import sys

def check_and_install_tidal_dl():
    try:
        # pip install --upgrade tidal-dl-ng first?
        result = subprocess.run(["tidal-dl-ng", "--version"], capture_output=True, text=True)
        print('> tidal-dl-ng installed version', result.stdout,)
        if result.returncode != 0:
            raise Exception("tidal-dl-ng not installed")
    except Exception:
        print("> tidal-dl-ng not found, installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "tidal-dl-ng"])

def default_Settings():
    check_and_install_tidal_dl()
    data = utils.load_json('td_downloader-config.json');
    utils.save_downloader_settings(data)

def check_login():
    result = subprocess.run(["tidal-dl-ng", "login"], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)

def download_playlist(playlist_id, timeout=60):
    check_and_install_tidal_dl()
    
    playlist_link = f"https://tidal.com/browse/playlist/{playlist_id}"
    command = ["tidal-dl-ng", "dl", playlist_link]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        print(result.stdout)
        print(result.stderr)
    except subprocess.TimeoutExpired:
        print(f"> timed out after {timeout} seconds.\n> please go to settings> download troubleshooting")
