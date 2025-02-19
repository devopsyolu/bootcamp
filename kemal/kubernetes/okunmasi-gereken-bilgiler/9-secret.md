# Secret Hakkında

Kubernetes'te *Secret*, genellikle veritabanı parolaları, API anahtarları, token'lar veya sertifikalar gibi hassas bilgileri güvenli bir şekilde saklamak ve yönetmek için kullanılan bir kaynaktır. Böylece bu bilgileri düz metin (plain text) olarak doğrudan konfigürasyon dosyalarına eklemekten kaçınarak güvenlik risklerini azaltabilirsiniz.

## Kubernetes Secret Nedir?
- **Kimlik doğrulama ve erişim bilgilerini gizli tutmak için** kullanılır.  
- *Base64* ile encode edilerek saklanır. Ancak bu, şifrelemekten farklıdır. Üretim ortamında ek şifreleme yöntemleri kullanmak önerilir.  
- Pod'lar, üzerlerinde tanımlanan ortamlara (environment variables) veya *volume* olarak bu bilgilere erişebilir.

## Secret Türleri
1. **Opaque**  
   - Herhangi bir key-value çiftini tek seferde encode ederek saklamak için en temel tiptir.

2. **docker-registry**  
   - Özel Docker konteyner kayıtlarına (registry) erişim için kullanılır.  
   - `kubernetes.io/dockercfg` veya `kubernetes.io/dockerconfigjson` gibi türlerle oluşturulur.

3. **tls**  
   - Sunucu SSL/TLS sertifikası ve anahtar çiftini saklar.

## Secret Nasıl Oluşturulur?

### 1. Komut Satırı (kubectl) ile
```bash
kubectl create secret generic <secret-adı> \
  --from-literal=KULLANICI_ADI=kemal \
  --from-literal=PAROLA=12345
```

### 2. YAML Üzerinden
```yaml:path/to/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: Opaque
data:
  # Base64 ile encode edilmiş değerler
  KULLANICI_ADI: a2VtYWw=
  PAROLA: MTIzNDU=
```

## Secret'ı Pod İçerisinde Kullanma
Pod manifest'inizde, Secret değerlerini ortam değişkeni (environment variable) veya bir volume olarak tanımlayabilirsiniz. Aşağıda ortam değişkeni olarak kullanma örneği görebilirsiniz:

```yaml:path/to/pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-demo-pod
spec:
  containers:
  - name: demo-container
    image: busybox
    command: ["/bin/sh", "-c", "echo $KULLANICI_ADI ve $PAROLA; sleep 3600"]
    env:
    - name: KULLANICI_ADI
      valueFrom:
        secretKeyRef:
          name: my-secret
          key: KULLANICI_ADI
    - name: PAROLA
      valueFrom:
        secretKeyRef:
          name: my-secret
          key: PAROLA
  restartPolicy: Never
```

## Özet
- Hassas verileri sır (secret) olarak saklayarak güvenliği artırır.  
- Base64 ile saklandığından, konfigürasyon dosyalarında veriyi temel düzeyde gizler ancak tam şifreleme sağlamaz.  
- Kurumsal projelerde ek şifreleme ve anahtar yönetimi yöntemleri önerilir.  
- Pod'lar bu verilere doğrudan ortam değişkeni veya volume olarak erişebilir.  

Bu yöntemle, Kubernetes ortamlarında kritik verileri yönetirken güvenliği büyük ölçüde artırabilirsiniz.
