# Kubernetes StatefulSet Nedir?

**StatefulSet**, Kubernetes'te **durum bilgisi olan (stateful)** uygulamaları yönetmek için kullanılan bir üst düzey nesnedir. Uygulamanın sürdürmesi gereken veriler veya kimlik bilgileri olduğunda (örn. veritabanı, dağıtık dosya sistemi, vb.) **StatefulSet** genellikle tercih edilir. Pod'lar arasındaki kimlik (identity), depolama (storage) ve ağ (network) ilişkileri korunarak, bu Pod'ların **tümleşik, tutarlı ve sıralı** bir şekilde başlatılması, durdurulması, yeniden adlandırılması sağlanır.

## StatefulSet Özellikleri

1. **Kararlı (Persistent) Kimlik (Stable Network ID ve Kimlik)**  
   StatefulSet tarafından yönetilen her bir Pod, diğer Pod'lardan farklı bir sırayla adlandırılır (örn. `web-0`, `web-1`) ve DNS hostnames gibi ağa dair kimlikler otomatik olarak atanır. Böylece, yeniden başlatma veya yeni sürüme geçişten sonra bile Pod kimlikleri kalıcı olmak üzere korunur.

2. **Veri Bağımlılığı ve Tutarlılık**  
   Veritabanları veya dağıtık dosya sistemleri gibi veri tutarlılığı ve replikasyonu gerektiren senaryolarda, her Pod'un kendi kalıcılık katmanına (PVC) erişmesi önemlidir. StatefulSet, Pod'lara özel PersistentVolumeClaim (PVC) yönetimi sağlar; Pod tekrar başlatılsa da aynı depolama alanını (volume) kullanır.

3. **Sıralı Başlatma ve Durdurma**  
   StatefulSet, Pod'ları belirli bir sıralamayla (örn. önce `pod-0`, sonra `pod-1`) başlatır ve yine ters sırayla sonlandırabilir. Bu mekanizma, tutarlı bir küme kurulumu için kritik öneme sahiptir (örn. üyelerin sırayla eklenip çıkarılması).

4. **Otomatik Ölçeklendirme**  
   StatefulSet'te de `replicas` sayısını ayarlayarak Pod'ları ölçeklendirebilirsiniz. Ancak, durum bilgisi olan uygulamalarda her yeni Pod veri replikasyonu, koordinasyon vb. ek konfigürasyonlar gerektirebilir.

5. **Rolling Update ve Geri Alma**  
   Deployment'taki gibi Rolling Update benzeri bir sistem kullanabilirsiniz; fakat veriye dayalı uygulamalarda (örn. Redis, Cassandra) güncellemelerin sıralı yapılması ve her Pod'un kapanmadan önce veriyi güvenle aktarması gerekebilir. Bu nedenle Rolling Update işlemleri daha kontrollü ve yavaş gerçekleşir.

---

## Örnek StatefulSet Manifesti

Aşağıda, üç kopya (replica) halinde çalışan basit bir StatefulSet örneği yer almaktadır. Bu örnekte, her Pod kendine ait bir depolama `PersistentVolumeClaim` talep etmektedir:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
  labels:
    app: web
spec:
  serviceName: "web-service"
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx-container
        image: nginx:latest
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: standard
      resources:
        requests:
          storage: 1Gi
```

### Açıklamalar

1. **serviceName: "web-service"** → StatefulSet, Pod'lara DNS üzerinden ulaşmak için bir Headless Service kullanır (oluşturmuş olduğunuz veya oluşturacağınız bir Service).  
2. **replicas: 3** → Üç adet Pod (örn. `web-0`, `web-1`, `web-2`).  
3. **volumeClaimTemplates** → Her Pod'un kendi PersistentVolumeClaim'i otomatik oluşturulacak ve pod yaşam döngüsü boyunca kalıcı olarak bağlanacaktır.  
4. **network kimliği** → Pod'lar sırasıyla `web-0.web-service`, `web-1.web-service`, `web-2.web-service` gibi DNS isimlerine sahip olur.

---

## Ne Zaman StatefulSet Kullanılır?

- Veritabanı, dağıtık cache, dağıtık dosya sistemi gibi veri tutarlılığının kritik olduğu uygulamalar.  
- Her Pod'un uzun süreli kimlik (identity) ve depolama (storage) ihtiyacı olduğunda.  
- Uygulamaların kümede yeniden başlatılması veya ölçeklendirilmesi sırasında, belirli bir sıranın korunması gerektiğinde.

---

## StatefulSet ile İlgili Önemli Komutlar

- **Yaratma**:  
  ```bash
  kubectl apply -f statefulset.yaml
  ```
- **Durumu Görüntüleme**:  
  ```bash
  kubectl get statefulset
  kubectl describe statefulset/web
  ```
- **Pod Düzeyinde Görüntüleme**:  
  ```bash
  kubectl get pods -l app=web
  ```
- **Silme**:  
  ```bash
  kubectl delete statefulset web
  ```

---

## Sonuç

**StatefulSet**, Kubernetes'in durum bilgisi olan (stateful) uygulamalarını yönetmek için tasarlanmış kritik bir nesnedir. Pod'lar arasında değişmeyen kimlik, sıralı başlatma/durdurma ve kalıcı veri kullanılacağı durumlarda Deployment veya ReplicaSet yerine **StatefulSet** tercih edilir. Özellikle veritabanları, dağıtık sistemler ve veri tutarlılığı gözeten mikroservisler için temel yaklaşımdır.
