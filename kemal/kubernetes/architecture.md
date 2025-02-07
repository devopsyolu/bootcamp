# Kubernetes Mimarisi

Kubernetes, kontrol düzlemi (control plane) ve işçi düğümler (nodes) arasında dağıtılmış bir mimari kullanır.

## Kontrol Düzlemi Bileşenleri
- **API Server:** Küme ile etkileşim için tek giriş noktasıdır.
- **etcd:** Tüm küme verilerinin depolandığı, yüksek oranda erişilebilir anahtar-değer deposudur.
- **Controller Manager:** Kümedeki istenen durumu sağlamak için çeşitli kontrol döngülerini yönetir.
- **Scheduler:** Mevcut kaynaklara göre pod'ları uygun düğümlere atar.

## İşçi Düğüm Bileşenleri
- **Kubelet:** Her düğümde çalışan, pod'ları denetleyen ve konteynerlerin durumunu takip eden ajan.
- **Kube-proxy:** Ağ trafiğini yönetir ve servisler arasında yük dengeleme yapar.

Bu bileşenlerin nasıl etkileştiğini anlamak, Kubernetes'i verimli kullanmanızı ve sorun giderme işlemlerini kolaylaştırır. 