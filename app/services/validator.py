# Funkcje do sprawdzania podpisu\
from asn1crypto.core import Boolean
from pyhanko_certvalidator import ValidationContext
from pyhanko.keys import load_cert_from_pemder
from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.sign.validation import validate_pdf_signature
# import os

def verify_pdf_service(pdf_path: str, cert_path: str):
    """
    Sprawdza poprawność podpisu na pliku PDF oraz integralność (czy nie został zmodyfikowany po podpisie)

    :param pdf_path: Ścieżka do pliku, który ma być zweryfikowany
    :type pdf_path: str
    :param cert_path: Ścieżka do certyfikatu root CA
    :type cert_path: str
    :return: True/False
    """
    # print(f"Jestem w katalogu: {os.getcwd()}")
    # print(f"Szukam certyfikatu tutaj: {os.path.abspath(cert_path)}")
    root_cert = load_cert_from_pemder(cert_path)
    vc = ValidationContext(trust_roots=[root_cert])

    with open(pdf_path, 'rb') as doc:
        r = PdfFileReader(doc)
        for sig in r.embedded_signatures:
            status = validate_pdf_signature(sig, vc)
            if not (status.valid and status.intact):
                return False
        return True
            #print(status.pretty_print_details())

#print(verify_pdf_service("../../storage/as_klasyczna_signed.pdf", "../../certs/root_ca.crt"))