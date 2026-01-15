from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from app.core.config import CERTS_DIR, ROOT_CA_CERT_PATH, ROOT_CA_KEY_PATH
import datetime
import os

# PLIK MOŻNA URUCHOMIĆ TYLKO RAZ !!!!!
def generate_root_ca():
    """
    Tworzy hierarchię CA. Tworzy klucz prywatny oraz certyfikat CA.
    Można odpalić tylko raz.
    """

    os.makedirs(CERTS_DIR, exist_ok=True)
    try:
        if os.path.exists(ROOT_CA_KEY_PATH) or os.path.exists(ROOT_CA_CERT_PATH):
            raise FileExistsError

        root_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "PL"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Mazowieckie"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Warszawa"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "FileCert"),
            x509.NameAttribute(NameOID.COMMON_NAME, "FileCert Root CA"),
        ])

        root_cert = x509.CertificateBuilder().subject_name(
        subject
        ).issuer_name(
            issuer
        ).public_key(
            root_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.now(datetime.timezone.utc)
        ).not_valid_after(
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365 * 10)
        ).add_extension(
            x509.BasicConstraints(ca=True, path_length=None), critical=True,
        ).add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=True,
                crl_sign=True,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        ).add_extension(
            x509.SubjectKeyIdentifier.from_public_key(root_key.public_key()),
            critical=False, # to jest hash klucza, tylko przyśpiesza odszukiwanie
        ).sign(root_key, hashes.SHA256()) # self sign

        with open(ROOT_CA_KEY_PATH, "wb") as f:
            f.write(root_key.private_bytes(encoding=serialization.Encoding.PEM,
                                           format=serialization.PrivateFormat.TraditionalOpenSSL,
                                           encryption_algorithm=serialization.BestAvailableEncryption(b'password'))) # z .env powinno być, albo hash

        with open(ROOT_CA_CERT_PATH, "wb") as f:
            f.write(root_cert.public_bytes(serialization.Encoding.PEM))

    except FileExistsError:
        print("Skrypt już został raz uruchomiony!")

if __name__ == "__main__":
    generate_root_ca()