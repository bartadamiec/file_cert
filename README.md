https://docs.google.com/document/d/1mjJg9eoLCQeHyMP73PZQIEXsJfVzDKS_/edit
# File Cert: Secure PAdES Signing System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

**File Cert** to system backendowy zaprojektowany do bezpiecznego, kryptograficznego podpisywania i weryfikacji dokumentów PDF zgodnie ze standardem **PAdES** (PDF Advanced Electronic Signatures). Projekt realizowany jest jako praca inżynierska, kładąc nacisk na bezpieczeństwo danych, infrastrukturę PKI oraz architekturę systemów rozproszonych.

---

## 🚀 Kluczowe Funkcjonalności

* **Zarządzanie Plikami:** Bezpieczne przesyłanie i przechowywanie dokumentów PDF.
* **Podpis Elektroniczny:** Implementacja standardu PAdES (LTV enabled) przy użyciu biblioteki `pyHanko`.
* **Infrastruktura PKI:** Obsługa kluczy RSA i certyfikatów X.509 (obsługa formatu `.p12`).
* **Weryfikacja Integralności:** Sprawdzanie poprawności kryptograficznej podpisu oraz integralności pliku (wykrywanie modyfikacji).
* **Raportowanie:** Generowanie raportów walidacyjnych w formacie PDF.
* **Klient CLI:** Dedykowane narzędzie wiersza poleceń do interakcji z API.

---

## 🛠️ Stack Technologiczny

* **Język:** Python 3.11+
* **Backend Framework:** FastAPI (ASGI)
* **Serwer:** Uvicorn
* **Kryptografia & PDF:** pyHanko, OpenSSL, Cryptography
* **Walidacja Danych:** Pydantic
* **Narzędzia:** Git, Swagger UI (OpenAPI)

---

## 📅 Harmonogram Realizacji (Roadmap)

Projekt realizowany jest w cyklach (Kamieniach Milowych). Poniżej znajduje się szczegółowy harmonogram prac.

### ✅ M1: Koncept i Research
**Termin:** 14.10.2025 - 27.10.2025
- [x] Zdefiniowanie wstępnego konceptu projektu.
- [x] Analiza literatury i standardów (PAdES, PKI).
- [x] Dobór stosu technologicznego (FastAPI, pyHanko).

### ✅ M2: Projektowanie Systemu
**Termin:** 03.11.2025 - 12.11.2025
- [x] Opracowanie diagramów Use Case (UML).
- [x] Zdefiniowanie MVP (Minimum Viable Product).
- [x] Konfiguracja repozytorium Git i środowiska CI/CD.
- [x] Analiza teoretyczna infrastruktury PKI (Private Key Infrastructure).

### ✅ M3: Analiza Techniczna (Deep Dive)
**Termin:** 13.11.2025 - 24.11.2025
- [x] Niskopoziomowa analiza struktury PDF (ByteRange, Incremental Update).
- [x] Nauka biblioteki `pyHanko` oraz frameworka `FastAPI`.
- [x] Zrozumienie polityki modyfikacji i funkcji skrótu (SHA-256).

### 🚧 M4: Fundament Aplikacji (Obecny Etap)
**Termin:** 25.11.2025 - 08.12.2025
- [ ] Implementacja serwera FastAPI (Setup & Configuration).
- [ ] Stworzenie endpointu `/upload` (obsługa przesyłania plików).
- [ ] Generowanie testowych certyfikatów X.509 i kontenerów `.p12` (OpenSSL).
- **Cel:** Działający upload plików i gotowe środowisko kryptograficzne.

### 📅 M5: Implementacja Podpisu (Core)
**Termin:** 09.12.2025 - 22.12.2025
- [ ] Implementacja endpointu `/sign`.
- [ ] Integr
