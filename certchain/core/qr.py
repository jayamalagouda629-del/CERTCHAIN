"""FEATURE 2: QR code generation.
NOTE: QR holds the verify URL with USN only. It can NOT contain the PDF's own hash
(the hash is computed AFTER the QR is embedded)."""
import qrcode
from PIL import Image
from . import config

def verification_url(usn: str) -> str:
    return f"{config.VERIFY_BASE_URL}/Verifier?usn={usn}"

def make_qr_image(usn: str) -> Image.Image:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=2)
    qr.add_data(verification_url(usn))
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white").convert("RGB")
