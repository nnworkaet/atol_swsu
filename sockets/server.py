import socket
import threading
import json


HOST = '0.0.0.0'
PORT = 1337


cashbox_conns = {}
client_conn = None


def handle_client(client_socket):
    global cashbox_conns, client_conn

    try:
        client_type = client_socket.recv(1024).decode('utf-8').strip()
        print(f"Client type received: {client_type}")

        if client_type.startswith('cashbox'):
            _, cashbox_id = client_type.split(':')
            cashbox_conns[cashbox_id] = client_socket
            print(f"Cashbox {cashbox_id} connected")
        elif client_type == 'client':
            client_conn = client_socket
            print("Client connected")
        else:
            print("Unknown client type")
            client_socket.close()
            return

        while True:
            if client_type == 'client' and client_conn:
                json_data = client_conn.recv(1024).decode('utf-8')
                print(f"Received from client: {json_data}")

                if not json_data:
                    print("Client disconnected or no data received.")
                    break

                parsed_data = json.loads(json_data)
                cashbox_id = str(parsed_data.get("cashbox_id"))

                if cashbox_id in cashbox_conns:
                    cashbox_conns[cashbox_id].sendall(json_data.encode('utf-8'))
                    processed_data = cashbox_conns[cashbox_id].recv(1024).decode('utf-8')
                    print(f"Processed data from cashbox {cashbox_id}: {processed_data}")

                    client_conn.sendall(processed_data.encode('utf-8'))
                else:
                    print(f"No cashbox with ID {cashbox_id} connected.")
                    client_conn.sendall(json.dumps({"error": "No such cashbox"}).encode('utf-8'))

    except ConnectionResetError as cre:
        print(f"Connection reset by peer: {cre}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print(f"Closing connection for {client_type}")
        client_socket.close()
        if client_type.startswith('cashbox'):
            _, cashbox_id = client_type.split(':')
            if cashbox_id in cashbox_conns:
                del cashbox_conns[cashbox_id]
        elif client_type == 'client':
            client_conn = None
        print(f"{client_type} disconnected")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    start_server()
