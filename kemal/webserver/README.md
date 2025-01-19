# Apache Server Testi ve Docker Kullanımı

Bu rehber, Docker kullanarak basit web sunucularını çalıştırmayı ve Apache HTTP Server ile yük dengeleme (load balancing) işlemini nasıl gerçekleştireceğinizi açıklar.

## Docker ile Basit Web Sunucuları Çalıştırma

Aşağıdaki komutlarla iki adet Docker container oluşturabilirsiniz. Bu container'ların içinde Python ile yazılmış basit bir web sunucusu çalışacaktır.

### 1. İlk Container (Port 8080)
```bash
docker build -t app8080 -f Dockerfile8080 .
docker run -d -p 8080:8080 app8080
```

### 2. İkinci Container (Port 8081)
```bash
docker build -t app8081 -f Dockerfile8081 .
docker run -d -p 8081:8081 app8081
```

### Test Etme
Container'ların çalıştığını aşağıdaki adreslerden kontrol edebilirsiniz:
- [http://localhost:8080](http://localhost:8080)
- [http://localhost:8081](http://localhost:8081)

Alternatif olarak, `curl` komutunu kullanabilirsiniz:
```bash
curl localhost:8080
curl localhost:8081
```

## Apache HTTP Server ile Yük Dengeleme (Load Balancing)

Apache HTTP Server'ı yük dengeleme amacıyla kullanmak istiyorsanız, `loadbalance.config` dosyasını Apache'nin yapılandırma dizininde kullanmanız gerekmektedir.

### Apache Servisinin Yönetimi
- Apache'nin çalışıp çalışmadığını kontrol etmek:
  ```bash
  sudo systemctl status apache2
  ```
- Apache'yi başlangıçta çalıştırmak için etkinleştirmek:
  ```bash
  sudo systemctl enable apache2
  ```
- Apache'yi başlatmak:
  ```bash
  sudo systemctl start apache2
  ```

### Portları Kontrol Etme
```bash
sudo ss -tulpn | grep LISTEN
```

### Apache Yük Dengeleme Yapılandırması

Apache'yi Docker ile veya işletim sistemi üzerinde kurabilirsiniz. Kurulum tamamlandıktan sonra aşağıdaki adımları izleyin:

1. **Yapılandırma Dosyasını Kopyalayın**
   `loadbalance.config` dosyasını Apache'nin yapılandırma dizinine kopyalayın:
   - Ubuntu'da:
     ```bash
     sudo cp loadbalance.config /etc/apache2/sites-available/
     ```
   - Alternatif olarak doğrudan:
     ```bash
     sudo cp loadbalance.config /etc/apache2/sites-enabled/
     ```

2. **Yapılandırmayı Etkinleştirin**
   Yapılandırmayı etkinleştirmek için:
   ```bash
   sudo a2ensite loadbalance.config
   ```

3. **Apache'yi Yeniden Başlatın**
   Değişikliklerin geçerli olması için Apache'yi yeniden başlatın:
   ```bash
   sudo systemctl restart apache2
   ```

# Reverse Proxy ile API Yönlendirme

Mevcut çalışan container için `/api` isteklerini bir hedef container'a yönlendirmek için reverse proxy kullanabilirsiniz. Bu amaçla, önceden hazırlanmış olan `reverseproxy.conf` dosyasını kullanabilirsiniz.

## Reverse Proxy Yapılandırması

Bu yapılandırma ile gelen istekler `/api` yoluna ulaştığında, 8080 portunda çalışan container'ınıza yönlendirilecektir.

### Adımlar

1. **reverseproxy.conf Dosyasını Hazırlama**
   `reverseproxy.conf` dosyası, Apache reverse proxy örneğidir:

2. **Dosyayı Apache Yapılandırma Dizini’ne Kopyalama**
   Apache kullanıyorsanız, dosyayı aşağıdaki komutla uygun dizine kopyalayın:
   ```bash
   sudo cp reverseproxy.conf /etc/apache2/sites-available/
   ```

3. **Konfigürasyonu Etkinleştirme**
   Apache'de bu dosyayı etkinleştirmek için aşağıdaki komutu çalıştırın:
   ```bash
   sudo a2ensite reverseproxy.conf
   ```

4. **Apache'yi Yeniden Başlatma**
   Yaptığınız değişikliklerin etkili olması için Apache'yi yeniden başlatın:
   ```bash
   sudo systemctl restart apache2
   ```

5. **Test Etme**
   Tarayıcınızdan veya `curl` komutuyla API isteklerini test edebilirsiniz:
   ```bash
   curl http://localhost/api
   ```

Bu adımlar tamamlandığında, `/api` istekleri 8080 portundaki container'ınıza yönlendirilmiş olacaktır.

Dosyalardaki servername kısmına dikkat edin.
