# Kubernetes'e Başlangıç

Bu rehber, yerel bir Kubernetes kümesi oluşturmak ve basit bir uygulama dağıtmak için adım adım Minikube kullanımını anlatmaktadır.

## Ön Gereksinimler
- **Minikube:** [Minikube Kurulumu](https://minikube.sigs.k8s.io/docs/start/)
- **kubectl:** [kubectl Kurulumu](https://kubernetes.io/docs/tasks/tools/)

## Minikube ile Küme Başlatma
1. Minikube'u sisteminize kurun.
2. Kümenizi başlatın:
   ```bash
   minikube start
   ```

## Basit Bir Uygulama Dağıtımı
1. Bir deployment oluşturun:
   ```bash
   kubectl create deployment nginx --image=nginx
   ```
2. Deployment'ı bir servis ile dış dünyaya açın:
   ```bash
   kubectl expose deployment nginx --port=80 --type=NodePort
   ```
3. Servis URL'sini alın:
   ```bash
   minikube service nginx --url
   ```

## İleri Düzey Kaynaklar
- [Kubernetes Resmi Dokümantasyonu](https://kubernetes.io/docs/)
- [Kubernetes Başlangıç Rehberi](https://kubernetes.io/docs/tutorials/kubernetes-basics/)

Bu adımları izleyerek Kubernetes'in temel özelliklerini deneyimleyebilir ve daha ileri konulara geçiş yapabilirsiniz. 