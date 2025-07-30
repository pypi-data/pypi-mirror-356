import socket
import json
import time

HOST = '127.0.0.1'
PORT = 9999
outfile = "telemetry.json"

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.bind((HOST, PORT))
    data_list = []

    print(f"Listening on {HOST}:{PORT} for telemetry...")
    start = time.time()
    while True:
        data, _ = sock.recvfrom(4096)
        try:
            js = json.loads(data.decode('utf-8'))
            # Add timestamp
            js['ts'] = time.time() - start
            data_list.append(js)
            # Optional: periodically flush to disk
            with open(outfile, 'w') as f:
                json.dump(data_list, f, indent=2)
        except json.JSONDecodeError:
            continue

if __name__ == "__main__":
    main()
