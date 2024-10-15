import os
from OpenSSL import crypto

def generate_self_signed_cert(cert_file, key_file):
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)
    cert = crypto.X509()
    cert.get_subject().C = "CN"
    cert.get_subject().ST = "Shenzhen"
    cert.get_subject().L = "Shenzhen"
    cert.get_subject().O = "yoyo solo"
    cert.get_subject().OU = "My Organization"
    cert.get_subject().CN = "localhost"
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')
    with open(cert_file, "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    with open(key_file, "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

def ensure_certificates():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir,'..'))

    cert_file = os.path.join(project_root, 'certs', 'cert.pem')
    key_file = os.path.join(project_root, 'certs', 'key.pem')

    if not os.path.exists(cert_file) or not os.path.exists(key_file):
        generate_self_signed_cert(cert_file, key_file)

if __name__ == "__main__":
    ensure_certificates()
