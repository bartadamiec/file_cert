# file_cert/generate_certs.sh
#!/bin/bash

# Ustawienie folderu docelowego
DIR="certs"
mkdir -p $DIR

echo "--- 1. Generowanie Root CA (Twój Wewnętrzny Urząd) ---"
# Klucz prywatny Root CA (Tajny!)
openssl genrsa -out $DIR/root_ca.key 4096
# Certyfikat Root CA (Publiczny) - ważny 10 lat
openssl req -x509 -new -nodes -key $DIR/root_ca.key -sha256 -days 3650 \
    -out $DIR/root_ca.crt \
    -subj "/C=PL/ST=Mazowieckie/L=Warszawa/O=FileCert Root Org/CN=FileCert Root CA"

echo "✅ Root CA gotowe."

echo "--- 2. Generowanie kluczy dla Użytkownika (Jan Kowalski) ---"
# Klucz prywatny użytkownika
openssl genrsa -out $DIR/user.key 2048
# Żądanie podpisania certyfikatu (CSR)
openssl req -new -key $DIR/user.key -out $DIR/user.csr \
    -subj "/C=PL/ST=Mazowieckie/L=Warszawa/O=FileCert Users/CN=Jan Kowalski/emailAddress=jan@example.com"

echo "--- 3. Podpisywanie certyfikatu użytkownika przez Root CA ---"
# Root CA podpisuje CSR Jana -> powstaje user.crt
openssl x509 -req -in $DIR/user.csr -CA $DIR/root_ca.crt -CAkey $DIR/root_ca.key -CAcreateserial \
    -out $DIR/user.crt -days 365 -sha256

echo "✅ Certyfikat Jana podpisany."

echo "--- 4. Pakowanie do formatu .p12 (Dla Klienta) ---"
# To jest ten plik, którego użyje pyHanko.
# Zostaniesz poproszony o hasło (ustaw np. 'tajnehaslo')
openssl pkcs12 -export -out $DIR/jan_kowalski.p12 \
    -inkey $DIR/user.key -in $DIR/user.crt \
    -certfile $DIR/root_ca.crt \
    -name "Jan Kowalski ID"

echo "🎉 SUKCES! Wszystkie klucze są w folderze /$DIR"