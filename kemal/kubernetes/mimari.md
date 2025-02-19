# Kubernetes Mimarisi ve Örnek Proje Çalışma Süreci

Kubernetes, **container** orkestrasyonu için tasarlanmış, dağıtık bir sistem mimarisine sahiptir. Bu mimari, **Control Plane** bileşenleri ve **Node'lar** (Worker Node'lar) arasında iş bölümü yapar. Aşağıda önce Kubernetes mimarisini, ardından örnek bir projenin nasıl çalıştığına dair senaryoyu inceleyeceğiz.

---

## 1. Kubernetes Mimarisi

### Control Plane Bileşenleri

1. **API Server**  
   - Kubernetes'in tüm işlemlerine (nesne oluşturma, silme, güncelleme vs.) tek **giriş noktası**dır.  
   - `kubectl`, diğer CLI araçları, veya herhangi bir istemci (SDK vb.) bu API sunucusu ile iletişim kurar.

2. **etcd**  
   - Tüm **kümede** (cluster) tutulan verilerin saklandığı, yüksek erişilebilirliğe sahip **anahtar-değer** veritabanıdır.  
   - Pod, Service, Deployment gibi Kubernetes nesneleri burada kalıcı biçimde kaydedilir.

3. **Controller Manager**  
   - Kubernetes'te "istekli durum" (desired state) ve "mevcut durum" (current state) sürekli kıyaslanır.  
   - Controller Manager, Pod'ların sayısı, Node ekleme/çıkarma, replikalar vb. konularda **kontrol döngülerini** (control loops) yöneterek küme durumu istenen hale getirir.

4. **Scheduler**  
   - Yeni oluşturulan Pod'ların hangi Node üzerinde çalışacağını "kaynak uygunluğunu" da hesaba katarak belirler.  
   - CPU, bellek, etiket/taşınabilirlik (taint/tolerations) gibi kıstaslar doğrultusunda en uygun Node'u seçer.

### Worker Node Bileşenleri

1. **Kubelet**  
   - Her Node üzerinde çalışan bir ajan.  
   - Pod'ların çalışır olduğundan, container'ların belirtilen imajları kullandığından, kaynak limitlerine uyduğundan ve sağlık durumlarından sorumludur.

2. **Container Runtime**  
   - Uygulamaların container içinde çalışmasını sağlayan yazılımdır (örn. Docker, containerd, CRI-O).  
   - Kubelet, container yönetiminin çoğunu bu runtime ile gerçekleştirir.

3. **kube-proxy**  
   - Kubernetes Service'lerine ulaşmak için Node üzerinde gerekli ağ kurallarını (iptables, IPVS vb.) yönetir.  
   - Service discovery ve yük dengeleme fonksiyonlarını üstlenir.

Bu mimari sayesinde Kubernetes, **yüksek erişilebilir**, **öz-organize** (self-healing) bir ortam sağlar.

---

## 2. Örnek Proje Çalışma Süreci

Bir proje geliştirildiğinde (ör. mikroservis tabanlı bir web uygulaması), Kubernetes bunu nasıl barındırır ve yönetir? Aşağıda örnek bir akış yer alıyor:

### Adım 1: Kod ve Container İmajı

1. **Geliştirici**, Node.js, Python, Java vb. ile uygulama kodunu yazar.  
2. **Dockerfile** gibi bir tanım kullanarak kodu bir **container imajına** dönüştürür (örn. `docker build -t my-app:1.0 .`).  
3. İmaj bir **container registry**'e (Docker Hub, GitLab Container Registry, ECR, GCR vb.) push'lanır.

### Adım 2: Deployment YAML Tanımları

1. Geliştirici veya DevOps mühendisi, Kubernetes için bir **Deployment** ve **Service** gibi YAML'lar yazar. Örnek bir Deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: my-app-container
          image: myregistry/my-app:1.0
          ports:
            - containerPort: 8080
          resources:
            limits:
              cpu: "500m"
              memory: "256Mi"
```

- **`replicas: 3`** ile uygulamamızdan 3 adet Pod'un çalışacağını tanımlıyoruz.  
- `image: myregistry/my-app:1.0` → Daha önce build & push ettiğimiz container imajı.

2. Servis tanımı (ör. tipe göre ClusterIP/NodePort/LoadBalancer) küme içi ve/veya dışına erişimi ayarlar:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  type: ClusterIP
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8080
```

- Bu Service, Pod'ların 8080 portuna gelen istekleri 80 numaralı port üzerinden yönlendirir.  
- `selector: app: my-app` → Deployment'taki `app=my-app` etiketine sahip Pod'lar hedeflenir.

### Adım 3: Uygulamayı Deploy Etme

1. **kubectl apply -f deployment.yaml** ve **kubectl apply -f service.yaml** komutlarıyla YAML'lar Kubernetes API Server'a gönderilir.  
2. **API Server** → Bu nesneleri vb. `etcd` veritabanına kaydeder.  
3. **Scheduler** → Yeni Pod'ların hangi Node üzerinde çalışacağını belirler (kaynak uygunluğu, Node etiketleri vb.).  
4. **Controller Manager** → `replicas=3` tanımını izleyecek, Pod sayısı 3 değilse ekleyecek/silecek.  
5. **Kubelet** (Node üzerinde) → Container imajını alır, container runtime çağırıp Pod'u çalıştırır.

### Adım 4: Uygulamanın Çalışması

1. **Pod'lar** 3 farklı Node'da (veya aynı Node'da) konumlanabilir.  
2. **kube-proxy** → `my-app-service`'e gelen istekleri bu Pod'lara dağıtır.  
3. Eğer dış dünyaya açmak istersek, Service'i `type: LoadBalancer` veya bir **Ingress** üzerinden tanımlayabiliriz.

### Adım 5: Otomatik İyileşme ve Ölçeklendirme

- Bir Pod çöker veya Node arızalanırsa, Controller Manager fark eder ve yeni Pod oluşturur.  
- Daha fazla yük gelirse, `kubectl scale` veya HPA (Horizontal Pod Autoscaler) üzerinden replikalar artırılabilir.

### Adım 6: Güvenlik ve RBAC

- Geliştiriciler bu nesneleri kendi **namespace**'leri altında deploy edebilir.  
- **Role** / **RoleBinding** ile sadece belirli namespace'lerde yetki verilebilir.  
- (Örnek Role/RBAC dosyaları için [13-role-rbac.md](13-role-rbac.md) dosyasına bakınız.)

---

## 3. Özet

1. **Kubernetes**, "**Control Plane** (API Server, etcd, Controller, Scheduler) + Worker Node (Kubelet, Container Runtime, kube-proxy)" tasarımıyla çalışır.  
2. **Geliştirici ekibi**, kodu container imajına dönüştürüp Kubernetes'e (Deployment, Service, Ingress vb. YAML tanımları) verir.  
3. **Controller Manager** ve **Scheduler**, bu YAML'larda belirtilen istekli durumu (replica sayısı, node seçimi vb.) hayata geçirir.  
4. **Pod'lar** Node'lar üzerinde container runtime aracılığıyla çalışır; **Service** ve **kube-proxy** ile trafik yönlendirilir.  
5. **RBAC** gibi güvenlik mekanizmaları, hangi kullanıcının/servis hesabının hangi namespace'te ne yapabileceğini belirler.  

Böylece Kubernetes, microservice ve container'larınızı **ölçeklenebilir**, **kendini iyileştirebilen** (self-healing) ve **hataya dayanıklı** bir platformda yönetmenize olanak tanır. 