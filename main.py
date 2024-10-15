import os
import ssl
from app import create_app
from util.create_ssl import ensure_certificates
from flask_talisman import Talisman


# 确保证书存在
# ensure_certificates()

app = create_app()
# talisman = Talisman(app, force_https=True)

if __name__ == '__main__':
    # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # cert_file = os.path.join(current_dir, 'certs', 'cert.pem')
    # key_file = os.path.join(current_dir, 'certs', 'key.pem')
    # ssl_context.load_cert_chain(certfile=cert_file, keyfile=key_file)
    # app.run(ssl_context=ssl_context, host='0.0.0.0', port=8000)
    app.run(debug=False, host='0.0.0.0', port=8000)
