# Kubernetes Role ve RBAC (Role-Based Access Control) Nedir?

Kubernetes'te **RBAC (Role-Based Access Control)**, kaynaklara (Pod, Service, Deployment vb.) ve işlemlere (list, get, create, delete vb.) yönelik erişim denetimini düzenleyen bir güvenlik yaklaşımıdır. RBAC, kullanıcıların (user, serviceaccount) veya grupların hangi işlemleri hangi kaynaklar üzerinde yapabileceklerini belirler.

---

## Temel Kavramlar

1. **Role**  
   - Belirli bir **namespace** içinde kaynaklara dosya erişim düzeyini tanımlar.  
   - Örneğin, Pod'lar üzerinde "get", "list", "watch" yapabilen ama "create" veya "delete" yapamayan bir Role oluşturabiliriz.

2. **ClusterRole**  
   - Tüm küme (cluster) genelinde veya namespace bağımsız işlem izni tanımlar.  
   - Örneğin, bir kullanıcıya tüm namespace'lerde Pod listeleme yetkisi verilebilir.

3. **RoleBinding**  
   - Role'ü bir kullanıcı veya gruba (ya da serviceaccount'a) **bağlar** (bind). Böylece o kullanıcı, söz konusu namespace içindeki kaynaklara Role'ün verdiği yetkiler doğrultusunda erişebilir.

4. **ClusterRoleBinding**  
   - ClusterRole'ü kullanıcı veya gruba (ya da serviceaccount'a) **küme genelinde** bağlar. Yani bu binding, cluster genelinde geçerli olur.

5. **User, Group, ServiceAccount**  
   - **User**: Kurumsal kimlik (LDAP/SSO) veya client certificate, OIDC token vb. yoluyla tanımlanır.  
   - **Group**: Birden çok kullanıcıyı ortak haklarla yönetmek için kullanılır.  
   - **ServiceAccount**: Kubernetes içindeki **Pod'ların** kimlik doğrulama (auth) yapabilmesi ve API istekleri yapmaya yetki kazanması için kullanılan hesap türüdür.

> **Not**: Kubernetes "User" yönetimini kendi iç mekanizmalarıyla doğrudan yapmaz. Genellikle PKI sertifikaları, OIDC, LDAP, SSO vb. entegre edilir. Demo/sade örneklerde genellikle `ServiceAccount` veya basit sertifikalar kullanılır.

---

## Örnek: Namespace İçinde Role ve RoleBinding

Aşağıdaki örnek, "dev-namespace" adlı bir namespace içindeki Pod'lar üzerinde belirli işlemlere (get, list, watch) izin veren bir **Role** tanımlar. Ardından bu Role'ü "dev-user" adlı bir kullanıcıya bağlamak için **RoleBinding** oluşturur.

### 1. Role Tanımı

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: dev-namespace
rules:
  - apiGroups: [""]          # core API group (Pod vb.)
    resources: ["pods"]      # hedef kaynak (pod)
    verbs: ["get","list","watch"]  # izin verilen işlemler
```

Açıklamalar:  
- `apiGroups: [""]` → Core API'deki (v1) kaynakları ifade eder.  
- `resources: ["pods"]` → Sadece Pod kaynağını hedef alıyor.  
- `verbs: ["get","list","watch"]` → Kullanıcının bu Pod'ları görebilmesi (okuma izni) sağlanıyor.

### 2. RoleBinding Tanımı

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: pod-reader-binding
  namespace: dev-namespace
subjects:
  - kind: User
    name: dev-user              # "dev-user" adlı kullanıcı
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

Açıklamalar:  
- `subjects` bölümü → Bu Role kiminle ilişkilendirilecekse onu belirtir (User, Group, ServiceAccount).  
- `roleRef` → Yukarıda tanımlanan `pod-reader` adlı Role'e atıfta bulunur.

> Komutlar:  
> ```bash
> kubectl apply -f pod-reader-role.yaml
> kubectl apply -f pod-reader-binding.yaml
> ```
> Ardından `dev-user`, "dev-namespace" içinde yalnızca Pod'ları okuyabilir (get/list/watch).

---

## Örnek: ClusterRole ve ClusterRoleBinding

Küme genelinde (tüm namespace'lerde) **Deployment** kaynaklarını güncelleme (update) yetkisi sağlamak isteyelim.

### 1. ClusterRole Tanımı

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: deployment-updater
rules:
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get","watch","list","update"]
```

