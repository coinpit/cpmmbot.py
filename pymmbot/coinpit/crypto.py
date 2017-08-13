import logging
import json
from nacl.bindings import crypto_sign, crypto_sign_BYTES
from nacl.encoding import Base64Encoder

logger = logging.getLogger('root')

def get_auth(user_id, name, secret, nonce, method, uri, body=None):
    if body is not None:
        if not isinstance(body, str):
            try:
                body = json.dumps(body, separators=(',', ':'))
            except ValueError as e:
                logger.exception('invalid body. json or string are valid body type')
    request_string = '{"method":"' + method + '","uri":"' + uri + (
        '",' if (body is None) else '","body":' + body + ',') + '"nonce":' + nonce + '}'
    logger.debug("message %s", request_string)
    raw_signed = crypto_sign(request_string.encode(), bytes.fromhex(secret))
    signature = Base64Encoder.encode(raw_signed[:crypto_sign_BYTES])
    return 'SIGN ' + user_id + "." + name + ':' + signature.decode()
