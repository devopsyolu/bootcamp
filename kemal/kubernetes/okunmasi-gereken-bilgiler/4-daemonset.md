# Kubernetes DaemonSet Nedir?

**DaemonSet**, Kubernetes kümesindeki her düğüm (node) üzerinde bir Pod çalıştırmak için kullanılan bir **Kubernetes** kaynağıdır. Böylece belirli bir Pod'un – örneğin log toplama, izleme, ağ yönetimi gibi – her node üzerinde otomatik olarak ayağa kalkması sağlanır.

## DaemonSet'in Temel Özellikleri

1. **Tüm Node'larda Konteyner Çalıştırma**  
   DaemonSet her node için bir kopya oluşturur. Node sayısı arttıkça, yeni node'lara otomatik olarak Pod yerleştirilir. Eğer bir node kümeden ayrılırsa, o node'daki Pod da silinir.

2. **Özel Node Seçimi**  
   DaemonSet, etiketlere (labels) göre filtrelenerek belirli node'larda çalışacak şekilde özelleştirilebilir. Böylece her node yerine sadece belirli etiketlere sahip node'larda Pod çalışması sağlanır.

3. **Log Toplama ve İzleme Senaryoları**  
   Genellikle log toplama (Fluentd, Logstash vb.) veya sistem izleme (örneğin Prometheus Node Exporter) gibi görevlerde kullanılır. Bu sayede her node'daki loglar veya metrikler rahatlıkla toplanabilir.

4. **Node Bazlı Konfigürasyon**  
   DaemonSet içerisinde bir Pod, node'un disk, network veya diğer özelleştirilmiş kaynaklarına **HostPath** gibi volume tiplerini kullanarak erişebilir. Böylece node seviyesindeki klasörler (örneğin: `/var/log`, `/var/run/docker.sock`) Pod içerisine basitçe bağlanabilir.

## Örnek Kullanım Senaryoları

- **Log Toplama (Fluentd, Logstash)**  
  Düğümler üzerindeki log dosyalarını toplayarak merkezi bir log yönetim sistemine gönderir.
- **Node İzleme (Node Exporter, Telegraf)**  
  Düğümlerin CPU, bellek, disk, ağ gibi metriklerini toplar ve zaman serisi veritabanına (örneğin Prometheus) gönderir.
- **Alt yapı Bileşenleri (CNI, CSI Plugin'ler)**  
  Ağ eklentileri, depolama sürücüleri gibi her node'da farklı yapılandırmaların olması gereken bileşenler DaemonSet olarak yönetilir.

## DaemonSet Komutlarına Örnekler

- **Oluşturma / Güncelleme**:  
  ```bash
  kubectl apply -f daemonset.yaml
  ```
- **Durumu Görüntüleme**:  
  ```bash
  kubectl get daemonsets
  kubectl describe daemonset log-collector
  ```
- **Node Bazında Pod Dağılımı**:  
  ```bash
  kubectl get pods -o wide
  ```
  Bu komutla Pod'ların hangi node üzerinde çalıştığını görebilirsiniz.
- **Silme**:  
  ```bash
  kubectl delete daemonset log-collector
  ```

## Sonuç

**DaemonSet**, Kubernetes ekosisteminde **her node üzerinde** çalışması gereken uygulamaları (log toplama, izleme, ağ bileşenleri vb.) yönetmenin en pratik yoludur. Yeni bir node eklendiğinde DaemonSet o node üzerinde bir Pod oluşturur, node çıkarıldığında ilgili Pod'u siler. Bu işleyiş, merkezi yönetim ve node bazında tutarlılık sağlamak isteyen her senaryoda büyük avantaj sunar.
