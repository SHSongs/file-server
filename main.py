import uvicorn

from typing import List

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, Response

app = FastAPI()

file_lst = []


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    if len(files) == 1:
        file = files[0]
        data = await file.read()

        headers = {
            'Content-Disposition': 'attachment; filename="filename.png"'
        }
        file_lst.append()
        return Response(data, headers=headers)
    else:
        return HTTPException(status_code=404, detail="아직 여러개의 파일은 올릴 수 없습니다.")


@app.get("/")
async def main():
    content = """
<body>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
