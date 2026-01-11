# Generowanie certyfikatów i kluczy
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
import datetime
from app.core.config import ROOT_CA_CERT_PATH, ROOT_CA_KEY_PATH
from pathlib import Path

def ca_service(username: str, password: str):
    user_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    with open(Path(f"../../storage/{username}_private_key.pem"), "wb") as f:
        f.write(user_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(b"password") # to musi być hashed lub .env, to jest haslo do kluucza prywatnego usera
    ))

    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "PL"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Mazowieckie"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Warszawa"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "FileCert"),
        x509.NameAttribute(NameOID.COMMON_NAME, "filecert.com"), # dla jakiej domeny certyfikat jest ważny
    ])).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName("mysite.com"),
            x509.DNSName("www.mysite.com"),
            x509.DNSName("subdomain.mysite.com"),
        ]),
        critical=False,
    ).sign(user_private_key, hashes.SHA256()) #wniosek podpisany przez klucz prywatny użytkownika
    # Zapisanie wniosku użytkownika
    with open(f"../../storage/{username}_csr.pem", "wb") as f:
        f.write(csr.public_bytes(serialization.Encoding.PEM))

    with open(ROOT_CA_KEY_PATH, "rb") as f:
        data = f.read()
        root_private_key = serialization.load_pem_private_key(data=data, password=b'password')

    with open(ROOT_CA_CERT_PATH, "rb") as f:
        data = f.read()
        root_cert = x509.load_pem_x509_certificate(data=data)

    # Certyfikat usera
    subject = csr.subject
    issuer = root_cert.subject

    user_cert = x509.CertificateBuilder().subject_name(
        subject
        ).issuer_name(
            issuer
        ).public_key(
            csr.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.now(datetime.timezone.utc)
        ).not_valid_after(
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365 * 10)
        ).add_extension(
            x509.BasicConstraints(ca=False, path_length=None), critical=True,
        ).add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=False,
                crl_sign=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        ).add_extension(
            x509.SubjectKeyIdentifier.from_public_key(csr.public_key()),
            critical=False, # to jest hash klucza, tylko przyśpiesza odszukiwanie
        ).sign(root_private_key, hashes.SHA256())

    p12 = serialization.pkcs12.serialize_key_and_certificates(name=username.encode('utf-8'),
                                                              key=user_private_key,
                                                              cert=user_cert,
                                                              cas=[root_cert],
                                                              encryption_algorithm=serialization.BestAvailableEncryption(password.encode('utf-8'))) # poprawić

    return p12