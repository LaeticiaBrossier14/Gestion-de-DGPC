"""HTTPS server for mobile testing — no openssl needed."""
import http.server, ssl, os, tempfile

PORT = 8443
DIR = os.path.dirname(os.path.abspath(__file__))
CERT = os.path.join(DIR, 'cert.pem')
KEY = os.path.join(DIR, 'key.pem')

# Generate self-signed cert using Python's ssl module
if not os.path.exists(CERT):
    try:
        # Try with cryptography library
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        import datetime

        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, u"collecte-audio")])
        cert = (x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.utcnow())
            .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
            .sign(key, hashes.SHA256())
        )
        with open(KEY, 'wb') as f:
            f.write(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.TraditionalOpenSSL, serialization.NoEncryption()))
        with open(CERT, 'wb') as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        print("✅ Certificat SSL généré avec cryptography")
    except ImportError:
        # Fallback: use subprocess with python -c
        print("⚠️ 'cryptography' non installé. Installation...")
        import subprocess
        subprocess.run(['pip', 'install', 'cryptography'], check=True)
        # Re-run this script
        subprocess.run(['python', __file__])
        exit()

os.chdir(DIR)
handler = http.server.SimpleHTTPRequestHandler
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain(CERT, KEY)

server = http.server.HTTPServer(('0.0.0.0', PORT), handler)
server.socket = ctx.wrap_socket(server.socket, server_side=True)
print(f"\n🔒 HTTPS server lancé!")
print(f"📱 Sur ton téléphone ouvre: https://192.168.2.17:{PORT}")
print(f"   ⚠️  Accepte l'avertissement de sécurité du navigateur")
print(f"   (Clique 'Paramètres avancés' → 'Continuer vers le site')\n")
server.serve_forever()
