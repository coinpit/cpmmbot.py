import json
import six
from nacl.bindings import crypto_sign, crypto_sign_BYTES
from nacl.encoding import Base64Encoder


def get_auth(user_id, name, secret, nonce, method, uri, body=None):
    if body is not None:
        if not isinstance(body, six.string_types):
            try:
                body = json.dumps(body, separators=(',', ':'))
            except ValueError as e:
                print('invalid body. json or string are valid body type')
    request_string = '{"method":"' + method + '","uri":"' + uri + (
        '",' if (body is None) else '","body":' + body + ',') + '"nonce":' + nonce + '}'
    print("message", request_string)
    raw_signed = crypto_sign(request_string.encode(), bytes.fromhex(secret))
    signature = Base64Encoder.encode(raw_signed[:crypto_sign_BYTES])
    return 'SIGN ' + user_id + "." + name + ':' + signature.decode()
