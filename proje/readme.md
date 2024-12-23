# Projeler

Merhaba arkadaşlar,

Burada öğrendiklerimizi pekiştirmek için projeleri paylaşacağım. Repository içinde gördüğünüz gibi `kemal` adında bir klasör var. Bu klasörü örnek alarak, kendi adınızla bir klasör oluşturmanızı rica ediyorum.

Herkes çalışma alanı oluşturmak için `main` branch'ten kendi yeni branch'ini oluşturabilir. Ancak, anlaşılır olması için branch ismini kendi adınız olarak belirlemenizi öneririm.

Mevcut repository'deki `kemal` klasörünün içindeki dosya ve klasör yapısını siz de kendi branch'inizde oluşturmalısınız.

Değişikliklerinizi Pull Request olarak açın ve `main` e birleştirmeye çalışın, birleştirirken squash, rebase, merge seçenekleri çıkacak bunlardan hangisi ile yapacağınızı PR'ın açıklama kısmına yazınız, beni reviewer olarak ekleyin. @ işaretini kullanarak beni mention edebilirsiniz.

## AWS Klasörü

### 1. EC2 Bilgileri
- `aws` klasörü içine, oluşturduğunuz Ubuntu sunucunuzun bilgilerini eklemenizi rica ediyorum.
  - **Adım 1**: `ec2.txt` dosyası oluşturun ve içine aynı formatta gerekli bilgileri yazın.
  - **Adım 2**: Sunucunun storage kısmında bulunan volume'u 8 GB'dan 10 GB'a genişletin. Bu işlem için şu kaynağı kullanabilirsiniz: [Amazon Docs: Recognize Expanded Volume on Linux](https://docs.aws.amazon.com/ebs/latest/userguide/recognize-expanded-volume-linux.html)
  - Genişletme işlemi sonrası, `lsblk` ve `df -hT` komutlarının çıktısını `volume.txt` adında bir dosyaya kaydedin.

---

## Linux Klasörü

### 2. Shell Script ve Servis
- `linux` klasörünün içinde `shell` adında yeni bir klasör oluşturun.
- Linux sunucunuzda, aşağıdaki işlemleri gerçekleştiren bir servis oluşturun:
  - Sunucuyu **`sudo apt update && sudo apt upgrade -y`** komutlarıyla güncelleyen bir shell script hazırlayın.
  - Bu komutun çıktısını yönlendirme sembolleri ile `/tmp` klasörüne aktarın.
  - Hazırladığınız script'i her gün sabah 5'te otomatik olarak çalışacak şekilde bir cronjob ile ayarlayın.
  - Linux servisini oluşturmak için shell script'inizi servis dosyası ile ilişkilendirin.
- İlgili örneklere klasördeki mevcut dosyalardan bakabilirsiniz.

---

## SSH Klasörü

### 3. SSH Anahtarları
- `ssh` klasöründe aşağıdaki adımları gerçekleştirin:
  - **`ssh-ed25519`**, **`ssh-rsa`**, ve **`ecdsa`** formatlarında SSH anahtarları oluşturun.
  - Bu anahtarların sadece **public** kısımlarını ilgili klasöre ekleyin.

---

Bu README.md dosyası, projeyi kolayca takip edebilmeniz ve uygulayabilmeniz için hazırlanmıştır. Herhangi bir sorunuz olursa, lütfen paylaşın. İyi çalışmalar!
