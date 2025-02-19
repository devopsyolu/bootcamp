# Kubernetes Label ve Annotations

## Label Nedir?
- **Label**, Kubernetes nesnelerine (Pod, Service, Deployment, Node vb.) eklenen anahtar-değer (key-value) çiftleridir.
- Nesnelerin gruplandırılması, kategorize edilmesi ve seçilmesi için kullanılır.
- Örneğin: `app: frontend`, `env: production`, `tier: backend`.
- Service veya Deployment gibi kaynakların hangi nesnelerle etkileşimde bulunacağını belirlemek için seçim (selector) mekanizmasında kullanılır.

## Annotation Nedir?
- **Annotation**, Kubernetes nesnelerine eklenen esnek anahtar-değer çiftleridir.
- Label'lardan farklı olarak, seçim veya gruplandırmada kullanılmaz.
- Daha çok ek metadata sağlamak, açıklamalar, yapılandırma detayları veya diğer ek bilgileri saklamak için kullanılır.

### Annotation Kullanım Alanları ve Örnekleri

1. **Açıklama (Description)**
    - Açıklayıcı bilgileri belirtmek için kullanılır.
    - Örnek:  
      `description: "Bu pod, üretim ortamında backend servislerini barındırır."`

2. **Sahiplik ve Bakım**
    - Nesnenin sahibi veya bakımından sorumlu takımı tanımlamak için.
    - Örnek:  
      `maintainer: "team@example.com"`

3. **Versiyon Bilgisi**
    - Nesnenin versiyonunu veya sürüm bilgisini takip etmek için.
    - Örnek:  
      `version: "v1.2.3"`

4. **Son Uygulanan Konfigürasyon**
    - `kubectl` ile uygulanan en son konfigürasyonu saklamak için kullanılır.
    - Örnek:  
      `kubectl.kubernetes.io/last-applied-configuration: '{"apiVersion": "v1", "kind": "Pod", ...}'`

5. **Özel Metadata**
    - Organizasyon içi veya özel entegrasyonlar için ek bilgileri saklamak amacıyla kullanılabilir.
    - Örnekler:
      - `mycompany.com/owner: "backend team"`
      - `mycompany.com/monitoring: "enabled"`

## Örnek YAML Dosyası

Aşağıdaki örnek, bir Pod için hem label hem de genişletilmiş annotation kullanımını göstermektedir:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: sample-pod
  labels:
    app: sample
    environment: production
  annotations:
    description: "Bu pod, üretim ortamında backend servislerini barındırır"
    maintainer: "team@example.com"
    version: "v1.2.3"
    kubectl.kubernetes.io/last-applied-configuration: |
      {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
          "name": "sample-pod"
        },
        "spec": {
          "containers": [
            {"name": "sample-container", "image": "nginx:latest"}
          ]
        }
      }
    mycompany.com/owner: "backend team"
spec:
  containers:
  - name: sample-container
    image: nginx:latest
```

## Best Practices
- **Tutarlılık:** Annotation anahtarlarını tutarlı ve anlaşılır şekilde adlandırın.
- **Amaca Uygun Kullanım:** Label'lar seçim ve gruplama için kullanılırken, annotation'lar ek metadata sağlamalıdır.
- **Dokümantasyon:** Kullandığınız annotation anahtarlarını takımınızın anlayacağı şekilde dokümante edin.
- **Gereksiz Bilgiden Kaçının:** Sadece gerekli bilgileri ekleyerek nesnenin okunabilirliğini koruyun. 