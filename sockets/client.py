import socket
import json
import time
import test_data

HOST = '0.0.0.0'
PORT = 1337


def main(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'client')

        time.sleep(1)

        json_data = json.dumps(data)
        s.sendall(json_data.encode('utf-8'))

        processed_data = s.recv(1024).decode('utf-8')
        print(f"Received processed data: {processed_data}")


if __name__ == "__main__":
    main(test_data.print_receipt_data)
