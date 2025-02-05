import json
import schedule
import time
import subprocess
from datetime import datetime
from discordwebhook import Discord

discord = Discord(url="<your webhook url>")

def save_ssh_logs():
    global filename 
    filename = datetime.now().strftime("%d_%m_%Y_%Hh_ssh_logs.json")

    with open(filename, "w") as f:
        subprocess.run(["sudo", "journalctl", "-u", "ssh", "--output=json"], stdout=f)

    print(f"[✅] Logs SSH sauvegardés dans {filename}")

schedule.every().hour.do(save_ssh_logs)

def read_logs(filename):   

    with open(filename, 'r') as file:
            data = json.load(file)
            for entry in data:
                message = entry.get("MESSAGE", None)
                rhost = entry.get("rhost", None)
                timestamp = entry.get("_SOURCE_REALTIME_TIMESTAMP", None)

                if timestamp:
                    timestamp_dt = datetime.fromtimestamp(int(timestamp) / 1000000)
                    time_str = timestamp_dt.strftime("%H:%M:%S")  
                else:
                    time_str = "inconnu"  
            
            
            for i in data['MESSAGE']:
                if 'Failed' in message():
                     discord.post(
    embeds=[{"title": "TENTATIVE DE CONNEXION SSH", "description": "Tentative de connexion SSH échoué à {time_str} depuis {rhost}" }],
)


#while True:
#    schedule.run_pending()
#    time.sleep(60)