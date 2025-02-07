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