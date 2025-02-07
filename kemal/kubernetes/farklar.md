# Kubernetes Nesneleri Arasındaki Farklar

Bu belge, Kubernetes içerisinde kullanılan temel nesneler arasındaki farkları özetlemektedir. Aşağıda her bir kaynak tipi için ayrıntılı karşılaştırmalar bulunmaktadır.

## Pod vs Service
- **Pod:**
  - Uygulamanın çalıştığı en temel birimdir.
  - Bir veya daha fazla container içerir.
  - Her pod, benzersiz bir IP adresine sahiptir.
- **Service:**
  - Pod'lara erişimi kolaylaştıran soyutlamadır.
  - Pod'ların IP adresleri dinamik olduğundan sabit bir erişim noktası sağlar.
  - Farklı tipleri vardır: ClusterIP, NodePort, LoadBalancer.

## ReplicaSet vs Deployment
- **ReplicaSet:**
  - Belirli sayıda pod'un çalışmasını garanti eder.
  - Yapısı daha basittir ve doğrudan kullanılmaz; genellikle Deployment tarafından yönetilir.
- **Deployment:**
  - ReplicaSet'leri oluşturur, günceller ve yönetir.
  - Rolling update (yavaş güncelleme) ve rollback gibi gelişmiş özellikler sunar.
  - Uygulamanın yaşam döngüsünü yönetmek için tercih edilir.

## StatefulSet vs Deployment
- **StatefulSet:**
  - Durum bilgisi gerektiren uygulamalar için kullanılır.
  - Pod'lara benzersiz ve kalıcı kimlikler verir (örn: app-0, app-1, ...).
  - Pod'ların sıralı ve belirli bir şekilde başlatılmasını sağlar.
  - Kalıcı depolama için sabit PersistentVolumeClaim bağlantıları kullanır.
- **Deployment (ve ReplicaSet):**
  - Durum bilgisi gerektirmeyen uygulamalar içindir.
  - Pod'lar arasında sıralı veya kalıcı kimlik garantisi sağlamaz.
  - Daha dinamik ve esnek bir yapı sunar.

## ConfigMap vs Secret
- **ConfigMap:**
  - Uygulama konfigürasyon dosyalarını ve ayarlarını saklar.
  - Düz metin verilerini içerir; base64 kodlama gerekmez.
  - Boyut limiti yaklaşık 1MB'dır.
- **Secret:**
  - Hassas verileri (şifre, token, sertifika) saklar.
  - Veriler base64 ile kodlanmıştır.
  - Boyut limiti yaklaşık 1MB'dır.
  - RBAC ile erişim kontrolü ve encryption at rest desteği bulunur.

## DaemonSet vs Deployment
- **DaemonSet:**
  - Her node üzerinde otomatik olarak bir pod çalıştırır.
  - Yeni node eklendiğinde otomatik pod oluşturur; node kaldırıldığında ilgili pod silinir.
  - Genellikle log toplama, izleme, node-exporter veya sistem görevleri için kullanılır.
- **Deployment:**
  - Pod'lar herhangi bir node üzerinde çalışabilir.
  - Belirli bir toplam pod sayısı belirtilir; node başına dağılım garanti edilmez.
  - Genel uygulama dağıtımları için tercih edilir.

## Job vs CronJob
- **Job:**
  - Tek seferlik çalıştırılması gereken görevleri yönetir.
  - İş tamamlandığında pod sonlanır.
  - Hata durumunda yeniden deneme sayılamaz veya belirli bir limit dahilinde tekrar denenir.
- **CronJob:**
  - Belirli zamanlamalara göre tekrarlanan görevleri yönetir.
  - Unix cron formatında zamanlama yapılır.
  - Her çalıştırma için yeni bir Job oluşturur.
  - Periyodik yedekleme, raporlama gibi işlemler için uygundur.

## Service vs Ingress
- **Service:**
  - Cluster içi servis keşfi ve load balancing sağlar.
  - Pod'lara sabit IP adresleri ve DNS isimleri atar.
  - Farklı tipleri vardır: ClusterIP, NodePort, LoadBalancer.
- **Ingress:**
  - Cluster dışından gelen HTTP/HTTPS trafiğini yönetir.
  - URL bazlı yönlendirme yapabilir, SSL/TLS terminasyonu sağlar.
  - Tek IP üzerinden birden fazla servise erişim imkanı sunar.
  - Name-based virtual hosting ve path-based routing desteği verir.

## PersistentVolume vs PersistentVolumeClaim
- **PersistentVolume (PV):**
  - Cluster seviyesinde tanımlanan kalıcı depolama kaynağıdır.
  - Admin tarafından oluşturulur ya da dinamik olarak provision edilir.
  - Storage class'a göre farklı depolama tipleri kullanılabilir.
- **PersistentVolumeClaim (PVC):**
  - Kullanıcının talep ettiği depolama kaynağını temsil eder.
  - Belirtilen boyut, erişim modu ve storage class değerlerine göre uygun bir PV ile eşleştirilir.
  - Pod'lar tarafından veri depolaması için kullanılır.

---

Bu belge, Kubernetes kaynaklarının nasıl çalıştığını ve hangi kullanım senaryosu için hangi kaynak tipinin tercih edilmesi gerektiğini anlamanıza yardımcı olacaktır.
