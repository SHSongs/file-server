import uvicorn

from typing import List

from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

import os

from application import upload_one_file, file_lst
from util import generate_zip, generate_key

app = FastAPI()
templates = Jinja2Templates(directory=os.path.abspath(os.path.expanduser("templates")))


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    if len(files) == 1:
        key = await upload_one_file(files[0])
        return "업로드 완료   시크릿 키: " + str(key)
    else:
        byte_files = []
        for file in files:
            data = await file.read()
            byte_files.append((file.filename, data))
            print("data 크기", len(data))

        file = generate_zip(byte_files)
        key = generate_key()
        print("시크릿 키", key)
        file_lst.append({'key': key, 'name': "file.zip", 'data': file})

        return "업로드 완료   시크릿 키: " + str(key)


@app.get("/downloadfile", response_class=HTMLResponse)
async def download_file(request: Request):
    return templates.TemplateResponse("item.html", {"request": request})


@app.post("/find_data")
async def find_data(request: Request, secret_key: int = Form(...)):
    data = None
    name = ""
    for i in range(len(file_lst)):
        if secret_key == file_lst[i]['key']:
            data = file_lst[i]['data']
            name = file_lst[i]['name']
            print('파일을 찾았다', secret_key)

            del file_lst[i]
            break

    if data:
        try:
            name.encode("latin-1")
        except:
            print("latin-1으로 변환 실패")
            extension = name.split('.')[-1]
            name = "file." + extension

        headers = {
            f'Content-Disposition': f'attachment; filename="{name}"'
        }
        return Response(data, headers=headers)
    else:
        return HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
