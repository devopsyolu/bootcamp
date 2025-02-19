Yukarıdaki örnekte `my-config` içinde tanımlı anahtar-değer çiftleri, `/etc/config` dizini içerisine dosya olarak yansıtılacaktır.

## Özet

- **ConfigMap**, Kubernetes ortamında uygulama ayarlarını yönetmenin yaygın yoludur.  
- Verileri gizlemeye ihtiyaç yoksa (örneğin hassas olmayan konfigürasyonlar) ConfigMap kullanılabilir. Eğer şifrelenmiş veri veya gizli anahtarlar varsa Secret nesnesi seçilmelidir.  
- ConfigMap verilerini environment değişkeni veya volume (dosya) olarak Pod'lara ileterek, uygulamalarınızın konfigürasyonunu esnek ve ölçeklenebilir şekilde yönetebilirsiniz.

Bu temel bilgilerle ConfigMap nesnelerini rahatlıkla oluşturup kullanabilirsiniz. Daha fazla detay için [Kubernetes ConfigMaps Resmi Dokümanı](https://kubernetes.io/docs/concepts/configuration/configmap/) bağlantısını inceleyebilirsiniz.

---

## ConfigMap Hakkında Ek Bilgi

ConfigMap'ler, Kubernetes içerisindeki uygulamalarınızın çalışmasını etkileyen konfigürasyon verilerini dışsallaştırmak için kullanılır. Böylece:

- **Çevresel Değişkenleri** kullanarak uygulamanın konfigürasyonunu tek bir satır bile kod değiştirmeden, sadece değerleri güncelleyerek değiştirebilirsiniz.
- **Dosya Hacmi (Volume)** olarak map edildiğinde, uygulamanız gerçek dosyalar üzerinden konfigürasyona erişebilir. Böylece uygulama içerisinde sabit kodlanmış konfigürasyona gerek kalmaz.

### Best Practices

1. **İsimlendirme:** ConfigMap isimleri, kullanım amacını veya ilgili uygulamayı belirtecek şekilde anlamlı tutulmalıdır.
2. **Versiyonlama:** Eğer belirli konfigürasyonlar sık değişiyorsa, güncellemeleri kontrol altında tutmak ve gerektiğinde geri alabilmek için versiyonlama stratejisi belirleyin (ör. etiketler veya ek açıklamalar (annotations) ile).
3. **İzolasyon:** Farklı uygulamalar veya farklı aşamalar (development, staging, production) için ayrı ConfigMap'ler oluşturmayı tercih edin.
4. **Böl ve Yönet:** Büyük ConfigMap oluşturmak yerine, ilişkili değerleri mantıksal şekilde küçük ConfigMap'lere bölebilirsiniz. Böylece yönetimi ve güncellemesi kolaylaşır.
5. **Gizlilik:** Hassas verileri asla ConfigMap içerisine koymayın. Bu tür veriler için mutlaka Kubernetes Secret nesnelerini tercih edin.
6. **Yeniden Yükleme (Reload):** Bazı uygulamalar, ConfigMap içeriği değiştiğinde otomatik olarak yeni konfigürasyonu yükleyebilir. Aksi durumda, POD'ları yeniden başlatmanız gerekebilir. Uygulamanın bu davranışını göz önünde bulundurun.

### Örnek Yükleme Stratejileri

- **Tek ConfigMap, Birden Fazla Pod:** Aynı uygulamanın birden fazla kopyası veya benzer konfigürasyonu paylaşan farklı mikro servislerde tek bir ConfigMap'i kullanabilirsiniz.  
- **Ortak Kullanım (Shared ConfigMap) + Özel ConfigMap:** Ortak parametreleri (Ör. log ayarları) paylaşan bir ConfigMap ve uygulamaya özgü ayarlarla ilgili ayrı bir ConfigMap tutarak, yönetimi kolaylaştırabilirsiniz.

Yukarıdaki pratikleri takip ederek, ConfigMap'lerinizi hem ölçeklenebilir hem de yönetilebilir bir yapı içerisinde konumlandırabilirsiniz.

## ConfigMap Oluşturma Örnekleri

### 1. Komut Satırı ile Oluşturma

```bash
kubectl create configmap my-config \
  --from-literal=APP_ENV=production \
  --from-literal=APP_PORT=8080
```

Yukarıdaki örnekte, `my-config` adıyla bir ConfigMap oluşturuluyor ve `APP_ENV` ile `APP_PORT` değerleri literal olarak ekleniyor.

### 2. Dosyadan ConfigMap Oluşturma

```bash
kubectl create configmap my-config-from-file \
  --from-file=app-config.yaml
```

`app-config.yaml` içinde uygulama ayarları yer alıyorsa, bu dosyayı direkt ConfigMap'e dönüştürebilirsiniz.

### 3. YAML Dosyası Kullanarak Oluşturma

```yaml:my-app/kubernetes/config-map.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-config
data:
  APP_ENV: production
  APP_PORT: "8080"
```

Daha sonra şu komutla deploy edebilirsiniz:

```bash
kubectl apply -f my-app/kubernetes/config-map.yaml
```

## ConfigMap Kullanımı

Pod veya Deployment manifest'inde, ConfigMap verilerini environment değişkeni veya dosya olarak kullanabilirsiniz.

### 1. Ortam Değişkeni Olarak Kullanım

```yaml:my-app/kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-app:latest
        env:
        - name: APP_ENV
          valueFrom:
            configMapKeyRef:
              name: my-config
              key: APP_ENV
        - name: APP_PORT
          valueFrom:
            configMapKeyRef:
              name: my-config
              key: APP_PORT
```

### 2. Dosya Olarak Kullanım (Volume Olarak Mount Etme)

```yaml:my-app/kubernetes/pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app-pod
spec:
  containers:
  - name: my-app
    image: my-app:latest
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
  volumes:
  - name: config-volume
    configMap:
      name: my-config
```

Yukarıdaki örnekte `my-config` içinde tanımlı anahtar-değer çiftleri, `/etc/config` dizini içerisine dosya olarak yansıtılacaktır.

## Özet

- **ConfigMap**, Kubernetes ortamında uygulama ayarlarını yönetmenin yaygın yoludur.  
- Verileri gizlemeye ihtiyaç yoksa (örneğin hassas olmayan konfigürasyonlar) ConfigMap kullanılabilir. Eğer şifrelenmiş veri veya gizli anahtarlar varsa Secret nesnesi seçilmelidir.  
- ConfigMap verilerini environment değişkeni veya volume (dosya) olarak Pod'lara ileterek, uygulamalarınızın konfigürasyonunu esnek ve ölçeklenebilir şekilde yönetebilirsiniz.

Bu temel bilgilerle ConfigMap nesnelerini rahatlıkla oluşturup kullanabilirsiniz. Daha fazla detay için [Kubernetes ConfigMaps Resmi Dokümanı](https://kubernetes.io/docs/concepts/configuration/configmap/) bağlantısını inceleyebilirsiniz. 