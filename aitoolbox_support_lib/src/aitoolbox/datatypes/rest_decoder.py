import json

from base64 import b64decode
import imageio

class RestDecoder():
    def decode(req_body):
        arguments = json.loads(req_body)

        return { k: RestDecoder.decode_argument(v) for k,v in arguments.items() }

    def decode_argument(arg):
        if isinstance(arg, (int, float, complex, str)):
            return arg
        
        if isinstance(arg, dict) and "_type" in arg:
            mime = arg["_type"]
            if mime.startswith("image/"):
                return RestDecoder.decode_image(mime,arg["_data"])

        return arg
    
    def decode_image(mime,data):
        bytes = b64decode(data)
        return imageio.imread(bytes)