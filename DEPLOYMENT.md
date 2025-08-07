# 🚀 Streamlit Cloud Deployment Talimatları

## 📋 Deployment Adımları

### 1. GitHub'a Push
```bash
git add .
git commit -m "Add Google Sheets feedback system"
git push origin main
```

### 2. Streamlit Cloud Deployment
1. [share.streamlit.io](https://share.streamlit.io) adresine gidin
2. GitHub repository'nizi seçin
3. `financial_news_analyzer/Start.py` dosyasını main file olarak seçin

### 3. Streamlit Cloud Secrets Yapılandırması

Streamlit Cloud'da app'inizi deploy ettikten sonra:

1. **App Settings** > **Secrets** bölümüne gidin
2. Aşağıdaki formatı kullanarak secrets ekleyin:

```toml
# Google Sheets configuration
GOOGLE_SHEET_ID = "1XzHbtgOl6AOE-lg7y-E3z_G6dZ2gcvxb004Coxa6g8A"

# Google Cloud Service Account credentials
[gcp_service_account]
type = "service_account"
project_id = "GERÇEK_PROJECT_ID"
private_key_id = "GERÇEK_PRIVATE_KEY_ID"
private_key = "-----BEGIN PRIVATE KEY-----\nGERÇEK_PRIVATE_KEY\n-----END PRIVATE KEY-----\n"
client_email = "GERÇEK_SERVICE_ACCOUNT_EMAIL"
client_id = "GERÇEK_CLIENT_ID"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/oauth2/v3/certs/GERÇEK_SERVICE_ACCOUNT_EMAIL"
```

### 4. Google Cloud Service Account Oluşturma

1. **Google Cloud Console** > **IAM & Admin** > **Service Accounts**
2. **Create Service Account** ile yeni hesap oluşturun
3. **Editor** veya **Owner** rolü verin
4. **Keys** > **Add Key** > **JSON** ile key indirin
5. JSON'daki bilgileri Streamlit Cloud secrets'a kopyalayın

### 5. Google Sheets Paylaşımı

1. Google Sheets dosyanızı açın (ID: 1XzHbtgOl6AOE-lg7y-E3z_G6dZ2gcvxb004Coxa6g8A)
2. **Share** butonuna tıklayın
3. Service Account'ın email adresini ekleyin
4. **Editor** yetkisi verin

### 6. API'ları Etkinleştirin

Google Cloud Console'da:
- Google Sheets API
- Google Drive API

## 🔒 Güvenlik Notları

- ✅ `.gitignore` dosyası secrets.toml'i koruyor
- ✅ Local secrets.toml sadece placeholder değerler içeriyor
- ✅ Gerçek secrets sadece Streamlit Cloud'da
- ✅ GitHub repository'de hiçbir API key görünmeyecek

## 🎯 Beklenen Sonuç

Deploy tamamlandığında:
- Contact Us formu çalışacak
- Mesajlar Google Sheets'e kaydedilecek
- CSV fallback sistemi aktif kalacak
- Hiçbir API key GitHub'da görünmeyecek

## 🆘 Sorun Giderme

Eğer Google Sheets çalışmazsa:
1. Service Account email'inin sheets'e eklendiğini kontrol edin
2. API'ların etkinleştirildiğini kontrol edin
3. Streamlit Cloud secrets'ın doğru formatta olduğunu kontrol edin
4. CSV fallback sistemi devreye girecek

---

Bu dosyayı GitHub'a da ekleyebilirsiniz - hiçbir hassas bilgi içermiyor! 🚀
