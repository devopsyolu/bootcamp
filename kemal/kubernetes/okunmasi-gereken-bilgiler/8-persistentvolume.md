# Kubernetes PersistentVolume (PV) Nedir?

**PersistentVolume (PV)**, Kubernetes kümelerinde **kalıcı** depolama (storage) alanı sağlamak için kullanılan küresel (cluster-level) bir nesnedir. PV, fiziksel depolama kaynaklarını (örneğin NFS, AWS EBS, GCE Persistent Disk, vb.) Kubernetes API üzerinden tanımlar. Uygulamalarınız bu kalıcı depolama alanına **PersistentVolumeClaim (PVC)** yoluyla erişir.

---

## PersistentVolume Özellikleri

1. **Kalıcı Depolama Kaynağı**  
   - Pod'lar yeniden başlatılsa veya silinse bile veri, PV üzerinde kalıcı olarak saklanır.  
   - Fiziksel veya buluttaki depolama birimlerini soyut bir nesne haline getirerek sunar.

2. **Kurumsal Depolama Entegrasyonları**  
   - NFS, iSCSI, FC (Fibre Channel), Ceph, AWS EBS, GCP PD, Azure Disk gibi pek çok altyapıyla uyumlu şekilde çalışır.  
   - Sahip olduğunuz depolama sistemlerini Kubernetes altında yönetebilirsiniz.

3. **Erişim Modları (Access Modes)**  
   - **ReadWriteOnce (RWO)**: Tek bir Node üzerinden hem okuma hem yazma.  
   - **ReadOnlyMany (ROX)**: Birçok Node'dan salt-okunur erişim.  
   - **ReadWriteMany (RWX)**: Birçok Node'dan hem okuma hem de yazma (örneğin paylaşımlı dosya sistemleriyle).

4. **Reclaim Policy**  
   - *Retain*: PVC silinse bile veriyi tutmaya devam eder. (Elle temizlenmesi gerekir.)  
   - *Recycle*: Dosya sistemi içeriğini siler ve yeniden kullanılabilir hale getirir.  
   - *Delete*: PVC silindiğinde otomatik olarak PV ve arka plandaki fiziksel depolama da silinir.

5. **Statik ve Dinamik PV**  
   - *Statik Provisioning*: Depolama yöneticisi, kümeye PV nesnesini manuel olarak ekler. PVC, buna eşleşirse kullanım başlar.  
   - *Dinamik Provisioning (StorageClass)*: StorageClass üzerinden, PVC istendiğinde PV otomatik oluşturulur.

---

## PV ile StorageClass Kullanımı Arasındaki Fark

### 1. Statik Provisioning (Direkt PV Kullanımı)  
- **Kim Tanımlar?**  
  Genellikle bir sistem yöneticisi (admin) önceden fiziksel bir depolama birimini ayarlar ve bunu Kubernetes'e "PV" olarak tanıtır.  
- **Adımlar**  
  1. Admin, bir PV YAML dosyası oluşturur ve uygular.  
  2. Geliştirici, PV'nin özelliklerine uygun bir PVC gönderir.  
  3. Kubernetes, bu PVC ile PV'yi "bind" eder.  
- **Avantaj**  
  Kontrol ve şeffaflık tamamen yöneticinin elindedir. Depolama alanı üzerinde tam hâkimiyet ve adım adım yükleme söz konusudur.  
- **Dezavantaj**  
  Yeni bir depolama alanı gerektiğinde her seferinde yöneticinin manuel işlemleri yapması gerekebilir. Ölçeklendirmeye uygun değildir.

### 2. Dinamik Provisioning (StorageClass ile PV)  
- **Kim Tanımlar?**  
  Yöneticiler, farklı depolama türleri ve parametreleri için StorageClass nesnelerini tanımlarlar (örn. gp2, gp3, iops, encryption).  
- **Adımlar**  
  1. PVC, `storageClassName` alanında ilgili StorageClass'ı çağırır.  
  2. Kubernetes otomatik olarak PV oluşturur ve bu PVC'ye bağlar.  
