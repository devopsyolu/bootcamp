#!/bin/bash

# Kalıcı log dosyası
LOG_FILE="/var/log/update_log.txt"

# Güncelleme işlemlerini log dosyasına yazdır
{
    echo "Güncelleme Başladı: $(date)"
    sudo apt update && sudo apt upgrade -y
    echo "Güncelleme Tamamlandı: $(date)"
} >> "$LOG_FILE" 2>&1

