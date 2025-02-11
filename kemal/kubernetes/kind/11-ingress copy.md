# Kubernetes Ingress Nedir?

**Ingress**, Kubernetes üzerinde çalışan servislerinize (Services) **dış dünyadan / internet üzerinden** erişim sağlamak için kullanılan bir Network nesnesidir. Genellikle bir **Ingress Controller** (Nginx Ingress Controller, Traefik vb.) ile birlikte çalışır ve HTTP/HTTPS gibi katmanlarda istekleri yönlendirerek yük dengeleme, SSL sonlandırması, sanal host (host-based routing) ve yol tabanlı (path-based routing) yönlendirme gibi yetenekler sunar.

---

## Ingress Controller ve Ingress İletişimi

1. **Ingress Nesnesi Tanımlanır**  
   - Kullanıcı, bir YAML manifesti (ör. `my-ingress.yaml`) oluşturur ve `kubectl apply -f` komutuyla Kubernetes'e bildirir.  
   - Bu manifestte, hangi alan ad(lar)ı (`host: example.com`), hangi path'lerin (`/app`) hangi Service'e yönlendirileceği belirtilir.

2. **Kubernetes API Sunucusu (API Server)**  
   - Kullanıcıdan gelen Ingress kaydını Kubernetes veri tabanına (etcd) yazar.  
   - Ingress Controller, Kubernetes API Sunucusuna sürekli sorgu yaparak (watch mekanizması) yeni Ingress tanımlarını veya güncellemeleri takip eder.

3. **Ingress Controller**  
   - Kendi içinde bir Pod (veya Pod seti) olarak çalışır (örn. Nginx Ingress Controller, Traefik vb.).  
   - Kubernetes API Sunucusunu izleyerek (watch) yeni veya değiştirilmiş Ingress kaydı olup olmadığını takip eder.  
   - Bir Ingress kaydı gördüğünde, konfigürasyonunu kendisine entegre eder (ör. Nginx Ingress Controller, Nginx konfigürasyon dosyasını yeniler).
   - Ardından, dış dünyadan gelen HTTP/HTTPS isteklerini, Ingress tanımında yazan kurallara göre ilgili Service(ler)e yönlendirir.

