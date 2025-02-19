# Kubernetes'de Pod Otomatik Ölçeklendirme (Autoscaling)

Kubernetes, uygulamalarınızın değişen yüklerle başa çıkabilmesi için otomatik ölçeklendirme yetenekleri sunar. Pod otomatik ölçeklendirme, uygulamanızın kaynak kullanımına bağlı olarak pod sayısını dinamik olarak ayarlar. Bu, uygulamanızın performansını optimize ederken aynı zamanda kaynak kullanımını da verimli hale getirir.

## Horizontal Pod Autoscaler (HPA)

Kubernetes'te en yaygın kullanılan otomatik ölçeklendirme mekanizması **Horizontal Pod Autoscaler (HPA)**'dır. HPA, pod sayısını CPU kullanımı, bellek kullanımı veya özel metriklere göre otomatik olarak artırır veya azaltır.

### HPA'nın Çalışma Prensibi

- **Metrik Toplama**: HPA, Kubernetes Metrics Server üzerinden metrikleri toplar.
- **Ölçeklendirme Kararı**: Toplanan metrikler, önceden belirlenen hedeflere göre değerlendirilir.
- **Uygulama**: Gerekli görüldüğünde pod sayısı artırılır veya azaltılır.

## HPA Nasıl Kurulur?

### 1. Metrics Server Kurulumu

HPA'nın çalışabilmesi için kümede Metrics Server'ın kurulu olması gerekir.

```bash
# Metrics Server kurulumu
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

### 2. Uygulama (Deployment) Oluşturma

Örnek olarak basit bir Nginx deployment oluşturabiliriz.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 1 # Başlangıçta 1 pod
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
        resources:
          requests:
            cpu: 100m
          limits:
            cpu: 500m
```

### 3. HPA Kaynağı Oluşturma

Şimdi HPA tanımını oluşturabiliriz.

```yaml
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: nginx-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nginx-deployment
  minReplicas: 1
  maxReplicas: 10
  targetCPUUtilizationPercentage: 50
```

Bu tanım, CPU kullanımı %50'nin üzerine çıktığında pod sayısını otomatik olarak artıracaktır.

### 4. Kaynakları Uygulama

Oluşturduğumuz deployment ve HPA tanımlarını kümede uygulayalım.

```bash
kubectl apply -f deployment.yaml
kubectl apply -f hpa.yaml
```

### 5. HPA Durumunu İzleme

HPA'nın durumunu ve metriklerini görüntülemek için:

```bash
kubectl get hpa
```

## Örnek: Yük Testi ile HPA'yı Test Etme

Pod'ların otomatik ölçeklenmesini gözlemlemek için yük testi yapabiliriz.

```bash
# Yeni bir pod oluşturup içine girelim
kubectl run -i --tty load-generator --image=busybox /bin/sh

# İçeride aşağıdaki komutla sürekli istek gönderelim
while true; do wget -q -O- http://nginx-service; done
```