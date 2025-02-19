# Kubernetes Endpoints

**Kubernetes Endpoints** bir Kubernetes servisinin (Service) arka planda hangi Pod IP adreslerine yönlendirme yaptığını gösteren bir Kubernetes kaynağıdır. Bir Service oluşturduğunuzda, Kubernetes otomatik olarak ona ait bir Endpoints kaynağı da oluşturur (Service ismi ile aynı isme sahip). Servisin etiket seçicisine (label selector) uyan tüm Pod'lar, Endpoints kaynağı üzerinden IP adresleri ile listelenir.

## Nasıl Çalışır?

1. **Service Tanımı:** Kubernetes'te bir Service oluşturduğunuzda, bu servis belirli etiketlere (labels) sahip Pod'ları hedef alır.  
2. **Endpoints Nesnesi:** Service'e uyan Pod'ların IP adreslerini içeren bir Endpoints nesnesi oluşturulur.  
3. **Yönlendirme (Routing):** Kubernetes, bu Endpoints kaynağını kullanarak, servise gelen trafiği doğru Pod'lara yönlendirir.

## Örnek Komutlar

### Endpoints Kaynaklarını Listeleme
```bash
kubectl get endpoints
```

Bu komutla tüm Endpoints kaynaklarının listesini görebilirsiniz.

### Belirli Bir Servise Ait Endpoints Detayları
```bash
kubectl describe endpoints <service-ismi>
```

Bu komut, belirtilen servise ait Endpoints kaynağının detaylarını gösterir (hangi Pod'ların IP adresleriyle eşleştiği gibi).

## Örnek YAML

Aşağıdaki örnekte, `my-service` bir Service adıdır ve Kubernetes otomatik olarak buna ait `Endpoints` nesnesini oluşturur. Normalde elle oluşturulması gerekmez ancak konsepti anlamak için basit bir Endpoints tanımı şöyle görünebilir:

```yaml
apiVersion: v1
kind: Endpoints
metadata:
  name: my-service
subsets:
  - addresses:
      - ip: 10.244.1.5
    ports:
      - port: 80
```

Gerçekte, `addresses` alanı, Service'e uyan Pod'ların IP adreslerini gösterirken `ports` alanı, servisin dinlediği port numaralarını içerir.

## Dikkat Edilmesi Gereken Noktalar

- **Otomatik Yönetim:** Bir Service tanımladığınızda, Kubernetes bu Service ile eşleşen Pod'ları izler ve Endpoints listesini otomatik olarak günceller. Elle düzenlemeniz genellikle gerekmez.  
- **Pod'lar Eşleşmezse:** Service'in etiket seçicisiyle eşleşen Pod yoksa, Endpoints kaynağı oluşturulabilir fakat `addresses` listesi boş kalır.  
- **Sağlık Kontrolleri (Probes) ve Ağ Yapısı:** Service ve Endpoints, Podların DNS veya IP adresleri bazında sağlıklı şekilde birbirine bağlanmasını sağlar. Bu sayede yatay ölçekleme, otomatik yeniden başlatma gibi Kubernetes özelliklerinden sorunsuz faydalanabilirsiniz.
