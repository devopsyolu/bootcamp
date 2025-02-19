# Kubernetes PersistentVolumeClaim (PVC) Nedir?

**PersistentVolumeClaim (PVC)**, Kubernetes'teki uygulamaların (Pod'ların) kalıcı depolama ihtiyacını talep etmek için kullanılan bir nesnedir. PVC, **PersistentVolume (PV)** veya **StorageClass** aracılığıyla sağlanan depolama kaynaklarına bağlanmayı sağlar. Böylece uygulamalar, verileri Pod'ların ömründen bağımsız olarak saklayabilir.

---

## PVC ve PV İlişkisi

1. **PVC** (Talep)  
   - Hangi erişim modu (ReadWriteOnce, ReadWriteMany vb.), ne kadar kapasite (örn. 5Gi) ve varsa hangi StorageClass'ı istediğini belirtir.  
2. **PV** (Kaynak)  
   - Depolamanın kaynağıdır. NFS, iSCSI, AWS EBS vb. fiziksel altyapılar buna bağlanarak tanımlanır.  
3. **Bağlanma (Binding)**  
   - PVC, gereksinimlerini karşılayan bir PV bulursa otomatik bind edilir.  
   - Eğer PVC, bir StorageClass belirtmişse **dinamik oluşturma** (Dynamic Provisioning) devreye girebilir.

<p align="center">
  <img src="https://user-images.githubusercontent.com/ce-sharif/k8s-pvc-diagram.png" alt="Kubernetes PVC-PV Bağlantısı" width="450" />
</p>

---

## PVC Kullanımı (Statik Provisioning)

"Statik" yöntemde önceden oluşturulmuş bir **PersistentVolume** mevcuttur. Örnek:

### 1. PV Tanımı (Örnek: NFS)

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-nfs
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteMany
  nfs:
    path: /path_on_nfs_server
    server: 192.168.1.10
  persistentVolumeReclaimPolicy: Retain
```

### 2. PVC Tanımı (Statik)

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-static-claim
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 5Gi
```

> Kubernetes, "my-static-claim" adlı PVC'yi "pv-nfs" ile **bind** eder. Çünkü her ikisi de `ReadWriteMany` erişim moduna ve `5Gi` depolama boyutuna sahiptir. Bu yöntemde yönetici, PV'yi önceden manuel olarak tanımladığı için buna "statik provisioning" denir.

---

## PVC Kullanımı (Dinamik Provisioning)

Dinamik yöntemde, **StorageClass** üzerinden yeni bir PV otomatik olarak oluşturulur. Bu yaklaşım, büyük ölçekte ve bulut ortamlarında önerilir.

### 1. StorageClass Tanımı (Örnek: AWS EBS CSI)

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: aws-ebs-gp3-csi
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  fsType: ext4
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
```

### 2. PVC Tanımı (Dinamik)

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-dynamic-claim
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: aws-ebs-gp3-csi
  resources:
    requests:
      storage: 5Gi
```

> Bu PVC, `storageClassName` olarak "aws-ebs-gp3-csi"yi belirttiğinden Kubernetes, dinamik olarak **yeni bir EBS disk** oluşturur ve otomatik bir **PV** nesnesi yaratıp PVC'yle eşler.

---

## Pod İçerisinde PVC Kullanımı

İster statik ister dinamik elde edilmiş olsun, bir Pod YAML'ında volume tanımları şu şekilde yapılır:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: example-pod
spec:
  containers:
    - name: app-container
      image: nginx:latest
      volumeMounts:
        - mountPath: "/usr/share/nginx/html"
          name: my-storage
  volumes:
    - name: my-storage
      persistentVolumeClaim:
        claimName: my-dynamic-claim
```

> "my-dynamic-claim" adlı PVC üzerinden otomatik veya statik bir PV'ye bağlanır. Böylece "/usr/share/nginx/html" dizini kalıcı bir dosya sistemine dönüşür.

---

## Önemli Komutlar

1. **PVC'leri Listelemek**  
   ```bash
   kubectl get pvc
   ```
2. **PVC Detaylarını Görüntülemek**  
   ```bash
   kubectl describe pvc my-static-claim
   ```
3. **Oluşturma / Güncelleme**  
   ```bash
   kubectl apply -f pvc.yaml
   ```
4. **Silme**  
   ```bash
   kubectl delete pvc my-dynamic-claim
   ```

---

## Sonuç

**PersistentVolumeClaim (PVC)**, Kubernetes'te uygulamaların kalıcı depolama kaynağına basit bir şekilde erişim talep etmelerini sağlar.  
- *Statik Provisioning* → Önceden tanımlanmış PV'lerle (ör. NFS, iSCSI) manuel eşleşme.  
- *Dinamik Provisioning* → **StorageClass** yoluyla otomatik PV oluşturma.  

Bu mekanizma, Kubernetes ekosisteminde **taşınabilir**, **kalıcı** ve **kolay yönetilebilir** bir depolama deneyimi sunar.