4. **Service & Pod'lar**  
   - Kubernetes Service, küme içindeki Pod'lara sabit bir DNS adı ve sanal IP sağlar.  
   - Ingress Controller, aldığı trafiği hedef Service'in IP:port'una (ya da ClusterIP'sine) gönderir.  
   - Yük dengeleme, path veya host bazlı yönlendirme gibi detaylar Controller üzerinden yönetilir.

<p align="center">
  <img src="https://user-images.githubusercontent.com/ce-sharif/ingress-controller-diagram.png" alt="Ingress ile Ingress Controller İletişimi" width="600" />
</p>

Yukarıdaki diyagramda:
- **(1)** Kullanıcı, bir Ingress tanımlamasını Kubernetes API'sine gönderir.  
- **(2)** Ingress Controller, API Sunucusuna bağlanarak mevcut Ingress kayıtlarını izler.  
- **(3)** Controller, bu bilgileri alarak kendi konfigürasyonunu (örneğin Nginx config) günceller.  
- **(4)** İnternet'ten gelen istekler, Controller'ın dış IP veya LoadBalancer adresine gelir.  
- **(5)** Controller, istekleri Ingress kurallarına göre ilgili Service'e iletir.

---

## Neden Ingress Kullanılır?

1. **Tek Bir Giriş Noktası (Single Entry Point)**  
   - Şirket içi veya buluttaki birçok Service'i, tek bir dış IP veya DNS üzerinden yönetmenizi sağlar.  
   - Servislere (Service) ayrı ayrı LoadBalancer oluşturmak yerine tüm HTTP/HTTPS trafiğini Ingress üzerinden yönlendirebilirsiniz.

2. **HTTP/HTTPS Yönlendirme Kuralları**  
   - Farklı domain (ör. "app.example.com", "api.example.com") veya path ("/login", "/orders") tabanlı yönlendirmeler yapabilirsiniz.  
   - SSL sonlandırması ile TLS sertifikalarını Ingress Controller üstünde yönetmek mümkün.

3. **Maliyet ve Kaynak Yönetimi**  
   - Bulut ortamlarında, her Service için ayrı bir LoadBalancer kaynağı (örn. AWS ELB/ALB) ayırmak pahalı olabilir. Ingress ile tek seferde tüm HTTP trafiğini yönetmek daha verimli bir çözüm sunar.

4. **Gelişmiş Yük Dengeleme (Load Balancing)**  
   - Layer 7 routing yetenekleriyle, istekleri ilgili backend Service'e yönlendirir.  
   - Metrikler, kurallar, rate limiting, ip kısıtlaması, webhook gibi ek özellikler eklenebilir (Ingress Controller'ınızın yeteneklerine göre).

---

## Service ile Ingress Nasıl Kullanılır?

Bir Kubernetes Service, küme içindeki Pod'ları sabit IP ve isim sağlayarak temsil eder. Ancak Servis dış dünyaya açılmak istenirse iki temel yaklaşım bulunur:

1. Her Servis için **NodePort** veya **LoadBalancer** tipi kullanmak.  
2. Tüm HTTP/HTTPS servislerini **Ingress** üzerinden yönlendirmek.

İkinci yaklaşımın avantajı, tek bir dış IP/LoadBalancer üzerinden birden fazla Servise ulaşımı **host-based** veya **path-based** olarak yönetebilmenizdir.

Aşağıdaki şemada bunun mantığı görülmektedir:

```
        Internet
           |
       [ Ingress Controller ]   <- (Nginx, Traefik, vb.)
       /            \
      /              \
[web-app-service]    [api-service]
```

- "web-app-service" ve "api-service" küme içinde sadece "ClusterIP" olarak tanımlanabilir.  
- Ingress, gelen trafiği (örneğin "/app" ve "/api") bu Servislere yönlendirir.

---

## Örnek Ingress Manifesti

Aşağıdaki örnekte, "my-ingress" isimli bir Ingress tanımını görüyoruz. Bu Ingress, "example.com" alan adına gelen isteklerde "/app" yolunu "web-app-service" isimli Service'e yönlendirir:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  annotations:
    # Nginx Ingress Controller örneği
    kubernetes.io/ingress.class: "nginx"
spec:
  rules:
  - host: example.com
    http:
      paths:
      - path: /app
        pathType: Prefix
        backend:
          service:
            name: web-app-service
            port:
              number: 80
```

1. **`kubernetes.io/ingress.class: "nginx"`**  
   - Bu Ingress tanımının Nginx Ingress Controller tarafından yönetileceğini belirtir.  
2. **`rules.host: example.com`**  
   - "example.com" alan adına gelen trafiği yönlendirmeye yarayan kural.  
3. **`path: /app`**  
   - "/app" path'i ile gelen istekleri "web-app-service"e iletir.  
4. **`service.name: web-app-service`**  
   - Ingress, hedef Service olarak "web-app-service"i kullanır.  
5. **`service.port.number: 80`**  
   - Service'in 80 numaralı portunu dinler.

> Dış dünyadan `http://example.com/app` ile gelen istek, Ingress üzerinden `web-app-service`in 80 numaralı portuna yönlendirilir. Service de Pod'lara yükü dağıtır.

---

## Ingress Controller Tipik Kurulum Süreci

1. **Controller'ı Kurma**  
   - Nginx Ingress Controller, Traefik, HAProxy, Kong veya Istio Gateway gibi bir Ingress Controller seçip kümenize yükleyin (Helm, Operator, YAML vb. ile).
2. **Public IP / LoadBalancer**  
   - Ingress Controller Pod'ları genelde bir Service (tipik olarak `type: LoadBalancer`) aracılığıyla dış IP elde eder.  
   - Böylece internet üzerinden gelen trafik Ingress Controller'a gelir.
3. **Ingress Tanımı Ekleme**  
   - Yukarıdaki örnekteki gibi YAML dosyalarıyla Ingress kuralları eklersiniz.  
   - Controller, API Server'a kaydedilen Ingress kaydını okuyarak konfigürasyonunu günceller.
4. **Trafik Yönlendirme ve Test**  
   - "example.com" DNS adınız Ingress Controller'ın IP'sine yönlendirilir.  
   - Kullanıcılar `http://example.com/app` adresini ziyaret ettiğinde, Ingress Controller istekleri "web-app-service" Pod'larına dağıtır.

---

## Özet Avantajlar

1. **Daha Az Kaynak Tüketimi**  
   - Çok sayıda Service'in her birini LoadBalancer yapmak yerine tek bir LoadBalancer + Ingress Controller yaklaşımıyla maliyetler düşer.  
2. **Ölçeklenebilirlik**  
   - Yeni bir Service eklediğinizde, yalnızca Ingress nesnesine ekleme yaparak trafiği yönlendirebilirsiniz.  
3. **Zengin Routing Kuralları**  
   - Path-based, host-based routing, SSL/TLS desteği, HTTP üstbilgisi yönlendirmesi gibi Layer 7 özelliklerini destekler.  
4. **Kolay Yönetim**  
   - Tüm HTTP/HTTPS giriş noktalarını tek yerde (Ingress Controller) sade bir YAML tanımıyla yönetebilirsiniz.

---

## Sonuç

**Ingress**, Kubernetes'te **servisleri dışa açmak** için kullanılan güçlü ve esnek bir ağ bileşenidir.  
- Bir **Ingress Controller** (örn. Nginx, Traefik) ile API'yi izleyerek Ingress tanımlarını düzenli olarak günceller ve uygular.  
- **Tek noktadan** çeşitli Service'lere HTTP/HTTPS yönlendirmesi yapabileceğiniz için hem basit hem de ekonomik bir çözüm sunar.  
- SSL sonlandırma, domain/path bazlı routing, yüksek seviyeli güvenlik ve yönetim özellikleriyle **mikroservis** mimarilerinde popüler ve **kritik** bir parçadır.
