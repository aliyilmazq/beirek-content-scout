# BEIREK Content Scout

Yenilenebilir enerji, altyapı, proje yönetimi ve yatırım alanlarındaki haberleri otomatik tarayan, filtreleyen ve içerik üreten CLI uygulaması.

## Kurulum

```bash
# Virtual environment oluştur
python -m venv venv
source venv/bin/activate  # macOS/Linux

# Bağımlılıkları yükle
pip install -r requirements.txt
```

## Gereksinimler

- Python 3.10+
- Claude CLI kurulu ve çalışır durumda
- macOS/Linux

## Kullanım

```bash
python main.py
```

## Özellikler

- **Haber Tarama**: 300+ kaynaktan RSS/Web scraping
- **Akıllı Filtreleme**: Claude AI ile BEIREK ilgi alanına göre filtreleme
- **İçerik Üretimi**: 3 formatta içerik (Makale, LinkedIn, Twitter)
- **Günlük Kavram**: 7000+ terimlik sözlükten günlük kavram tanıtımı
- **İstek Havuzu**: Manuel konu taleplerini işleme
- **Anti-Halüsinasyon**: Kaynak doğrulama sistemi

## Klasör Yapısı

```
beirek-content-scout/
├── main.py              # Ana uygulama
├── config.yaml          # Ayarlar
├── sources.yaml         # Kaynak listesi
├── modules/             # Python modülleri
├── prompts/             # Claude promptları
├── data/                # Veritabanı
└── logs/                # Log dosyaları
```

## İçerik Formatları

| Format | Hedef Kitle | Uzunluk |
|--------|-------------|---------|
| Makale | C-level, finansçılar | 1500-2500 kelime |
| LinkedIn | Board/C-Level yöneticiler | 150-300 kelime |
| Twitter | Profesyonel kitle | 5-10 tweet |

## Lisans

BEIREK Internal Use Only
