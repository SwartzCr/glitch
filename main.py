from flask import Flask, request, jsonify
import numpy, StringIO, base64, glitch, sys
from PIL import Image

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        json = request.get_json(force=True)
        data = json["content"]["data"].split(";")
        try:
            image = Image.open(StringIO.StringIO(base64.b64decode(data[1].split(",")[1])))
            print image
        except:
            return jsonify(json)
        image = image.convert("RGB")
        array_image = numpy.asarray(image)
        array_image.flags.writeable = True
        glitched_image = glitch.main(array_image)
        try:
            out_image = Image.fromarray(glitched_image)
        except:
            return jsonify(json)
        sio = StringIO.StringIO()
        out_image.save(sio, "JPEG", quality=100)
        try:
            b64blob = base64.b64encode(sio.getvalue())
        except:
            print sys.exc_info()[:]
        # re-jsonify and return here
        out = {"content": { "data" : "data:image/jpeg;base64,"+b64blob},
               "meta" : {}}
        return jsonify(**out)
    else:
        return "this is where my revist server lives"

if __name__ == '__main__':
    app.run()
