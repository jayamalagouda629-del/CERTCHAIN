from core.hashing import sha256_hex, hex_to_bytes32
from core.pdf_generator import StudentData, generate_certificate

S = StudentData("1MV25MC030", "Jayamala M Gouda", "MCA", 80, 8.5, "2027-06-30")

def test_hash_format():
    h = sha256_hex(b"abc"); assert h.startswith("0x") and len(h) == 66
    assert len(hex_to_bytes32(h)) == 32

def test_pdf_is_deterministic():
    assert sha256_hex(generate_certificate(S)) == sha256_hex(generate_certificate(S))

def test_tamper_changes_hash():
    pdf = generate_certificate(S)
    t = bytearray(pdf); t[len(t)//2] ^= 1
    assert sha256_hex(pdf) != sha256_hex(bytes(t))

def test_cgpa_change_changes_hash():
    S2 = StudentData("1MV25MC030", "Jayamala M Gouda", "MCA", 80, 9.5, "2027-06-30")
    assert sha256_hex(generate_certificate(S)) != sha256_hex(generate_certificate(S2))
