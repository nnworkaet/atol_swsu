import socket
import threading
import json


cashboxes = {}


def handle_cashbox(client_socket, cashbox_number):
    global cashboxes
    cashboxes[cashbox_number] = client_socket
    print(f"Cashbox {cashbox_number} registered and waiting for tasks.")
    try:
        while True:
            request = client_socket.recv(4096).decode('utf-8')
            if not request:
                print(f"Cashbox {cashbox_number} disconnected.")
                break

            data = json.loads(request)

            client_socket.send(json.dumps(data).encode('utf-8'))
            print(f"Sent print result to cashbox {cashbox_number}: {data}")
    except Exception as e:
        print(f"Error handling cashbox {cashbox_number}: {e}")
    finally:
        client_socket.close()
        del cashboxes[cashbox_number]
        print(f"Cashbox {cashbox_number} disconnected")


def handle_client(client_socket):
    try:
        # get json
        request = client_socket.recv(4096).decode('utf-8')
        data = json.loads(request)
        print(f"Received task from client: {data}")

        cashbox_number = data.get("cashbox_number")
        if not cashbox_number or cashbox_number not in cashboxes:
            response = {"error": "Invalid or disconnected cashbox number"}
            client_socket.send(json.dumps(response).encode('utf-8'))
            print(f"Sent error response to client: {response}")
        else:
            # send json on cashbox
            cashbox_socket = cashboxes[cashbox_number]
            cashbox_socket.send(request.encode('utf-8'))
            print(f"Sent task to cashbox {cashbox_number}: {request}")

            # getting answer
            response = cashbox_socket.recv(4096).decode('utf-8')
            print(f"Received response from cashbox {cashbox_number}: {response}")
            client_socket.send(response.encode('utf-8'))
            print(f"Sent response back to client: {response}")
    except Exception as e:
        print(f"Error handling client: {e}")
        response = {"error": str(e)}
        client_socket.send(json.dumps(response).encode('utf-8'))
        print(f"Sent error response to client: {response}")
    finally:
        client_socket.close()


def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] Listening on {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        # cashbox or client
        client_type = client_socket.recv(1024).decode('utf-8')
        if client_type.startswith("cashbox:"):
            cashbox_number = client_type.split(":")[1]
            client_handler = threading.Thread(
                target=handle_cashbox,
                args=(client_socket, cashbox_number)
            )
        else:
            client_handler = threading.Thread(
                target=handle_client,
                args=(client_socket,)
            )
        client_handler.start()


if __name__ == "__main__":
    start_server("127.0.0.1", 8765)
