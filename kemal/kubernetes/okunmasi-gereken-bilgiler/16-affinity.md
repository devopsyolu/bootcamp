# Kubernetes Affinity, Anti-Affinity ve NodeSelector

Kubernetes'te "affinity", "anti-affinity" ve "nodeSelector" kavramları, pod'ların belirli düğümlerde (node) veya diğer pod'larla birlikte veya ayrı olarak yerleştirilmesini kontrol etmek için kullanılır. Bu kavramlar, uygulamalarınızın daha iyi performans göstermesi, daha güvenilir olması veya belirli donanım kaynaklarını kullanması için pod'ların yerleştirilmesini optimize etmenize yardımcı olabilir.

## NodeSelector

`nodeSelector`, pod'ların belirli etiketlere sahip düğümlerde çalışmasını sağlamak için kullanılan en basit yöntemdir. Pod tanımında `nodeSelector` kullanarak, pod'un çalışabileceği düğümleri etiketlere göre seçebilirsiniz.

### NodeSelector Örneği

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx
  nodeSelector:
    disktype: ssd
```

## Affinity ve Anti-Affinity

`Affinity` ve `anti-affinity`, pod'ların yerleştirilmesi için daha esnek ve güçlü bir kontrol sağlar. İki tür affinity vardır:

### Node Affinity
Node affinity, pod'ların belirli etiketlere sahip düğümlerde çalışmasını sağlar. İki modda çalışabilir:
- `requiredDuringSchedulingIgnoredDuringExecution`: Zorunlu kurallar.
- `preferredDuringSchedulingIgnoredDuringExecution`: Tercih edilen kurallar.

#### Node Affinity Örneği

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: disktype
            operator: In
            values:
            - ssd
  containers:
  - name: nginx
    image: nginx
```

### Pod Affinity/Anti-Affinity
Pod affinity ve anti-affinity, pod'ların diğer pod'larla birlikte veya ayrı olarak yerleştirilmesini kontrol eder.

#### Pod Anti-Affinity Örneği

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  affinity:
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - nginx
        topologyKey: kubernetes.io/hostname
  containers:
  - name: nginx
    image: nginx
```

## NodeSelector, Affinity ve Anti-Affinity Arasındaki Farklar

| Özellik                | NodeSelector                          | Affinity                              | Anti-Affinity                        |
|------------------------|---------------------------------------|---------------------------------------|---------------------------------------|
| **Esneklik**           | Basit ve kısıtlı                      | Daha esnek ve güçlü                   | Daha esnek ve güçlü                   |
| **Kullanım Amacı**     | Belirli etiketlere sahip düğümlerde çalıştırma | Pod'ların belirli düğümlerde veya pod'larla birlikte çalışmasını sağlama | Pod'ların belirli pod'lardan ayrı çalışmasını sağlama |
| **Zorunluluk**         | Zorunlu                               | Zorunlu veya tercih edilen            | Zorunlu veya tercih edilen            |
| **Karmaşıklık**        | Basit                                 | Daha karmaşık                         | Daha karmaşık                         |

Bu kavramlar, Kubernetes'te uygulamalarınızın dağıtımını optimize etmenize ve belirli iş yüklerini daha iyi yönetmenize yardımcı olur. Affinity ve anti-affinity kuralları, uygulamalarınızın performansını artırabilir, kaynak kullanımını optimize edebilir ve daha iyi hata toleransı sağlayabilir.

## Taints ve Tolerations

Kubernetes'te `taints` (lekeler) ve `tolerations` (toleranslar), düğümlerin (nodes) belirli pod'ları kabul etmesini veya reddetmesini kontrol etmek için kullanılan mekanizmalardır. Bu kavramlar, `affinity`, `anti-affinity` ve `nodeSelector` ile birlikte çalışarak pod'ların düğümlere yerleştirilmesini daha da esnek hale getirir.

### Taints (Lekeler)
- **Tanım**: Bir düğüme `taint` ekleyerek, o düğümün belirli pod'ları kabul etmesini engelleyebilirsiniz. Bir düğüm, üzerinde `taint` olduğu sürece, sadece bu `taint`'i tolere edebilen pod'ları kabul eder.
- **Kullanım Amacı**: Özel düğümleri belirli iş yükleri için ayırmak veya düğümlerin belirli pod'ları çalıştırmasını engellemek için kullanılır.
- **Örnek**: Bir düğümü sadece GPU gerektiren iş yükleri için ayırmak istiyorsanız, bu düğüme bir `taint` ekleyebilirsiniz.

#### Düğüme Taint Ekleme
```bash
kubectl taint nodes <node-name> key=value:NoSchedule
```

### Tolerations (Toleranslar)
- **Tanım**: `Tolerations`, bir pod'un belirli `taint`'lere sahip düğümlerde çalışmasına izin verir. Bir pod, bir düğümdeki `taint`'i tolere edebiliyorsa, o düğümde çalışabilir.
- **Kullanım Amacı**: Belirli `taint`'lere sahip düğümlerde çalışması gereken pod'lar için kullanılır.
- **Örnek**: GPU gerektiren bir pod, GPU düğümlerindeki `taint`'i tolere edebilir.

#### Pod'a Toleration Ekleme
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gpu-pod
spec:
  containers:
  - name: gpu-container
    image: nvidia/cuda:11.0-base
  tolerations:
  - key: "key"
    operator: "Equal"
    value: "value"
    effect: "NoSchedule"
```

### Taints ve Tolerations Arasındaki İlişki
- **Temel İlişki**: `Taints`, düğümlerin pod'ları reddetmesini sağlar; `tolerations` ise pod'ların bu reddedilmeyi aşmasına izin verir.
- **Birlikte Çalışma**: Bir düğümde `taint` varsa, sadece bu `taint`'i tolere edebilen pod'lar o düğümde çalışabilir. Diğer pod'lar, bu düğümde çalışamaz.

### Taints ve Tolerations'ın Etkileri
| Etki Türü         | Açıklama                                                                 |
|--------------------|-------------------------------------------------------------------------|
| `NoSchedule`       | Pod'lar bu düğüme yerleştirilmez (mevcut pod'lar etkilenmez).           |
| `PreferNoSchedule` | Kubernetes, bu düğüme pod yerleştirmemeyi tercih eder (zorunlu değil).  |
| `NoExecute`        | Mevcut pod'lar da bu düğümden kaldırılır (eğer tolerasyon yoksa).       |

### **Taints ve Tolerations ile Affinity/Anti-Affinity Arasındaki İlişki**
- **Affinity/Anti-Affinity**: Pod'ların belirli düğümlerde veya diğer pod'larla birlikte/ayrı çalışmasını sağlar.
- **Taints/Tolerations**: Düğümlerin belirli pod'ları kabul etmesini veya reddetmesini sağlar.
- **Birlikte Kullanım**: `Affinity` ve `anti-affinity`, pod'ların yerleştirilmesini kontrol ederken; `taints` ve `tolerations`, düğümlerin hangi pod'ları kabul edeceğini kontrol eder. Bu iki mekanizma birlikte kullanılarak, pod'ların yerleştirilmesi üzerinde daha fazla kontrol sağlanabilir.
