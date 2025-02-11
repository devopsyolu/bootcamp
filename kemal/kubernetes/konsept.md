# Temel Kubernetes Kavramları

## Pod'lar
- **Tanım:** Bir veya daha fazla konteynerin aynı ağ ve depolama kaynaklarını paylaştığı çalışma birimleridir.
- **Özellikler:** Ortak IP adresi, hostname ve depolama alanları.

## Deployment
- **İşlev:** Pod'ların ve ReplicaSet'lerin deklaratif yönetimini sağlar.
- **Faydalar:** Rolling update, ölçeklendirme ve hata durumunda geri dönüş (rollback) yeteneklerini destekler.

## Service
- **Tanım:** Pod'ları dış dünyaya veya diğer servis bileşenlerine bağlamak için soyut bir erişim yöntemi sağlar.
- **Türleri:** ClusterIP, NodePort, LoadBalancer.

## ReplicaSet
- **Görev:** Belirli sayıda pod örneğinin daima çalışır durumda olmasını sağlar.
- **Kullanım Alanı:** Deployment tarafından yönetilir.

## Ek Kavramlar
- **StatefulSet & DaemonSet:** Sırasıyla durum gerektiren uygulamalar ve tüm düğümlerde çalışan uygulamalar için kullanılır.
- **Namespace:** Kaynakların izole edilmesi ve gruplandırılması için mantıksal bölümlerdir.
- **ConfigMap & Secret:** Yapılandırma verilerini ve gizli bilgileri yönetmek için kullanılır.

Bu temel kavramlar, Kubernetes üzerinde uygulamalarınızı nasıl dağıtacağınızı ve yöneteceğinizi anlamanın anahtarıdır.

## 0-intro.md
Kubernetes'e hızlı bir giriş ve temel kavramlara genel bakış sağlar. Kümenin yapısı, temel bileşenler ve konteyner orkestrasyonunun ne olduğu gibi temel bilgiler yer alır.

## 1-pod.md
Kubernetes'in en küçük dağıtım birimi olan **Pod** hakkında bilgi verir. Bir veya birden fazla container'ın ağ ve depolama kaynaklarını paylaşarak nasıl çalıştığını ve yaşam döngüsünü açıklar.

## 2-deployment.md
**Deployment** nesnesinin, Pod'ları ve ReplicaSet'leri ön tanımlı (deklaratif) bir yöntemle yönetmek için nasıl kullanıldığını anlatır. Rolling update, ölçeklendirme ve rollback (geri dönüş) gibi özellikleri öne çıkarır.

## 3-replicaset.md
Kubernetes'in **ReplicaSet** nesnesiyle belirli sayıda Pod'un sürekli olarak çalışır durumda tutulmasını sağlar. Genelde Deployment tarafından yönetilir, Pod replikasyon kontrolünü detaylandırır.

## 4-statefulset.md
**StatefulSet**, sürekli veri tutma ihtiyacı olan (durumlu) uygulamaların yönetimi için özel bir kaynaktır. Her Pod'un kalıcı kimlik (persistent ID) kazanmasını ve sıralı başlatma/durdurma akışı gibi durum gerektiren özellikleri destekler.

## 5-daemonset.md
**DaemonSet**, tüm (veya belirli) Node'larda tek bir Pod kopyasının çalışmasını garanti eder. Sistemle ilgili arka plan hizmetleri (ör. log toplama, ağ izleme ajanları) için kullanılır.

## 6-service.md
**Service**, Kubernetes içindeki Pod'lara kalıcı bir IP ve DNS ismi sunarak ağ erişimini kolaylaştırır. "ClusterIP", "NodePort", "LoadBalancer" gibi tipleriyle iç veya dış ağ bağlantısı oluşturmak mümkündür.

## 7-configmap-secret.md
**ConfigMap** ve **Secret**, uygulama yapılandırma verilerini ve hassas bilgileri (parola, token vb.) yönetmek için kullanılır. Bu ikisi, container imajlarını yeniden oluşturmadan ortam değişkeni veya dosya bazlı konfigürasyon sunmayı kolaylaştırır.

## 8-persistentvolume.md
**PersistentVolume (PV)**, Kubernetes'te fiziksel depolama kaynaklarını (NFS, AWS EBS, GCP PD vb.) soyut bir şekilde temsil eder. Pod'lar "PersistentVolumeClaim" üzerinden bu depolama alanına bağlanarak verilerini kalıcı saklayabilir.

## 9-persistentvolumeclaim.md
**PersistentVolumeClaim (PVC)**, Pod'ların storage ihtiyacını talep ettiği nesnedir. PVC, mevcut PV'lerle eşleşerek veya bir StorageClass aracılığıyla dinamik olarak PV oluşturularak kalıcı depolamaya erişim sağlar.

## 10-service-lb.md
"LoadBalancer" tipi Service, bulut sağlayıcı (AWS, GCP, Azure) ile entegre olarak Pod'lara tekil bir harici IP veya DNS adresi atar. İnternet üzerinden doğrudan erişim için "type: LoadBalancer" ayarının nasıl kullanıldığı anlatılır.

## 11-ingress.md
**Ingress**, HTTP/HTTPS isteklerini farklı Service'lere yönlendiren bir nesnedir. Host-based veya path-based routing, SSL/TLS terminasyonu gibi özelliklerle dış dünyadan gelen trafiği tek bir giriş noktasından yönetmeyi sağlar.

## 12-gatewayapi.md
**Gateway API**, Ingress API'nin ötesine geçerek daha esnek ve modüler ağ yönlendirme sunar. Gateway, GatewayClass, HTTPRoute gibi nesnelerle gelişmiş protokol desteği, rollere göre ayrılmış yönetim ve daha zengin routing senaryoları sunar.

## 13-role-rbac.md
**RBAC** (Role-Based Access Control) mekanizmasını açıklar. Role, ClusterRole, RoleBinding, ClusterRoleBinding nesneleriyle hangi kullanıcının hangi kaynaklar üzerinde hangi işlemleri yapabileceğini (create, delete, list vb.) detaylandırır. 