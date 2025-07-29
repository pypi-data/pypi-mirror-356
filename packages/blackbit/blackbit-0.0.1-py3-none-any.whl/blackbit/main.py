import sys
import os
import shutil
import time
import zipfile
import pickle
import io
import psutil
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from datetime import datetime
from cryptography.fernet import Fernet
from tqdm import tqdm
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import subprocess

# ------------------------------------------------------------------------
# GLOBALS
# ------------------------------------------------------------------------
TEMP_DIR = Path("temp")

# ------------------------------------------------------------------------
# UTILITY FUNCTIONS WITH ASCII-ONLY HACKER VIBE
# ------------------------------------------------------------------------
def slow_print(text, delay=0.02, newline=True):
    """Typewriter effect for any message."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    if newline:
        print()

def hacker_log(msg):
    """Success / OK style messages."""
    slow_print(f"\033[92m[OK]    {msg}\033[0m", delay=0.005)

def error_log(msg):
    """Error / failure style messages."""
    slow_print(f"\033[91m[ERROR] {msg}\033[0m", delay=0.005)

def info_log(msg):
    """Informational / status messages."""
    slow_print(f"\033[94m[INFO]  {msg}\033[0m", delay=0.01)

# ------------------------------------------------------------------------
# SETUP & CLEANUP
# ------------------------------------------------------------------------
def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def secure_delete(path, passes=3):
    try:
        path = Path(path)
        length = path.stat().st_size
        with path.open("r+b") as f:
            for _ in range(passes):
                f.seek(0)
                f.write(os.urandom(length))
        path.unlink()
        hacker_log(f"Securely deleted: {path}")
    except Exception as e:
        error_log(f"Secure delete failed: {e}")

# ------------------------------------------------------------------------
# GOOGLE DRIVE AUTH
# ------------------------------------------------------------------------
_CLIENT_CONFIG = {
    "installed": {
        "client_id": "689361682155-c1np2fdpf5e3vtenirku38648mt4p9fq.apps.googleusercontent.com",
        "project_id": "master-might-460013-s2",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "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",
        "redirect_uris": ["http://localhost"]
    }
}
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_drive():
    token_file = 'token.pickle'
    creds = None
    if os.path.exists(token_file):
        with open(token_file, 'rb') as f:
            creds = pickle.load(f)
    if not creds or not getattr(creds, 'valid', False):
        if creds and getattr(creds, 'expired', False) and getattr(creds, 'refresh_token', None):
            info_log("Refreshing Google Drive session...")
            creds.refresh(Request())
        else:
            info_log("Opening secure authorization window...")
            flow = InstalledAppFlow.from_client_config(_CLIENT_CONFIG, SCOPES)
            creds = flow.run_local_server(
                port=0,
                authorization_prompt_message='',
                success_message='\n[INFO] Authorization successful! You may close this tab.\n'
            )
        with open(token_file, 'wb') as f:
            pickle.dump(creds, f)
    return build('drive', 'v3', credentials=creds)

# ------------------------------------------------------------------------
# UPLOAD / DOWNLOAD
# ------------------------------------------------------------------------
def upload_to_drive(local_path, remote_name):
    svc = authenticate_drive()
    media = MediaFileUpload(local_path, resumable=True)
    try:
        req = svc.files().create(body={'name': remote_name}, media_body=media, fields='id')
        with tqdm(total=os.path.getsize(local_path), unit='B', unit_scale=True, desc="Uploading", ncols=100) as pbar:
            response = None
            while not response:
                status, response = req.next_chunk()
                if status:
                    pbar.update(status.resumable_progress - pbar.n)
        hacker_log(f"Uploaded to Drive: {remote_name}")
        return True
    except Exception as e:
        error_log(f"Upload failed: {e}")
        return False

def download_from_drive(remote_name, dest_path):
    svc = authenticate_drive()
    try:
        resp = svc.files().list(q=f"name='{remote_name}'", spaces='drive', fields='files(id,size)').execute()
        items = resp.get('files', [])
        if not items:
            error_log(f"{remote_name} not found on Drive")
            return False
        file_id, size = items[0]['id'], int(items[0].get('size', 0))
        fh = io.FileIO(dest_path, 'wb')
        downloader = MediaIoBaseDownload(fh, svc.files().get_media(fileId=file_id))
        with tqdm(total=size, unit='B', unit_scale=True, desc="Downloading", ncols=100) as pbar:
            done = False
            while not done:
                status, done = downloader.next_chunk()
                pbar.update(status.resumable_progress - pbar.n)
        hacker_log(f"Downloaded from Drive: {remote_name}")
        return True
    except Exception as e:
        error_log(f"Download failed: {e}")
        return False

# ------------------------------------------------------------------------
# USB DRIVE SELECTION
# ------------------------------------------------------------------------
def get_removable_drives():
    return [p.device for p in psutil.disk_partitions(all=False) if 'removable' in p.opts or 'cdrom' in p.opts]

def select_usb_drive():
    drives = get_removable_drives()
    if not drives:
        error_log("No USB drives detected")
        return None
    if len(drives) > 1:
        info_log("Multiple removable drives found:")
        for i, d in enumerate(drives, 1):
            print(f"  [{i}] {d}")
        while True:
            try:
                idx = int(input("Select USB drive #: ")) - 1
                if 0 <= idx < len(drives):
                    return drives[idx]
            except:
                pass
            error_log("Invalid selection")
    return drives[0]

# ------------------------------------------------------------------------
# ENCRYPT / DECRYPT HELPERS
# ------------------------------------------------------------------------
def generate_key():
    return Fernet.generate_key()

def save_key(key, path):
    with open(path, 'wb') as f:
        f.write(key)
    hacker_log(f"Key saved to USB: {Path(path).name}")

def encrypt_file(inp, outp, key):
    if not os.path.exists(inp):
        error_log(f"File not found: {inp}")
        return False
    try:
        f = Fernet(key)
        name_bytes = Path(inp).name.encode()
        header = len(name_bytes).to_bytes(4, 'big') + name_bytes
        total = os.path.getsize(inp)
        with open(inp, 'rb') as inf, open(outp, 'wb') as outf, \
             tqdm(total=total, unit='B', unit_scale=True, desc="Encrypting", ncols=100) as pbar:
            outf.write(header)
            pbar.update(len(header))
            while True:
                chunk = inf.read(64*1024)
                if not chunk:
                    break
                enc = f.encrypt(chunk)
                outf.write(len(enc).to_bytes(4, 'big') + enc)
                pbar.update(len(chunk))
        return True
    except Exception as e:
        error_log(f"Encryption failed: {e}")
        return False

def decrypt_file(inp, outdir, key):
    f = Fernet(key)
    with open(inp, 'rb') as inf:
        name_len = int.from_bytes(inf.read(4), 'big')
        fname = inf.read(name_len).decode()
    outp = Path(outdir) / fname
    ensure_dir(outdir)
    total = os.path.getsize(inp) - 4 - name_len
    with open(inp, 'rb') as inf, open(outp, 'wb') as outf, \
         tqdm(total=total, unit='B', unit_scale=True, desc="Decrypting", ncols=100) as pbar:
        inf.read(4 + name_len)
        while True:
            hdr = inf.read(4)
            if not hdr:
                break
            size = int.from_bytes(hdr, 'big')
            block = inf.read(size)
            dec = f.decrypt(block)
            outf.write(dec)
            pbar.update(size + 4)
    return str(outp)

# ------------------------------------------------------------------------
# ENCRYPTION WORKFLOW
# ------------------------------------------------------------------------
def encryption_workflow():
    ensure_dir(TEMP_DIR)
    usb = select_usb_drive()
    if not usb:
        return
    root = tk.Tk(); root.withdraw()
    paths = filedialog.askopenfilenames(title="Select files/folders")
    root.destroy()
    if not paths:
        error_log("No files selected")
        return
    all_files = []
    for p in paths:
        if os.path.isdir(p):
            for r, _, fs in os.walk(p):
                all_files += [os.path.join(r, f) for f in fs]
        else:
            all_files.append(p)
    src_name = (Path(os.path.commonpath(all_files)).name if len(all_files)>1 else Path(all_files[0]).stem)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    base = f"{src_name}_{timestamp}"

    key = generate_key()
    save_key(key, os.path.join(usb, f"{base}.key"))

    # create a temporary zip if needed
    if len(all_files) > 1:
        zip_path = TEMP_DIR / f"{base}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for fpath in all_files:
                zf.write(fpath, os.path.relpath(fpath, os.path.commonpath(all_files)))
        ...  # (all previous code remains unchanged)
        inp = zip_path
    else:
        inp = all_files[0]

    encf = TEMP_DIR / f"{base}.encrypted"
    encrypt_success = encrypt_file(inp, encf, key)
    if not encrypt_success:
        return
    hacker_log(f"Encryption complete: {encf}")

    if len(all_files) > 1 and zip_path.exists():
        secure_delete(zip_path)

    info_log("Choose storage destination for encrypted file:")
    print("  [1] Save locally")
    print("  [2] Upload to cloud only")
    print("  [3] Save locally & upload to cloud")
    print("  [4] Return to Home Menu")

    while True:
        c = input("\033[92m[>>] \033[0m Your choice: ").strip()
        if c in {'1','2','3'}:
            break
        elif c == '4':
            print("[BACK] Returning to Home Menu...")
            if encf.exists(): secure_delete(encf)
            key_path = Path(usb) / f"{base}.key"
            if key_path.exists(): secure_delete(key_path)
            return
        else:
            error_log("Invalid option. Choose 1–4.")

    if c in {'1','3'}:
        root = tk.Tk(); root.withdraw()
        save_path = filedialog.asksaveasfilename(
            title="Save encrypted file as…",
            defaultextension=".encrypted",
            initialfile=encf.name
        )
        root.destroy()
        if not save_path:
            error_log("Save cancelled")
            return
        try:
            shutil.move(str(encf), save_path)
        except Exception as e:
            info_log(f"Move failed ({e}); copying instead…")
            shutil.copy2(str(encf), save_path)
            secure_delete(encf)
        hacker_log(f"Saved locally at: {save_path}")
        upload_source = save_path
    else:
        upload_source = str(encf)

    if c in {'2','3'}:
        upload_to_drive(upload_source, Path(upload_source).name)

    if Path(encf).exists():
        secure_delete(encf)

# ------------------------------------------------------------------------
# DECRYPTION WORKFLOW
# ------------------------------------------------------------------------
def decryption_workflow():
    ensure_dir(TEMP_DIR)
    usb = select_usb_drive()
    if not usb:
        return

    info_log("Select Decryption Source:")
    print("  [1] Local Storage")
    print("  [2] Cloud Storage")
    print("  [3] Cancel")
    while True:
        choice = input("[>>] ").strip()
        if choice in {'1','2','3'}:
            break
        error_log("Invalid option. Choose 1-3.")
    if choice == '3':
        return

    # Local or cloud selection
    if choice == '1':
        root = tk.Tk(); root.withdraw()
        encf = filedialog.askopenfilename(
            title="Select encrypted file", initialdir=TEMP_DIR,
            filetypes=[("Encrypted","*.encrypted")]
        )
        root.destroy()
        if not encf:
            return
        keyf = filedialog.askopenfilename(
            title="Select key file", initialdir=usb,
            filetypes=[("Key","*.key")]
        )
        if not keyf:
            return
    else:
        # Cloud storage
        try:
            keys = [f for f in os.listdir(usb) if f.endswith('.key')]
        except Exception:
            error_log("USB drive not accessible.")
            return
        if not keys:
            error_log("No keys found on USB.")
            return
        info_log("Available keys:")
        for idx, k in enumerate(keys,1): print(f"  [{idx}] {k}")
        print("  [0] Cancel")
        while True:
            sel = input("Select key #:").strip()
            if sel == '0': return
            if sel.isdigit() and 1 <= int(sel) <= len(keys):
                keyf = os.path.join(usb, keys[int(sel)-1])
                break
            error_log("Enter a valid number.")
        base = Path(keyf).stem
        encf = TEMP_DIR / f"{base}.encrypted"
        if not download_from_drive(f"{base}.encrypted", encf):
            return

    # Load key and decrypt
    try:
        with open(keyf,'rb') as f: key = f.read()
    except Exception as e:
        error_log(f"Failed loading key: {e}")
        return

    decrypted = decrypt_file(encf, TEMP_DIR, key)
    if not decrypted:
        return
    hacker_log(f"Decryption complete: {decrypted}")

    # Save decrypted file
    root = tk.Tk(); root.withdraw()
    save_as = filedialog.asksaveasfilename(
        title="Save decrypted file as…",
        initialfile=Path(decrypted).name
    )
    root.destroy()
    if not save_as:
        error_log("Save canceled; file remains in temp.")
        return

    try:
        shutil.move(decrypted, save_as)
    except Exception as e:
        info_log(f"Move failed ({e}); copying instead…")
        shutil.copy2(decrypted, save_as)
        secure_delete(decrypted)
    hacker_log(f"Saved decrypted file at: {save_as}")

    # Cleanup encrypted blob
    if Path(encf).exists(): secure_delete(encf)

    # Open folder
    folder = Path(save_as).parent
    if sys.platform.startswith('win'):
        subprocess.Popen(['explorer', str(folder)])
    else:
        opener = 'open' if sys.platform=='darwin' else 'xdg-open'
        subprocess.Popen([opener, str(folder)])

# ------------------------------------------------------------------------
# MAIN ENTRY
# ------------------------------------------------------------------------
if __name__ == "__main__":
    ensure_dir(TEMP_DIR)
    slow_print("[BOOT] Blackbit v0.0.1..", 0.03)
    art = r"""/==================================================================\
||  ██████╗ ██╗      █████╗  ██████╗██╗  ██╗██████╗ ██╗████████╗  ||
||  ██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██║╚══██╔══╝  ||
||  ██████╔╝██║     ███████║██║     █████╔╝ ██████╞╝██║   ██║     ||
||  ██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██╔══██╗██║   ██║     ||
||  ███████╝███████╗██║  ██║╚██████╗██║  ██╗██████╞╝██║   ██║     ||
||  ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝ ╚═╝   ╚═╝     ||
\==================================================================/"""
    slow_print(f"\033[93m{art}\033[0m",0.000001)
    slow_print("\033[92m[SECURE] Terminal session established...\033[0m",0.01)

    while True:
        info_log("Select operation:")
        print("  [1] Encrypt files")
        print("  [2] Decrypt files")
        print("  [3] Exit")
        ch = input("\033[92m[>>] \033[0m").strip()
        if ch=='1':
            print("[ENCRYPT] Starting encryption...")
            encryption_workflow()
        elif ch=='2':
            print("[DECRYPT] Starting decryption...")
            decryption_workflow()
        elif ch=='3':
            print("[EXIT] Goodbye!")
            break
        else:
            error_log(f"Invalid option: {ch}")
