# Kubernetes CronJob Nedir?

**CronJob**, Kubernetes üzerinde belirli zaman aralıklarında veya cron formatına uygun bir takvimde tekrarlı görevler (Job'lar) çalıştırmak için kullanılan bir nesnedir. Örneğin, her gün saat 02:00'de yedekleme almak veya saat başı log arşivlemek. CronJob, Kubernetes'in Job yapısını kullanarak periyodik iş planlamasını sağlar.

---

## CronJob Özellikleri

1. **Zaman Planlaması (Cron FORMAT)**  
   - `spec.schedule` alanında kullanılan cron benzeri zamanlama ifadesi, periyodik görevlerin hangi sıklıkla tetikleneceğini belirler.  
   - Örneğin `"0 2 * * *"` ifadesi, her gün saat 02:00'de tetiklenen bir işi belirtir.

2. **Job Şablonu**  
   - `spec.jobTemplate`, nasıl bir Job oluşturulacağını tarif eder.  
   - Burada tanımlanan şablon, CronJob her tetiklendiğinde bir Job oluşturur ve o Job'un Pod'ları çalıştırılır.

3. **Başarım ve Silme Politikaları**  
   - `spec.successfulJobsHistoryLimit`, başarıyla biten Job'ların kaydını ne kadar süre saklayacağını belirtir.  
   - `spec.failedJobsHistoryLimit`, hatalı Job'ların kaydını ne kadar süre saklanacağını belirler.

4. **Concurrency Policy (Eşzamanlılık Politikası)**  
   - `Allow`: Varsayılan olarak eski Job hala çalışıyorken yeni Job da başlar.  
   - `Forbid`: Eğer önceki Job hala çalışıyorsa yeni Job başlamaz.  
   - `Replace`: Devam eden Job varsa sonlandırılır ve yerine yenisi başlatılır.

5. **Başlangıç Tarihi ve Son Ömür (Starting Deadline ve ActiveDeadlineSeconds)**  
   - Bazı durumlarda Job gecikmeli tetiklenebilir. `startingDeadlineSeconds`, gecikme durumunda Job'un tetiklenmesini iptal ya da geciktirme için kullanılır.  
   - `activeDeadlineSeconds`, Pod'un maksimum çalışma süresini kısıtlar.

---

## Örnek CronJob Manifest Dosyası

Aşağıdaki örnek, her saat başı bir Job oluşturan bir CronJob tanımı göstermektedir:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: hourly-job
spec:
  schedule: "0 * * * *"       # Her saat başı
  concurrencyPolicy: Forbid   # Bir önceki job devam ediyorsa yeni job başlamasın
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
          - name: hello
            image: busybox:latest
            command: ["echo", "Bu cronjob saat basi calisir"]
```

1. **`schedule: "0 * * * *"`**  
   Her saat başında Job'u tetikler.

2. **`concurrencyPolicy: Forbid`**  
   Önceki Job tamamlanmadan yeni Job başlatılmayacak.

3. **`jobTemplate`**  
   CronJob tetiklendiğinde oluşturulacak Job'un şablonunu belirtir.

4. **`restartPolicy: OnFailure`**  
   Pod başarısız olursa tekrar başlatılmaya çalışılır, ancak başarılı olursa yeni bir Pod oluşturulmaz (Job mantığına uygun).

---

## CronJob Komutlarına Örnekler

- **Oluşturma / Güncelleme**:  
  ```bash
  kubectl apply -f cronjob.yaml
  ```
- **Durumu Görüntüleme**:  
  ```bash
  kubectl get cronjobs
  kubectl describe cronjob hourly-job
  ```
- **Job'ların Kayıtlarını İnceleme**:  
  ```bash
  kubectl get jobs
  ```
  CronJob'un tetiklenmesi sonucu oluşan Job'ları takip edebilirsiniz.
- **CronJob Silme**:  
  ```bash
  kubectl delete cronjob hourly-job
  ```

---

## Kullanım Senaryoları

1. **Düzenli Yedekleme veya Raporlama**  
   Veritabanlarından günlük veya saatlik yedek almak.  
2. **Periodik Log Arşivleme**  
   Her gece log dosyalarını sıkıştırıp merkezi bir depoya aktarmak.  
3. **Periyodik Bakım İşlemleri**  
   Örneğin, gereksiz verileri temizleme, dosya sisteminde rota güncellemesi vb.

---

## Sonuç

**CronJob**, Kubernetes'te Job nesnesinin "takvimli" (scheduled) sürümüdür. Bu sayede geleneksel "cron" sisteminde olduğu gibi, belirli periyotlarla tekrarlanan işleri container tabanlı modern mimarinizde kolayca planlayabilir ve yönetebilirsiniz. Bir CronJob her tetiklendiğinde yeni bir Job yaratır, böylece zamanlama ve batch iş sürekliliği Zahmetsiz şekilde sağlanır.
