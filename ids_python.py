import json
import schedule # type: ignore
import time
import subprocess
from datetime import datetime
from discordwebhook import Discord # type: ignore

discord = Discord(url="<your webhook url>")

def save_ssh_logs():
    global filename 
    filename = datetime.now().strftime("%d_%m_%Y_%Hh_ssh_logs.json") # Nommage en fonction de la date

    with open(filename, "w") as f:
        subprocess.run(["sudo", "journalctl", "-u", "ssh", "--output=json"], stdout=f) # Ecrire les logs dans le fichier

    print(f"[✅] Logs SSH sauvegardés dans {filename}")

    schedule.every().hour.do(save_ssh_logs) # Check pour des tentatives d'intrusions toutes les heures
    

def read_logs(filename):   

    with open(filename, 'r') as file:
        
            data = json.load(file)
            failed_count = 0

            for entry in data:
                message = entry.get("MESSAGE", None)
                if "Failed" in message: 
                    failed_count += 1 # Compter le nombre de connexion échoués
                rhost = entry.get("rhost", None) # Récupérer les adresses IPs des attaquants
                timestamp = entry.get("_SOURCE_REALTIME_TIMESTAMP", None)

                if timestamp:
                    timestamp_dt = datetime.fromtimestamp(int(timestamp) / 1000000) # Convertir en format plus lisible
                    time_str = timestamp_dt.strftime("%H:%M:%S")  
                else:
                    time_str = "inconnu"  
            
                #for i in data['MESSAGE']:
                if failed_count >= 3:
                    Discord.post( 
    embeds=[{"title": "TENTATIVE DE CONNEXION SSH", "description": f"@Admin Tentative de connexion SSH échoué à {time_str} depuis {rhost}", "color": 16711680 }]) # Alerte Discord à chaque tentative d'intrusion
                else:
                    continue

while True:
    schedule.run_pending()
    time.sleep(60)
