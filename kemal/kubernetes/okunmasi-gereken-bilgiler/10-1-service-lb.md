# Kubernetes Service: LoadBalancer Tipi

Kubernetes'te bir **Service**, Pod'lara sabit bir DNS ismi ve IP adresi sağlayarak **iç** (ClusterIP) veya **dış** (NodePort, LoadBalancer) ağ erişimini düzenler.  
Eğer Servis'in **type** alanı `LoadBalancer` olarak tanımlanırsa, Kubernetes **bulut sağlayıcısıyla** (AWS, GCP, Azure vb.) entegre çalışarak **harici** bir yük dengeleyici (Load Balancer) oluşturur. Böylece internet üzerinden, tek bir IP veya DNS adresiyle bu Servis'e erişmek mümkün hale gelir.

---

## LoadBalancer Servis Nedir?

1. **Harici Erişim (External Access)**  
   - Service, `type: LoadBalancer` olarak ayarlandığında, bulut sağlayıcı otomatik olarak bir **Layer 4** (TCP/UDP) veya **Layer 7** (elbette sağlayıcı desteğine göre) yük dengeleyici oluşturur.  
   - Örnek: AWS üzerinde "ELB/ALB," GCP üzerinde "Network/HTTP(S) Load Balancer" gibi kaynaklar devreye girer.

2. **Dinamik IP veya DNS**  
   - Bulut sağlayıcısı, oluşturduğu Load Balancer'a bir **harici IP adresi** veya **DNS adı** atar.  
   - Bu adres veya DNS, Kubernetes dışındaki istemcilerin (ör. son kullanıcı tarayıcıları) Servis'e erişmesini sağlar.

3. **Pod Trafik Yönlendirmesi**  
   - Load Balancer'a gelen trafik, Kubernetes'in arka planda oluşturduğu NodePort ve iptables/ipvs kuralları aracılığıyla doğru Pod'lara yönlendirilir.  
   - Service, istediğiniz portları açmanızı sağlar. Tüm Node'lara aynı NodePort atanır, Load Balancer da hangi Node'a gidilmesi gerektiğini bilir.

4. **Bulut Tabanlı Yetenekler**  
   - Sağlayıcının sunduğu ek özellikler (örn. SSL terminasyonu, health check, cross-zone load balancing) LoadBalancer servise entegre edilebilir.  
   - Örneğin AWS'de health check için "/healthz" endpoint'i tanımlayabilir, Azure'da Public/Private LB türlerini seçebilirsiniz.

5. **Maliyet ve Kapsam**  
   - Her LoadBalancer Servisi, bulut sağlayıcı tarafında fiziksel ya da sanal bir yüke (kaynağa) dönüşür. Bu, ek maliyet anlamına gelebilir.  
   - Özellikle çok sayıda Service'i dışa açmak istediğinizde, Ingress gibi çözümlerle tek bir Load Balancer üzerinden birden fazla Service yönetme seçeneği düşünülür.

---

## Örnek LoadBalancer Service Manifesti

Aşağıda, "web-app-service" adında `type: LoadBalancer` bir Service tanımı görebilirsiniz:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-app-service
spec:
  type: LoadBalancer
  selector:
    app: web-app
  ports:
    - port: 80
      targetPort: 8080
      protocol: TCP
```

1. **`type: LoadBalancer`**  
   - Bulut sağlayıcısına "Servis için bir yük dengeleyici oluştur" talimatıdır.  
2. **`selector: app: web-app`**  
   - `app=web-app` etiketine sahip Pod'lara trafiği yönlendireceğini belirtir.  
3. **`ports.port: 80 -> targetPort: 8080`**  
   - Harici istekler 80 portundan kabul edilir, Pod'da çalışan uygulamanın 8080 portuna iletilir.  
4. **Sağlayıcı Bağlı Parametreler**  
   - AWS, GCP, Azure gibi platformlarda, Service'e ek annotation veya parametre eklenerek (örn. `service.beta.kubernetes.io/aws-load-balancer-internal: "true"`) farklı LB özellikleri ayarlanabilir.

---

## LoadBalancer ve NodePort Farkı

- **NodePort**  
  - Service, her Node üzerinde belirlenen bir port açar (30000-32767 arası).  
  - Dış erişim için Node IP + NodePort kullanılır, ek bir Load Balancer gerekmez.  
  - Genelde geliştirme/test amaçlı ya da basit senaryolarda tercih edilir.  

- **LoadBalancer**  
  - Otomatik bir dış Load Balancer kaynağı oluşturur (Cloud Provider).  
  - "Kullanım kolaylığı" ve "harici trafik" için ideal bir yaklaşım (özellikle üretim ortamlarında).  
  - Daha profesyonel yük dengeleme özellikleriyle gelir.  

---

## LoadBalancer Servisi Kullanmanın Artıları

1. **Kolay Dış Erişim**  
   - Tek bir kubectl manifestiyle uygulamanızın dış dünyaya açılmasını sağlayabilirsiniz.  
2. **Bulut Uyumlu Otomasyon**  
   - AWS, GCP veya Azure, LB kaynaklarını otomatik oluşturarak yönetir; fikir veya API bilgisi gerekmez.  
3. **Sağlayıcı Özellikleri**  
   - Health check, SSL terminasyonu, güvenlik duvarı kuralları gibi ek bulut özelliklerini servise entegre edebilirsiniz.  

---

## Dezavantajlar ve Alternatifler

1. **Ek Maliyet**  
   - Her LoadBalancer Servisi, bulut sağlayıcısında ek bir kaynak oluşturduğundan ekstra ücretlendirme olabilir.  
2. **Sınırlı Layer 7 Routing**  
   - LoadBalancer tipi Service genelde Layer 4 (TCP/UDP) seviyesinde, bazen sınırlı Layer 7 özellikleriyle çalışır. Gelişmiş yönlendirme (ör. path-based) için Ingress kullanılabilir.  
3. **Çok Servis Senaryolarında Dağınıklık**  
   - Bir kümeye birçok LoadBalancer eklendiğinde yönetilmesi güçleşebilir. Yüksek trafik ve çok mikrosite barındıran ortamlarda **Ingress Controller** tercih edilir.

---

## Sonuç

**LoadBalancer tipi Service**, Kubernetes'te **harici** (internet üzerinden) erişimi en hızlı ve basit şekilde etkinleştiren seçenektir.  
- Küme içindeki Pod'ları hedef alan bir Service, bulut sağlayıcınızla entegre biçimde otomatik bir **Load Balancer** kaynağı oluşturur.  
- Yeni bir IP veya DNS adı verilir ve internet üzerinden doğrudan bu Service'e ulaşılabilir.  
- Fazla sayıda dışa açık uygulama için maliyet veya yönetim karmaşası artabileceğinden **Ingress** gibi çözümler de göz önünde bulundurulmalıdır.
