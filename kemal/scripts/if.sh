#!/bin/bash
if [ -f "/etc/passwd" ]; then
    echo "/etc/passwd dosyası mevcut."
else
    echo "/etc/passwd dosyası bulunamadı (çok olası değil!)."
fi