Açıklamalar:  
- `apiGroups: ["apps"]` → Deployments kaynağının bulunduğu API group.  
- `resources: ["deployments"]` → Hedef kaynak türü.  
- `verbs: ["get","watch","list","update"]` → Bu işlemlerin tüm namespace'lerde yapılmasına izin verilecek.

### 2. ClusterRoleBinding Tanımı

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: deployment-updater-binding
subjects:
  - kind: User
    name: tom@company.com        # E-posta veya kimlik doğrulaması bu şekilde olabilir
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: deployment-updater
  apiGroup: rbac.authorization.k8s.io
```

Bunun sonucu olarak "tom@company.com" adlı kullanıcı, küme genelindeki tüm namespace'lerde Deployment kaynaklarını görüntüleyebilir ve güncelleyebilir. Ancak **silme veya oluşturma** iznine sahip olmaz, çünkü `verbs'te "delete" veya "create" yoktur.

> Komutlar:  
> ```bash
> kubectl apply -f deployment-updater-clusterrole.yaml
> kubectl apply -f deployment-updater-binding.yaml
> ```

---

## Örnek: ServiceAccount ile RoleBinding

Kimi zaman bir uygulama (Pod) içinden Kubernetes API'si çağrısı yapılması gerekir. Böyle bir durumda **ServiceAccount** tanımlarız.

### 1. ServiceAccount Oluşturma

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-service-account
  namespace: dev-namespace
```

### 2. RoleBinding Yapısı

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: sa-binding
  namespace: dev-namespace
subjects:
  - kind: ServiceAccount
    name: my-service-account   # Yukarıda oluşturduğumuz ServiceAccount
    namespace: dev-namespace
roleRef:
  kind: Role
  name: pod-reader            # Mevcut Role (örnek)
  apiGroup: rbac.authorization.k8s.io
```

Bu şekilde Pod, "my-service-account" ile çalıştırılırsa, "dev-namespace" içindeki Pod'ları `get/list/watch` edebilir. Örneğin YAML'daki Pod spec:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
  namespace: dev-namespace
spec:
  serviceAccountName: my-service-account
  containers:
    - name: main
      image: alpine
      command: ["/bin/sh","-c","sleep 3600"]
```

> Bu Pod içinden `kubectl get pods -n dev-namespace` (veya API çağrılarının eşdeğerini) yapabilirsiniz. Yetkiler "pod-reader" Rolleriyle sınırlı olacağından diğer kaynaklara erişimi olmaz.

---

## Kullanıcı (User) Oluşturma Notları

- Kubernetes yerleşik bir kullanıcı yönetimi sunmaz.  
- Genellikle PKI sertifikası, OIDC, Active Directory/LDAP veya benzeri kimlik sağlayıcılar entegre edilir.  
- Lab/demolar için bazen "kubeconfig" üzerinde sertifika veya token'lar manuel oluşturularak "user1," "user2" gibi adlar verilir.  
- "kind: ServiceAccount" ise ekteki Pod vs. senaryoları için Kubernetes içi kimliklerdir.

---

## Özet

**RBAC (Role-Based Access Control)**, Kubernetes'te **kim** (user, group, serviceaccount) **hangi işlem(ler)i** (verbs: get, list, create, delete vb.) **hangi kaynak(lar)** (pods, deployments, secrets vb.) **hangi scope'da** (namespace veya cluster genelinde) yapabilir sorusuna ince ayar yapmayı sağlar.

- **Role** ve **RoleBinding**: Namespace düzeyi izni kısıtlamak için ideal.  
- **ClusterRole** ve **ClusterRoleBinding**: Küme genelinde yetki vermek için kullanılır.  
- **ServiceAccount**: Pod'ların Kubernetes API ile iletişim kurması için kullanılan hesaplardır.

Doğru RBAC planlaması, güvenli ve düzenli bir Kubernetes kullanımı için **hayati** öneme sahiptir. 