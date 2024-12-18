echo "For Döngüsü Örneği (liste):"
for item in "merhaba" "dünya" "linux" "bash"
do
    echo "Kelime: $item"
    sleep 1
done


sleep 3

echo "For Döngüsü Örneği (aralık):"
for i in {1..5}; do
    echo "Sayı: $i"
    sleep 1
done

echo "For Döngüsü Örneği (klasördeki dosyalar):"
for dosya in *.txt; do
    echo "Bulunan txt dosyası: $dosya"
done
