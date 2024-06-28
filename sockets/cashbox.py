import socket
import json
import atol_utility

atol_utility = atol_utility.AtolUtility(lib_path=r"C:\Program Files\Atol\Drivers10\KKT\bin\fptr10.dll")


def connect_to_server(host, port, cashbox_number):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client.send(f"cashbox:{cashbox_number}".encode("utf-8"))
    print(f"Connected to server as cashbox {cashbox_number}")
    return client


def main():
    server_host = "127.0.0.1"
    server_port = 8765
    cashbox_port = "COM3"

    if not atol_utility.open_connection(cashbox_port):
        print("error no connection to the cashbox port")
        return {"error": "error no connection to the cashbox port"}

    client = connect_to_server(server_host, server_port, cashbox_port)

    while True:
        request = client.recv(4096).decode("utf-8")
        if not request:
            print(f"Cashbox {cashbox_port} disconnected from server.")
            break

        data = json.loads(request)
        modified_json = {key: value for key, value in data.items() if key != 'cashbox_number'}
        json_str = json.dumps(modified_json)
        print(json_str, type(json_str))

        # cashbox print
        response = atol_utility.print_receipt(json_str)
        print("response", response)
        client.send(json.dumps(response).encode('utf-8'))

    client.close()


if __name__ == "__main__":
    main()
