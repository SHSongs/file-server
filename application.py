from util import generate_key, generate_zip

file_lst = []


async def upload_one_file(file):
    data = await file.read()
    print("data 크기", len(data))

    key = generate_key()
    print("시크릿 키", key)
    file_lst.append({'key': key, 'name': file.filename, 'data': data})

    return key


async def upload_many_file(files):
    byte_files = []
    for file in files:
        data = await file.read()
        byte_files.append((file.filename, data))
        print("data 크기", len(data))

    file = generate_zip(byte_files)
    key = generate_key()
    print("시크릿 키", key)
    file_lst.append({'key': key, 'name': "file.zip", 'data': file})
    return key
