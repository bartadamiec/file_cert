from pyhanko.sign import signers, fields
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter


def sign_pdf_service(input_pdf_path: str, output_pdf_path: str, p12_path: str, p12_password: str):
    """
    Signs a PDF document using a digital certificate from a PKCS#12 container.

    This service applies a PAdES signature with LTA (Long Term Validation) settings enabled,
    ensuring the signature remains valid over time.

    :param input_pdf_path: Path to the source PDF file to be signed
    :param output_pdf_path: Path where the signed PDF will be saved
    :param p12_path: Path to the PKCS#12 certificate file (.p12 or .pfx)
    :param p12_password: Password to decrypt the PKCS#12 container private key
    :raise FileNotFoundError: If the input PDF or certificate file does not exist
    :raise ValueError: If the provided password for the certificate is incorrect
    :return: Path to the signed PDF file
    """

    signer = signers.SimpleSigner.load_pkcs12(
        pfx_file=p12_path, # path to container
        passphrase=p12_password.encode('utf-8') # user's password to container
    )

    # sign metadata
    signature_meta = signers.PdfSignatureMetadata(
        field_name='Signature',
        reason='Document Authentication',
        location='Warsaw, PL',
        use_pades_lta=True, # LTA adding timestamps chain to sign
        subfilter=fields.SigSeedSubFilter.PADES
    )

    # read, sign and save pdf file
    with open(input_pdf_path, 'rb') as in_file:
        with open(output_pdf_path, 'wb') as out_file:
            signers.sign_pdf(
                IncrementalPdfFileWriter(in_file),
                signature_meta=signature_meta,
                signer=signer,
                output=out_file,
            )

    return output_pdf_path