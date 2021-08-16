from PIL import Image
import requests

async def resize_img(url, reduce_scale = 4):

    r = requests.get(url, stream=True)
    r.raw.decode_content = True # handle spurious Content-Encoding

    img = Image.open(r.raw)
    img = img.convert("RGBA")
    width, height = img.size
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            newData.append((0, 0, 0, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img = img.resize((int(width/reduce_scale), int(height/reduce_scale)))
    return img