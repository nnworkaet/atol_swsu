import atol_utility


atol_utility = atol_utility.AtolUtility(lib_path=r"C:\Program Files\Atol\Drivers10\KKT\bin\fptr10.dll")

if not atol_utility.open_connection("COM3"):
    print("error no connection")
else:
    #result = atol_utility.print_receipt('{ "uuid": "85b6eab7-57ab-46dd-b3f6-06a42e550360", "taskJson": { "items" : [ { "amount" : 3000, "name" : "Розы", "paymentMethod" : "fullPayment", "paymentObject" : "service", "price" : 300, "quantity" : 10, "tax" : { "type" : "vat10" }, "type" : "position" }, { "amount" : 350, "name" : "Биг мак", "paymentMethod" : "fullPayment", "paymentObject" : "service", "price" : 350, "quantity" : 1, "tax" : { "type" : "vat10" }, "type" : "position" } ], "operator" : { "name" : "Иванов", "vatin" : "123654789507" }, "payments" : [ { "sum" : 3500.0, "type" : "cash" } ], "type" : "sell" } }')
    #result = atol_utility.open_shift("Иванов А", "665805954074")
    #result = atol_utility.close_shift("Иванов А", "665805954074")
    #result = atol_utility.cashier_status()
    #result = atol_utility.get_receipt_result("85b6eab7-57ab-46dd-b3f6-06a42e550360")
    #result = atol_utility.get_fiscal_document_data("123")
    pass
