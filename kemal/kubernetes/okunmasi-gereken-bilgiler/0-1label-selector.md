# Kubernetes Label ve Selector

## Label Nedir?
- Label, Kubernetes nesnelerine (Pod, Service, Deployment, Node vb.) eklenen key-value çiftleridir
- Nesneleri kategorize etmek ve organize etmek için kullanılır
- Örnek: `app: frontend`, `env: production`, `tier: web`

## Label Kullanım Senaryoları
- Uygulamaları sürümlere göre ayırmak (`version: v1`, `version: v2`)
- Ortamları etiketlemek (`env: dev`, `env: test`, `env: prod`)
- Takım veya departman bilgisi eklemek (`team: backend`, `team: frontend`)
- Node'ları etiketleyerek belirli iş yüklerini belirli donanımlara yönlendirmek (`disktype: ssd`, `region: us-west`)

## Selector Nedir?
- Selector, belirli label'lara sahip nesneleri seçmek için kullanılır
- Service'lerin hangi Pod'lara trafik yönlendireceğini belirler
- Deployment'ların hangi Pod'ları yöneteceğini tanımlar
- NodeSelector ile Pod'ların belirli Node'larda çalışmasını sağlar

## Selector Türleri
1. **Eşitlik Bazlı Selector**
   - `=` veya `==`: Eşit olanları seçer
   - `!=`: Eşit olmayanları seçer
   - Örnek: `env=production`, `tier!=backend`

2. **Set Bazlı Selector**
   - `in`: Belirtilen değerlerden birini içerenleri seçer
   - `notin`: Belirtilen değerleri içermeyenleri seçer
   - `exists`: Belirtilen key'e sahip olanları seçer
   - Örnek: `env in (production, staging)`, `tier notin (frontend, backend)`

## Örnek YAML

```yaml:kemal/kubernetes/kind/0-1label-selector.md
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  labels:
    app: web
    env: production
    tier: frontend
spec:
  containers:
  - name: nginx
    image: nginx:1.19
  nodeSelector:
    disktype: ssd
```

```yaml:kemal/kubernetes/kind/0-1label-selector.md
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: web
    tier: frontend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
```

## Best Practices
- Label'ları tutarlı bir şekilde kullanın
- Çok fazla label eklemekten kaçının
- Anlamlı ve açıklayıcı label isimleri seçin
- Label'ları dokümantasyonda belirtin
