# generating certificates and keys
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
import datetime
from app.core.config import ROOT_CA_CERT_PATH, ROOT_CA_KEY_PATH, STORAGE
from pathlib import Path
import os

def ca_service(username: str, password: str):
    """
    Generating user's certificate and returns in PKCS#12 container.

    :param username: User's name (Common Name).
    :param password: User's password to encrypt the PKCS#12 container.
    :return: PKCS#12 content in bytes.
    """

    root_ca_pass = os.getenv("ROOT_CA_PASSWORD")
    if not root_ca_pass:
        raise ValueError("Server Error: Root CA not configured.")

    user_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048) # generating user's private key
    pk_path = Path(f"{STORAGE}/{username}_private_key.pem")
    # saving user's private key
    try:
        with open(pk_path, "wb") as f:
            f.write(user_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(password.encode("utf-8")) # encrypted by user's password
        ))
    except Exception:
        if pk_path.is_file():
            pk_path.unlink() # deleting key if exists
    # certificate signing request
    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "PL"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Mazowieckie"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Warsaw"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "FileCert"),
        x509.NameAttribute(NameOID.COMMON_NAME, username),
    ])).sign(user_private_key, hashes.SHA256()) # request signed by user's private key

    # saving user's request
    csr_path = Path(f"{STORAGE}/{username}_csr.pem")
    try:
        with open(csr_path, "wb") as f:
            f.write(csr.public_bytes(serialization.Encoding.PEM)) # serializing from object to bytes
    except Exception:
        if csr_path.is_file():
            csr_path.unlink() # deleting csr if exists

    with open(ROOT_CA_KEY_PATH, "rb") as f:
        data = f.read()
        root_private_key = serialization.load_pem_private_key(data=data, password=root_ca_pass.encode('utf-8'))

    with open(ROOT_CA_CERT_PATH, "rb") as f:
        data = f.read()
        root_cert = x509.load_pem_x509_certificate(data=data)

    # user's certificate
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
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365) # valid for year
        ).add_extension(
            x509.BasicConstraints(ca=False, path_length=None), critical=True, # must be ca=False!!!
        ).add_extension(
            x509.KeyUsage(
                digital_signature=True, # cert use case is only to sign files
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
            critical=False, # key's hash, only accelerating searching
        ).sign(root_private_key, hashes.SHA256())

    p12 = serialization.pkcs12.serialize_key_and_certificates(name=username.encode('utf-8'),
                                                              key=user_private_key,
                                                              cert=user_cert,
                                                              cas=[root_cert],
                                                              encryption_algorithm=serialization.BestAvailableEncryption(password.encode('utf-8'))) # user's password need to open container
    return p12





