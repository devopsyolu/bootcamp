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

# Nginx ile Yük Dengeleme ve Reverse Proxy Kullanımı

## Docker Container'ları Oluşturma

Nginx'de yük dengeleme (Load Balancing) kullanmak için öncelikle Flask uygulamalarını Docker container'lar olarak çalıştırın. Bu adımları izleyebilirsiniz:

1. Aşağıdaki komutları çalıştırabilmek için Dockerfile ile aynı dizinde (örneğin `/nginx/flask/`) olmalısınız.

   ### Flask Uygulamalarının Docker Container Olarak Oluşturulması:
   ```bash
   docker build -t flask5000 .
   docker run -d -p 5000:5000 flask5000

   docker build -t flask5001 .
   docker run -d -p 5001:5001 flask5001
   ```

2. Container'ların çalıştığını test etmek için:
   ```bash
   curl localhost:5000
   curl localhost:5001
   ```

## Nginx ile Yük Dengeleme (Load Balancing)

### Nginx Yapılandırması

Nginx'in kurulu olduğunu varsayarak, şu adımları takip edin:

1. **Konfigürasyon Dosyası:**
   - `nginx.conf` dosyasını düzenleyin veya `/etc/nginx/sites-enabled/` dizininde yeni bir dosya oluşturun.
   - Alternatif olarak, bu klasörde bulunan mevcut `lb.conf` dosyasını kullanabilirsiniz.

2. **Nginx Servisinin Yönetimi:**
   ```bash
   sudo systemctl status nginx # Durumu kontrol edin
   sudo systemctl start nginx  # Servisi başlatın
   ```

3. **Dinlenen Portları Kontrol Etme:**
   ```bash
   sudo ss -tulpn
   ```

### Yapılandırma Detayları

- Bu yük dengeleme konfigurasyonunda, 8080 portunda yayın yapılır.
- `server_name` olarak `nginx.devopsyolu.tr` tanımlıdır. Eğer bir alan adınız yoksa, bunu `_` ile değiştirebilirsiniz.

### Flask Uygulamalarında Değişiklik Yapma

Flask uygulamalarının içinde POST, DELETE gibi özellikleri test edebilirsiniz. Bununla ilgili açıklamalar `app.py` dosyasında mevcuttur.

## Nginx ile Reverse Proxy

### Reverse Proxy Konfigürasyonu

Nginx'de reverse proxy kullanmak için önceden hazırlanmış `reverseproxy.conf` dosyasını kullanabilirsiniz. Bu dosyada yük dengeleme özelliklerinin yanı sıra, belirli yolların belirli portlara yönlendirilmesi tanımlanmıştır.

### Reverse Proxy Detayları

1. **/app1 Yolu:**
   - `/app1` yoluna gelen istekler sadece 5000 portundaki container'dan yanıt alır.
   - `app1` tanımı, 5001 portundaki container'da yoktur. Bu nedenle, bu davraşı anlamak için `app.py` dosyasını inceleyebilirsiniz.

2. **Dinlenen Port:**
   - Reverse proxy özelliği, 8081 portunda dinleme yapar. Bu ayarları kendi ihtiyaçlarınıza göre değiştirerek test edebilirsiniz.

### Reverse Proxy Amacı

Reverse proxy, gelen istemci isteklerini uygun şekilde içerideki sunuculara yönlendirmek için kullanılır. Bu özelliği kullanarak uygulamanızın çeşitli senaryolarını test edebilirsiniz.

