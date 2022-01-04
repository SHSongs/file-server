import uvicorn

from typing import List

from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

file_lst = []


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    if len(files) == 1:
        file = files[0]
        data = await file.read()
        print(len(data))
        file_lst.append({'key': 1234, 'name': file.filename, 'data': data})
        return "업로드 완료"
    else:
        return HTTPException(status_code=404, detail="아직 여러개의 파일은 올릴 수 없습니다.")


@app.get("/downloadfile", response_class=HTMLResponse)
async def download_file(request: Request):
    return templates.TemplateResponse("item.html", {"request": request})


@app.post("/find_data")
async def find_data(request: Request, secret_key: int = Form(...)):
    data = None
    name = None
    for i in range(len(file_lst)):
        if secret_key == file_lst[i]['key']:
            data = file_lst[i]['data']
            name = file_lst[i]['name']
            print('파일을 찾았다', secret_key)

            del file_lst[i]
            break

    if data:
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
