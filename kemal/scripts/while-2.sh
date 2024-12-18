#!/bin/bash

# Sayaç değişkeni
counter=1

echo "Bir while döngüsü başlatılıyor. Sayaç 5 olduğunda duracak."

while true; do
    # Sayaç değerini ekrana yazdır
    echo "Sayaç: $counter"

    # Sayaç 5'e ulaşırsa döngüyü sonlandır
    if [ $counter -eq 5 ]; then
        echo "Sayaç 5 oldu, döngü sona eriyor..."
        break
    fi

    # Sayaç değerini artır
    counter=$((counter + 1))
    
    # Bir süre beklemek için (isteğe bağlı)
    sleep 1
done

echo "Döngü tamamlandı."
