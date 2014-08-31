from flask import Flask, request, jsonify
import numpy, StringIO, base64, glitch
from PIL import Image

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        json = request.get_json(force=True)
        data = json["content"]["data"].split(";")
        try:
            image = Image.open(StringIO.StringIO(base64.b64decode(data[1])))
        except:
            return jsonify(json)
        image = image.convert("RGB")
        array_image = numpy.asarray(img)
        array_image.flags.writeable = True
        glitched_image = glitch.main(array_image)
        out_image = Image.fromarray(glitched_image)
        # re-jsonify and return here
    else:
        return "this is where my revist server lives"

if __name__ == '__main__':
    app.run()
