Plan:
M1 Koncept i Research
14.10.2025 - 27.10.2025
Wstępne zdefiniowanie zamysłu projektu
Znalezienie literatury omawiające zagadnienie
Znalezienie bibliotek z których będę korzystać
Kryterium przejścia:
Zdefiniowany koncept projektu
Zgromadzenie pozycji literatury

M2
3.11.2025 -12.11.2025
Diagram use case w notacji UML 
Zdefiniowanie MVP produktu
Abstrakt 
Utworzenie repozytorium Git
Wstępna konfiguracja środowiska roboczego
Udostępnienie folderu z dokumentacją
Zdobyta wiedza:
PKI - private key infrastructure
Podczas podpisu, podpisujące jest uwierzytelniany za pomocą klucza prywatnego (ceryfikat X.509)
Kryterium przejścia:
Utworzone reopozytorium Git
Skonfigurowane środowisko
Gotowy diagram Use Case
Zrozumienie PKI

M3
13.11.2025 - 24.11.2025
Nauka PyHanko
Nauka FastAPI
Zdobyta wiedza:
Struktura podpisu 
Zakres bajtów które pokrywa podpis
Funkcja Hashująca
Polityka modyfikacji
Kryterium przejścia:
Podstawowe rozumienie działania PyHanko, FastAPI
Zdobyta wiedza o strukturze plików PDF
Udostępnienie folderu z dokumentacją

M4 Fundament
25.11.2025 - 8.12.2025
Serwer FastAPI działa bez błędów
Napisać pierwsze endpointy
Można przesłać PDF przez API (POST), plik zostaje zapisany
Wygenerowane certyfikaty testowe (.p12, na dysku lokalnym)
Kryterium przejścia: 
plik PDF na serwerze
.p12 na dysku
 
M5 Kryptografia i podpis
9.12.2025 - 22.12.2025
Endpoint POST /sign pobiera plik z serwera
Nałożenie podpisu PAdES używając lokalnego certyfikatu .p12
Utworzenie nowego pliku, który zostaje rozpoznany przez program Adobe Reader jako “podpisany”

Kryterium przejścia: 
plik PDF z widocznym panelem podpisu

M6 Weryfikacja i raport
28.12.2025 - 5.01.2026
Endpoint POST /verify przyjmuje podpisany plik
Backend zwraca plik JSON, np.  {"valid": true, "signer": "Jan Kowalski"}
Generowanie raportu w postaci pliku PDF, potwierdzającego lub negujące weryfikacje
Endpointy /auth, /login,  generowanie tokenów (JWT) i zabezpieczenie endpointów.
Kryterium przejścia: 
API zwraca wartość True dla podpisanego niemodyfikowanego po podpisie pliku lub wartość False, w przypadku, gdy plik jest niepodpisany, bądź został zmodyfikowany po podpisie.


M7 Klient CLI
6.01.2026 - 19.01.2026
*Obsługa z poziomu CLI
Kryterium przejścia: 
Działający proces z poziomu CLI. Przykład:
Klient uruchamia skrypt 
>>>python client.py sign <nazwa_pliku>.pdf
<nazwa_pliku>_signed.pdf
Skrypt wysyła plik →  czeka na odpowiedź serwera podpisującego → pobiera podpisany plik na dysk lokalny

M8 Final
20.01.2026 -26.01.2026
Testowanie programu
Utworzenie pliku README.md, który opisuje proces instalacji potrzebnych bibliotek oraz uruchomienia od początku programu
Dokumentacja zredagowana zgodnie ze standardem IEEE

Kryterium przejścia
Program działa zgodnie z zamysłem bez błędów
Dokumentacja zgodna ze standardem IEEE
