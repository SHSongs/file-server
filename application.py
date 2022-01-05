from util import generate_key

file_lst = []


async def upload_one_file(file):
    data = await file.read()
    print("data 크기", len(data))

    key = generate_key()
    print("시크릿 키", key)
    file_lst.append({'key': key, 'name': file.filename, 'data': data})

    return key
