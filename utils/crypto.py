import base64

def encode_pass(password):
    return base64.b64encode(password.encode()).decode()

def decode_pass(encoded_password):
    try:
        return base64.b64decode(encoded_password.encode()).decode()
    except:
        return None