# Kubernetes Gateway API Nedir?

**Gateway API**, Kubernetes topluluğunun ağ yönlendirme (networking) temelini zenginleştirmek ve standartlaştırmak için geliştirdiği yeni bir **daha geniş özellikli** API setidir. Mevcut **Ingress** nesnesine kıyasla daha esnek, genişletilebilir (extensible) ve rollere dayalı (role-oriented) bir özellikle geliştirilmiştir. Daha karmaşık trafik yönlendirme senaryolarında (örneğin farklı katmanlar, proxyler, canary deployment, multi-cluster iletişim vb.) daha modüler bir yaklaşım sunar.

## Neden Gateway API?

1. **Genişletilebilirlik (Extensibility)**  
   - Yeni protokoller, gelişmiş yönlendirme kuralları, yetkilendirme, uç (edge) proxy vb. konuları ele almak için Ingress API'sinden daha geniş bir kapsama sahiptir.

2. **Role-Oriented Tasarım**  
   - Ağ yöneticisi, uygulama geliştirme ekibi ve platform yöneticisini birbirinden ayrıştırabilecek bir yapıdadır.  
   - Örneğin "infrastructure provider" Gateway nesnesi oluştururken, "application owner" HTTPRoute nesnelerini yönetebilir.

3. **Çeşitli Kaynak Türleri**  
   - Gateway API, Ingress gibi tek bir kaynaktan ziyade, birden fazla kaynağa (ör. Gateway, HTTPRoute, TCPRoute, TLSRoute, UDPRoute, gRPCRoute) sahiptir. Her biri farklı yönlendirme senaryolarını temsil eder.

4. **Controller'ların Kolay Entegrasyonu**  
   - Herhangi bir ağ (network) veya "service mesh" sağlayıcısı, Gateway API kaynaklarını **destekleyen** bir Controller yazarak Kubernetes'e sorunsuz şekilde entegre olabilir (örn. Contour, Istio, HAProxy, Traefik, Nginx vb.).

---

## Gateway API Temel Nesneleri

### 1. GatewayClass

- **GatewayClass**, "Gateway" kaynaklarının nasıl oluşturulduğunu belirleyen bir **şablon** ya da **sürücü** gibidir.  
- Tıpkı StorageClass'ın PersistentVolume oluşturma yöntemlerini tarif etmesi gibi, GatewayClass da bir **networking / load balancer** sağlayıcısının kurallarını, özelliklerini tanımlar.  
- Bir kümede çoklu GatewayClass tanımlanabilir (ör. "public-lb-class", "private-lb-class").

Örnek GatewayClass tanımı:

```yaml
apiVersion: gateway.networking.k8s.io/v1beta1
kind: GatewayClass
metadata:
  name: public-lb-class
spec:
  controllerName: example.net/gateway-controller
```
> Bu, "public-lb-class" adlı bir GatewayClass oluşturur, `controllerName` alanı hangi controller'ın bu GatewayClass'ı yöneteceğini gösterir.

### 2. Gateway

- **Gateway**, yük dengeleme veya trafik yönlendirme noktasını temsil eder; bir nevi "Ingress Controller"a benzer ama daha modüler.  
- Hangi protokol ve port'un dinleneceğini, hangi IP veya host(lar) üzerinde yayına açılacağını ve hangi GatewayClass'ı kullanacağını belirtir.

Örnek bir Gateway manifesti:

```yaml
apiVersion: gateway.networking.k8s.io/v1beta1
kind: Gateway
metadata:
  name: public-gateway
spec:
  gatewayClassName: public-lb-class
  listeners:
  - name: http
    protocol: HTTP
    port: 80
    hostname: "example.com"
  - name: https
    protocol: HTTPS
    port: 443
    hostname: "example.com"
    tls:
      mode: Terminate
      certificateRef:
        kind: Secret
        name: tls-secret
```
Açıklamalar:  
- `gatewayClassName: public-lb-class` → Bu Gateway, "public-lb-class" GatewayClass tarafından yönetilecek.  
- İki tane "listener" var: HTTP (80) ve HTTPS (443).  
- Hostname "example.com" üzerinden gelen trafiği alacak. HTTPS için "tls-secret" (bir Kubernetes Secret) kullanarak SSL sonlandırma yapacak.

### 3. Route (HTTPRoute, TCPRoute, TLSRoute, UDPRoute, GRPCRoute)

- **Route** nesneleri, trafik yönlendirmesinde esneklik sağlar.  
- Örneğin **HTTPRoute** ile path, header veya host bazında kural yazabilir; **TCPRoute** veya **TLSRoute** ile TCP/TLS seviyesinde yönlendirme gerçekleştirebilirsiniz.  
- Route, Gateway'e "bağlanarak" veya "ref" vererek ilgili Gateway'in hangi trafiği Route'un tanımladığı yere yönlendirmesi gerektiğini belirtir.

Örnek HTTPRoute:

```yaml
apiVersion: gateway.networking.k8s.io/v1beta1
kind: HTTPRoute
metadata:
  name: web-app-route
spec:
  parentRefs:
  - name: public-gateway
    sectionName: http
  hostnames:
  - "app.example.com"
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: "/"
    backendRefs:
    - name: web-app-service
      port: 80
```

Açıklamalar:  
- `parentRefs: public-gateway` → Bu HTTPRoute, "public-gateway" isimli Gateway'in "http" 
  listener'ına bağlanıyor.  
- `hostnames: "app.example.com"` → Bu Route sadece bu hostname'e gelen isteklerle ilgilenir.  
- `rules` bölümündeki `matches` → "/" path'ine gelen trafiği `web-app-service`in 80 numaralı portuna yönlendirir.

