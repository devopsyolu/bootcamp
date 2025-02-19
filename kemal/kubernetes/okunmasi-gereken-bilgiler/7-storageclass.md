# Kubernetes StorageClass Nedir?

**StorageClass**, Kubernetes'te dinamik depolama kaynaklarının yönetilmesini sağlayan bir nesnedir. Uygulamalarınızın (Pod, Deployment, StatefulSet vb.) ihtiyaç duyduğu kalıcı depolama alanlarını (PersistentVolume) oluştururken farklı depolama profilleri, geri bildirim politikaları ve parametreleri kullanabilmenize olanak tanır.

---

## StorageClass'in Temel Özellikleri

1. **Dinamik Olarak PersistentVolume Oluşturma**  
   - Bir **PersistentVolumeClaim (PVC)**, belirli bir StorageClass'a referans vererek gönderildiğinde Kubernetes otomatik olarak yeni bir **PersistentVolume (PV)** oluşturabilir.  
   - Geleneksel yöntemlerde, yöneticinin (admin) manuel olarak PV tanımlaması gerekir; ancak StorageClass sayesinde bu işlem otomatik ve dinamik hale gelir.

2. **Depolama Sağlayıcılarını (Provisioner) Belirleme**  
   - StorageClass, hangi **storage eklentisi (provisioner)** kullanılacağını belirtir. Örneğin, `kubernetes.io/aws-ebs` (in-tree) veya `ebs.csi.aws.com` (AWS EBS CSI driver) gibi.
   - Her bulut sağlayıcısı veya depolama çözümü için farklı parametreler girilerek farklı StorageClass tanımlanabilir.

3. **Parametreler ve Geri Dönüş (Reclaim) Politikaları**  
   - `parameters` alanı, blok boyutu, replikasyon faktörü, depolama tipi (SSD/HDD), verinin şifrelenmesi gibi depolama çözümüne özgü ayarları içerir.  
   - `reclaimPolicy` ile kullanım bitince PV'nin ne yapması gerektiğini tanımlarsınız. `Delete` (tamamen sil) veya `Retain` (elde tut) seçenekleri sıklıkla kullanılır.

4. **Çoklu StorageClass Desteği**  
   - Kubernetes kümesinde, farklı nitelik ve performans özelliklerine sahip birden fazla StorageClass aynı anda tanımlanabilir.  
   - Örneğin, "hızlı SSD depolama" için bir StorageClass, "ekonomik HDD depolama" için başka bir StorageClass oluşturabilirsiniz.

5. **Varsayılan (Default) StorageClass**  
   - Bir StorageClass, `storageclass.kubernetes.io/is-default-class: "true"` etiketiyle işaretlenirse kube içindeki varsayılan depolama sınıfı olur. Böylece PVC'lerde `StorageClassName` belirtilmediği durumlarda otomatik olarak bu sınıf kullanılır.

---

## Örnek StorageClass (In-tree AWS EBS)

Aşağıdaki örnekte, AWS EBS **in-tree driver** (kubernetes.io/aws-ebs) kullanan basit bir StorageClass tanımı gösterilmektedir:

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: aws-ebs-gp2
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
  fsType: ext4
reclaimPolicy: Delete
volumeBindingMode: Immediate
```
1. **`provisioner: kubernetes.io/aws-ebs`**  
   - Bu StorageClass, AWS EBS kullanarak dinamik PV oluşturacak (in-tree sürücü).
2. **`annotations`**  
   - Varsayılan StorageClass olarak işaretlenmiştir (`is-default-class: "true"`).
3. **`parameters`**  
   - `type: gp2`, AWS üzerinde gp2 tipinde bir EBS hacmi oluşturur.  
   - `fsType: ext4`, oluşturulacak disk ext4 dosya sistemiyle formatlanır.
4. **`reclaimPolicy: Delete`**  
   - Bu PV'nin kullanımı bittiğinde otomatik olarak silinir.
5. **`volumeBindingMode: Immediate`**  
   - PVC oluşturulurken eş zamanlı PV tahsisi yapılır.  

> **Not**  
> "In-tree" sürücülerin Kubernetes'teki desteği kısıtlanmaya başlamıştır. AWS EBS için, out-of-tree **CSI** sürücüsü tercih edilmesi önerilir.

---

## Örnek StorageClass (AWS EBS CSI Driver)

AWS EBS CSI driver (out-of-tree) kullanarak oluşturulan bir StorageClass örneği ise şu şekildedir:

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: aws-ebs-gp3-csi
  annotations:
    storageclass.kubernetes.io/is-default-class: "false"
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  fsType: ext4
  encrypted: "true"
  # kmsKeyId: "arn:aws:kms:us-east-1:123456789012:key/abcd-efgh-ijkl" # Opsiyonel
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
```

