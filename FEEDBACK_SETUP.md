# 📊 Feedback Sistem Kurulum Rehberi

Bu rehber, Streamlit Cloud'da Contact Us sayfasındaki feedback'leri Google Sheets'e kaydetmek için gerekli adımları açıklar.

## 🔧 Kurulum Adımları

### 1. Google Cloud Console Kurulumu

1. [Google Cloud Console](https://console.cloud.google.com)'a gidin
2. Yeni bir proje oluşturun veya mevcut projeyi seçin
3. **APIs & Services > Library** bölümüne gidin
4. Şu API'leri etkinleştirin:
   - Google Sheets API
   - Google Drive API

### 2. Service Account Oluşturma

1. **APIs & Services > Credentials** bölümüne gidin
2. **Create Credentials > Service Account** seçin
3. Service account bilgilerini doldurun:
   - Name: `streamlit-feedback-service`
   - Description: `Service account for Streamlit feedback system`
4. **Create and Continue** tıklayın
5. Role olarak **Editor** seçin (veya daha kısıtlı izinler için custom role)
6. **Done** tıklayın

### 3. JSON Key Oluşturma

1. Oluşturulan service account'a tıklayın
2. **Keys** sekmesine gidin
3. **Add Key > Create New Key** seçin
4. **JSON** formatını seçin ve indirin
5. Bu JSON dosyasını güvenli bir yerde saklayın

### 4. Google Sheets Hazırlama

1. [Google Sheets](https://sheets.google.com)'te yeni bir spreadsheet oluşturun
2. Adını "Financial News Analyzer - Feedback" yapın
3. URL'den Sheet ID'yi kopyalayın:
   ```
   https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit
   ```
4. Service account email adresini sheet'e editör olarak ekleyin:
   - **Share** butonuna tıklayın
   - Service account email'i ekleyin (JSON'da `client_email`)
   - **Editor** yetkisi verin

### 5. Streamlit Secrets Konfigürasyonu

#### Yerel Geliştirme İçin:

`.streamlit/secrets.toml` dosyasını düzenleyin:

```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project-id.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project-id.iam.gserviceaccount.com"

GOOGLE_SHEET_ID = "your-google-sheet-id"
```

#### Streamlit Cloud İçin:

1. Streamlit Cloud dashboard'unuza gidin
2. App'inizi seçin
3. **Settings > Secrets** bölümüne gidin
4. Yukarıdaki TOML formatındaki bilgileri yapıştırın

### 6. Güvenlik Notları

- JSON key dosyasını asla Git'e commit etmeyin
- `.streamlit/secrets.toml` dosyasını `.gitignore`'a ekleyin
- Service account'a minimum gerekli yetkileri verin
- Düzenli olarak keys'leri rotate edin

## 🔄 Fallback Sistemi

Sistem şu sırayla çalışır:

1. **Google Sheets** (Birincil)
2. **CSV Dosyası** (Fallback)

Eğer Google Sheets bağlantısı başarısız olursa, sistem otomatik olarak CSV dosyasına kaydeder.

## 📋 Test Etme

1. Uygulamayı çalıştırın
2. Contact Us sayfasına gidin
3. Test mesajı gönderin
4. Google Sheets'te verinin görünmesini kontrol edin

## 🐛 Sorun Giderme

### Yaygın Hatalar:

1. **"Permission denied"**: Service account'un sheet'e erişimi yok
2. **"API not enabled"**: Google Sheets API etkinleştirilmemiş
3. **"Invalid credentials"**: JSON key bilgileri yanlış

### Çözümler:

1. Service account email'in sheet'e editor erişimi olduğunu kontrol edin
2. API'lerin etkinleştirildiğini kontrol edin
3. JSON key bilgilerinin doğru kopyalandığını kontrol edin

## 📊 Veri Yapısı

Google Sheets'te şu kolonlar oluşturulacak:

| Timestamp | Name | Email | Message | Status |
|-----------|------|--------|---------|--------|
| 2024-01-01 12:00:00 | Enes | enes@example.com | Test mesajı | Yeni |

Bu sayede feedback'leri kolayca takip edebilir ve yönetebilirsiniz.
