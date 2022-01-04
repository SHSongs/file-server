import uvicorn

from typing import List

from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

file_lst = []


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    if len(files) == 1:
        file = files[0]
        data = await file.read()

        file_lst.append({'key': 1234, 'data': data})
        return "업로드 완료"
    else:
        return HTTPException(status_code=404, detail="아직 여러개의 파일은 올릴 수 없습니다.")


@app.get("/downloadfile", response_class=HTMLResponse)
async def download_file(request: Request):
    return templates.TemplateResponse("item.html", {"request": request})


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

<form action="/downloadfile/" method="get">
<button type="submit">다운로드</button>
</form>
</body>
    """
    return HTMLResponse(content=content)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
