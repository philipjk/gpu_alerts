import subprocess
import json
import csv
import time
import requests
import os

# Define the log interval in seconds
LOG_INTERVAL = 60*5
CHAT_ID = "-1001910393142"
BOT_TOKEN = os.environ.get('BOT_TOKEN')
TEMPERATURE_THRESHOLD = 75
SEND_REQ = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
ROOM_SENSOR = "http://10.30.3.236/data"

def push(filename):
    users_output = subprocess.check_output(["gpustat", "--json"])
    output = json.loads(users_output)
    t = output["query_time"]
    # use only day, hour and minute info
    t = t[5:16]
    room_temp = get_room_temp()
    for gpu in output["gpus"]:
        users = []
        utilization = gpu['utilization.gpu']
        for p in gpu["processes"]:
            users.append(p["username"])
        # Append the GPU data to the CSV file
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([t, gpu["index"], gpu["memory.used"], 
                             gpu["temperature.gpu"], utilization,
                             users, room_temp])
        if gpu["temperature.gpu"] > TEMPERATURE_THRESHOLD:
            usr_str = ', '.join(users)
            data = (f"""GPU {gpu['index']} is at {gpu['temperature.gpu']}°C. Alert user(s) {usr_str}.""")
            also = f" Room temperature is {room_temp}°C."
            requests.post(SEND_REQ, data={"chat_id": CHAT_ID, "text": data+also})

def get_room_temp():
    try:
        # get temp from ROOM_SENSOR, which returns a json
        temp = requests.get(ROOM_SENSOR).json()['t']
        return temp
    except:
        return None

# Initialize the CSV file with a header row
fname = time.strftime("%m-%d-%H-%M") + ".csv"
with open(fname, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['time', 'gpu_index', 'memory_used', 'temperature', 'utilization', 'users', 'room_temp'])

try:
    while True:
        push(fname)
        time.sleep(LOG_INTERVAL)
except KeyboardInterrupt:
    print("Exiting...")
    push(fname)
       