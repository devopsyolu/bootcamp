# Kubernetes Role ve RBAC (Role-Based Access Control) Nedir?

Kubernetes'te **RBAC (Role-Based Access Control)**, kaynaklara (Pod, Service, Deployment vb.) ve işlemlere (list, get, create, delete vb.) yönelik erişimi denetleyen bir güvenlik yaklaşımıdır. RBAC, kullanıcıların (User, ServiceAccount) veya grupların hangi işlemleri hangi kaynaklar üzerinde yapabileceklerini belirler.

---

## Özet Hatırlatma: Role, ClusterRole, RoleBinding, ClusterRoleBinding

- **Role** / **RoleBinding** → Namespace boyutunda yetki verir.  
- **ClusterRole** / **ClusterRoleBinding** → Küme çapında yetki verir.  
- **ServiceAccount** → Pod'ların Kubernetes API istekleri yapması için kullandığı öntanımlı hesaplar.  
- **User / Group** → Dış kimlik doğrulama yöntemi (LDAP/SSO/Certificates/IAM) veya kubeconfig ile tanımlanan kimlikler.

Daha önce Role, RoleBinding ve benzeri YAML örneklerini anlatmıştık. Şimdi **AWS EKS** ve **Minikube** ortamlarında User/Group yönetimi nasıl yapılır, ona değinelim.

---

## AWS EKS Ortamında Kullanıcı / Grup Yönetimi

AWS EKS'de Kubernetes, **IAM** (Identity and Access Management) servisinin rollerini ve kullanıcılarını tanıyabilmek için bir **mapping** (eşleştirme) sistemine sahiptir. EKS kontrol düzlemi, kube-apiserver kimin hangi eylemleri yapabileceğini belirlerken **aws-auth** ConfigMap'i kullanarak IAM entity → RBAC nesneleri arasında ilişki kurar.

### 1. aws-auth ConfigMap

EKS oluşturduğunuzda, varsayılan olarak bir IAM user/role (Cluster Creator) "system:masters" yetkisine sahip olur. Diğer kullanıcıların eklenmesi için, EKS Worker Node'ların yer aldığı namespace'te (genellikle `kube-system`) "aws-auth" adlı bir ConfigMap mevcuttur.

ConfigMap'te tipik bir yapı şöyledir (kısaltılmış örnek):

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: aws-auth
  namespace: kube-system
data:
  mapRoles: |
    - rolearn: arn:aws:iam::111122223333:role/EKS-NodeInstanceRole
      username: system:node:{{EC2PrivateDNSName}}
      groups:
        - system:bootstrappers
        - system:nodes
    - rolearn: arn:aws:iam::111122223333:role/DevOpsAdmin
      username: devops-admin
      groups:
        - system:masters
  mapUsers: |
    - userarn: arn:aws:iam::111122223333:user/john@example.com
      username: john
      groups:
        - eks-developers
