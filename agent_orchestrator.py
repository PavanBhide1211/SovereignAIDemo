import os
import requests
import json
from datetime import datetime

# --- CONFIGURATION ---
CLIENT_ID = os.getenv("ONEDRIVE_CLIENT_ID")
CLIENT_SECRET = os.getenv("ONEDRIVE_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("ONEDRIVE_REFRESH_TOKEN")

def get_access_token():
    url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }
    response = requests.post(url, data=data).json()
    return response.get("access_token")

def sync_to_onedrive(file_path):
    token = get_access_token()
    if not token: return
    
    file_name = os.path.basename(file_path)
    url = f"https://graph.microsoft.com/v1.0/me/drive/root:/SovereignAI_Logs/{file_name}:/content"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/octet-stream"}
    
    with open(file_path, "rb") as f:
        requests.put(url, headers=headers, data=f)

def job_dependency_checklist():
    print(f"[{datetime.now()}] Running Job Dependency Checklist...")
    # Add logic here to check queue/next_task.json
    return True

if __name__ == "__main__":
    if job_dependency_checklist():
        # Execute agent logic here
        log_file = "logs/audit.log"
        with open(log_file, "a") as f:
            f.write(f"Execution at {datetime.now()} - Success\n")
        
        sync_to_onedrive(log_file)
        print("Pipeline cycle complete. State synced to OneDrive.")