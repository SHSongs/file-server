from util import generate_key, generate_zip

file_lst = []


def register_file(name, data):
    key = generate_key()
    print("시크릿 키", key)
    file_lst.append({'key': key, 'name': name, 'data': data})
    return key


async def upload_one_file(file):
    data = await file.read()
    print("data 크기", len(data))
    key = register_file(file.filename, data)
    return key


async def upload_many_file(files):
    byte_files = []
    for file in files:
        data = await file.read()
        byte_files.append((file.filename, data))
        print("data 크기", len(data))

    file = generate_zip(byte_files)
    key = register_file("file.zip", file)
    return key