```

Açıklamalar:  
- **mapRoles** → IAM **Role** ARN'lerini Kubernetes gruplarıyla (ör. `system:masters`, `system:nodes`) ve `username` özellikleriyle eşleştirir.  
- **mapUsers** → IAM **User** ARN'lerini Kubernetes içinde "username" ve "groups" atamalarıyla ilişkilendirir.

Kullanıcının AWS IAM tarafında kimlik doğrulaması başarılı olunca, EKS "aws-auth" ConfigMap'e bakarak o kullanıcıya (veya role) hangi grup(lar) verilmiş, öğrenir. Ardından RBAC kurallarında (RoleBinding vb.) bu gruplarla ilişkili yetkileri uygular.  

> **Not**: "system:masters" grubuna atananlar cluster-admin seviyesinde tam yetki kazanırlar. Üretim ortamında çok dikkatli yönetilmesi gerekir.

### 2. RBAC Nesneleri ile Tamamlamak

Yukarıda eklenen "john" adlı kullanıcı, "eks-developers" grubunda. Kubernetes'te kendisine şu şekilde bir RoleBinding yapabilirsiniz:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: dev-binding
  namespace: dev-namespace
subjects:
  - kind: Group
    name: eks-developers
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

Böylece "eks-developers" grubundaki herkes (john da dahil) `pod-reader` rolünün izinlerini kullanabilir.  

### Kullanıcının Erişimi / Kubeconfig

- AWS CLI (veya "aws-iam-authenticator") kullanarak EKS cluster'a bağlanabilirsiniz.  
- `aws eks update-kubeconfig --name <cluster-name> --region <region>` komutu ile "~/.kube/config" otomatik güncellenir.  
- Gelen isteklerde IAM rolu/kullanıcısı kube-apiserver'a iletilir -> "aws-auth" ConfigMap ile eşleştirme -> RBAC policy uygulanır.

---

## Minikube Ortamında Kullanıcı / Grup Yönetimi

Minikube, lokal bir Kubernetes kümesi oluşturur ve **varsayılan** ayarlarda tek bir kullanıcı (kubeconfig'de cluster-admin) ile kullanılır. Ancak ek kullanıcılar oluşturmak ve test amacıyla RBAC senaryoları deneyimlemek mümkündür.

### 1. X.509 Sertifikası ile Ek Kullanıcı Oluşturma (Örnek)

Bir yaklaşım, **Client Certificate** oluşturarak minikube apiserver'ında doğrulamaktır:

1. **Key ve CSR Oluşturma**  
   ```bash
   openssl genrsa -out devuser.key 2048
   openssl req -new -key devuser.key -out devuser.csr \
     -subj "/CN=dev-user/O=dev-group"
   ```

   - `CN=dev-user` → Kullanıcı adı  
   - `O=dev-group` → Grup adı (opsiyonel, `_O_` ile tek bir grup gibi düşünebilirsiniz)

2. **CA (minikube CA) İle CSR'yi İmzalama**  
   - Minikube, bir yerel CA'ya sahiptir. Onunla bu CSR'yi imzalayacağız.  
   - Minikube CA sertifikasını (ca.crt / ca.key) bulmanız veya minikube CLI ile imzalamanız gerekebilir. Bir yöntem:
     ```bash
     sudo cp ~/.minikube/ca.crt ~/my-ca.crt
     sudo cp ~/.minikube/ca.key ~/my-ca.key
     openssl x509 -req -in devuser.csr -CA my-ca.crt -CAkey my-ca.key \
       -CAcreateserial -out devuser.crt -days 365
     ```
3. **Kubeconfig Güncelleme**  
   ```bash
   kubectl config set-credentials dev-user \
       --client-certificate=devuser.crt \
       --client-key=devuser.key
   kubectl config set-context dev-user-context \
       --cluster=minikube \
       --namespace=dev-namespace \
       --user=dev-user
   ```
   > Artık `kubectl --context=dev-user-context get pods` komutu "dev-user" kimliğiyle sorgu yapar.

4. **RBAC Policy Uygulamak**  
   - `Role` / `RoleBinding` oluşturabilir, "dev-user" adını `subjects` alanında kullanarak izinleri kısıtlayabilirsiniz.  
   - Örnek bir RoleBinding (benzer):
     ```yaml
     apiVersion: rbac.authorization.k8s.io/v1
     kind: RoleBinding
     metadata:
       name: dev-binding
       namespace: dev-namespace
     subjects:
       - kind: User
         name: dev-user
         apiGroup: rbac.authorization.k8s.io
     roleRef:
       kind: Role
       name: pod-reader
       apiGroup: rbac.authorization.k8s.io
     ```

### 2. Basit OIDC / Token Yaklaşımı

Minikube'de kimlik yönetimi genellikle test/demolar için sertifika yoluyla yapılır. İsterseniz [dex](https://github.com/dexidp/dex) gibi bir kimlik sağlayıcı (OIDC) kurup minikube ile entegre etmeniz de mümkündür, ancak bu tipik demolar dışında daha gelişmiş bir konfigürasyon gerektirir.

---

## Sonuç

- **AWS EKS** → Kullanıcı/grup tanımları, **IAM** + "aws-auth" ConfigMap eşleştirmesiyle yapılır. IAM user veya role, `mapUsers` / `mapRoles` alanları sayesinde Kubernetes'te belli kullanıcı/gruplarla eşleşir ve RBAC devreye girer.  
- **Minikube** → Varsayılan tek kullanıcı (kubeconfig'de cluster-admin). Ek kullanıcı / grup oluşturmak için en yaygın yol, **x.509 sertifikaları** veya benzer kimlik doğrulama mekanizmalarıdır. RBAC Role/RoleBinding ile yetkiler kısıtlanabilir.

Bu yaklaşımlarla, farklı ortamlarda (lokal veya bulut) **Kubernetes User/Group** yönetimini gerçekleştirip RBAC prensiplerini uygulayabilirsiniz.
