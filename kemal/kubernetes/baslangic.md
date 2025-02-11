

# Kubernetes Cluster Kurma Yöntemleri

Bu dokümanda Kubernetes kümesini (cluster) kurmak için birkaç farklı yaklaşımı inceleyeceğiz.  
1) Yerel (lokal) ortamlarda öğrenme ve geliştirme amaçlı kullanılan Minikube.  
2) Üretim/gerçek ortamlar için "self-managed (kendi kendine barındırılan)" Kubernetes kurulumu.  

Aşağıdaki adımları **adım adım** takip edebilir veya kendi senaryonuza uygun bölümleri uygulayabilirsiniz.

---

## 1. Minikube Kurulumu

[Minikube](https://minikube.sigs.k8s.io/docs/start/) özellikle geliştiriciler ve Kubernetes'e yeni başlayanlar için tasarlanmış bir araçtır. Tek bir makinede (sanal veya fiziksel) **Minikube** çalıştırarak:

- Kubernetes Control Plane + Worker Node'u tek bir Node içerisinde deneyimleyebilirsiniz.  
- Kendi makinenizde basit bir küme oluşturup pratik yapabilirsiniz.

### 1.1 Ön Gereksinimler

- Sanal makine (VM) oluşturma özelliği (VirtualBox, Docker, Hyper-V vb.)  
- Kubectl (Kubernetes komut satırı aracı)

### 1.2 Minikube Kurma

Aşağıda örnek olarak Linux ortamında Minikube nasıl kurulur (diğer platformlar için resmi dokümantasyona bakabilirsiniz):

1) Kubectl kurulumu (eğer yoksa):
    
    curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"

    chmod +x kubectl
    sudo mv kubectl /usr/local/bin/

2) Minikube kurulumu:
    
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo install minikube-linux-amd64 /usr/local/bin/minikube

### 1.3 Minikube ile Küme Başlatma

1) Basit bir küme başlatmak:
    
    minikube start

2) Özelleştirilmiş kaynaklarla başlatmak (örneğin 2 vCPU, 4GB RAM):
    
    minikube start --cpus=2 --memory=4096

3) Kümenin durumunu görmek:
    
    minikube status

4) Kümenin durdurulması ve silinmesi:
    
    minikube stop
    minikube delete

> Not: Minikube, varsayılan olarak tek bir Node (hepsi bir arada) oluşturur. Gelişmiş testler için MULTI-NODE Minikube da etkinleştirilebilir (örneğin: --nodes 2).

### 1.4 Minikube ile Uygulama Dağıtma Örneği

1) Örnek bir Nginx Deployment oluşturun:
    
    kubectl create deployment nginx --image=nginx

2) Servisi, NodePort türüyle oluşturun:
    
    kubectl expose deployment nginx --port=80 --type=NodePort

3) Uygulamaya tarayıcıdan erişmek için:
    
    minikube service nginx --url

Böylece Minikube üzerinde ilk Kubernetes uygulamanızı çalıştırmış oldunuz.

---

## 2. Self-Hosted (Kendi Kendine) Kubernetes Kurulumu

Geniş ölçekli veya **üretim** ortamında Kubernetes kurmak için çeşitli yöntemler vardır. Bu kısımda, bir **sanal makine kümesi** (VM'ler) üzerinde "kubeadm" komutuyla temel bir kurulum örneği paylaşılır. Bu yöntem "bare-metal" (fiziksel makineler) veya "private cloud" (OpenStack, VMware vb.) platformlarda da benzer şekilde işleyecektir.

### 2.1 Mimari ve Gereksinimler

- Kontrol düzlemi (Master Node) ve Worker Node'lar için ayrı makineler veya VM'ler ayarlayın.  
- Her Node üzerinde en az 2 CPU, 2GB RAM (daha fazlası önerilir) ve internet bağlantısı olmalı.  
- Linux dağıtımı (Ubuntu, CentOS vb.) kullanabilirsiniz.  
- Her Node'da "container runtime" (containerd, Docker veya CRI-O) kurulu olmalı.

### 2.2 Adım Adım Kurulum (kubeadm)

Aşağıdaki adımlar örnek olarak Ubuntu (≥ 20.04) üzerinde gösterilmektedir.

#### 2.2.1 Ortam Hazırlığı

1) Makine (veya VM) güncellemeleri:

    sudo apt update
    sudo apt upgrade -y

2) Docker veya containerd kurulumu (örnek Docker):

    sudo apt install docker.io -y
    sudo systemctl enable docker
    sudo systemctl start docker

