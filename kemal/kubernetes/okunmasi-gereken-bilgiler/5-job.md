# Kubernetes Job Nedir?

**Job**, Kubernetes'te *batch* veya *tek seferlik* (one-time) iş yüklerini çalıştırmak için kullanılan bir nesnedir. Bir Job, belirlenen sayıdaki Pod'un başarıyla tamamlanmasını garanti eder. Süreç tamamlandığında Job da sonlanır. Özellikle, kısa süreli veya planlı olarak tek seferlik işlemleri (örn. veri migrasyonu, batch raporlama, yedekleme) yürütmek için idealdir.

## Job Özellikleri

1. **Completions**  
   - `spec.completions`, kaç adet başarılı Pod tamamlanmasının gereken toplam işi temsil ettiğini belirler. Örneğin `completions: 3` ile her biri başarılı şekilde biten 3 Pod, Job'un tamamlandığını ifade eder.

2. **Parallelism**  
   - `spec.parallelism`, aynı anda çalışan Pod sayısını belirler. Örneğin `parallelism: 2`, aynı anda 2 Pod'un çalışacağını, diğer Pod'ların ise bu ikisi tamamlandıkça sırasıyla devreye gireceğini gösterir.

3. **RestartPolicy**  
   - Job Pod'lar genellikle `restartPolicy: Never` veya `restartPolicy: OnFailure` ile çalıştırılır. Bir Pod başarısız olursa, Kubernetes yeni bir Pod oluşturarak Job'un tamamlanmasını sağlar. Mevcut Pod ise tekrar başlatılmaz.

4. **Tek Seferlik Görevler**  
   - Job tamamlandıktan sonra Pod'lar silinebilir veya logları saklanabilir. Bu mekanizma sürekli çalışan sunucu uygulamalar (Deployment, StatefulSet) yerine tek seferlik iş ve batch senaryolarında tercih edilir.

5. **Backoff Limit**  
   - `spec.backoffLimit`, Pod'lar ardışık şekilde hataya düşerse Job'un yeni yeniden deneme (retry) girişimlerini kaç kez yapacağını kontrol eder. Örneğin `backoffLimit: 4` ile 4 kez yeniden deneme yapıldıktan sonra Job hata olarak işaretlenebilir.

---

## Örnek Job Manifest Dosyası

Aşağıdaki örnek, tek seferlik bir komut çalıştıran Job tanımını göstermektedir:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: example-job
spec:
  parallelism: 1       # Aynı anda çalışan Pod sayısı
  completions: 1       # Toplam başarıyla tamamlanması gereken Pod sayısı
  backoffLimit: 4      # Başarısızlık durumunda en fazla kaç kez yeniden deneme
  template:
    metadata:
      name: example-job-pod
    spec:
      restartPolicy: Never
      containers:
      - name: busybox
        image: busybox:latest
        command: ["echo", "Merhaba, bu bir Job örneğidir"]
```

1. **`parallelism: 1`**  
   Job aynı anda sadece 1 Pod çalıştırır.  

2. **`completions: 1`**  
   Başarıyla tamamlanması gereken Pod sayısı 1 olarak belirlenmiştir. Pod başarılı olduğunda Job da tamamlanmış sayılır.

3. **`backoffLimit: 4`**  
   İş (Pod) başarısız olursa, toplamda 4 kez yeniden denenir.  

4. **`restartPolicy: Never`**  
   Pod başarısız olursa tekrar başlatılmak yerine yeni bir Pod oluşturulur.

---

## Job Komutlarına Örnekler

- **Oluşturma / Güncelleme**:  
  ```bash
  kubectl apply -f job.yaml
  ```

- **Durumu Görüntüleme**:  
  ```bash
  kubectl get jobs
  kubectl describe job example-job
  ```

- **Pod Çıkış Logları**:  
  ```bash
  kubectl logs <job-pod-ismi>
  ```

- **Silme**:  
  ```bash
  kubectl delete job example-job
  ```

---

## CronJob (Süreklilik) İlişkisi

Eğer Job'un düzenli zaman aralıklarıyla (örn. her gece saat 02.00'de) çalışması gerekiyorsa **CronJob** nesnesi tercih edilir. CronJob, Job'u belirlenen cron zamanlama ifadesine göre periyodik olarak tetikler.

---

## Sonuç

**Job**, Kubernetes'in *batch* veya tek seferlik iş senaryolarına getirdiği çözümdür. Belirli bir sayıda Pod başarılı olduktan sonra tamamlanması ve kümedeki yeniden deneme mekanizması gibi özellikleriyle, *stateless* ve kısa süreli görevler için idealdir. Daha ileri, zamanlanmış görevler için de **CronJob** devreye girer.
