# Kubernetes Taints ve Tolerations

Kubernetes'ta taints ve tolerations, pod'ların belirli node'larda çalışmasını kontrol etmek için kullanılan mekanizmalardır. Bu mekanizmalar, belirli node'ların belirli pod'lar tarafından kullanılmasını veya kullanılmamasını sağlamak için kullanılır.

## Taints

Taints, bir node'a uygulanan ve o node'un belirli pod'lar tarafından kullanılmasını engelleyen etiketlerdir. Bir node'a taint uygulandığında, yalnızca bu taint'e uygun toleration'ları olan pod'lar o node'da çalışabilir. Taints üç bileşenden oluşur:

1. **Key**: Taint'in anahtar değeri.
2. **Value**: Taint'in değer kısmı.
3. **Effect**: Taint'in etkisi. Üç tür etkisi olabilir:
   - `NoSchedule`: Toleration'ı olmayan pod'lar bu node'a schedule edilmez.
   - `PreferNoSchedule`: Toleration'ı olmayan pod'lar mümkünse bu node'a schedule edilmez.
   - `NoExecute`: Toleration'ı olmayan pod'lar bu node'dan çıkarılır.

## Tolerations

Tolerations, pod'lara eklenen ve belirli taint'leri "tolerate" etmelerini sağlayan etiketlerdir. Toleration'lar, pod'ların belirli taint'lere sahip node'larda çalışmasına izin verir. Toleration'lar da benzer şekilde key, value ve effect bileşenlerinden oluşur.

## Örnek Kullanım

Aşağıda bir node'a taint ekleme ve bir pod'a toleration ekleme örneği verilmiştir:

### Node'a Taint Ekleme

```bash
kubectl taint nodes <node-name> key=value:NoSchedule
```

### Pod'a Toleration Ekleme

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
  - name: my-container
    image: my-image
  tolerations:
  - key: "key"
    operator: "Equal"
    value: "value"
    effect: "NoSchedule"
```

Bu örnekte, `my-pod` adlı pod, `key=value:NoSchedule` taint'ine sahip bir node'da çalışabilir. Toleration'lar, pod'ların belirli taint'lere sahip node'larda çalışmasına izin vererek esneklik sağlar.
