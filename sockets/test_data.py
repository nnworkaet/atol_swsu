
print_receipt_data = {
            "cashbox_id": "COM3",
            "uuid": "9eac7-50kb-00ad-b3f6-06a42e550450",
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

openshift_data = {
            "cashbox_id": "COM3",
            "event": "openshift",
            "taskJson": {
                "operator": {
                    "name": "Иванов",
                    "vatin": "123654789507"
                },
            }
        }

closeshift_data = {
            "cashbox_id": "COM3",
            "event": "closeshift",
            "taskJson": {
                "operator": {
                    "name": "Иванов",
                    "vatin": "123654789507"
                },
            }
        }

cashier_status_data = {
            "cashbox_id": "COM3",
            "event": "cashier_status",
        }

get_receipt_result_data = {
            "cashbox_id": "COM3",
            "uuid": "9eac7-50kb-00ad-b3f6-06a42e550450",
            "event": "get_receipt_result",
        }

get_fiscal_document_data = {
            "cashbox_id": "COM3",
            "fdn": "123",
            "event": "get_receipt_result",
        }