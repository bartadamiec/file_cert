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

echo "--- 3. Podpisywanie certyfikatu użytkownika przez Root CA (Z DODANIEM UPRAWNIEŃ) ---"
# Tworzymy tymczasową konfiguraję rozszerzeń, której brakowało wcześniej
# nonRepudiation - to jest to, czego wymagało PyHanko!
EXTENSIONS="keyUsage = critical, digitalSignature, nonRepudiation"

# Root CA podpisuje CSR Jana, wstrzykując wymagane flagi
openssl x509 -req -in $DIR/user.csr \
    -CA $DIR/root_ca.crt -CAkey $DIR/root_ca.key -CAcreateserial \
    -out $DIR/user.crt -days 365 -sha256 \
    -extfile <(echo "$EXTENSIONS")

echo "✅ Certyfikat Jana podpisany (z flagą nonRepudiation)."

echo "--- 4. Pakowanie do formatu .p12 (Dla Klienta) ---"
# Usuwamy stary plik p12 jeśli istnieje, żeby nie było konfliktów
rm -f $DIR/jan_kowalski.p12

# Pakujemy nowy certyfikat
openssl pkcs12 -export -out $DIR/jan_kowalski.p12 \
    -inkey $DIR/user.key -in $DIR/user.crt \
    -certfile $DIR/root_ca.crt \
    -name "Jan Kowalski ID" \
    -passout pass:tajnehaslo

# UWAGA: Ustawiłem hasło na sztywno: 'tajnehaslo' (dla łatwości testów),
# żebyś nie musiał go wpisywać ręcznie przy każdym uruchomieniu skryptu.

echo "🎉 SUKCES! Wszystkie nowe klucze są w folderze /$DIR"