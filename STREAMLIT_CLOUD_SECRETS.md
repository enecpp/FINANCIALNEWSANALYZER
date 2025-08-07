# 🔐 Streamlit Cloud Secrets Kurulumu

**Önemli:** API anahtarlarını GitHub'a commit etmeyin! Bu rehber güvenli kurulum için hazırlanmıştır.

## 🚀 Streamlit Cloud'da Secrets Ayarlama

### 1. Streamlit Cloud Dashboard

1. [Streamlit Cloud](https://share.streamlit.io)'a gidin
2. GitHub hesabınızla giriş yapın
3. Repository'nizi seçin ve deploy edin

### 2. Secrets Konfigürasyonu

1. **App dashboard'unda "⚙️ Settings" tıklayın**
2. **"🔐 Secrets" sekmesine gidin**
3. **Aşağıdaki TOML formatındaki konfigürasyonu yapıştırın:**

```toml
[gcp_service_account]
type = "service_account"
project_id = "your-actual-project-id"
private_key_id = "your-actual-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_ACTUAL_PRIVATE_KEY\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project-id.iam.gserviceaccount.com"
client_id = "your-actual-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project-id.iam.gserviceaccount.com"

GOOGLE_SHEET_ID = "your-actual-google-sheet-id"
```

### 3. Secrets Bilgilerini Alma

#### Google Cloud Service Account JSON'u:
1. Google Cloud Console'a gidin
2. Service Account oluşturun
3. JSON key indirin
4. JSON içindeki bilgileri yukarıdaki template'e kopyalayın

#### Google Sheets ID:
1. Google Sheets'te spreadsheet oluşturun
2. URL'den ID'yi kopyalayın:
   ```
   https://docs.google.com/spreadsheets/d/{BU_KISIM_SHEET_ID}/edit
   ```

## 🛡️ Güvenlik Önlemleri

### ✅ Doğru Yaklaşım:
- Secrets sadece Streamlit Cloud dashboard'unda
- API anahtarları GitHub'da değil
- `.streamlit/` klasörü gitignore'da

### ❌ Yanlış Yaklaşım:
- API anahtarlarını kod içinde yazmak
- secrets.toml'u Git'e commit etmek
- API anahtarlarını public repository'de bırakmak

## 🧪 Test Etme

1. Streamlit Cloud'da app'i deploy edin
2. Contact Us sayfasına gidin
3. Test mesajı gönderin
4. Google Sheets'te verinin göründüğünü kontrol edin

## 🔄 Yerel Geliştirme

Yerel geliştirme için:
1. `secrets.toml.template` dosyasını kopyalayın
2. `secrets.toml` olarak kaydedin
3. Gerçek API bilgilerini girin
4. **Asla Git'e commit etmeyin!**

## 📋 Checklist

- [ ] Google Cloud Console'da proje oluşturdum
- [ ] Service Account oluşturdum
- [ ] JSON key indirdim
- [ ] Google Sheets oluşturdum
- [ ] Service Account'u sheet'e editor olarak ekledim
- [ ] Streamlit Cloud'da secrets ayarladım
- [ ] Test mesajı gönderip çalıştığını doğruladım
- [ ] API anahtarlarının GitHub'da olmadığını kontrol ettim

Bu checklist'i tamamladığınızda sistem güvenli şekilde çalışacaktır! 🎉
