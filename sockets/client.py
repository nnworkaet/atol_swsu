import socket
import json


def connect_to_server(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client.send("client".encode('utf-8'))
    print(f"Connected to server")
    return client


def main():
    server_host = '127.0.0.1'
    server_port = 8765

    client = connect_to_server(server_host, server_port)

    # json
    json_data = {
        "cashbox_number": "COM3",
        "uuid": "02999eac7-50kb-00ad-b3f6-06a42e550450",
        "taskJson": {
            "items": [
                {
                    "amount": 3000,
                    "name": "Розы",
                    "paymentMethod": "fullPayment",
                    "paymentObject": "service",
                    "price": 300,
                    "quantity": 10,
                    "tax": {"type": "vat10"},
                    "type": "position"
                },
                {
                    "amount": 350,
                    "name": "Биг мак",
                    "paymentMethod": "fullPayment",
                    "paymentObject": "service",
                    "price": 350,
                    "quantity": 1,
                    "tax": {"type": "vat10"},
                    "type": "position"
                }
            ],
            "operator": {
                "name": "Иванов",
                "vatin": "123654789507"
            },
            "payments": [
                {
                    "sum": 3500.0,
                    "type": "cash"
                }
            ],
            "type": "sell"
        }
    }

    # sending json
    client.send(json.dumps(json_data).encode('utf-8'))
    print(f"Sent JSON data to server: {json.dumps(json_data)}")

    # getting answer
    response = client.recv(4096).decode('utf-8')
    print(f"Server response: {response}")

    client.close()


if __name__ == "__main__":
    main()
