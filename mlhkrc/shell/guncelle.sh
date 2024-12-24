#!/bin/bash

# Log dosyası yolu
LOG_FILE="/tmp/guncelle.txt"

# Güncelleme işlemlerini log dosyasına yazdır
{
    echo "Güncelleme Başladı: $(date)"
    sudo apt update && sudo apt upgrade -y
    echo "Güncelleme Tamamlandı: $(date)"
} >> "$LOG_FILE" 2>&1
