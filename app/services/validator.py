from pyhanko_certvalidator import ValidationContext
from pyhanko.keys import load_cert_from_pemder
from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.sign.validation import validate_pdf_signature
from pathlib import Path
from app.core.config import ROOT_CA_CERT_PATH

def verify_pdf_service(pdf_path: str):
    """
    Verifying PDF file's sign accuracy and integrity (if wasn't modified after signing).

    :param pdf_path: Path to file that will be verified.
    :return: Boolean if is valid, list of dictionaries with verifying results.
    """

    cert_path = Path(ROOT_CA_CERT_PATH)
    root_cert = load_cert_from_pemder(cert_path)
    vc = ValidationContext(trust_roots=[root_cert])
    results = []
    is_all_valid = True

    with open(pdf_path, 'rb') as doc:
        r = PdfFileReader(doc)

        # if not signed
        if not r.embedded_signatures:
            return False, {"error" : "File is not signed"}

        # checking all the possible signs
        for sig in r.embedded_signatures:
            status = validate_pdf_signature(sig, vc)

            # returning false if even one sign is invalid
            if not (status.valid and status.intact):
                is_all_valid = False

            cert = status.signing_cert
            subject = cert.subject.native # conversion to python's data structures (asn1crypto)
            signer_name = subject.get('common_name', 'Unknown')

            results.append({
                "signer" : signer_name,
                "valid" : status.valid,
                "intact" : status.intact, # integrity
                "trusted" : status.trusted, # if it signed by root CA
                "signing_time" : status.signer_reported_dt.isoformat() if status.signer_reported_dt else None,
                "validation_time" : status.validation_time.isoformat(),
                "algorithm" : status.md_algorithm
            })

        return is_all_valid, results