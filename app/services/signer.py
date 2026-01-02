from pyhanko.sign import signers, fields
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter


def sign_pdf_service(input_pdf_path: str, output_pdf_path: str, p12_path: str, p12_password: str):
    """
    Podpisuje plik PDF przy użyciu certyfikatu w formacie PKCS#12.

    :param input_pdf_path: Ścieżka do pliku PDF, który ma zostać podpisany
    :type input_pdf_path: str
    :param output_pdf_path: Ścieżka docelowa, gdzie zostanie zapisany podpisany plik
    :type output_pdf_path: str
    :param p12_path: Ścieżka do pliku certyfikatu (format .p12 lub .pfx)
    :type p12_path: str
    :param p12_password: Hasło odbezpieczające kontener certyfikatu
    :type p12_password: str
    :raise FileNotFoundError: Jeśli plik wejściowy lub certyfikat nie istnieje
    :return: Ścieżka do utworzonego, podpisanego pliku PDF
    :rtype: str
    """

    signer = signers.SimpleSigner.load_pkcs12(
        pfx_file=p12_path, # ścieżka do .p12 /certs
        passphrase=p12_password.encode('utf-8') # hasło do .p12
    )

    # Metadane podpisu
    signature_meta = signers.PdfSignatureMetadata(
        field_name='Signature',
        reason='Potwierdzenie autentyczności dokumentu',
        location='Warszawa, PL',
        use_pades_lta=True, # dodaje łańcuch timestampów do podpisu, LTA
        subfilter=fields.SigSeedSubFilter.PADES
    )

    # Odczyt, podpis i zapis pliku
    with open(input_pdf_path, 'rb') as in_file:
        with open(output_pdf_path, 'wb') as out_file:
            signers.sign_pdf(
                IncrementalPdfFileWriter(in_file),
                signature_meta=signature_meta,
                signer=signer,
                output=out_file,
            )

    return output_pdf_path