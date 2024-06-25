import utils.libfptr10 as libfptr
from models.receipt import Receipt
from utils.database import get_db_session, initialize_db

import json
import datetime


class AtolUtility():
    def __init__(self, lib_path: str):
        initialize_db()
        self.fptr = libfptr.IFptr(lib_path)

    # Input data: Port
    # Example: "COM3"
    def open_connection(self, port: str) -> bool:
        self.fptr.open()
        self.fptr.setSingleSetting(libfptr.IFptr.LIBFPTR_SETTING_MODEL, str(libfptr.IFptr.LIBFPTR_MODEL_ATOL_AUTO))
        self.fptr.setSingleSetting(libfptr.IFptr.LIBFPTR_SETTING_PORT, str(libfptr.IFptr.LIBFPTR_PORT_COM))
        self.fptr.setSingleSetting(libfptr.IFptr.LIBFPTR_SETTING_COM_FILE, port)
        self.fptr.setSingleSetting(libfptr.IFptr.LIBFPTR_SETTING_BAUDRATE, str(libfptr.IFptr.LIBFPTR_PORT_BR_115200))
        self.fptr.applySingleSettings()

        is_opened = self.fptr.isOpened()
        return is_opened != 0

    @staticmethod
    def is_uuid_in_db(uuid: str) -> bool:
        with get_db_session() as session:
            receipt = session.query(Receipt).filter(Receipt.uuid == uuid).first()
            return receipt is not None

    # Input data: TaskJson
    # Example: '{ "uuid": "85b6eab7-57ab-46dd-b3f6-06a42e550360", "taskJson": { "items" : [ { "amount" : 3000, "name" : "Розы", "paymentMethod" : "fullPayment", "paymentObject" : "service", "price" : 300, "quantity" : 10, "tax" : { "type" : "vat10" }, "type" : "position" }, { "amount" : 350, "name" : "Биг мак", "paymentMethod" : "fullPayment", "paymentObject" : "service", "price" : 350, "quantity" : 1, "tax" : { "type" : "vat10" }, "type" : "position" } ], "operator" : { "name" : "Иванов", "vatin" : "123654789507" }, "payments" : [ { "sum" : 3500.0, "type" : "cash" } ], "type" : "sell" } }'
    def print_receipt(self, task_data: str) -> dict:
        task_data_str = json.loads(task_data)

        uuid = task_data_str.get("uuid")
        receipt_body = task_data_str.get("taskJson")

        if not uuid or not receipt_body:
            return {"error": "missing uuid or taskJson"}

        if self.is_uuid_in_db(uuid):
            return {"error": "Receipt with this UUID already exists"}

        json_str = json.dumps(receipt_body, ensure_ascii=False)

        self.fptr.queryData()

        self.fptr.setParam(libfptr.IFptr.LIBFPTR_PARAM_JSON_DATA, param=json_str)
        if self.fptr.validateJson() != 0:
            return {"error": "wrong JSON format"}

        self.fptr.setParam(libfptr.IFptr.LIBFPTR_PARAM_JSON_DATA, param=json_str)
        self.fptr.processJson()

        result = self.fptr.getParamString(libfptr.IFptr.LIBFPTR_PARAM_JSON_DATA)

        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        receipt_callback = result if result else ""

        receipt = Receipt(uuid=uuid, receipt_callback=receipt_callback, created_at=created_at)

        with get_db_session() as session:
            session.add(receipt)
            session.commit()

        if receipt_callback == '':
            return {"result": receipt_callback}

        return {"result": json.loads(receipt_callback)}

    # Input data:
    # Cashier Name and VATIN
    # Return:
    # If document closed boolean value
    def open_shift(self, cashier_name: str, vatin: str) -> bool:
        self.fptr.setParam(1021, cashier_name)
        self.fptr.setParam(1203, vatin)
        self.fptr.operatorLogin()

        self.fptr.openShift()

        return bool(self.fptr.checkDocumentClosed())

    # Input data:
    # Cashier Name and VATIN
    # Return:
    # If document closed boolean value
    def close_shift(self, cashier_name: str, vatin: str) -> bool:
        self.fptr.setParam(1021, cashier_name)
        self.fptr.setParam(1203, vatin)
        self.fptr.operatorLogin()

        self.fptr.setParam(libfptr.IFptr.LIBFPTR_PARAM_REPORT_TYPE, libfptr.IFptr.LIBFPTR_RT_CLOSE_SHIFT)
        self.fptr.report()

        return bool(self.fptr.checkDocumentClosed())

    def cashier_status(self):
        self.fptr.setParam(libfptr.IFptr.LIBFPTR_PARAM_DATA_TYPE, libfptr.IFptr.LIBFPTR_DT_SHORT_STATUS)
        self.fptr.queryData()

        is_cash_drawer_opened = self.fptr.getParamBool(libfptr.IFptr.LIBFPTR_PARAM_CASHDRAWER_OPENED)
        is_paper_present = self.fptr.getParamBool(libfptr.IFptr.LIBFPTR_PARAM_RECEIPT_PAPER_PRESENT)
        is_paper_near_end = self.fptr.getParamBool(libfptr.IFptr.LIBFPTR_PARAM_PAPER_NEAR_END)
        is_cover_opened = self.fptr.getParamBool(libfptr.IFptr.LIBFPTR_PARAM_COVER_OPENED)

        return {
            "result": {
                "isCashDrawerOpened": is_cash_drawer_opened,
                "isPaperPresent": is_paper_present,
                "isPaperNearEnd": is_paper_near_end,
                "isCoverOpened": is_cover_opened
            }
        }

    def get_receipt_result(self, uuid: str):
        with get_db_session() as session:
            receipt = session.query(Receipt).filter(Receipt.uuid == uuid).first()
            if receipt:
                return {"receipt_callback": receipt.receipt_callback}
            else:
                return {"error": "Receipt not found"}

    def get_fiscal_document_data(self, fdn: str) -> dict:
        json_str = '{ "type": "getFnDocument", "fiscalDocumentNumber": ' + fdn + ', "withRawData": true }'
        self.fptr.setParam(libfptr.IFptr.LIBFPTR_PARAM_JSON_DATA, param=json_str)
        if self.fptr.validateJson() != 0:
            return {"error": "wrong JSON format"}

        self.fptr.setParam(libfptr.IFptr.LIBFPTR_PARAM_JSON_DATA, param=json_str)
        self.fptr.processJson()

        result = self.fptr.getParamString(libfptr.IFptr.LIBFPTR_PARAM_JSON_DATA)
        return result
