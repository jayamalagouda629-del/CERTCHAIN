"""FEATURE 3: Certificate PDF. Deterministic: same input -> same bytes -> same hash."""
import io
from dataclasses import dataclass
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from . import config
from .qr import make_qr_image

@dataclass
class StudentData:
    usn: str
    full_name: str
    program: str
    total_credits: int
    cgpa: float
    graduation_date: str  # fixed by admin, never 'now'

def generate_certificate(s: StudentData) -> bytes:
    buf = io.BytesIO()
    # invariant=1 removes timestamps/random IDs -> reproducible bytes
    c = canvas.Canvas(buf, pagesize=landscape(A4), invariant=1)
    w, h = landscape(A4)
    c.setTitle(f"Degree Certificate - {s.usn}")
    c.setLineWidth(3); c.rect(25, 25, w - 50, h - 50)
    c.setFont("Helvetica-Bold", 22); c.drawCentredString(w / 2, h - 80, config.INSTITUTION_NAME.upper())
    c.setFont("Helvetica", 14); c.drawCentredString(w / 2, h - 120, "DEGREE CERTIFICATE")
    c.setFont("Helvetica", 13); c.drawCentredString(w / 2, h - 180, "This is to certify that")
    c.setFont("Helvetica-Bold", 24); c.drawCentredString(w / 2, h - 220, s.full_name)
    c.setFont("Helvetica", 13)
    c.drawCentredString(w / 2, h - 255, f"USN: {s.usn}")
    c.drawCentredString(w / 2, h - 285, f"has successfully completed {s.program}")
    c.drawCentredString(w / 2, h - 315, f"Credits: {s.total_credits}    CGPA: {s.cgpa:.2f}")
    c.drawCentredString(w / 2, h - 345, f"Date of Graduation: {s.graduation_date}")
    c.drawImage(ImageReader(make_qr_image(s.usn)), w - 160, 50, 100, 100)
    c.setFont("Helvetica", 8); c.drawString(60, 60, "Scan QR or upload this PDF at the verifier portal to authenticate.")
    c.showPage(); c.save()
    return buf.getvalue()
