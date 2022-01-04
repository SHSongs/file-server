import uvicorn

from typing import List

from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

import random
import os

app = FastAPI()
templates = Jinja2Templates(directory=os.path.abspath(os.path.expanduser("templates")))

file_lst = []

keys = random.sample(range(10000, 100000), 1000)
key_num = 0


def generate_key():
    global key_num
    key_num += 1
    return keys[key_num]


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    if len(files) == 1:
        file = files[0]
        data = await file.read()
        print("data 크기", len(data))
        key = generate_key()
        print("시크릿 키", key)
        file_lst.append({'key': key, 'name': file.filename, 'data': data})
        return "업로드 완료   시크릿 키: " + str(key)
    else:
        return HTTPException(status_code=404, detail="아직 여러개의 파일은 올릴 수 없습니다.")


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
            name = name.encode("latin-1")
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


@app.get("/")
async def main():
    content = """
<body>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">

<br>
<br>
<br>

<a href="/downloadfile">다운로드</a>

</body>
    """
    return HTMLResponse(content=content)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