1. **`provisioner: ebs.csi.aws.com`**  
   - **AWS EBS CSI driver** kullanılır. "Out-of-tree" olarak da bilinir.  
2. **`parameters.type: gp3`**  
   - gp3 tipi EBS hacimleri oluşturur. `fsType` ext4 olarak biçimlendirir.  
3. **`encrypted: "true"`**  
   - EBS hacmini AWS KMS ile şifreler (isteğe bağlı).  
4. **`volumeBindingMode: WaitForFirstConsumer`**  
   - PV ancak bir Pod gerçekten PVC kullandığında oluşturulur. Bu yaklaşım, Pod'un hangi Availability Zone'da koştuğuna göre PV riskini azaltır.  
5. **`allowVolumeExpansion: true`**  
   - Sonradan PVC boyutunu büyütmeye (volume expansion) olanak tanır.

---

## StorageClass ile PVC İlişkisi

Bir **PersistentVolumeClaim** (PVC), `storageClassName` alanında istediğiniz StorageClass'ı (ör. `aws-ebs-gp3-csi`) referans gösterirse Kubernetes otomatik olarak bu StorageClass parametrelerini kullanarak bir **PersistentVolume** oluşturur. Örnek bir PVC:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-ebs-csi-claim
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: aws-ebs-gp3-csi
  resources:
    requests:
      storage: 5Gi
```
1. **`storageClassName: aws-ebs-gp3-csi`**  
   - PVC, ihtiyaç duyduğu PV'yi `aws-ebs-gp3-csi` StorageClass üzerinden talep edecek.
2. **`resources.requests.storage: 5Gi`**  
   - Kullanım için talep edilen depolama miktarı 5 GB olarak belirtilmiştir.

Bu PVC bir Pod içerisinde volume olarak bağlandığında, uygulama verilerini **dinamik oluşturulmuş** EBS diskinde saklar.

---

## Komutlar ve Yönetim

- **StorageClass'ları Listeleme**:  
  ```bash
  kubectl get storageclass
  ```
- **Detaylarını İnceleme**:  
  ```bash
  kubectl describe storageclass <storageclass-name>
  ```
- **Silme**:  
  ```bash
  kubectl delete storageclass <storageclass-name>
  ```

> **Kurulum**:  
> AWS EBS CSI driver'ı kullanabilmek için, EBS CSI eklentisinin kümenize yüklenmiş ve etkin durumda olması gerekir. (Ör. "helm install aws-ebs-csi-driver/aws-ebs-csi-driver" vb.)

---

## Sonuç

**StorageClass**, Kubernetes'te **dinamik depolama** yönetimini mümkün kılar. Hem **in-tree** (eski yaklaşım) hem de **out-of-tree / CSI** sürücüleri destekleyerek farklı bulut sağlayıcıları veya özel depolama sistemleriyle çalışmanıza olanak tanır. AWS EBS özelinde:

- **In-Tree**: `provisioner: kubernetes.io/aws-ebs` (geleneksel, ancak desteği gelecekte kısıtlanacak)  
- **CSI Driver**: `provisioner: ebs.csi.aws.com` (güncel ve önerilen yöntem)

Uygulama ekibinin sadece "PVC" talep etmesi yeterli olurken, yöneticiler StorageClass tanımlarını yöneterek doğru performans, boyut ve politikaları sunabilir. Bu şekilde mikroservis mimarilerinde bile ihtiyaç duyulan kalıcı depolama altyapısı **esnek**, **kararlı** ve **kolay** bir şekilde otomatik sağlanmış olur.
