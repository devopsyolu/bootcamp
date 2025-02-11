# Kubernetes Pod Nedir?

**Pod**, Kubernetes'in en küçük ve temel uygulama çalıştırma birimidir. Bir veya birden fazla konteyneri (container) çalıştıran **mantıksal** bir birim olarak düşünülebilir. Aynı Pod içindeki konteynerler, ağ kaynaklarını (IP adresi, portlar) ve dosya sisteminin bazı kısımlarını (volume, config dosyaları gibi) paylaşır.

## Pod'un Temel Özellikleri

1. **Tekil IP Adresi**  
   Kubernetes, her Pod'a tekil bir IP atar. Pod içindeki tüm konteynerler bu IP adresini ve ağ arabirimini paylaşır. Konteynerler arası iletişim, localhost (127.0.0.1) üzerinden sağlanarak basitleştirilir.

2. **Kısa Ömürlüdür**  
   Pod'lar kalıcı olmaya yönelik tasarlanmamıştır. Uygulamanızın ölçeklenmesi, yeniden başlatılması veya node arızaları gibi durumlarda Pod'lar yeniden oluşturulabilir. Kalıcı veriler veya durum bilgisi gerekiyorsa ek olarak PersistentVolumeClaim vb. çözümlerle entegre edilmesi gerekir.

3. **Çoklu Konteyner Desteği**  
   Tek bir Pod içerisinde birden fazla konteyner çalışabilir. Bu konteynerler, ortak bir amaç için birlikte çalışırken kaynaklarını ve volume, network gibi yapılarını paylaşırlar. "Sidecar" kullanımı bu yaklaşımın bir örneğidir (örn. bir ana uygulama konteyneri ve log toplayan yardımcı konteyner).

4. **Volume Paylaşımı**  
   Aynı Pod içindeki konteynerler **volume**'ları paylaşabilir. Örneğin, web uygulaması Pod'unda bir konteyner, kullanıcıların yüklediği dosyaları bir volume içine kaydederken, ikinci bir konteyner bu verileri işleyebilir.

5. **Yaşam Döngüsü Yönetimi**  
   Pod yaşam döngüsü, örneğin:
   - **Init Container**: Ön hazırlıklar (örn. config dosyasını indirmek).  
   - **Running**: Ana uygulamanın çalışması.  
   - **Termination**: Pod'un kapanması.  
   Kubernetes, her adımın sırasını ve sağlık durumunu denetler.

---

## Pod Tanımlama Örneği

Aşağıdaki örnekte, tek bir Nginx konteyneri çalıştıran basit bir Pod tanımlaması yer almaktadır:

```
apiVersion: v1
kind: Pod
metadata:
  name: my-nginx
  labels:
    app: web
spec:
  containers:
  - name: nginx-container
    image: nginx:latest
    ports:
    - containerPort: 80
```

1. **apiVersion: v1 & kind: Pod**  
   Kaynağın bir Pod olduğunu belirtir.
2. **metadata.name: my-nginx**  
   Pod'a atanan isim.
3. **labels: app: web**  
   Pod'a eklenmiş etiket; örneğin serviste veya ReplicaSet'te kullanılabilir.
4. **spec.containers**  
   Pod içindeki konteynerleri listeler. Bu örnekte tek bir **nginx** konteyneri çalıştırılır.

---

## Pod'un Oluşturulması ve Yönetimi

- **Oluşturma**:  
  ```bash
  kubectl apply -f my-nginx-pod.yaml
  ```
- **Durumu Görme**:  
  ```bash
  kubectl get pods
  kubectl describe pod my-nginx
  ```
- **Pod'a Erişim**:  
  ```bash
  kubectl port-forward pod/my-nginx 8080:80
  ```
  Bu sayede localhost:8080 üstünden container içindeki nginx sunucusuna erişebilirsiniz.
- **Pod Silme**:  
  ```bash
  kubectl delete pod my-nginx
  ```

---

## Pod Kullanım Alanları

- **Basit Denemeler**: Yeni bir imaj test ederken veya geçici kısa süreli görevler çalıştırırken.  
- **Init Container**: Uygulamanın başlamasından önce yapılandırma, dosya kopyalama vb. adımlar için.  
- **Yan Hizmet (Sidecar) Konteynerler**: Log işleme, proxy, metrik toplama gibi ek işlevler bir ana uygulama konteyneriyle aynı Pod içerisinde konumlanabilir.

---

## Sonuç

Kubernetess'te **Pod**, bir veya birden fazla konteynerin bir arada **aynı mantıksal birim** içinde çalıştırıldığı en temel yönetim nesnesidir. Uygulamalar genellikle **ReplicaSet** veya **Deployment** gibi daha üst düzey bileşenlerle ölçeklenir ve yönetilir; ancak temelinde her şey Pod olarak yaşam döngüsünü sürdürür.