- **Avantaj**  
  Geliştiriciler disk boyutu, erişim modu gibi basit parametreler dışında hiçbir ayrıntıya dokunmadan PVC tanımlayabilirler. Yeni projelerin depolama ihtiyaçları **otomatik** gidilir.  
- **Dezavantaj**  
  StorageClass parametreleri yanlış veya yetersiz tanımlanırsa, oluşturulan PV gerekli standartları karşılamayabilir. Yönetici tarafında doğru konfigürasyon şarttır.

**Özetle**, **statik yöntem** küçük ve sabit sayıdaki depolama alanını yönetmek için yeterliyken, **StorageClass'ın sunduğu dinamik yöntem** büyük ve sık değişen projelerde ölçeklenebilir ve otomatik bir yaklaşım sunar.

---

## Mimari Bakış

1. **Yönetici (Admin)**  
   - Statik yaklaşımda: Fiziksel depolama altyapısına uygun şekilde PV nesneleri oluşturur.  
   - Dinamik yaklaşımda: StorageClass nesnelerini tanımlar, fiziksel altyapı parametrelerini (provisioner, reclaim policy, encryption vb.) ayarlar.

2. **Geliştirici (Developer)**  
   - *Statik* yaklaşımda: Mevcut PV özelliklerine uygun PVC yazar.  
   - *Dinamik* yaklaşımda: Sadece uygun "storageClassName" ve depolama boyutunu yazan bir PVC yazar, Kubernetes geri kalanını otomatik halleder.

3. **Kubernetes**  
   - *Statik* PV bulursa PVC ile eşleştirir.  
   - *Dinamik* olarak StorageClass kullanırsa, arka plandaki sağlayıcı (AWS EBS, GCE PD, vs.) üzerinden **yeni** bir disk oluşturur ve PV-PVC'yi eşler.

---

## Örnek PersistentVolume Manifesti

Aşağıdaki örnekte, yerel bir **NFS** kaynağı kullanan statik bir PV tanımı yer almaktadır:

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

1. **`capacity: 5Gi`**  
   - PV, 5 GB boyutunda depolama alanı sağlar.  
2. **`accessModes: ReadWriteMany`**  
   - Birden fazla node'un aynı anda okuma-yazma yapabilmesini destekler.  
3. **`nfs:`**  
   - NFS sunucu adresini ve path'ini işaret eder.  
4. **`persistentVolumeReclaimPolicy: Retain`**  
   - PVC silinse de veri elde tutulur.

### Statik PVC Örneği

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-nfs-claim
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 5Gi
```
> Kubernetes uygun statik bir PV (pv-nfs) bularak bağlar.

### Dinamik PVC Örneği (StorageClass Kullanımı)

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-ebs-claim
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: aws-ebs-gp3-csi
  resources:
    requests:
      storage: 5Gi
```
> Kubernetes, `aws-ebs-gp3-csi` adlı StorageClass tanımını kullanarak AWS EBS'de yeni bir disk **dinamik** oluşturur, PV'yi kaydeder ve bu PVC'ye bind eder.

---

## Önemli Komutlar

1. **PV'leri Listeleme**  
   ```bash
   kubectl get pv
   ```
2. **Detaylı İnceleme**  
   ```bash
   kubectl describe pv pv-nfs
   ```
3. **Oluşturma / Güncelleme**  
   ```bash
   kubectl apply -f pv-nfs.yaml
   ```
4. **Silme**  
   ```bash
   kubectl delete pv pv-nfs
   ```

---

## Sonuç

**PersistentVolume (PV)**, Kubernetes'te **fiziksel ve kalıcı depolama** kaynaklarını temsil eder. Uygulamalar **PersistentVolumeClaim (PVC)** ile bu alanları talep ederek Pod'lar için kalıcı veri sağlanır.  
Tekrarlamak gerekirse, **statik provisioning** modelinde PV'yi yöneticiler bizzat YAML dosyası üzerinden tanımlarken, **dinamik provisioning** **StorageClass** kullanımıyla **otomatik** ve **ölçeklenebilir** bir hale gelir. Her iki yaklaşım da Kubernetes'in kalıcı veriyi nasıl güvenilir ve yönetilebilir biçimde sunduğunun altını çizer.
