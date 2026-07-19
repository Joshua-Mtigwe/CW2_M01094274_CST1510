import pyotp
import qrcode
import io

def generate_secret():
    return pyotp.random_base32()


def generate_qr(username, secret):

    uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=username,
        issuer_name="CSDF AI"
    )

    qr = qrcode.make(uri)

    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer


def verify_code(secret, code):

    totp = pyotp.TOTP(secret)

    return totp.verify(code)