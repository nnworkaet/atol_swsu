from libfptr10 import IFptr
from fastapi import FastAPI
from models import Inputdata
import uvicorn
import json

app = FastAPI()

fptr = IFptr(
    lib_path=r"C:\Program Files\Atol\Drivers10\KKT\bin\fptr10.dll"
)


@app.post("/print_check")
def print_check(data: Inputdata):

    fptr.open()
    fptr.setSingleSetting(IFptr.LIBFPTR_SETTING_MODEL, str(IFptr.LIBFPTR_MODEL_ATOL_AUTO))
    fptr.setSingleSetting(IFptr.LIBFPTR_SETTING_PORT, str(IFptr.LIBFPTR_PORT_COM))
    fptr.setSingleSetting(IFptr.LIBFPTR_SETTING_COM_FILE, value=data.port)
    fptr.setSingleSetting(IFptr.LIBFPTR_SETTING_BAUDRATE, str(IFptr.LIBFPTR_PORT_BR_115200))
    fptr.applySingleSettings()

    is_opened = fptr.isOpened()
    if is_opened == 0:
        return {"error": "no connection"}

    fptr.queryData()
    json_str = json.dumps(data.receiptBody, ensure_ascii=False)

    fptr.setParam(IFptr.LIBFPTR_PARAM_JSON_DATA, param=json_str)
    if fptr.validateJson() != 0:
        print(fptr.validateJson())
        return {"error": "wrong JSON format"}

    fptr.setParam(IFptr.LIBFPTR_PARAM_JSON_DATA, param=json_str)
    fptr.processJson()

    result = fptr.getParamString(IFptr.LIBFPTR_PARAM_JSON_DATA)

    if result == '':
        return {"result": result}

    return {"result": json.loads(result)}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=1234)
