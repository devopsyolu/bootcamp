# Kubernetes Deployment Nedir?

**Deployment**, Kubernetes üzerinde bir uygulamayı (Pod'lar) yönetmek, güncellemek ve ölçeklendirmek için kullanılan üst düzey bir nesnedir. Aşağıdaki temel işlevleri yerine getirir:

1. **Deklaratif Yönetim (Desired State)**  
   - **replicas:** Kaç adet Pod çalışacağını "istek" olarak belirtirsiniz; Kubernetes, bu sayıyı korumak için Pod ekleyip siler.  
   - **template:** Pod'ların nasıl oluşturulacağını belirler (örn. hangi container imajını veya hangi portları kullanacağını).  

2. **Rolling Update ve Geri Alma (Rollback)**  
   - **Rolling güncelleme:** Yeni sürüme geçerken, eski Pod'lar kademeli olarak ölçek küçültülür ve yeni versiyon Pod'lar kademeli olarak devreye alınır.  
   - **Rollback:** Yeni sürümde sorun olursa, Deployment'ı bir önceki sağlıklı sürüme hızlıca döndürebilirsiniz.

3. **Kolay Ölçeklendirme**  
   - Deployment, hem manuel hem de otomatik (HPA - Horizontal Pod Autoscaler) ölçeklendirme için uygundur.  
   - `replicas` alanını arttırarak ya da azaltarak Pod sayısını dilediğiniz gibi değiştirebilirsiniz.

4. **ReplicaSet Yönetimi**  
   - Deployment, istenen durumu sağlamak için gerçekte ReplicaSet nesnelerini yönetir.  
   - Her yeni versiyonda, Kubernetes yeni bir ReplicaSet devreye alır ve eski ReplicaSet'i devreden çıkarır.

5. **Gözlemleme ve Durum Takibi**  
   - `kubectl get deployments` veya `kubectl describe deployment <isim>` komutlarıyla güncel durumu, ReplicaSet bilgilerini ve güncelleme sürecinin ilerlemesini görüntüleyebilirsiniz.

---

- **`maxUnavailable`: Güncelleme sırasında aynı anda devre dışı kalabilecek maksimum Pod sayısı.  
- **`maxSurge`: Güncelleme sırasında, mevcut `replicas` sayısından ne kadar daha fazla Pod'un geçici olarak oluşturulabileceğini kontrol eder.

---

## Örnek Deployment Manifesti

Aşağıdaki örnekte, bir Nginx tabanlı uygulamayı üç kopya (replica) çalıştıran basit bir Deployment yer almaktadır:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx-container
        image: nginx:latest
        ports:
        - containerPort: 80
```

1. **`replicas: 3`** – 3 adet Nginx Pod'u oluşturur.  
2. **`selector.matchLabels`** – Bu etiketlerle oluşturulan Pod'lar Deployment'ın yönetimi altında olur.  
3. **`template.spec.containers`** – Pod içindeki konteyner(ler), bu örnekte **nginx** konteynerini tanımlar.

---

## Dağıtım Stratejisi (Deployment Strategy)

Varsayılan olarak **RollingUpdate** stratejisi kullanılır:

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
```

- **`maxUnavailable: 1`** → Güncelleme sırasında aynı anda devre dışı kalabilecek maksimum Pod sayısı.  
- **`maxSurge: 1`** → Güncelleme sırasında, mevcut `replicas` sayısından 1 fazla Pod oluşturulabilir.

---

## Rollout ve Rollback

### Rollout (Güncelleme)

Yeni sürümü devreye almak için YAML'daki imaj veya benzeri konfigürasyon değişikliklerinizi uygulayın:
```bash
kubectl apply -f deployment.yaml
```
Güncellemenin durumunu görmek için:
```bash
kubectl rollout status deployment/nginx-deployment
```
Ayrıca, sürüm geçmişini inceleyebilirsiniz:
```bash
kubectl rollout history deployment/nginx-deployment
```

### Rollback (Geri Alma)

Güncelleme sonrası bir sorun oluşursa, önceki sağlıklı sürüme dönmek için:
```bash
kubectl rollout undo deployment/nginx-deployment
```
Belirli bir revision numarasına dönmek isterseniz:
```bash
kubectl rollout undo deployment/nginx-deployment --to-revision=2
```

---

## Neden Deployment Kullanılır?

1. **Kolay Yönetim**  
   ReplicaSet ve Pod'ları ayrı ayrı yönetme yerine, tek bir nesne üzerinden tam kontrol sağlanır.  

2. **Sıfıra Yakın Kesintiyle Güncelleme**  
   Rolling update stratejisi sayesinde uygulamanızın yeni versiyonunu dağıtırken sistem sürekli çalışır durumda kalabilir.

3. **Hızlı Geri Alma (Rollback)**  
   Sorunlu bir sürümde, bir önceki sağlıklı sürüme kolayca geri dönülebilir.

4. **Otomatik ve Manuel Ölçeklendirme**  
   `replicas` değerini değiştirerek ölçeklendirme kolaydır. Ayrıca HPA (Horizontal Pod Autoscaler) ile CPU/bellek kullanımına göre otomatik ölçeklendirme yapabilirsiniz.

5. **Üst Seviye API Deneyimi**  
   Kubernetes kullanıcıları arasında en sık kullanılan nesnelerden biri olup neredeyse her mikroservisin "can damarı" olarak kabul edilir.

---

## Deployment Komutlarına Örnekler

- **Oluşturma / Güncelleme**:  
  ```bash
  kubectl apply -f deployment.yaml
  ```

- **Durumu Görme**:  
  ```bash
  kubectl get deployments
  kubectl describe deployment nginx-deployment
  ```

- **Ölçeklendirme**:  
  ```bash
  kubectl scale deployment/nginx-deployment --replicas=5
  ```

- **Silme**:  
  ```bash
  kubectl delete deployment/nginx-deployment
  ```

---

## Sonuç

**Deployment**, Kubernetes ekosisteminde uygulamaların güvenilir bir biçimde yönetilmesini sağlayan güçlü bir araçtır. Uygulamanın istediğiniz kopya sayısıyla, istediğiniz sürümde ve minimum kesintiyle çalışmasını kolayca organize edebilir, gerektiğinde otomatik veya manuel ölçeklendirme ve *rollback* gibi gelişmiş yeteneklerden faydalanabilirsiniz.
