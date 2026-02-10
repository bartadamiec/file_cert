<div align="center">
  
[![Documentation](https://img.shields.io/badge/Documentation_and_Developing_Process-PDF_(PL)-blue?style=for-the-badge&logo=adobeacrobatreader&logoColor=white)](docs/File_Cert_Dokumentacja.pdf)

<br>

![Python](https://img.shields.io/badge/python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat)
![Status](https://img.shields.io/badge/status-MVP%20Completed-orange.svg?style=flat)

<br>

![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg?style=flat&logo=fastapi&logoColor=white)
![Typer](https://img.shields.io/badge/Typer-CLI-black.svg?style=flat&logo=terminal&logoColor=white)
![PyHanko](https://img.shields.io/badge/PyHanko-PAdES-0052CC.svg?style=flat&logo=adobeacrobatreader&logoColor=white)
![Cryptography](https://img.shields.io/badge/Cryptography-PKI-red.svg?style=flat&logo=moleculer&logoColor=white)

</div>

## Key Features (MVP)

The system focuses on the "Critical Path" of document security:

* **Internal CA (PKI)**: The system acts as its own Trust Anchor. It generates RSA 4096-bit keys and issues **X.509** certificates bundled in secure **PKCS#12** (`.p12`) containers.

* **PAdES Signatures**: Implements **PDF Advanced Electronic Signatures**. It uses **Incremental Updates** to append signatures without breaking the document's binary integrity.

* **Verification & Reporting**: It doesn't just say "Valid" or "Invalid". It generates a detailed **PDF Report** containing the signer's identity, timestamps, integrity status, and hashing algorithms used.

* **Secure Auth**: Stateless authentication using **JWT** (JSON Web Tokens) and **OAuth2** standards.

* **CLI Client**: A dedicated terminal app (built with **Typer**) so you don't have to manually `curl` the API.

## Tech Stack

I chose **Python 3.12** as the core language. Here is why I picked specific tools:

* **FastAPI (Backend)**: I initially considered **Django** (since I knew it well), but I switched to **FastAPI** in Sprint 3. I needed native asynchronous support (**ASGI**) for handling heavy I/O operations like PDF uploads and signing. Plus, automatic Swagger documentation is a lifesaver.

* **MongoDB**: To ensure user data persistence and schema flexibility.

* **PyHanko & Cryptography**: These are the engines under the hood. `pyHanko` handles the complex PDF structure (**LTV**, **PAdES**), while `cryptography` manages the low-level keys and certificates.

* **Typer & Rich**: For building a beautiful, user-friendly CLI.

## Architecture

The system follows a Client-Server model:

* **Client (CLI)**: Sends commands (`register`, `upload`, `sign`, `verify`) and handles file transfers.

* **Server**: Authenticates users via **JWT**, manages the Internal CA, and executes cryptographic operations.

* **Storage**: Securely stores encrypted private keys and user documents.

* **The Workflow**: `Register` (Get `.p12` identity) → `Login` (Get **JWT**) → `Upload PDF` → `Sign` (Server applies **PAdES**) → `Verify` (Get PDF Report).

## Installation & Setup

Want to run this locally? Follow these steps.

1. Clone the repo
```bash
git clone [https://github.com/your-username/file-cert.git](https://github.com/your-username/file-cert.git)
cd file_cert
```
2. Set up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```
3. Install Dependencies
```bash
pip install -r requirements.txt
```
4. Configuration

Create a `.env` file in the root directory. You can use the example below:

```Ini, TOML
SECRET_KEY=generate_a_secure_hex_key_here
ALGORITHM=HS256
MONGO_PATH=mongodb://localhost:27017/
DB_NAME=file_cert_db
CERTS_DIR=./certs
ROOT_CA_KEY=root_ca.key
ROOT_CA_CERT=root_ca.crt
STORAGE=./storage
```
5. Initialize the PKI (Important!)

Before running the server, you need to generate the Root CA (Trust Anchor). I wrote a script for this:
```bash
python init_ca.py
```
This generates the root keys and self-signed certificate required for the system to work.

## Usage
1. Start the Server
```bash
uvicorn app.main:app --reload
```

The API docs will be available at: http://127.0.0.1:8000/docs  

2. Use the CLI Client

Open a new terminal and try the full flow:

#### Register (Auto-generates your keys & certs!)
```bash
python client/client.py register
```
#### Login
```bash
python client/client.py login
```
#### Upload a file
```bash
python client/client.py upload my_thesis.pdf
```
#### Sign it!
```bash
python client/client.py sign my_thesis.pdf
```
#### Verify it (Generates a report)
```bash
python client/client.py verify my_thesis.pdf
```
### License

Distributed under the **MIT License**. See `LICENSE` for more information.

Author: Bartłomiej Adamiec