3) swap devre dışı bırakılması (Kubernetes swap'i sevmez):

    sudo swapoff -a
    # /etc/fstab içinde swap satırını yorum satırı (#) yaparak yeniden başlattığınızda da swap açılmasın.

4) sysctl ayarları (net.bridge vs.):

    cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
    br_netfilter
    EOF

    cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf 
    net.bridge.bridge-nf-call-ip6tables = 1
    net.bridge.bridge-nf-call-iptables = 1
    EOF

    sudo sysctl --system

#### 2.2.2 kubeadm, kubelet, kubectl Kurulumu

1) Kubernetes paket deposunu ekleme:

    curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
    sudo apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-xenial main"

2) Paketlerin yüklenmesi:

    sudo apt update
    sudo apt install -y kubeadm kubelet kubectl

3) kubelet servisini etkinleştirme:

    sudo systemctl enable kubelet

#### 2.2.3 Kontrol Düzlemi (Master Node) Kurulumu

Bu adımlar **Master** olarak konumlandırmak istediğiniz makinede/VM'de yapılır.

1) kubeadm init komutu:

    sudo kubeadm init --pod-network-cidr=10.244.0.0/16

    # --pod-network-cidr Flannel gibi ağ eklentisi (CNI) kullanılacaksa tipik olarak 10.244.0.0/16 atanır.
    # Komut başarıyla biterse size "kubeadm join" komutuyla Worker Node ekleme talimatı verecektir.

2) Kubectl konfigürasyonu ayarlama:

    mkdir -p $HOME/.kube
    sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
    sudo chown $(id -u):$(id -g) $HOME/.kube/config

3) Pod network (CNI) eklentisi yükleme (ör. Flannel):

    kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml

    # Başka CNI'ler (Calico, Weave Net vb.) de kullanılabilir.

#### 2.2.4 Worker Node'ların Eklenmesi

1) Worker Node VM/makinelerinde de "kubeadm, kubelet, kubectl" paketlerini aynı yöntemle yükleyin.  
2) Master Node'daki kurulum tamamlandığında size bir `kubeadm join ...` komutu vermiş olacaktır. Bunu Worker Node üzerinde çalıştırın:

    sudo kubeadm join <master-ip>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>

3) Worker Node katıldıktan sonra Master Node'da:

    kubectl get nodes

    # Worker Node'ların "Ready" durumda olup olmadığını kontrol edin.

#### 2.2.5 Başarılı Kurulum Kontrolü

- "kubectl get pods -A" komutu ile tüm namespace'lerdeki Pod'lara bakın. CNI eklentisi, CoreDNS, kube-proxy vb. bileşenler çalışıyor mu?  
- "kubectl get nodes" ile Worker Node'lar Ready mi?  
- Artık uygulamalarınızı Deploy / Service / Ingress vb. nesneler ile dağıtmaya başlayabilirsiniz.

---

## 3. Diğer Seçenekler ve Özet

- **Kops, Kubespray vb.** → AWS veya diğer bulut ortamlarda üretim düzeyinde Kubernetes kurmaya yarayan komut satırı araçları.  
- **Managed Kubernetes** → AWS EKS, GCP GKE, Azure AKS gibi bulut sağlayıcılarının yönetilen (managed) Kubernetes çözümleri. Kendi kontrol düzlemiyle uğraşmaz, yalnızca Worker Node'ları yönetirsiniz.  

### Özet

1. **Minikube** → Öğrenme, yerel test ve demosu için ideal. Tek komutla cluster başlatıp durdurma kolaylığı sunar.  
2. **Self-Hosted** (kubeadm) → Üretim veya şirket içi ortamlarda, kendi clusterınızı tamamen yönetmeniz gerektiğinde kullanılır. Adım adım kurulum, Master + Worker Node ayrımı, ağ eklentileri (CNI), RBAC ve monitörleme gibi konuları sizin konfigüre etmeniz gerekir.  
3. **Managed Kubernetes** → Bulut sağlayıcınız altyapıyı sunar, siz sadece iş yüklerinizi deploy edersiniz.

Bu rehberle hem Minikube (lokal ortam) hem de kubeadm (self-managed) kurulum hakkında temel bir fikir sahibi olabilirsiniz. Mimariniz ve gereksinimleriniz doğrultusunda size en uygun yöntemi seçebilir, **Kubernetes** ekosistemindeki diğer araçların (Helm, Kustomize, vs.) yardımıyla işinizi daha da kolaylaştırabilirsiniz. 