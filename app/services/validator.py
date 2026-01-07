# Funkcje do sprawdzania podpisu\
from pyhanko_certvalidator import ValidationContext
from pyhanko.keys import load_cert_from_pemder
from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.sign.validation import validate_pdf_signature
# from config import ROOT_PATH

def verify_pdf_service(pdf_path: str):
    """
    Sprawdza poprawność podpisu na pliku PDF oraz integralność (czy nie został zmodyfikowany po podpisie)

    :param pdf_path: Ścieżka do pliku, który ma być zweryfikowany
    :type pdf_path: str
    :param cert_path: Ścieżka do certyfikatu root CA
    :type cert_path: str
    :return: True/False
    """

    cert_path = "/certs/root_ca.crt"
    root_cert = load_cert_from_pemder(cert_path)
    vc = ValidationContext(trust_roots=[root_cert])
    results = []
    is_all_valid = True

    with open(pdf_path, 'rb') as doc:
        r = PdfFileReader(doc)

        if not r.embedded_signatures:
            return False, {"error" : "File is not signed"}

        for sig in r.embedded_signatures:
            status = validate_pdf_signature(sig, vc)

            if not (status.valid and status.intact):
                is_all_valid = False

            cert = status.signing_cert
            subject = cert.subject.native
            signer_name = subject.get('common_name', 'Nieznany')

            results.append({
                "signer" : signer_name,
                "valid" : status.valid,
                "intact" : status.intact,
                "trusted" : status.trusted,
                "signing_time" : status.signer_reported_dt.isoformat() if status.signer_reported_dt else None,
                "validation_time" : status.validation_time.isoformat() if status.signer_reported_dt else None,
                "algorithm" : status.md_algorithm
            })

        return is_all_valid, results

# print(verify_pdf_service("../../storage/as_klasyczna_signed.pdf"))