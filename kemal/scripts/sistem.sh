#!/bin/bash

echo "=== Sistem Bilgileri ==="

# 1. Mevcut kullanıcıyı göster
echo "Şu anki kullanıcı: $(whoami)"

# 2. Sistemin çalışma süresini göster
echo "Sistem çalışma süresi: $(uptime -p)"

# 3. Disk kullanımını göster
echo "Disk kullanımı:"
df -h | grep "^/dev"

# 4. Çalışan ilk 3 süreci göster
echo "Çalışan en yoğun 3 süreç:"
ps aux --sort=-%mem | head -n 4

echo "=== İşlem Tamamlandı ==="
