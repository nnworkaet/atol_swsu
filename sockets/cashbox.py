import socket
import json
import atol_utility


HOST = '0.0.0.0'
PORT = 1337
COM = "COM3"

atol_utility = atol_utility.AtolUtility(lib_path=r"C:\Program Files\Atol\Drivers10\KKT\bin\fptr10.dll")


def process_data(data):

    parsed_data = json.loads(data)

    if not atol_utility.open_connection(COM):
        print("error no connection to the cashbox port")
        return json.dumps({"error": "no connection to the cashbox port"})

    if parsed_data.get("event") == "openshift":
        operator_info = parsed_data.get("taskJson", {}).get("operator", {})
        name = operator_info.get("name")
        vatin = operator_info.get("vatin")
        result = atol_utility.open_shift(cashier_name=name, vatin=vatin)
        return json.dumps({"result": result})

    if parsed_data.get("event") == "closeshift":
        operator_info = parsed_data.get("taskJson", {}).get("operator", {})
        name = operator_info.get("name")
        vatin = operator_info.get("vatin")
        result = atol_utility.close_shift(cashier_name=name, vatin=vatin)
        return json.dumps({"result": result})

    if parsed_data.get("event") == "cashier_status":
        result = atol_utility.cashier_status()
        return json.dumps({"result": result})

    if parsed_data.get("event") == "get_receipt_result":
        uuid = parsed_data.get("uuid")
        result = atol_utility.get_receipt_result(uuid)
        return json.dumps({"result": result})

    if parsed_data.get("event") == "get_fiscal_document_data":
        fdn = parsed_data.get("fdn")
        result = atol_utility.get_fiscal_document_data(fdn)
        return json.dumps({"result": result})

    else:
        result = atol_utility.print_receipt(data)

    return json.dumps({"result": result})


def main(cashbox_id):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(f'cashbox:{cashbox_id}'.encode('utf-8'))

        while True:
            try:
                json_data = s.recv(1024).decode('utf-8')
                if json_data:
                    print(f"Received JSON to process: {json_data}")
                    processed_data = process_data(json_data)
                    s.sendall(processed_data.encode('utf-8'))
            except ConnectionResetError as cre:
                print(f"Connection reset by peer: {cre}")
                break
            except Exception as e:
                print(f"Exception: {e}")
                break


if __name__ == "__main__":
    main(COM)
