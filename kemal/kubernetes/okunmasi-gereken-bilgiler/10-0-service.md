# Kubernetes Service (Servis) Nedir?

**Service (Servis)**, Kubernetes'te aynı görevi yapan veya aynı uygulamaya ait olan Pod'lar arasındaki ağ iletişimini düzenleyen bir soyutlama katmanıdır. Pod'lar kısa ömürlü oldukları için IP adresleri veya sayıları sürekli değişebilir. Service ise sabit bir DNS adı (ör. `my-service`) ve sanal IP sağlayarak, dış/diğer servislerin Pod'lara kolaylıkla ve kararlılıkla erişmesini sağlar.

---
## Kubernetes Mimarisi ve Servis İlişkisi

Kubernetes mimarisi genel olarak aşağıdaki bileşenlerden oluşur:

1. **Master Node**  
   - **API Server**: Tüm Kubernetes işlevlerini dışarıya açar (REST API).  
   - **Scheduler**: Pod'ların hangi node üzerinde çalışacağını belirler.  
   - **Controller Manager**: ReplicaSet, Deployment gibi kontrol döngülerinin (control loop) çalışmasını sağlar.  
   - **Etcd**: Kubernetes konfigürasyon ve durum verilerini saklayan dağıtık anahtar-değer deposu.

2. **Worker Node**  
   - **Kubelet**: Master'dan gelen talimatları uygular, Pod'ları başlatır.  
   - **Container Runtime**: Pod içerisindeki konteynerleri (örn. Docker, containerd) çalıştırır.  
   - **Kube-Proxy**: Node üzerinde ağ trafiğini yöneten servis. Service nesnelerinin ağ kurallarını uygular.

3. **Pod**  
   - Bir veya daha fazla konteynerin bir arada çalıştığı Kubernetes'in en küçük dağıtım birimidir.  
   - IP adresi ve yaşam döngüsü kısıtlıdır.

4. **Service**  
   - Pod'lara sabit bir ağ kimliği sağlar.  
   - Yük dengeleme (load balancing) ve yeniden başlatılan Pod'ların IP adreslerinin değişmesini telafi eder.  
   - Farklı tipleri vardır: ClusterIP, NodePort, LoadBalancer vb.

### Service'lerin Çalışma Mantığı

- **Label Selector**: Servis, belirli etiketlere (lbl: `app=myapp` gibi) sahip Pod'ları hedef alır.  
- **Endpoint (EndpointSlices)**: Servis, bu etiketlere sahip Pod adreslerini "endpoint" listesinde tutar.  
- **Ağ Erişimi**: İhtiyaca göre, sadece küme içi (ClusterIP) ya da küme dışı-Load Balancer gibi seçenekler kullanılabilir.

<p align="center">
  <img src="https://user-images.githubusercontent.com/ce-sharif/kubernetes-service-architecture.png" alt="Kubernetes Service Mimarisi" width="400" />
</p>

---
## Örnek Service Tanımı

Aşağıdaki YAML, `app: myapp` etiketine sahip Pod'ları hedef alan basit bir **ClusterIP** tipindeki servisi tanımlar:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
  labels:
    app: myapp-service
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
    - name: http
      port: 80          # Service'in dinleyeceği port
      targetPort: 8080  # Pod içindeki konteyner portu
```

1. **`type: ClusterIP`**  
   - Varsayılan servis tipidir. Yalnızca küme içindeki kaynakların erişimine izin verir.  
2. **`selector: app: myapp`**  
   - `app: myapp` etiketine sahip Pod'lar, bu servis tarafından hedeflenir.  
3. **`ports.port: 80`**  
   - Servis bu port üzerinden dinler.  
4. **`ports.targetPort: 8080`**  
   - Pod içindeki konteynerin çalıştığı port.

---
## Service Tipleri

1. **ClusterIP (Varsayılan)**  
   - Yalnızca küme içi erişime açıktır. Pod'lar veya başka servisler, bu IP:port üzerinden iletişim kurar.  

2. **NodePort**  
   - Her node'da aynı portu açarak küme dışında da erişim sağlar. Genellikle test ve geliştirme ortamlarında sık kullanılır.  

3. **LoadBalancer**  
   - Bulut sağlayıcıları (örn. GCP, AWS, Azure) ile entegre olarak, dış dünyadan gelen trafiği yüksek seviyede yönlendirir. Otomatik olarak bir load balancer oluşturulur (örn. AWS ELB).  

4. **ExternalName**  
   - İç DNS üzerinden Service adını, harici bir DNS adına yönlendirmek için kullanılır.

---
## Service Komutlarına Örnekler

- **Listeleme ve Durum Görme**:  
  ```bash
  kubectl get services
  kubectl describe service my-service
  ```

- **Oluşturma / Güncelleme**:  
  ```bash
  kubectl apply -f my-service.yaml
  ```

- **Silme**:  
  ```bash
  kubectl delete service my-service
  ```

---
## Kullanım Senaryoları

1. **Mikroservis İletişimi**  
   Her mikroservis, farklı Deploymen veya StatefulSet Pod'larını "service" üzerinden bulup iletişim kurar.

2. **İç Ağ Üzerinden Uygulamalara Erişim**  
   İdari araçlar, logging, monitoring vb. yalnızca küme içinden erişilen servislerde (ClusterIP) veya node üzerinden erişilen (NodePort) servislere ihtiyaç duyar.

3. **Dış Dünyaya Açık Uygulamalar**  
   LoadBalancer tipindeki servis, trafik dağıtıcısını (load balancer) otomatik devreye sokarak internet üzerinden erişim sağlar.

---
## Sonuç

Kubernetes mimarisinde **Service**, Pod'lara sabit bir erişim kimliği sunarak ağ karmaşasını soyutlar. Pod'ların ömrü kısa ve IP adresleri değişken olsa da, servis adı ve IP'si her zaman sabit kalır. Bu sayede:

- *Yeni eklenen ya da yeniden başlatılan Pod'lar otomatik olarak servis arkasına dahil olur.*  
- *Yük dengeleme (load balancing) mantığıyla, talep herhangi bir çalışan Pod'a yönlendirilir.*  

Bu yapıyla Kubernetes, birbirini bulup haberleşmesi gereken mikroservisler ya da dış dünyaya açılan uygulamalar için **kararlı, ölçeklenebilir ve yönetilebilir** bir ağ modeli sağlar.
