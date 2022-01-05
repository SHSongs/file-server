import random
from io import BytesIO
import zipfile


def generate_zip(files):
    mem_zip = BytesIO()

    with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.writestr(f[0], f[1])

    return mem_zip.getvalue()


keys = random.sample(range(10000, 100000), 1000)
key_num = 0


def generate_key():
    global key_num
    key_num += 1
    return keys[key_num]
