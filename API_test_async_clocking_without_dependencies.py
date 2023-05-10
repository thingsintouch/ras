import requests
import datetime

# create a timestamp UNIX from a date string
stamp1 = "2023-02-06 14:06:00"

timestamp = int(datetime.datetime.strptime(stamp1, "%Y-%m-%d %H:%M:%S").timestamp()) 
print(f"timestamp: {timestamp}")

# timestamp = "1675775097"

card_code = "c0a88821" # Abigail Peterson
template = "https://o15.thingserp.com:443/iot/"
serial = "e52d743d-714f-461d-8135-a21216ad6b6e"
passphrase = "9c184e00-1778-4831-ad2a-67f856da56cd"

# card_code = "607fa0d3" # Sergi Casau
# template = "https://www.forgeflow.com:443/iot/"
# serial = "f0502a92-b42b-4965-b15b-5cec8dd09ede"
# passphrase = "7bea50e2-1d74-4c2a-818b-89f62990338d"


requestURL  = template + serial + "/action"
payload     = {
    'passphrase'    : passphrase,
    "card_code"     : str(card_code),
    "timestamp"     : int(timestamp)
    }

posting = requests.post(url=requestURL, data=payload, verify= False, timeout=150000)
try:
    answer = posting.json()
    print(f"full answer {answer}")
    registered = answer.get("logged", False)
    print(f"clocking registered (state): {registered}")
except:
    print(f"posting: {posting}")