### 4. Backend (Service, Policy vb.)

- Route nesnelerinde "backendRefs" ile tanımlanan hedef, tipik olarak bir **Service** (örn. `web-app-service`).  
- Böylece Gateway → HTTPRoute → Service → Pod zinciriyle trafik yönlendirilir.

---

## Gateway API Nesneleri Arası İlişki

1. **GatewayClass** → "Hangi yük dengeleyici / ağ controller'ına sahibiz?" sorusunu yanıtlar.  
2. **Gateway** → "Bu yük dengeleyiciyi nasıl konfigüre ediyoruz? (port, IP, protokol, sertifika, vb.)"  
3. **Route (HTTPRoute, TCPRoute, vb.)** → "Hangi kuralla hangi Service'e veya Pod'a yönlendirme yapacağız?"  
4. **Service / Backend** → "Route'un ileteceği nihai hedef neresi?"  

Bu model, eski Ingress API'sindeki tek bir kaynağı parçalara ayırarak yetkileri ve sorumlulukları paylaştırmayı mümkün kılar. Yöneticiler Gateway ile uğraşırken, uygulama ekipleri sadece Route tanımlarını yönetebilir.

---

## Diğer İlgili Objeler / Kavramlar

1. **ReferencePolicy**  
   - Farklı Namespace'ler arasındaki Route ve Gateway referanslarını düzenlemek, güvenli hale getirmek için kullanılır.  
   - Örneğin "production" namespace'inde bulunan Gateway'in "dev" namespace'indeki bir HTTPRoute'u kabul etmesi için gerekli izni verebilirsiniz.

2. **TLS Configurations**  
   - Gateway ve Route düzeyinde TLS ayarları yapılabilir. Örneğin "Passthrough" moduyla sonlandırmayı Service'e bırakabilirsiniz veya "Terminate" moduyla Gateway üzerinde SSL sonlandırması yapabilirsiniz.

3. **Cross-Namespace / Multi-Tenancy**  
   - Gateway, bir namespace'te bulunurken, HTTPRoute başka bir namespace'te barınabilir. Bu, multi-tenant ortamlarda (bir kümede farklı takımlar / projeler) esneklik sağlar.

4. **Gateway API CRDs ve Sürümler**  
   - Gateway API şu an "v1beta1" düzeyinde. Zamanla kararlı (stable / v1) sürümler de gelişecektir.  
   - Cluster'a yüklenmesi için CRD'ler (Custom Resource Definition) gerekiyor. Resmi repo veya dağıtım (Helm/Operator) aracılığıyla kurabilirsiniz.

---

## Farklı Gateway Controller Örnekleri

- **Kubernetes-sigs/gateway-api** → Referans implementasyon.  
- **Nginx** → NGINX Gateway, Gateway API'yi destekleyen bir controller modülü sunmaya başladı.  
- **Istio** → Istio 1.13+ sürümleriyle Gateway API desteğini arttırdı.  
- **Contour** → Heptio/VMware tarafından geliştirilmiş Envoy tabanlı bir ingress/gateway çözümü.  
- **HAProxy, Traefik** → Kısmi veya deneme amaçlı Gateway API desteği mevcut veya planlanmış durumda.

---

## Benzerlik ve Farklılıklar: Ingress vs Gateway API

| Özellik             | Ingress                               | Gateway API                                         |
|---------------------|---------------------------------------|-----------------------------------------------------|
| Nesne Sayısı        | Tekçildir (Ingress nesnesi).           | Gateway, GatewayClass, Route vb. çok parçalı olacak şekilde tasarlanmıştır. |
| Genişletilebilirlik | Sınırlı, annotations ile yapılır.      | CRD bazlı, protokoller ve yönlendirme kuralları daha esnek.                 |
| Roller              | Basit (Ingress + Controller).          | Role-oriented design: Adminler Gateway kurar, uygulama sahipleri Route yönetir. |
| Protokoller         | Ağırlıklı HTTP/HTTPS (bazı eklentilerle TCP/UDP) | HTTP, TCP, UDP, gRPC, TLS vb. protokol-specifik Route kaynakları.   |
| Durum (Status)      | Tek bir Ingress kaynak durumu.         | Gateway ve Route ayrı statü alanlarına sahip, detaylı durum raporlama.         |
| Geleceği            | Stabil, ama özellik sınırlı olabilir.  | Aktif geliştiriliyor, gelecekte **Ingress API'nin yerini** kısmen alması amaçlanıyor. |

---

## Sonuç

**Gateway API**, Kubernetes dünyasında **daha modüler, rollere dayalı (role-oriented) ve protokol odaklı** bir ağ yönlendirme yaklaşıma doğru önemli bir adımdır.  
- `GatewayClass` → "Nasıl ve hangi ağ controller'ıyla?"  
- `Gateway` → "Hangi IP/port/hostname/protocol ile dinleyip, nerede sonlandıracağız?"  
- `HTTPRoute/TCPRoute/TLSRoute/UDPRoute` → "Trafiği hangi Service veya backend'e yönlendireceğiz?"  

Bu nesneler sayesinde **Infrastruture** ekibi Gateway tanımlarını yönetebilir, **Application** ekipleri kendi Route kural setlerini oluşturabilir.  
Özellikle çok çeşitli protokol-akışlarını yöneten, hush/hals domain/path bazlı karmaşık senaryolara sahip veya **multi-tenant** (çoklu proje takımının paylaştığı büyük Kubernetes kümeleri) ortamlarda Gateway API esneklik ve temiz bir ayrışma sunar.
