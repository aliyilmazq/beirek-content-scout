# BEIREK Content Scout
## Proje İhtiyaç Dokümantasyonu (PRD)

---

## 1. PROJE ÖZETİ

### 1.1 Amaç
Yenilenebilir enerji, altyapı, proje yönetimi ve yatırım alanlarındaki haber kaynaklarını otomatik tarayan, BEIREK'in ilgi alanına giren içerikleri filtreleyen, seçilen içeriklerden farklı formatlarda profesyonel içerik üreten ve organize eden bir masaüstü CLI uygulaması.

### 1.2 Hedef Kullanıcı
BEIREK ekibi - içerik pazarlama ve thought leadership çalışmaları için.

### 1.3 Temel Özellikler
- 300+ kaynaktan otomatik haber tarama (RSS + Web scraping)
- Claude CLI ile akıllı filtreleme (BEIREK ilgi alanı)
- Kullanıcı seçimi sonrası içerik üretimi
- 3 format: Research-grade makale, LinkedIn post, Twitter thread
- **BEIREK çalışma alanlarına göre organize klasör yapısı**
- Typefully'e manuel aktarım için hazır çıktılar

### 1.4 İçerik Üretim Modları
Sistem üç farklı modda içerik üretir:

| Mod | Açıklama | Sıklık |
|-----|----------|--------|
| **Haber Bazlı** | Kaynak havuzundan taranan güncel haberlerden üretim | Günlük tarama |
| **Günlük Kavram** | 7000+ kavramlık sözlükten dinamik seçim ile kavram tanıtımı | Her gün 1 kavram |
| **İstek Havuzu** | Manuel olarak belirtilen konularda içerik üretimi | Talep üzerine |

### 1.5 İçerik Formatları ve Hedef Kitleler

Her içerik 3 farklı formatta üretilir. **Her format farklı kitleye, farklı dil ve yaklaşımla hitap eder:**

| Format | Hedef Kitle | Ton & Yaklaşım | Uzunluk |
|--------|-------------|----------------|---------|
| **Makale** | C-level, hukuk danışmanları, proje finansçıları | Akademik-profesyonel, analitik, derinlemesine | 1500-2500 kelime |
| **LinkedIn** | Board/C-Level yöneticiler, karar vericiler | Samimi, şeffaf, BEIREK bakış açısı + çözüm odaklı | 150-300 kelime |
| **Twitter** | Geniş profesyonel kitle, sektör takipçileri | Punchy, dikkat çekici, her tweet bağımsız değerli | 5-10 tweet |

**ÖNEMLİ:** Aynı konu işlense bile her format birbirinden bağımsız yazılır. Aynı cümlelerin kopyalanması YASAKTIR.

---

## 2. BEIREK ÇALIŞMA ALANLARI VE HİZMETLER

### 2.0 Ana Çalışma Alanları (8 Alan)

Her içerik bu 8 çalışma alanından birine atanır ve ilgili klasöre kaydedilir:

#### 1. Deal & Contract Advisory
> Karmaşık anlaşmaları uçtan uca yönetiriz—term sheet tasarımından kapanışa ve kapanış sonrası yükümlülük takibine kadar.

| Alt Başlık | Açıklama |
|------------|----------|
| Deal Architecture & Term Sheet Design | Anlaşma mimarisi ve ön protokol tasarımı |
| Transaction Governance & Negotiation | İşlem yönetişimi ve müzakere |
| Contract Lifecycle Management (CLM) | Sözleşme yaşam döngüsü yönetimi |
| Data Room & Due Diligence Coordination | Veri odası ve durum tespiti koordinasyonu |

#### 2. CEO Office & Governance
> Stratejiyi uygulama disiplinine dönüştüren, yapılandırılmış yönetişim ve performans yönetimi ile bir CEO Ofisi kuruyoruz.

| Alt Başlık | Açıklama |
|------------|----------|
| CEO Office Setup & Operating Rhythm | CEO ofisi kurulumu ve operasyon ritmi |
| Authority Matrix & Approval Workflows | Yetki matrisi ve onay iş akışları |
| OKR/KPI Architecture | OKR/KPI mimarisi |
| Executive Reporting & Risk Governance | Üst yönetim raporlaması ve risk yönetişimi |

#### 3. Development Finance & Compliance
> IFI/DFI ilişkilerini yönetir, sağlam kanıt ve raporlama sistemleriyle borç veren gereksinimlerine tam uyumu sağlarız.

| Alt Başlık | Açıklama |
|------------|----------|
| IFI/DFI Relationship Management | Uluslararası finans kuruluşları ilişki yönetimi |
| Requirements Library & Traceability | Gereksinim kütüphanesi ve izlenebilirlik |
| Lender-Grade Reporting Factory | Borç veren seviyesinde raporlama altyapısı |
| Covenant Monitoring & Compliance | Taahhüt izleme ve uyum |

#### 4. Project Development & Finance
> İlk vizyondan bankable projeye kadar fizibilite, izin, paydaş geliştirme ve yatırım yapılandırmasını yönetiriz.

| Alt Başlık | Açıklama |
|------------|----------|
| Feasibility Studies & Roadmap | Fizibilite çalışmaları ve yol haritası |
| Site Assessment & Permitting | Saha değerlendirmesi ve izinler |
| Project Finance Structuring | Proje finansmanı yapılandırması |
| Financial Modeling & Value Engineering | Finansal modelleme ve değer mühendisliği |

#### 5. Engineering & Delivery
> Tasarımdan devreye almaya kadar kapsamlı EPCM hizmetleri sunarak projelerin zamanında ve şartnameye uygun teslimini sağlarız.

| Alt Başlık | Açıklama |
|------------|----------|
| FEED & Detailed Design Management | Ön uç mühendislik ve detaylı tasarım yönetimi |
| Procurement & Vendor Governance | Tedarik ve satıcı yönetişimi |
| EPC/Construction Management | EPC/İnşaat yönetimi |
| Commissioning & Performance Testing | Devreye alma ve performans testi |

#### 6. Asset Management (O&M)
> Varlıkların operasyonel devirden ömür sonu planlamasına kadar tüm yaşam döngüsü boyunca en yüksek verimlilikle çalışmasını sağlarız.

| Alt Başlık | Açıklama |
|------------|----------|
| O&M Governance & SLA Management | İşletme-bakım yönetişimi ve SLA yönetimi |
| Performance Monitoring & Optimization | Performans izleme ve optimizasyon |
| Predictive Maintenance Strategy | Öngörücü bakım stratejisi |
| Modernization & Decommissioning | Modernizasyon ve hizmetten çıkarma |

#### 7. GTM & JV Management
> Yapılandırılmış ortak seçimi, JV yönetişimi ve ticari uygulama çerçeveleriyle pazara giriş genişlemesini yürütürüz.

| Alt Başlık | Açıklama |
|------------|----------|
| Market Entry Strategy & Execution | Pazar giriş stratejisi ve uygulama |
| Partner Development & Selection | Ortak geliştirme ve seçimi |
| JV Setup & Governance Controls | Ortak girişim kurulumu ve yönetişim kontrolleri |
| Commercial Frameworks & KPIs | Ticari çerçeveler ve KPI'lar |

#### 8. Digital Platforms
> Karmaşık organizasyonları yönetilebilir ve ölçeklenebilir kılan dijital uygulama omurgasını inşa ederiz.

| Alt Başlık | Açıklama |
|------------|----------|
| ERP & Enterprise Digitization | ERP ve kurumsal dijitalleşme |
| PMIS/PPM Implementation | Proje yönetim bilgi sistemi uygulaması |
| Data & AI Enablement | Veri ve yapay zeka etkinleştirme |

---

## 3. FİLTRELEME KRİTERLERİ

Claude filtreleme yaparken şu konulara odaklanacak:

### 3.1 Birincil İlgi Alanları
- Utility-scale güneş enerjisi projeleri (50MW+)
- Rüzgar enerjisi projeleri (onshore/offshore)
- Enerji depolama sistemleri (BESS)
- Data center altyapı projeleri
- Şebeke modernizasyonu ve transmission projeleri
- Proje finansmanı ve IFI/DFI haberleri
- EPC kontratları ve mega proje ihaleleri
- ABD enerji politikaları ve teşvikler (IRA, vb.)

### 3.2 İkincil İlgi Alanları
- Hidrojen ve yeşil amonyak projeleri
- Proje yönetimi metodolojileri ve trendler
- Digital twin ve PMIS teknolojileri
- ESG ve sürdürülebilirlik raporlaması
- Enerji sektöründe M&A aktiviteleri

### 3.3 Coğrafi Odak
- Birincil: ABD (özellikle Texas, California, Arizona, Virginia)
- İkincil: Latin Amerika, Orta Doğu

### 3.4 Hariç Tutulacaklar
- Residential/konut ölçekli projeler
- Genel ekonomi haberleri (enerji/altyapı bağlantısı olmayan)
- Şirket içi duyurular (earning calls, vb.)
- Ürün lansmanları (panel/türbin üreticileri)

---

## 4. TEKNİK GEREKSİNİMLER

### 3.1 Sistem Gereksinimleri
- Python 3.10+
- Claude CLI kurulu ve çalışır durumda
- macOS/Linux terminal
- İnternet bağlantısı

### 3.2 Python Bağımlılıkları
```
feedparser>=6.0.0      # RSS okuma
requests>=2.31.0       # HTTP istekleri
beautifulsoup4>=4.12.0 # Web scraping
lxml>=4.9.0            # HTML parsing
pyyaml>=6.0.0          # Konfigürasyon
rich>=13.0.0           # Terminal UI
sqlite3                # Veritabanı (built-in)
datetime               # Tarih işlemleri (built-in)
subprocess             # Claude CLI çağrısı (built-in)
```

### 3.3 Claude CLI Kullanımı
```bash
# Temel çağrı formatı
echo "prompt" | claude

# Dosya ile çağrı
cat input.txt | claude

# Çıktıyı dosyaya yazma
echo "prompt" | claude > output.txt
```

---

## 5. DOSYA VE KLASÖR YAPISI

### 5.1 Uygulama Yapısı

```
beirek-content-scout/
│
├── main.py                     # Ana uygulama giriş noktası
├── config.yaml                 # Uygulama ayarları
├── sources.yaml                # Kaynak listesi (RSS URL'leri)
├── requirements.txt            # Python bağımlılıkları
├── README.md                   # Kurulum ve kullanım kılavuzu
│
├── modules/
│   ├── __init__.py
│   ├── scanner.py              # RSS/Web tarama modülü
│   ├── filter.py               # Claude ile filtreleme
│   ├── generator.py            # İçerik üretimi
│   ├── storage.py              # Dosya kaydetme işlemleri
│   └── ui.py                   # Terminal arayüzü
│
├── prompts/
│   ├── filter_prompt.txt       # Filtreleme için system prompt
│   ├── article_prompt.txt      # Makale üretimi promptu
│   ├── linkedin_prompt.txt     # LinkedIn post promptu
│   ├── twitter_prompt.txt      # Twitter thread promptu
│   └── concept_prompt.txt      # Günlük kavram promptu
│
├── data/
│   ├── scout.db                # SQLite veritabanı
│   └── cache/                  # Geçici önbellek dosyaları
```

### 5.2 İçerik Klasör Yapısı (BEIREK Alanlarına Göre)

Tüm üretilen içerikler `content/` klasörü altında BEIREK çalışma alanlarına göre numaralı şekilde organize edilir:

```
content/
│
├── 1-deal-contract-advisory/
│   ├── 1-deal-architecture-term-sheet-design/
│   ├── 2-transaction-governance-negotiation/
│   ├── 3-contract-lifecycle-management/
│   └── 4-data-room-due-diligence-coordination/
│
├── 2-ceo-office-governance/
│   ├── 1-ceo-office-setup-operating-rhythm/
│   ├── 2-authority-matrix-approval-workflows/
│   ├── 3-okr-kpi-architecture/
│   └── 4-executive-reporting-risk-governance/
│
├── 3-development-finance-compliance/
│   ├── 1-ifi-dfi-relationship-management/
│   ├── 2-requirements-library-traceability/
│   ├── 3-lender-grade-reporting-factory/
│   └── 4-covenant-monitoring-compliance/
│
├── 4-project-development-finance/
│   ├── 1-feasibility-studies-roadmap/
│   ├── 2-site-assessment-permitting/
│   ├── 3-project-finance-structuring/
│   └── 4-financial-modeling-value-engineering/
│
├── 5-engineering-delivery/
│   ├── 1-feed-detailed-design-management/
│   ├── 2-procurement-vendor-governance/
│   ├── 3-epc-construction-management/
│   └── 4-commissioning-performance-testing/
│
├── 6-asset-management-om/
│   ├── 1-om-governance-sla-management/
│   ├── 2-performance-monitoring-optimization/
│   ├── 3-predictive-maintenance-strategy/
│   └── 4-modernization-decommissioning/
│
├── 7-gtm-jv-management/
│   ├── 1-market-entry-strategy-execution/
│   ├── 2-partner-development-selection/
│   ├── 3-jv-setup-governance-controls/
│   └── 4-commercial-frameworks-kpis/
│
├── 8-digital-platforms/
│   ├── 1-erp-enterprise-digitization/
│   ├── 2-pmis-ppm-implementation/
│   └── 3-data-ai-enablement/
│
├── 9-daily-concepts/                          # Günlük Kavram Tanıtımları
│   ├── kavram-sozlugu.md                      # 7000+ terimlik sözlük referansı
│   └── 2026-01-30_kavram_force-majeure/      # Örnek kavram içeriği
│       ├── makale.md
│       ├── linkedin.md
│       └── twitter.md
│
└── 10-istek-havuzu/                          # Manuel İçerik Talepleri
    ├── NASIL-KULLANILIR.md
    └── {konu-basligi}/                       # Kullanıcının açtığı klasör
        ├── brief.md                          # (Opsiyonel) İçerik briefingi
        ├── makale.md
        ├── linkedin.md
        └── twitter.md
```

### 5.3 İçerik Dosya Adlandırma Kuralı

```
{YYYY-MM-DD}_{tur}_{slug-title}/
├── makale.md
├── linkedin.md
└── twitter.md

Örnekler:
4-project-development-finance/3-project-finance-structuring/
└── 2026-01-30_haber_texas-solar-project-milestone/

9-daily-concepts/
└── 2026-01-30_kavram_force-majeure/

10-istek-havuzu/
└── neom-hydrogen-financing/
```

### 5.4 İstek Havuzu Kullanımı

1. Kullanıcı `content/10-istek-havuzu/` altına konu başlığıyla klasör açar
2. (Opsiyonel) `brief.md` dosyasıyla detay verir
3. Sistem içeriği üretir ve klasöre kaydeder
4. İçerik ilgili BEIREK alanına da kopyalanır

---

## 6. VERİTABANI ŞEMASI

### 5.1 sources (Kaynaklar)
```sql
CREATE TABLE sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    rss_url TEXT,
    category TEXT,
    priority INTEGER DEFAULT 2,  -- 1: yüksek, 2: orta, 3: düşük
    last_checked DATETIME,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 5.2 articles (Taranan Makaleler)
```sql
CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id INTEGER,
    title TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    summary TEXT,
    published_at DATETIME,
    scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    relevance_score REAL,        -- Claude'un verdiği 0-10 puan
    is_relevant BOOLEAN,
    is_selected BOOLEAN DEFAULT 0,
    is_processed BOOLEAN DEFAULT 0,
    FOREIGN KEY (source_id) REFERENCES sources(id)
);
```

### 5.3 generated_content (Üretilen İçerikler)
```sql
CREATE TABLE generated_content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id INTEGER,
    content_type TEXT,           -- 'article', 'linkedin', 'twitter'
    title TEXT,
    content TEXT,
    file_path TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_published BOOLEAN DEFAULT 0,
    published_at DATETIME,
    FOREIGN KEY (article_id) REFERENCES articles(id)
);
```

### 6.4 scan_history (Tarama Geçmişi)
```sql
CREATE TABLE scan_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at DATETIME,
    completed_at DATETIME,
    sources_scanned INTEGER,
    articles_found INTEGER,
    articles_relevant INTEGER,
    status TEXT                  -- 'completed', 'failed', 'partial'
);
```

### 6.5 glossary (Sözlük Havuzu)
```sql
CREATE TABLE glossary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    term_en TEXT NOT NULL,              -- İngilizce terim
    term_tr TEXT,                       -- Türkçe terim (varsa)
    category TEXT,                      -- Kategori (finance, legal, technical, vb.)
    source_line INTEGER,                -- Sözlük dosyasındaki satır numarası
    is_used BOOLEAN DEFAULT 0,          -- Daha önce seçildi mi?
    used_date DATE,                     -- Seçildiği tarih
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 6.6 daily_concepts (Günlük Kavram Üretimleri)
```sql
CREATE TABLE daily_concepts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    glossary_id INTEGER,                -- Sözlükten seçilen terim ID
    concept_en TEXT NOT NULL,           -- İngilizce kavram
    concept_tr TEXT,                    -- Türkçe kavram
    beirek_area TEXT NOT NULL,          -- Atanan BEIREK çalışma alanı
    beirek_subarea TEXT,                -- Alt alan
    selection_reason TEXT,              -- Neden bu kavram seçildi?
    published_date DATE,                -- Yayın tarihi
    content_path TEXT,                  -- Üretilen içerik klasörü
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (glossary_id) REFERENCES glossary(id)
);
```

### 6.7 content_requests (İstek Havuzu)
```sql
CREATE TABLE content_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    folder_name TEXT NOT NULL,          -- Klasör adı
    topic TEXT,                         -- Konu başlığı
    brief TEXT,                         -- Brief içeriği (varsa)
    beirek_area TEXT,                   -- Atanan BEIREK alanı
    status TEXT DEFAULT 'pending',      -- 'pending', 'processing', 'completed'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    content_path TEXT                   -- Üretilen içerik klasörü
);
```

---

## 7. MODÜL DETAYLARI

### 7.1 scanner.py - Tarama Modülü

**Fonksiyonlar:**

```python
def get_active_sources() -> list:
    """Veritabanından aktif kaynakları çeker"""

def fetch_rss_feed(url: str) -> list:
    """RSS feed'den son makaleleri çeker"""

def scrape_webpage(url: str) -> dict:
    """RSS olmayan sitelerden içerik çeker"""

def extract_article_content(url: str) -> str:
    """Makale sayfasından ana içeriği çıkarır"""

def scan_all_sources(limit_per_source: int = 10) -> list:
    """Tüm kaynakları tarar, son makaleleri toplar"""

def is_already_scanned(url: str) -> bool:
    """URL daha önce tarandı mı kontrol eder"""
```

**Tarama Mantığı:**
1. Önce RSS feed dene
2. RSS yoksa veya hata verirse web scraping yap
3. Son 24-48 saat içindeki içerikleri al
4. Daha önce taranmış URL'leri atla
5. Her kaynaktan max 10 içerik al

---

### 7.2 filter.py - Filtreleme Modülü

**Fonksiyonlar:**

```python
def prepare_filter_prompt(articles: list) -> str:
    """Makaleleri filtreleme promptuna hazırlar"""

def call_claude_filter(prompt: str) -> str:
    """Claude CLI çağırarak filtreleme yapar"""

def parse_filter_response(response: str) -> list:
    """Claude yanıtını parse eder, skorları çıkarır"""

def filter_articles(articles: list) -> list:
    """Ana filtreleme fonksiyonu - ilgili makaleleri döner"""

def get_relevance_explanation(article: dict) -> str:
    """Neden ilgili/ilgisiz olduğunu açıklar"""
```

**Filtreleme Akışı:**
1. Taranan makaleleri batch'ler halinde grupla (10'ar)
2. Her batch için Claude'a gönder
3. Claude 0-10 arası relevance score verir
4. Score >= 7 olanları "relevant" işaretle
5. Sonuçları veritabanına kaydet

---

### 7.3 generator.py - İçerik Üretim Modülü

**Fonksiyonlar:**

```python
def fetch_full_article(url: str) -> str:
    """Seçilen makalenin tam içeriğini çeker"""

def generate_research_article(source_content: str, topic: str) -> str:
    """Research-grade makale üretir"""

def generate_linkedin_post(source_content: str, topic: str) -> str:
    """LinkedIn post üretir"""

def generate_twitter_thread(source_content: str, topic: str) -> str:
    """Twitter thread üretir"""

def call_claude_generate(prompt: str) -> str:
    """Claude CLI ile içerik üretir"""

def generate_all_formats(article: dict) -> dict:
    """Tüm formatları tek seferde üretir"""
```

**Üretim Parametreleri:**

| Format | Uzunluk | Ton | Özellikler |
|--------|---------|-----|------------|
| Research Article | 1500-2500 kelime | Profesyonel, thought leadership | Gerçek veriler + BEIREK özgün yorumu |
| LinkedIn Post | 150-300 kelime | Profesyonel, engaging | Hook, insight, CTA, 3-5 emoji max |
| Twitter Thread | 5-10 tweet | Conversational, punchy | Numaralı, her tweet bağımsız okunabilir |

---

### 7.4 storage.py - Depolama Modülü

**Fonksiyonlar:**

```python
def save_content(content: str, content_type: str, title: str) -> str:
    """İçeriği uygun klasöre kaydeder, path döner"""

def create_daily_folder(content_type: str) -> str:
    """Günlük klasör oluşturur (YYYY-MM-DD)"""

def generate_filename(title: str, content_type: str) -> str:
    """SEO-friendly dosya adı üretir"""

def archive_old_content(days: int = 30) -> int:
    """Eski içerikleri archive'a taşır"""

def export_for_typefully(content_id: int) -> str:
    """Typefully'e uygun formatta export eder"""

def get_content_stats() -> dict:
    """İstatistikleri döner (toplam, bu hafta, vb.)"""
```

**Dosya Adlandırma Kuralı:**
```
{YYYY-MM-DD}_{slug-title}_{format}.md

Örnek:
2026-01-30_texas-solar-project-milestone_article.md
2026-01-30_texas-solar-project-milestone_linkedin.md
2026-01-30_texas-solar-project-milestone_twitter.md
```

---

### 7.5 ui.py - Terminal Arayüzü

**Fonksiyonlar:**

```python
def show_main_menu() -> str:
    """Ana menüyü gösterir, seçim alır"""

def show_scan_progress(current: int, total: int):
    """Tarama progress bar gösterir"""

def show_article_list(articles: list) -> list:
    """Filtrelenmiş makaleleri listeler, seçim alır"""

def show_generation_options() -> list:
    """Hangi formatların üretileceğini sorar"""

def show_summary(stats: dict):
    """İşlem özetini gösterir"""

def confirm_action(message: str) -> bool:
    """Onay alır (y/n)"""
```

---

## 8. KULLANICI AKIŞI (USER FLOW)

```
┌─────────────────────────────────────────────────────────────────┐
│                         BAŞLANGIÇ                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ANA MENÜ                                                        │
│  ─────────                                                       │
│  [1] 🔍 Yeni Tarama Başlat                                       │
│  [2] 📋 Bekleyen İçerikleri Gör                                  │
│  [3] ✍️  İçerik Üret (Seçilmişlerden)                            │
│  [4] 📊 İstatistikler                                            │
│  [5] ⚙️  Ayarlar                                                 │
│  [6] 🚪 Çıkış                                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ [1] TARAMA       │ │ [2] BEKLEYENLER  │ │ [3] ÜRETİM       │
│                  │ │                  │ │                  │
│ • Kaynakları tara│ │ • Listeyi göster │ │ • Format seç     │
│ • Progress göster│ │ • Detay göster   │ │ • Claude üret    │
│ • Claude filtrele│ │ • Seç/Kaldır     │ │ • Dosyaya kaydet │
│ • Sonuç göster   │ │                  │ │ • Özet göster    │
└──────────────────┘ └──────────────────┘ └──────────────────┘
```

---

## 9. EKRAN TASARIMLARI (ASCII)

### 8.1 Ana Menü
```
╔══════════════════════════════════════════════════════════════╗
║           BEIREK Content Scout v1.0                          ║
║           ─────────────────────────                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║   [1] 🔍  Yeni Tarama Başlat                                 ║
║   [2] 📋  Bekleyen İçerikleri Gör (12 adet)                  ║
║   [3] ✍️   İçerik Üret                                       ║
║   [4] 📊  İstatistikler                                      ║
║   [5] ⚙️   Ayarlar                                           ║
║   [6] 🚪  Çıkış                                              ║
║                                                              ║
║   Son tarama: 2026-01-30 09:15                               ║
║   Bu hafta üretilen: 8 makale, 15 post                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
Seçiminiz [1-6]: _
```

### 8.2 Tarama Ekranı
```
╔══════════════════════════════════════════════════════════════╗
║  🔍 TARAMA DEVAM EDİYOR                                      ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Kaynak: PV Magazine                                         ║
║  [████████████████████░░░░░░░░░░] 65% (195/300)              ║
║                                                              ║
║  ✓ Taranan: 195 kaynak                                       ║
║  ✓ Bulunan: 847 makale                                       ║
║  ⏳ Filtreleniyor...                                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### 8.3 Makale Listesi ve Seçim
```
╔══════════════════════════════════════════════════════════════╗
║  📋 FİLTRELENMİŞ İÇERİKLER (23 adet)                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  [ ] 1. Texas 500MW Solar Project Reaches Financial Close    ║
║        📰 IJ Global | ⭐ 9.2 | 🕐 2 saat önce                ║
║                                                              ║
║  [✓] 2. BESS Market to Triple by 2030, Says BloombergNEF     ║
║        📰 Energy Storage News | ⭐ 8.8 | 🕐 5 saat önce      ║
║                                                              ║
║  [ ] 3. Data Center Boom Drives Grid Investment              ║
║        📰 Utility Dive | ⭐ 8.5 | 🕐 8 saat önce             ║
║                                                              ║
║  [✓] 4. EIB Approves $200M for Chilean Wind Farm             ║
║        📰 Recharge News | ⭐ 8.1 | 🕐 12 saat önce           ║
║                                                              ║
║  ───────────────────────────────────────────────────────     ║
║  [A] Tümünü seç  [N] Hiçbirini seçme  [D] Detay gör          ║
║  [S] Seçilenlerle devam et  [M] Ana menü                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
Seçim (numara veya komut): _
```

### 8.4 İçerik Üretim Seçenekleri
```
╔══════════════════════════════════════════════════════════════╗
║  ✍️  İÇERİK ÜRETİMİ                                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Seçilen makale:                                             ║
║  "BESS Market to Triple by 2030, Says BloombergNEF"          ║
║                                                              ║
║  Hangi formatları üreteyim?                                  ║
║                                                              ║
║  [1] 📝 Sadece Research Article                              ║
║  [2] 💼 Sadece LinkedIn Post                                 ║
║  [3] 🐦 Sadece Twitter Thread                                ║
║  [4] 📝💼 Article + LinkedIn                                 ║
║  [5] 📝🐦 Article + Twitter                                  ║
║  [6] 💼🐦 LinkedIn + Twitter                                 ║
║  [7] 📝💼🐦 Hepsi                                            ║
║                                                              ║
║  [M] Ana menü                                                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
Seçiminiz [1-7]: _
```

### 8.5 Üretim Sonuç Ekranı
```
╔══════════════════════════════════════════════════════════════╗
║  ✅ İÇERİK ÜRETİLDİ                                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📝 Research Article                                         ║
║     └─ outputs/articles/2026-01-30/bess-market-growth.md     ║
║        2,145 kelime | Hazır ✓                                ║
║                                                              ║
║  💼 LinkedIn Post                                            ║
║     └─ outputs/linkedin/2026-01-30/bess-market-growth.md     ║
║        234 kelime | Hazır ✓                                  ║
║                                                              ║
║  🐦 Twitter Thread                                           ║
║     └─ outputs/twitter/2026-01-30/bess-market-growth.md      ║
║        7 tweet | Hazır ✓                                     ║
║                                                              ║
║  ───────────────────────────────────────────────────────     ║
║  [O] Dosyaları aç  [T] Typefully'e kopyala  [M] Ana menü     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 10. PROMPT ŞABLONLARI

### 9.0 İÇERİK YAPISI: VERİ → YORUM → ÇÖZÜM

Her içerik 3 temel bölümden oluşmalı:

```
┌─────────────────────────────────────────────────────────────────┐
│                     İÇERİK YAPISI                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1️⃣  GERÇEK VERİ                                                │
│      ────────────                                               │
│      • Kaynaklardan alınan rakamlar, isimler, tarihler          │
│      • Halüsinasyon YASAK                                       │
│      • Link/atıf GEREKMEZ                                       │
│                                                                  │
│  2️⃣  BEIREK YORUMU                                              │
│      ──────────────                                             │
│      • Bu ne anlama geliyor?                                    │
│      • Geliştiriciler/yatırımcılar için çıkarımlar             │
│      • Sektör perspektifi ve trend analizi                      │
│      • Özgün thought leadership                                 │
│                                                                  │
│  3️⃣  BEIREK ÇÖZÜMÜ                                              │
│      ──────────────                                             │
│      • Bu sorunu/fırsatı nasıl değerlendiriyoruz?              │
│      • Hangi hizmetimiz bu konuda yardımcı olur?               │
│      • Neden bizimle çalışmalılar?                             │
│      • Soft CTA (hard sell YAPMA)                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### BEIREK HİZMET - KONU EŞLEŞTİRME TABLOSU

| Konu/Haber Türü | İlgili BEIREK Hizmeti | Örnek CTA |
|-----------------|----------------------|-----------|
| Financial close, proje finansmanı | Development Finance & Compliance | "Finansal kapanış sürecinizi hızlandıralım" |
| IFI/DFI kredileri, Dünya Bankası | Development Finance & Compliance | "IFI gereksinimlerini birlikte yönetelim" |
| EPC kontratı, inşaat başlangıcı | Engineering & Delivery (EPCM) | "EPC sürecinizi optimize edelim" |
| M&A, proje satışı, yatırım | Deal & Contract Advisory | "Due diligence sürecinize destek olalım" |
| O&M, performans, işletme | Asset Management | "Varlık performansınızı artıralım" |
| Dijitalleşme, PMIS, veri | Digital Platforms | "Proje yönetim altyapınızı kuralım" |
| Yeni pazar girişi, JV | GTM & JV Management | "Pazar giriş stratejinizi birlikte oluşturalım" |
| Kurumsal yönetim, strateji | CEO Office & Governance | "Yönetişim altyapınızı güçlendirelim" |

### ÖRNEK İÇERİK AKIŞI

**Haber:** "Texas'ta 500MW Solar Proje Financial Close'a Ulaştı"

```
1️⃣ VERİ:
"Texas'ta 500MW kapasiteli utility-scale solar projesi, $450 milyon 
finansmanla financial close aşamasına ulaştı. Proje 2027'de 
devreye alınacak ve 120,000 haneye enerji sağlayacak."

2️⃣ BEIREK YORUMU:
"Bu ölçekte bir projenin 18 ayda finansal kapanışa ulaşması dikkat çekici. 
Sektör ortalaması 24-36 ay. Başarının sırrı: erken aşamada kurulan 
lender-grade raporlama altyapısı ve IFI gereksinimlerinin proaktif yönetimi.

Pek çok geliştirici bu aşamada 6+ ay kaybediyor. Dokümantasyon kaosuna 
giren projeler, yatırımcı güvenini de kaybediyor."

3️⃣ BEIREK ÇÖZÜMÜ:
"BEIREK olarak Development Finance & Compliance hizmetimizle tam da bu 
darboğazı çözüyoruz. Proje başlangıcından itibaren IFI gereksinim 
kütüphanesi oluşturuyor, lender raporlama altyapısını kuruyoruz.

Sonuç? Daha hızlı kapanış, daha düşük işlem maliyeti.

Projenizin finansman sürecini değerlendirelim mi?"
```

---

### 10.1 Filtreleme Promptu (filter_prompt.txt)
```
Sen BEIREK için içerik filtreleme asistanısın. BEIREK, ABD merkezli bir proje yönetimi ve danışmanlık firması. Uzmanlık alanları:

- Utility-scale yenilenebilir enerji projeleri (güneş, rüzgar, BESS)
- Data center altyapısı
- Proje finansmanı ve IFI/DFI ilişkileri
- EPC yönetimi ve mega projeler

Aşağıdaki haber başlıklarını ve özetlerini değerlendir. Her biri için:
1. 0-10 arası relevance score ver
2. Tek cümlelik gerekçe yaz

Sadece şu formatta yanıt ver:
---
ID: [numara]
SCORE: [0-10]
REASON: [gerekçe]
---

DEĞERLENDİRİLECEK İÇERİKLER:
{articles}
```

### 10.2 Research Article Promptu (article_prompt.txt)
```
Sen BEIREK'in thought leadership yazarısın. Kaynak içerikteki VERİLERİ kullanarak özgün bir analiz yaz.

⚠️ KRİTİK KURALLAR:

VERİLER İÇİN (HALÜSİNASYON YASAK):
- Rakamlar (MW, $, %, tarih) SADECE kaynak metinden
- Şirket/proje isimleri SADECE kaynak metinden
- Olmayan veri UYDURMAK YASAK

YORUMLAR İÇİN (ÖZGÜN OLACAK):
- BEIREK perspektifinden analiz yap
- Proje geliştirici/yatırımcı bakış açısı kullan
- "Bu ne anlama geliyor?" sorusunu cevapla
- Pratik çıkarımlar ve öngörüler sun

BEIREK ÇÖZÜMÜ İÇİN (LEAD GENERATION):
- Bu konuda BEIREK nasıl yardımcı olabilir?
- Hangi hizmetlerimiz bu sorunu çözüyor?
- Neden bizimle çalışmalılar?

FORMAT KURALLARI:
- Kaynak linki veya atıf GEREKMEZ
- "...göre", "...raporuna göre" KULLANMA
- Verileri doğrudan yaz, sanki kendi bilgin

YAPI (ÖNEMLİ):
1. Dikkat çekici başlık
2. Executive summary (2-3 cümle)
3. Giriş ve bağlam (gerçek verilerle)
4. Ana analiz (3-4 bölüm) - BEIREK yorumları ile
5. Zorluklar ve riskler - sektörün yaşadığı sorunlar
6. BEIREK YAKLAŞIMI - "Biz bu konuda ne yapıyoruz?"
   - Hangi hizmetlerimiz bu sorunu çözüyor
   - Metodolojimiz ve farklılığımız
   - Başarı hikayelerimiz (varsa)
7. Sonuç ve CTA - "Projenizi birlikte değerlendirelim"

BEIREK HİZMET ALANLARI (İÇERİĞE GÖRE KULLAN):
- Deal & Contract Advisory
- CEO Office & Governance  
- Development Finance & Compliance (IFI/DFI)
- Project Development & Finance
- Engineering & Delivery (EPCM)
- Asset Management (O&M)
- GTM & JV Management
- Digital Platforms (PMIS, ERP)

ÖRNEK BEIREK ÇÖZÜMÜ BÖLÜMÜ:
"Bu tür utility-scale projelerde finansal kapanışa ulaşmak, düzinelerce 
bağımsız değişkenin aynı anda yönetilmesini gerektiriyor. BEIREK olarak, 
Development Finance & Compliance hizmetimizle IFI/DFI gereksinimlerini 
baştan sona yönetiyor, lender-grade raporlama altyapısı kuruyoruz. 
Projenizin finansal kapanış sürecini hızlandırmak için..."

UZUNLUK: 1500-2500 kelime
TON: Profesyonel, analitik, thought leadership + soft sell

KAYNAK İÇERİK:
{source_content}

KONU:
{topic}
```

### 10.3 LinkedIn Post Promptu (linkedin_prompt.txt)
```
Sen BEIREK'in LinkedIn thought leadership yazarısın.

HEDEF KİTLE:
- Board/C-Level yöneticiler (CEO, CFO, COO)
- Yönetim Kurulu üyeleri
- Üst düzey karar vericiler
- Proje sponsorları ve yatırımcılar

⚠️ VERİLER: Kaynak metindeki rakamları kullan, UYDURMAK YASAK
✅ BAKIŞ AÇISI: BEIREK bu konuya nasıl bakıyor?
🎯 ÇÖZÜM: Biz bu problemi nasıl çözüyoruz?

TON VE YAKLAŞIM:
- Samimi ve şeffaf (kurumsal soğukluk YOK)
- Çözüm odaklı (eleştiri veya şikayet YOK)
- Kavga çıkarmadan, yapıcı
- "Biz biliyoruz siz bilmiyorsunuz" havası YOK
- Karşılıklı diyalog ve paylaşım havası

YAPI (4 BÖLÜM):
1. HOOK: Dikkat çekici açılış + gerçek rakam/veri
2. PROBLEM: Sektörün yaşadığı zorluk (kısa ve net)
3. BEIREK YAKLAŞIMI: "Biz bu konuya farklı bakıyoruz..."
   - Bakış açımız nedir?
   - Nasıl çözüyoruz?
   - Metodolojimiz ne?
4. CTA: "Biz böyle çözüyoruz. Sizin projelerinizde bu nasıl yönetiliyor?"

KURALLAR:
- 150-300 kelime arası
- Kısa paragraflar (2-3 cümle max)
- Ok işaretleri (→) ile liste yapılabilir
- Kaynak linki/atıf GEREKMEZ
- 4-5 alakalı hashtag ekle
- Hard sell YAPMA

ÖRNEK FORMAT:
---
Force majeure maddeleri çoğu projede "standart hüküm" olarak geçiliyor.

Ta ki bir kriz çıkana kadar.

Son 3 yılda sektörde force majeure bildirimleri %340 arttı. Ama bildirimlerin sadece %23'ü sözleşmesel olarak geçerli kabul edildi.

Bu uçurum bize bir şey söylüyor: Sözleşmelerimiz değişen dünyaya ayak uyduramadı.

BEIREK olarak bu konuya farklı bakıyoruz.

Force majeure maddesini "hukuki zorunluluk" değil, "risk yönetimi aracı" olarak ele alıyoruz. Sözleşme müzakeresinin en başında şu soruyu soruyoruz:

"Bu proje hangi beklenmedik olaylardan etkilenebilir ve her senaryo için taraflar nasıl davranmalı?"

Bu sorunun cevabını bulmak için projeye özgü risk haritası çıkarıyoruz. Sonra sözleşme dilini buna göre şekillendiriyoruz:
→ Hangi olaylar kapsama girer
→ Bildirim nasıl yapılır
→ Kademeli sonuç mekanizması

Kriz anında taraflar mahkemeye değil, sözleşmeye bakıyor.

Biz böyle çözüyoruz.

Sizin projelerinizde force majeure riski nasıl yönetiliyor?

#projectfinance #contractmanagement #riskmanagement #infrastructure #energyprojects
---

KAYNAK İÇERİK:
{source_content}

KONU:
{topic}
```

### 10.4 Twitter Thread Promptu (twitter_prompt.txt)
```
Sen BEIREK'in Twitter thought leadership yazarısın.

⚠️ VERİLER: Kaynak metindeki rakamları kullan, UYDURMAK YASAK
✅ YORUMLAR: BEIREK perspektifinden özgün analiz
🎯 ÇÖZÜM: Son tweet'te BEIREK'in bu konudaki yaklaşımı
📎 ATIF: Kaynak linki GEREKMEZ

KURALLAR:
- 5-10 tweet arası
- Her tweet max 280 karakter
- Her tweet bağımsız okunabilmeli
- İlk tweet = güçlü hook + gerçek veri
- Ortada = analiz ve BEIREK yorumu
- Son tweet = BEIREK çözümü + engagement
- Numaralı format: 1/, 2/, vb.

YAPI:
1/ [HOOK] Dikkat çekici veri ile aç
2/ [BAĞLAM] Neden önemli?
3/ [VERİ 1] Gerçek rakam/insight
4/ [VERİ 2] Gerçek rakam/insight  
5/ [YORUM] BEIREK analizi - bu ne anlama geliyor?
6/ [ZORLUK] Sektörün yaşadığı sorun
7/ [ÇÖZÜM] BEIREK bu konuda ne yapıyor?
8/ [CTA] Engagement sorusu veya soft CTA

ÖRNEK:
---
1/ 🔋 500MW solar project just hit financial close in Texas.
   $450M investment. Here's why this matters 🧵

2/ Grid-scale solar is booming, but the real story isn't the MW.
   It's how fast deals are closing.

3/ This project went from development to financial close in 18 months.
   Industry average? 24-36 months.

4/ The secret? Streamlined IFI compliance and lender reporting.
   Most projects get stuck here for 6+ months.

5/ At BEIREK, we see this pattern constantly:
   Great projects delayed by documentation chaos.

6/ Our Development Finance team builds lender-grade reporting 
   infrastructure from day one. Result? Faster closes.

7/ The energy transition needs speed. 
   We help developers move faster without cutting corners.

8/ What's slowing down your project's financial close?
   Let's talk → DM open

#renewableenergy #projectfinance #solar
---

KAYNAK İÇERİK:
{source_content}

KONU:
{topic}
```

### 10.5 Kavram Seçim Promptu (concept_selection_prompt.txt)
```
Sen BEIREK için günlük kavram seçim asistanısın.

GÖREV:
Aşağıdaki sözlük listesinden bugün tanıtılacak EN UYGUN kavramı seç.

SEÇİM KRİTERLERİ (ÖNCELİK SIRASINA GÖRE):

1. BEIREK UYUMU (ZORUNLU)
   - 8 çalışma alanından birine doğrudan bağlı olmalı
   - Deal & Contract, CEO Office, Development Finance, Project Development,
     Engineering, Asset Management, GTM & JV, Digital Platforms

2. ÇARPICILIK (ÇOK ÖNEMLİ)
   - Sektörde tartışmalı veya güncel bir konu mu?
   - C-level yöneticilerin ilgisini çeker mi?
   - "Herkesin bildiği sıradan terim" OLMASIN

3. GÜNCEL BAĞLANTI (TERCİH)
   - Bugünkü haberlerle bağlantı kurulabilir mi?
   - Sektördeki aktif tartışmalarla ilişkili mi?

4. TEKRARSIZLIK (ZORUNLU)
   - Daha önce seçilmemiş olmalı

ÇIKTI FORMATI:
---
KAVRAM_EN: [İngilizce terim]
KAVRAM_TR: [Türkçe karşılık]
BEIREK_ALANI: [1-8 arası alan numarası ve adı]
SECIM_NEDENI: [Neden bu kavram seçildi? 1-2 cümle]
TARTISMA_NOKTASI: [Sektördeki güncel tartışma nedir?]
---

SÖZLÜK LİSTESİ:
{glossary_terms}

DAHA ÖNCE KULLANILAN KAVRAMLAR:
{used_concepts}
```

### 10.6 Günlük Kavram İçerik Promptu (concept_content_prompt.txt)
```
Sen BEIREK'in thought leadership yazarısın. Seçilen kavram için 3 formatta içerik üreteceksin.

KAVRAM BİLGİLERİ:
- İngilizce: {concept_en}
- Türkçe: {concept_tr}
- BEIREK Alanı: {beirek_area}
- Seçim Nedeni: {selection_reason}
- Tartışma Noktası: {discussion_point}

═══════════════════════════════════════════════════════════════════
FORMAT 1: MAKALE (1500-2500 kelime)
═══════════════════════════════════════════════════════════════════
Hedef Kitle: C-level, hukuk danışmanları, proje finansçıları
Ton: Akademik-profesyonel, analitik, derinlemesine

YAPI:
1. Dikkat çekici başlık
2. Executive summary (2-3 cümle)
3. Kavram tanımı ve tarihsel bağlam
4. Sektörel önemi - neden şimdi konuşuyoruz?
5. Güncel tartışmalar ve farklı bakış açıları
6. Pratik örnekler ve vaka analizleri
7. BEIREK YAKLAŞIMI:
   - Biz bu konuya nasıl bakıyoruz?
   - Metodolojimiz nedir?
   - Nasıl çözüm sunuyoruz?
8. Sonuç ve soft CTA

═══════════════════════════════════════════════════════════════════
FORMAT 2: LINKEDIN (150-300 kelime)
═══════════════════════════════════════════════════════════════════
Hedef Kitle: Board/C-Level yöneticiler, karar vericiler
Ton: Samimi, şeffaf, çözüm odaklı

YAPI:
1. HOOK: Dikkat çekici açılış (kavramla ilgili şaşırtıcı veri/insight)
2. PROBLEM: Bu kavram neden önemli? Sektör ne yaşıyor?
3. BEIREK YAKLAŞIMI: "Biz bu konuya farklı bakıyoruz..."
   - Bakış açımız
   - Nasıl çözüyoruz?
4. CTA: "Biz böyle çözüyoruz. Sizde bu nasıl yönetiliyor?"

Kurallar:
- Kısa paragraflar
- Samimi ton (kurumsal soğukluk YOK)
- 4-5 hashtag

═══════════════════════════════════════════════════════════════════
FORMAT 3: TWITTER (5-10 tweet)
═══════════════════════════════════════════════════════════════════
Hedef Kitle: Geniş profesyonel kitle
Ton: Punchy, dikkat çekici

YAPI:
1/ Hook + kavram tanımı (thread açılışı)
2/ Neden önemli?
3-5/ Tartışma noktaları, farklı bakış açıları
6-7/ BEIREK perspektifi
8/ Engagement sorusu

Kurallar:
- Her tweet max 280 karakter
- Her tweet bağımsız okunabilmeli
- Numaralı format (1/, 2/, vb.)
```

---

## 11. KONFİGÜRASYON DOSYALARI

### 11.1 config.yaml
```yaml
# BEIREK Content Scout Configuration

app:
  name: "BEIREK Content Scout"
  version: "1.0.0"

scanning:
  max_articles_per_source: 10
  lookback_hours: 48
  batch_size: 10
  timeout_seconds: 30

filtering:
  min_relevance_score: 7
  claude_model: "default"

generation:
  article_min_words: 1500
  article_max_words: 2500
  linkedin_min_words: 150
  linkedin_max_words: 300
  twitter_min_tweets: 5
  twitter_max_tweets: 10

storage:
  base_path: "./outputs"
  archive_after_days: 30
  
database:
  path: "./data/scout.db"

ui:
  show_emojis: true
  color_output: true
```

### 11.2 sources.yaml (Örnek)
```yaml
# Kaynak Listesi

solar:
  - name: "PV Magazine"
    url: "https://pv-magazine.com"
    rss: "https://pv-magazine.com/feed/"
    priority: 1
    
  - name: "Solar Power World"
    url: "https://solarpowerworld.com"
    rss: "https://solarpowerworld.com/feed/"
    priority: 1

wind:
  - name: "Recharge News"
    url: "https://rechargenews.com"
    rss: "https://rechargenews.com/feed/"
    priority: 1

storage:
  - name: "Energy Storage News"
    url: "https://energy-storage.news"
    rss: "https://energy-storage.news/feed/"
    priority: 1

datacenter:
  - name: "Data Center Dynamics"
    url: "https://datacenterdynamics.com"
    rss: "https://datacenterdynamics.com/feed/"
    priority: 1

project_finance:
  - name: "IJ Global"
    url: "https://ijglobal.com"
    rss: null  # Scraping required
    priority: 1

# ... diğer kaynaklar
```

---

## 12. HATA YÖNETİMİ

### 12.1 Olası Hatalar ve Çözümler

| Hata | Sebep | Çözüm |
|------|-------|-------|
| RSS timeout | Kaynak yavaş/çökmüş | Skip et, sonraki kaynağa geç |
| Claude CLI error | CLI kurulu değil | Kullanıcıya uyarı göster |
| Rate limit | Çok hızlı istek | Exponential backoff uygula |
| Parse error | HTML yapısı değişmiş | Fallback parser kullan |
| Disk full | Yer yok | Eski dosyaları arşivle/sil |

### 12.2 Logging
```
data/logs/
├── scout_2026-01-30.log      # Günlük log
├── errors_2026-01-30.log     # Sadece hatalar
└── claude_calls.log          # Claude çağrı geçmişi
```

---

## 13. DETAYLI GELİŞTİRME PLANI

Bu bölüm, projenin sıfırdan tamamlanmasına kadar atılacak **her adımı** detaylı olarak tanımlar.

---

### ADIM 1: PROJE İSKELETİ OLUŞTURMA

**Amaç:** Tüm klasör yapısını ve boş dosyaları oluşturmak.

**1.1 Ana Proje Klasörü**
```
beirek-content-scout/
├── main.py
├── config.yaml
├── sources.yaml
├── requirements.txt
├── README.md
├── .gitignore
│
├── modules/
│   ├── __init__.py
│   ├── scanner.py
│   ├── filter.py
│   ├── generator.py
│   ├── storage.py
│   ├── ui.py
│   ├── concept_manager.py      # Günlük kavram yönetimi
│   └── request_manager.py      # İstek havuzu yönetimi
│
├── prompts/
│   ├── filter_prompt.txt
│   ├── article_prompt.txt
│   ├── linkedin_prompt.txt
│   ├── twitter_prompt.txt
│   ├── concept_selection_prompt.txt
│   └── concept_content_prompt.txt
│
├── data/
│   ├── scout.db               # (otomatik oluşur)
│   └── cache/
│
└── logs/
```

**1.2 Oluşturulacak Dosyalar (Sırayla)**

| # | Dosya | İçerik | Bağımlılık |
|---|-------|--------|------------|
| 1 | `.gitignore` | Python standart + data/, logs/, cache/ | - |
| 2 | `requirements.txt` | Tüm Python paketleri | - |
| 3 | `config.yaml` | Uygulama ayarları | - |
| 4 | `sources.yaml` | 300+ kaynak listesi | - |
| 5 | `modules/__init__.py` | Boş (modül tanımlama) | - |
| 6 | Tüm prompt dosyaları | PRD'deki promptlar | - |

**1.3 requirements.txt İçeriği**
```
feedparser>=6.0.0
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
pyyaml>=6.0.0
rich>=13.0.0
python-dateutil>=2.8.0
```

**1.4 config.yaml İçeriği**
```yaml
# BEIREK Content Scout Ayarları

app:
  name: "BEIREK Content Scout"
  version: "1.0.0"

database:
  path: "data/scout.db"

scanning:
  max_articles_per_source: 10
  scan_interval_hours: 24
  timeout_seconds: 30

filtering:
  min_relevance_score: 7
  batch_size: 10

content:
  output_base_path: "../content"

beirek_areas:
  1: "deal-contract-advisory"
  2: "ceo-office-governance"
  3: "development-finance-compliance"
  4: "project-development-finance"
  5: "engineering-delivery"
  6: "asset-management-om"
  7: "gtm-jv-management"
  8: "digital-platforms"

logging:
  level: "INFO"
  path: "logs/"
```

**1.5 Çıktı:** İskelet klasör yapısı hazır, tüm boş dosyalar yerinde.

---

### ADIM 2: VERİTABANI MODÜLÜ (storage.py)

**Amaç:** SQLite veritabanı oluşturma ve tüm CRUD işlemlerini tanımlama.

**2.1 Veritabanı Başlatma Fonksiyonu**
```python
def init_database() -> None:
    """
    Veritabanını oluşturur, tüm tabloları oluşturur.

    Çalışma:
    1. data/scout.db dosyasını oluştur (yoksa)
    2. Tüm CREATE TABLE ifadelerini çalıştır
    3. Varsayılan verileri ekle (kaynaklar)

    Tablolar:
    - sources
    - articles
    - generated_content
    - scan_history
    - glossary
    - daily_concepts
    - content_requests
    """
```

**2.2 Kaynak (Sources) İşlemleri**
```python
def add_source(name: str, url: str, rss_url: str = None, category: str = None, priority: int = 2) -> int:
    """Yeni kaynak ekler, ID döner"""

def get_active_sources() -> list[dict]:
    """Aktif kaynakları döner"""

def update_source_last_checked(source_id: int) -> None:
    """Kaynağın son tarama zamanını günceller"""

def deactivate_source(source_id: int) -> None:
    """Kaynağı deaktif yapar"""
```

**2.3 Makale (Articles) İşlemleri**
```python
def add_article(source_id: int, title: str, url: str, summary: str = None, published_at: datetime = None) -> int:
    """Yeni makale ekler, ID döner"""

def article_exists(url: str) -> bool:
    """URL daha önce kaydedildi mi kontrol eder"""

def update_article_relevance(article_id: int, score: float, is_relevant: bool) -> None:
    """Makaleye relevance score atar"""

def get_relevant_articles(limit: int = 50) -> list[dict]:
    """İlgili ve seçilmemiş makaleleri döner"""

def mark_article_selected(article_id: int) -> None:
    """Makaleyi seçilmiş olarak işaretler"""

def mark_article_processed(article_id: int) -> None:
    """Makaleyi işlenmiş olarak işaretler"""

def get_pending_articles() -> list[dict]:
    """Seçilmiş ama işlenmemiş makaleleri döner"""
```

**2.4 Üretilen İçerik İşlemleri**
```python
def save_generated_content(article_id: int, content_type: str, title: str, content: str, file_path: str) -> int:
    """Üretilen içeriği kaydeder"""

def get_content_by_article(article_id: int) -> list[dict]:
    """Bir makale için üretilen tüm içerikleri döner"""

def mark_content_published(content_id: int) -> None:
    """İçeriği yayınlandı olarak işaretler"""
```

**2.5 Tarama Geçmişi**
```python
def start_scan() -> int:
    """Yeni tarama kaydı başlatır, ID döner"""

def complete_scan(scan_id: int, sources_scanned: int, articles_found: int, articles_relevant: int, status: str = 'completed') -> None:
    """Tarama kaydını tamamlar"""

def get_last_scan() -> dict:
    """Son tarama bilgisini döner"""
```

**2.6 Sözlük (Glossary) İşlemleri**
```python
def import_glossary_from_file(file_path: str) -> int:
    """
    Sözlük dosyasını veritabanına aktarır.

    Girdi: Markdown veya CSV formatında sözlük dosyası
    Çıktı: Eklenen terim sayısı

    İşlem:
    1. Dosyayı satır satır oku
    2. Her satırı parse et (term_en, term_tr, category)
    3. glossary tablosuna ekle
    4. Toplam sayıyı döner
    """

def get_unused_terms(limit: int = 100) -> list[dict]:
    """Henüz kullanılmamış terimleri döner"""

def mark_term_used(term_id: int, used_date: date) -> None:
    """Terimi kullanıldı olarak işaretler"""

def get_term_by_id(term_id: int) -> dict:
    """ID ile terim bilgisi döner"""

def search_terms(query: str) -> list[dict]:
    """Terim arar (İngilizce veya Türkçe)"""
```

**2.7 Günlük Kavram İşlemleri**
```python
def add_daily_concept(glossary_id: int, concept_en: str, concept_tr: str, beirek_area: str, beirek_subarea: str, selection_reason: str) -> int:
    """Günlük kavram kaydı oluşturur"""

def get_today_concept() -> dict | None:
    """Bugün için seçilen kavramı döner (varsa)"""

def get_concept_history(days: int = 30) -> list[dict]:
    """Son N günün kavramlarını döner"""

def update_concept_content_path(concept_id: int, content_path: str) -> None:
    """Kavram içerik yolunu günceller"""
```

**2.8 İstek Havuzu İşlemleri**
```python
def add_content_request(folder_name: str, topic: str = None, brief: str = None) -> int:
    """Yeni içerik isteği oluşturur"""

def get_pending_requests() -> list[dict]:
    """Bekleyen istekleri döner"""

def update_request_status(request_id: int, status: str) -> None:
    """İstek durumunu günceller"""

def complete_request(request_id: int, beirek_area: str, content_path: str) -> None:
    """İsteği tamamlandı olarak işaretler"""
```

**2.9 İstatistik Fonksiyonları**
```python
def get_stats() -> dict:
    """
    Genel istatistikleri döner:
    - total_sources: Toplam kaynak sayısı
    - total_articles: Toplam makale sayısı
    - relevant_articles: İlgili makale sayısı
    - processed_articles: İşlenmiş makale sayısı
    - total_content: Üretilen içerik sayısı
    - today_scans: Bugünkü tarama sayısı
    - total_concepts: Kullanılan kavram sayısı
    - pending_requests: Bekleyen istek sayısı
    """
```

**2.10 Çıktı:** Tam çalışan veritabanı modülü, tüm CRUD işlemleri hazır.

---

### ADIM 3: KAYNAK YÖNETİMİ (sources.yaml)

**Amaç:** 300+ haber kaynağını yapılandırmak.

**3.1 Kaynak Formatı**
```yaml
sources:
  # Birincil Kaynaklar (Yüksek Öncelik)
  primary:
    - name: "Utility Dive"
      url: "https://www.utilitydive.com"
      rss_url: "https://www.utilitydive.com/feeds/news/"
      category: "energy"
      priority: 1

    - name: "PV Magazine"
      url: "https://www.pv-magazine.com"
      rss_url: "https://www.pv-magazine.com/feed/"
      category: "solar"
      priority: 1

    # ... (50+ birincil kaynak)

  # İkincil Kaynaklar (Orta Öncelik)
  secondary:
    - name: "Energy Storage News"
      url: "https://www.energy-storage.news"
      rss_url: "https://www.energy-storage.news/feed/"
      category: "storage"
      priority: 2

    # ... (100+ ikincil kaynak)

  # Üçüncül Kaynaklar (Düşük Öncelik)
  tertiary:
    - name: "Reuters Energy"
      url: "https://www.reuters.com/business/energy/"
      rss_url: null  # RSS yok, scraping gerekli
      category: "general"
      priority: 3

    # ... (150+ üçüncül kaynak)
```

**3.2 Kaynak Kategorileri**
- `energy`: Genel enerji haberleri
- `solar`: Güneş enerjisi özel
- `wind`: Rüzgar enerjisi özel
- `storage`: Enerji depolama
- `grid`: Şebeke ve iletim
- `finance`: Proje finansmanı
- `policy`: Politika ve düzenleme
- `datacenter`: Veri merkezi
- `hydrogen`: Hidrojen ve yeşil yakıtlar
- `general`: Genel iş haberleri

**3.3 Çıktı:** Tam kaynak listesi (300+ kaynak) yapılandırılmış.

---

### ADIM 4: TARAMA MODÜLÜ (scanner.py)

**Amaç:** RSS ve web scraping ile haber toplama.

**4.1 Temel Fonksiyonlar**

```python
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import Optional
import yaml

class NewsScanner:
    def __init__(self, config_path: str = "config.yaml"):
        """
        Scanner'ı başlatır, ayarları yükler.

        İşlem:
        1. config.yaml oku
        2. sources.yaml oku
        3. Veritabanı bağlantısı al
        """

    def load_sources(self) -> list[dict]:
        """
        sources.yaml'dan kaynakları yükler.

        Çıktı: [
            {"name": "...", "url": "...", "rss_url": "...", "category": "...", "priority": 1},
            ...
        ]
        """

    def fetch_rss_feed(self, rss_url: str, max_items: int = 10) -> list[dict]:
        """
        RSS feed'den makaleleri çeker.

        Girdi: RSS URL, maksimum makale sayısı
        Çıktı: [
            {
                "title": "...",
                "url": "...",
                "summary": "...",
                "published_at": datetime,
                "source_name": "..."
            },
            ...
        ]

        Hata Yönetimi:
        - Timeout: 30 saniye sonra atla
        - Parse hatası: Loglayıp devam et
        - 404/500: Kaynağı geçici deaktif et
        """

    def scrape_website(self, url: str, max_items: int = 10) -> list[dict]:
        """
        RSS olmayan sitelerden scraping yapar.

        İşlem:
        1. Ana sayfayı çek
        2. Makale linklerini bul (site-specific selectors)
        3. Her makale için başlık ve özet çek

        Desteklenen Siteler:
        - Reuters: div.article-list
        - Bloomberg: section.market-news
        - (site başına özel selector tanımla)
        """

    def extract_article_content(self, url: str) -> dict:
        """
        Makale sayfasından tam içeriği çeker.

        Çıktı: {
            "title": "...",
            "content": "... (tam metin)",
            "author": "...",
            "date": datetime,
            "images": ["url1", "url2"]
        }

        Kullanılan Teknikler:
        - Readability algoritması
        - BeautifulSoup ile <article> tag'i
        - Meta tag'lerden bilgi çekme
        """

    def is_recent(self, published_at: datetime, hours: int = 48) -> bool:
        """Son N saat içinde mi kontrol eder"""

    def is_already_scanned(self, url: str) -> bool:
        """URL daha önce tarandı mı (veritabanı kontrolü)"""

    def scan_source(self, source: dict) -> list[dict]:
        """
        Tek bir kaynağı tarar.

        İşlem:
        1. RSS URL varsa fetch_rss_feed çağır
        2. RSS yoksa scrape_website çağır
        3. Her makale için is_already_scanned kontrol et
        4. Yeni makaleleri döner
        """

    def scan_all_sources(self, priority_filter: int = None) -> dict:
        """
        Tüm kaynakları tarar.

        Girdi: priority_filter (1, 2, 3 veya None=hepsi)

        İşlem:
        1. scan_history'de yeni kayıt başlat
        2. Her kaynağı sırayla tara (progress göster)
        3. Yeni makaleleri veritabanına kaydet
        4. scan_history'yi güncelle

        Çıktı: {
            "scan_id": 123,
            "sources_scanned": 45,
            "articles_found": 156,
            "new_articles": 89,
            "errors": ["source1: timeout", ...]
        }
        """
```

**4.2 Hata Yönetimi Stratejisi**
```python
class ScanError(Exception):
    """Tarama hatası base class"""

class RSSParseError(ScanError):
    """RSS parse hatası"""

class ScrapingError(ScanError):
    """Web scraping hatası"""

class TimeoutError(ScanError):
    """Timeout hatası"""

def handle_scan_error(source: dict, error: Exception) -> None:
    """
    Tarama hatasını yönetir.

    Stratejiler:
    - Timeout: 3 deneme, sonra atla
    - 404: Kaynağı kontrol et, deaktif et
    - Parse: Loglayıp devam et
    - Diğer: Logla, sonraki kaynağa geç
    """
```

**4.3 Çıktı:** Tam çalışan tarama modülü, tüm kaynaklardan haber çekebilir.

---

### ADIM 5: FİLTRELEME MODÜLÜ (filter.py)

**Amaç:** Claude CLI ile haberleri filtreleme ve skorlama.

**5.1 Temel Fonksiyonlar**

```python
import subprocess
import json
from typing import Optional

class ArticleFilter:
    def __init__(self, prompt_path: str = "prompts/filter_prompt.txt"):
        """
        Filter'ı başlatır.

        İşlem:
        1. filter_prompt.txt oku
        2. Claude CLI erişilebilirliğini kontrol et
        """

    def check_claude_cli(self) -> bool:
        """
        Claude CLI kurulu ve çalışıyor mu kontrol eder.

        Komut: claude --version
        """

    def prepare_batch_prompt(self, articles: list[dict]) -> str:
        """
        Makale batch'ini filtreleme promptuna hazırlar.

        Girdi: [
            {"id": 1, "title": "...", "summary": "...", "source": "..."},
            ...
        ]

        Çıktı: Prompt metni (filter_prompt.txt + makale listesi)

        Format:
        ```
        {filter_prompt içeriği}

        MAKALELER:

        [1] Başlık: Texas Solar Project...
        Kaynak: Utility Dive
        Özet: ...

        [2] Başlık: ...
        ...
        ```
        """

    def call_claude_cli(self, prompt: str) -> str:
        """
        Claude CLI'ı çağırır.

        Komut: echo "{prompt}" | claude

        Hata Yönetimi:
        - Timeout: 120 saniye
        - Hata: 3 deneme
        - Boş yanıt: Retry
        """

    def parse_filter_response(self, response: str) -> list[dict]:
        """
        Claude yanıtını parse eder.

        Beklenen Format:
        ```json
        [
            {"id": 1, "score": 9, "relevant": true, "reason": "..."},
            {"id": 2, "score": 3, "relevant": false, "reason": "..."},
            ...
        ]
        ```

        Hata Yönetimi:
        - JSON parse hatası: Regex ile çıkar
        - Eksik alan: Varsayılan değer ata
        """

    def filter_articles(self, articles: list[dict], batch_size: int = 10) -> list[dict]:
        """
        Ana filtreleme fonksiyonu.

        İşlem:
        1. Makaleleri batch_size'lık gruplara böl
        2. Her batch için:
           a. prepare_batch_prompt çağır
           b. call_claude_cli çağır
           c. parse_filter_response çağır
           d. Sonuçları birleştir
        3. Veritabanında relevance score güncelle
        4. score >= 7 olanları döner

        Çıktı: [
            {"id": 1, "title": "...", "score": 9, "reason": "...", ...},
            ...
        ]
        """

    def get_beirek_area(self, article: dict) -> tuple[str, str]:
        """
        Makale için BEIREK alanını belirler.

        İşlem:
        1. Claude'a makale içeriğini gönder
        2. 8 BEIREK alanından en uygununu seç
        3. Alt alanı da belirle

        Çıktı: ("4-project-development-finance", "3-project-finance-structuring")
        """
```

**5.2 Filtreleme Promptu (filter_prompt.txt)**
PRD'de tanımlanan prompt kullanılacak. Önemli noktalar:
- BEIREK ilgi alanları açıkça tanımlı
- 0-10 arası skorlama
- JSON formatında yanıt beklentisi

**5.3 Çıktı:** Makaleleri akıllıca filtreleyen modül hazır.

---

### ADIM 6: İÇERİK ÜRETİM MODÜLÜ (generator.py)

**Amaç:** 3 formatta (makale, LinkedIn, Twitter) içerik üretimi.

**6.1 Temel Fonksiyonlar**

```python
class ContentGenerator:
    def __init__(self):
        """
        Generator'ı başlatır.

        İşlem:
        1. Tüm prompt dosyalarını oku
        2. Prompt template'leri hazırla
        """
        self.prompts = {
            'article': self._load_prompt('article_prompt.txt'),
            'linkedin': self._load_prompt('linkedin_prompt.txt'),
            'twitter': self._load_prompt('twitter_prompt.txt'),
            'concept_selection': self._load_prompt('concept_selection_prompt.txt'),
            'concept_content': self._load_prompt('concept_content_prompt.txt')
        }

    def _load_prompt(self, filename: str) -> str:
        """Prompt dosyasını okur"""

    def fetch_full_article(self, url: str) -> str:
        """
        Makale URL'inden tam içeriği çeker.

        İşlem:
        1. URL'i aç
        2. Ana içeriği çıkar (readability)
        3. HTML temizle
        4. Metin olarak döner
        """

    def prepare_generation_prompt(self, template: str, source_content: str, topic: str, additional_context: dict = None) -> str:
        """
        Üretim promptunu hazırlar.

        İşlem:
        1. Template'e source_content ekle
        2. Topic ekle
        3. Ek bağlam varsa ekle
        4. Final promptu döner
        """

    def call_claude_generate(self, prompt: str, max_tokens: int = 4000) -> str:
        """
        Claude CLI ile içerik üretir.

        Komut: echo "{prompt}" | claude

        Parametreler:
        - max_tokens: İçerik uzunluğu kontrolü
        - Timeout: 180 saniye (içerik üretimi uzun sürebilir)
        """

    def generate_article(self, source_content: str, topic: str, beirek_area: str) -> str:
        """
        Research-grade makale üretir.

        Girdi:
        - source_content: Kaynak haber metni
        - topic: Konu başlığı
        - beirek_area: İçeriğin kaydedileceği BEIREK alanı

        Çıktı: Markdown formatında makale (1500-2500 kelime)

        Doğrulama:
        - Kelime sayısı kontrolü
        - Uydurma veri kontrolü (kaynak içerikte olmayan rakamlar)
        - BEIREK perspektifi kontrolü
        """

    def generate_linkedin(self, source_content: str, topic: str) -> str:
        """
        LinkedIn post üretir.

        Çıktı: 150-300 kelime, 4 bölüm yapısında

        Yapı Kontrolü:
        - Hook var mı?
        - Problem tanımı var mı?
        - BEIREK yaklaşımı var mı?
        - CTA var mı?
        """

    def generate_twitter(self, source_content: str, topic: str) -> str:
        """
        Twitter thread üretir.

        Çıktı: 5-10 tweet, numaralı format

        Kontroller:
        - Her tweet 280 karakter altında mı?
        - Numaralandırma doğru mu?
        - Thread bütünlüğü var mı?
        """

    def generate_all_formats(self, source_content: str, topic: str, beirek_area: str) -> dict:
        """
        Tüm formatları tek seferde üretir.

        İşlem:
        1. generate_article çağır
        2. generate_linkedin çağır
        3. generate_twitter çağır

        Çıktı: {
            "article": "...",
            "linkedin": "...",
            "twitter": "...",
            "metadata": {
                "topic": "...",
                "beirek_area": "...",
                "generated_at": datetime,
                "word_counts": {"article": 1800, "linkedin": 245, "twitter": 320}
            }
        }
        """

    def validate_content(self, content: str, content_type: str) -> tuple[bool, list[str]]:
        """
        Üretilen içeriği doğrular.

        Kontroller:
        - Uzunluk (min/max)
        - Format (markdown, numaralandırma vb.)
        - Yasak kelimeler (halüsinasyon işaretleri)

        Çıktı: (geçerli_mi, hata_listesi)
        """
```

**6.2 Anti-Halüsinasyon Sistemi**
```python
class HallucinationChecker:
    def __init__(self):
        """Halüsinasyon kontrol sistemi"""

    def extract_facts(self, content: str) -> list[dict]:
        """
        İçerikten faktleri (rakam, isim, tarih) çıkarır.

        Çıktı: [
            {"type": "number", "value": "500MW", "context": "..."},
            {"type": "name", "value": "Nextera Energy", "context": "..."},
            {"type": "date", "value": "2027", "context": "..."}
        ]
        """

    def verify_facts(self, facts: list[dict], source_content: str) -> list[dict]:
        """
        Faktlerin kaynak içerikte olup olmadığını kontrol eder.

        Çıktı: [
            {"fact": {...}, "verified": True, "source_match": "..."},
            {"fact": {...}, "verified": False, "warning": "Kaynakta bulunamadı"}
        ]
        """

    def check_content(self, generated_content: str, source_content: str) -> dict:
        """
        Tam halüsinasyon kontrolü yapar.

        Çıktı: {
            "passed": True/False,
            "facts_checked": 15,
            "facts_verified": 14,
            "warnings": ["Şu rakam kaynakta yok: ..."],
            "confidence": 0.93
        }
        """
```

**6.3 Çıktı:** 3 formatta içerik üretebilen, halüsinasyon kontrolü yapan modül.

---

### ADIM 7: GÜNLÜK KAVRAM YÖNETİMİ (concept_manager.py)

**Amaç:** 7000+ terimlik sözlükten günlük kavram seçimi ve içerik üretimi.

**7.1 Sözlük Yükleme**
```python
class ConceptManager:
    def __init__(self, glossary_path: str = "content/9-daily-concepts/kavram-sozlugu.md"):
        """
        Kavram yöneticisini başlatır.

        İşlem:
        1. Sözlük dosyasını kontrol et
        2. Veritabanı bağlantısı al
        """

    def import_glossary(self) -> int:
        """
        Sözlük dosyasını veritabanına aktarır.

        Format Beklentisi (Markdown):
        | # | Kavram (EN) | Kavram (TR) | Kategori |
        |---|-------------|-------------|----------|
        | 1 | Term Sheet | Ön Protokol | finance |

        İşlem:
        1. Markdown tablosunu parse et
        2. Her satırı glossary tablosuna ekle
        3. Toplam eklenen sayıyı döner
        """

    def get_unused_terms(self, category: str = None, limit: int = 50) -> list[dict]:
        """
        Henüz kullanılmamış terimleri döner.

        Girdi:
        - category: Belirli kategori filtresi (opsiyonel)
        - limit: Maksimum sayı

        Çıktı: [
            {"id": 1, "term_en": "...", "term_tr": "...", "category": "..."},
            ...
        ]
        """
```

**7.2 Kavram Seçimi**
```python
    def select_daily_concept(self, recent_news: list[dict] = None) -> dict:
        """
        Günün kavramını seçer.

        İşlem:
        1. Bugün için zaten seçilmiş kavram var mı kontrol et
        2. Varsa onu döner
        3. Yoksa:
           a. Kullanılmamış terimleri al
           b. Claude'a seçim promptunu gönder
           c. Seçilen kavramı daily_concepts'e kaydet
           d. glossary'de is_used=1 yap

        Seçim Kriterleri:
        - BEIREK alanlarından birine uygun
        - Çarpıcı, ilgi çekici
        - Güncel haberlerle bağlantı kurulabilir (varsa)
        - Daha önce seçilmemiş

        Çıktı: {
            "id": 1,
            "concept_en": "Force Majeure",
            "concept_tr": "Mücbir Sebep",
            "beirek_area": "1-deal-contract-advisory",
            "beirek_subarea": "3-contract-lifecycle-management",
            "selection_reason": "..."
        }
        """

    def _call_claude_for_selection(self, unused_terms: list[dict], recent_news: list[dict]) -> dict:
        """
        Claude'a kavram seçimi yaptırır.

        Prompt: concept_selection_prompt.txt

        Girdi:
        - Kullanılmamış terimler listesi
        - Son günün haberleri (varsa)

        Çıktı: Seçilen kavram bilgileri
        """
```

**7.3 Kavram İçerik Üretimi**
```python
    def generate_concept_content(self, concept: dict) -> dict:
        """
        Seçilen kavram için 3 formatta içerik üretir.

        İşlem:
        1. Kavram hakkında ek bilgi topla (web araması opsiyonel)
        2. concept_content_prompt ile içerik üret
        3. 3 formatı ayrı ayrı kaydet

        Çıktı: {
            "article": "...",
            "linkedin": "...",
            "twitter": "...",
            "content_path": "content/9-daily-concepts/2026-01-30_kavram_force-majeure/"
        }
        """

    def save_concept_content(self, concept: dict, content: dict) -> str:
        """
        Kavram içeriğini dosyalara kaydeder.

        Klasör: content/9-daily-concepts/{tarih}_kavram_{slug}/
        Dosyalar:
        - makale.md
        - linkedin.md
        - twitter.md

        Çıktı: Klasör yolu
        """

    def run_daily_concept_flow(self) -> dict:
        """
        Tam günlük kavram akışını çalıştırır.

        İşlem:
        1. select_daily_concept çağır
        2. generate_concept_content çağır
        3. save_concept_content çağır
        4. Veritabanını güncelle

        Çıktı: {
            "concept": {...},
            "content_generated": True,
            "content_path": "...",
            "word_counts": {...}
        }
        """
```

**7.4 Çıktı:** Tam çalışan günlük kavram sistemi.

---

### ADIM 8: İSTEK HAVUZU YÖNETİMİ (request_manager.py)

**Amaç:** Manuel içerik taleplerini yönetme.

**8.1 Temel Fonksiyonlar**
```python
import os
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RequestManager:
    def __init__(self, request_pool_path: str = "content/10-istek-havuzu"):
        """
        İstek havuzu yöneticisini başlatır.
        """
        self.pool_path = Path(request_pool_path)

    def scan_request_pool(self) -> list[dict]:
        """
        İstek havuzunu tarar, yeni klasörleri bulur.

        İşlem:
        1. 10-istek-havuzu altındaki klasörleri listele
        2. NASIL-KULLANILIR.md hariç tut
        3. Her klasör için:
           a. brief.md var mı kontrol et
           b. İçerik dosyaları (makale.md, linkedin.md, twitter.md) var mı
           c. Durumu belirle (pending, completed)

        Çıktı: [
            {
                "folder_name": "texas-grid-modernization",
                "folder_path": "content/10-istek-havuzu/texas-grid-modernization",
                "has_brief": True,
                "brief_content": "...",
                "status": "pending",
                "created_at": datetime
            },
            ...
        ]
        """

    def parse_brief(self, brief_path: str) -> dict:
        """
        brief.md dosyasını parse eder.

        Beklenen Format:
        ```markdown
        # Konu
        Texas Grid Modernization

        # Odak
        - $5B yatırım planı
        - Battery storage entegrasyonu

        # Hedef Kitle
        - Utility yöneticileri

        # BEIREK Alanı
        4-project-development-finance/3-project-finance-structuring
        ```

        Çıktı: {
            "topic": "Texas Grid Modernization",
            "focus_points": ["$5B yatırım planı", ...],
            "target_audience": ["Utility yöneticileri"],
            "beirek_area": "4-project-development-finance",
            "beirek_subarea": "3-project-finance-structuring"
        }
        """

    def process_request(self, request: dict) -> dict:
        """
        Tek bir isteği işler.

        İşlem:
        1. Brief varsa oku ve parse et
        2. Brief yoksa klasör adından konu çıkar
        3. Web'den ilgili bilgi topla (opsiyonel)
        4. 3 formatta içerik üret
        5. Dosyaları klasöre kaydet
        6. İlgili BEIREK alanına kopyala
        7. Veritabanını güncelle

        Çıktı: {
            "request_id": 1,
            "content_generated": True,
            "files_created": ["makale.md", "linkedin.md", "twitter.md"],
            "copied_to": "content/4-project-development-finance/..."
        }
        """

    def copy_to_beirek_area(self, source_folder: str, beirek_area: str, beirek_subarea: str) -> str:
        """
        İçeriği BEIREK alanına kopyalar.

        Çıktı: Hedef klasör yolu
        """

    def process_all_pending(self) -> dict:
        """
        Tüm bekleyen istekleri işler.

        Çıktı: {
            "processed": 3,
            "success": 3,
            "failed": 0,
            "details": [...]
        }
        """
```

**8.2 Klasör İzleme (Opsiyonel)**
```python
class RequestFolderWatcher(FileSystemEventHandler):
    """
    İstek havuzu klasörünü izler, yeni klasör eklenince tetiklenir.
    """

    def on_created(self, event):
        """Yeni klasör oluşturulduğunda çağrılır"""

    def start_watching(self):
        """Klasör izlemeyi başlatır (daemon thread)"""
```

**8.3 Çıktı:** İstek havuzu tam çalışır durumda.

---

### ADIM 9: DOSYA KAYDETME SİSTEMİ (storage.py - Ek)

**Amaç:** İçerikleri doğru klasörlere kaydetme.

**9.1 Dosya İşlemleri**
```python
class ContentStorage:
    def __init__(self, base_path: str = "content"):
        self.base_path = Path(base_path)

    def get_beirek_folder_path(self, beirek_area: str, beirek_subarea: str = None) -> Path:
        """
        BEIREK alan klasör yolunu döner.

        Girdi: "4-project-development-finance", "3-project-finance-structuring"
        Çıktı: Path("content/4-project-development-finance/3-project-finance-structuring")
        """

    def create_content_folder(self, beirek_area: str, beirek_subarea: str, content_type: str, slug: str) -> Path:
        """
        İçerik klasörü oluşturur.

        Format: {tarih}_{tür}_{slug}/

        Örnek:
        content/4-project-development-finance/3-project-finance-structuring/
        └── 2026-01-30_haber_texas-solar-milestone/
        """

    def generate_slug(self, title: str) -> str:
        """
        SEO-friendly slug üretir.

        "Texas Solar Project Reaches $500M Milestone"
        → "texas-solar-project-reaches-500m-milestone"
        """

    def save_content_files(self, folder_path: Path, content: dict) -> list[str]:
        """
        İçerik dosyalarını kaydeder.

        Dosyalar:
        - makale.md
        - linkedin.md
        - twitter.md

        Çıktı: Oluşturulan dosya yolları listesi
        """

    def add_frontmatter(self, content: str, metadata: dict) -> str:
        """
        Markdown içeriğe frontmatter ekler.

        Format:
        ```
        ---
        title: "..."
        date: "2026-01-30"
        beirek_area: "..."
        source_url: "..."
        ---

        {content}
        ```
        """
```

**9.2 Çıktı:** İçerikler doğru klasörlere kaydediliyor.

---

### ADIM 10: TERMİNAL ARAYÜZÜ (ui.py)

**Amaç:** Kullanıcı dostu CLI arayüzü.

**10.1 Rich Kütüphanesi ile UI**
```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm

console = Console()

class TerminalUI:
    def __init__(self):
        self.console = Console()

    def show_banner(self):
        """Uygulama banner'ını gösterir"""

    def show_main_menu(self) -> str:
        """
        Ana menüyü gösterir.

        ╔═══════════════════════════════════════╗
        ║     BEIREK Content Scout v1.0         ║
        ╠═══════════════════════════════════════╣
        ║  [1] 🔍 Yeni Tarama Başlat            ║
        ║  [2] 📰 Günlük Kavram Üret            ║
        ║  [3] 📋 İstek Havuzunu İşle           ║
        ║  [4] 📊 Bekleyen İçerikler            ║
        ║  [5] ✍️  İçerik Üret                   ║
        ║  [6] 📈 İstatistikler                 ║
        ║  [7] ⚙️  Ayarlar                       ║
        ║  [8] 🚪 Çıkış                         ║
        ╚═══════════════════════════════════════╝

        Çıktı: Seçilen menü numarası
        """

    def show_scan_progress(self, total_sources: int):
        """
        Tarama ilerlemesini gösterir.

        [████████████░░░░░░░░] 65/100 sources
        Current: Utility Dive
        Found: 45 articles
        """

    def show_article_table(self, articles: list[dict]) -> list[int]:
        """
        Filtrelenmiş makaleleri tablo olarak gösterir.

        ┌────┬─────────────────────────────────┬───────┬───────────────┐
        │ #  │ Başlık                          │ Skor  │ Kaynak        │
        ├────┼─────────────────────────────────┼───────┼───────────────┤
        │ 1  │ Texas Solar Project...          │ 9/10  │ Utility Dive  │
        │ 2  │ BESS Market Growth...           │ 8/10  │ PV Magazine   │
        └────┴─────────────────────────────────┴───────┴───────────────┘

        Seçim: 1,2,3 veya all
        """

    def show_article_detail(self, article: dict):
        """Makale detayını panel içinde gösterir"""

    def show_generation_options(self) -> list[str]:
        """
        Üretim formatı seçimi.

        Hangi formatlar üretilsin?
        [1] 📝 Sadece Makale
        [2] 💼 Sadece LinkedIn
        [3] 🐦 Sadece Twitter
        [4] 📝💼🐦 Hepsi (Önerilen)
        """

    def show_generation_progress(self, article_title: str, format_name: str):
        """
        Üretim ilerlemesini gösterir.

        Üretiliyor: "Texas Solar Project..."
        ├─ [✓] Makale (1847 kelime)
        ├─ [◐] LinkedIn...
        └─ [ ] Twitter
        """

    def show_summary(self, stats: dict):
        """
        İşlem özetini gösterir.

        ╔═══════════════════════════════════════╗
        ║           İşlem Tamamlandı            ║
        ╠═══════════════════════════════════════╣
        ║  Taranan kaynak:     45               ║
        ║  Bulunan makale:     156              ║
        ║  İlgili makale:      23               ║
        ║  Üretilen içerik:    9                ║
        ╚═══════════════════════════════════════╝
        """

    def show_concept_info(self, concept: dict):
        """Günün kavramını gösterir"""

    def show_request_list(self, requests: list[dict]):
        """İstek havuzundaki talepleri listeler"""

    def confirm(self, message: str) -> bool:
        """Onay alır"""

    def show_error(self, error: str):
        """Hata mesajı gösterir"""

    def show_success(self, message: str):
        """Başarı mesajı gösterir"""
```

**10.2 Çıktı:** Kullanıcı dostu, görsel CLI arayüzü.

---

### ADIM 11: ANA UYGULAMA (main.py)

**Amaç:** Tüm modülleri birleştiren ana giriş noktası.

**11.1 Ana Uygulama Yapısı**
```python
#!/usr/bin/env python3
"""
BEIREK Content Scout
Otomatik haber tarama ve içerik üretim aracı
"""

import sys
from pathlib import Path

from modules.scanner import NewsScanner
from modules.filter import ArticleFilter
from modules.generator import ContentGenerator
from modules.storage import ContentStorage, init_database
from modules.concept_manager import ConceptManager
from modules.request_manager import RequestManager
from modules.ui import TerminalUI

class ContentScout:
    def __init__(self):
        """
        Uygulamayı başlatır.

        İşlem:
        1. Veritabanını başlat
        2. Tüm modülleri initialize et
        3. UI'ı başlat
        """
        init_database()

        self.scanner = NewsScanner()
        self.filter = ArticleFilter()
        self.generator = ContentGenerator()
        self.storage = ContentStorage()
        self.concept_manager = ConceptManager()
        self.request_manager = RequestManager()
        self.ui = TerminalUI()

    def run(self):
        """
        Ana döngü - menü gösterir ve seçimleri işler.
        """
        self.ui.show_banner()

        while True:
            choice = self.ui.show_main_menu()

            if choice == '1':
                self.run_scan_flow()
            elif choice == '2':
                self.run_concept_flow()
            elif choice == '3':
                self.run_request_flow()
            elif choice == '4':
                self.show_pending_articles()
            elif choice == '5':
                self.run_generation_flow()
            elif choice == '6':
                self.show_statistics()
            elif choice == '7':
                self.show_settings()
            elif choice == '8':
                self.ui.show_success("Güle güle!")
                sys.exit(0)

    def run_scan_flow(self):
        """
        Tam tarama akışı.

        İşlem:
        1. Kaynakları tara (progress göster)
        2. Makaleleri filtrele (Claude)
        3. Sonuçları göster
        4. Kullanıcı seçim yaparsa kaydet
        """
        self.ui.show_success("Tarama başlatılıyor...")

        # 1. Tarama
        scan_result = self.scanner.scan_all_sources()

        # 2. Filtreleme
        articles = self.storage.get_unfiltered_articles()
        filtered = self.filter.filter_articles(articles)

        # 3. Sonuç göster
        self.ui.show_article_table(filtered)

        # 4. Seçim
        selected_ids = self.ui.show_article_table(filtered)
        for article_id in selected_ids:
            self.storage.mark_article_selected(article_id)

        self.ui.show_summary(scan_result)

    def run_concept_flow(self):
        """
        Günlük kavram akışı.

        İşlem:
        1. Bugün için kavram seçilmiş mi kontrol et
        2. Seçilmemişse kavram seç
        3. İçerik üret
        4. Kaydet
        """
        result = self.concept_manager.run_daily_concept_flow()
        self.ui.show_concept_info(result['concept'])
        self.ui.show_success(f"İçerik oluşturuldu: {result['content_path']}")

    def run_request_flow(self):
        """
        İstek havuzu akışı.

        İşlem:
        1. Bekleyen istekleri listele
        2. Kullanıcı seçim yaparsa işle
        3. Hepsini işle seçeneği
        """
        requests = self.request_manager.scan_request_pool()
        pending = [r for r in requests if r['status'] == 'pending']

        if not pending:
            self.ui.show_success("Bekleyen istek yok.")
            return

        self.ui.show_request_list(pending)

        if self.ui.confirm("Tüm bekleyen istekleri işle?"):
            result = self.request_manager.process_all_pending()
            self.ui.show_summary(result)

    def run_generation_flow(self):
        """
        Manuel içerik üretim akışı.

        İşlem:
        1. Seçilmiş ama işlenmemiş makaleleri göster
        2. Format seçimi al
        3. İçerik üret
        4. Kaydet
        """
        pending = self.storage.get_pending_articles()

        if not pending:
            self.ui.show_error("İşlenecek makale yok. Önce tarama yapın.")
            return

        self.ui.show_article_table(pending)
        selected_ids = self.ui.get_selection()
        formats = self.ui.show_generation_options()

        for article_id in selected_ids:
            article = self.storage.get_article(article_id)
            source_content = self.generator.fetch_full_article(article['url'])

            content = self.generator.generate_all_formats(
                source_content=source_content,
                topic=article['title'],
                beirek_area=article['beirek_area']
            )

            # Kaydet
            folder = self.storage.create_content_folder(
                beirek_area=article['beirek_area'],
                beirek_subarea=article['beirek_subarea'],
                content_type='haber',
                slug=article['title']
            )
            self.storage.save_content_files(folder, content)
            self.storage.mark_article_processed(article_id)

        self.ui.show_success("İçerik üretimi tamamlandı!")

    def show_pending_articles(self):
        """Bekleyen makaleleri gösterir"""

    def show_statistics(self):
        """İstatistikleri gösterir"""

    def show_settings(self):
        """Ayarları gösterir ve değişiklik yapmaya izin verir"""


def main():
    """Uygulama giriş noktası"""
    app = ContentScout()
    app.run()


if __name__ == "__main__":
    main()
```

**11.2 Çıktı:** Tam çalışır uygulama.

---

### ADIM 12: PROMPT DOSYALARI

**Amaç:** Tüm Claude promptlarını hazırlamak.

**12.1 Oluşturulacak Dosyalar**

| Dosya | İçerik | PRD Referansı |
|-------|--------|---------------|
| `filter_prompt.txt` | Filtreleme promptu | Bölüm 10.1 |
| `article_prompt.txt` | Makale üretim promptu | Bölüm 10.2 |
| `linkedin_prompt.txt` | LinkedIn promptu | Bölüm 10.3 |
| `twitter_prompt.txt` | Twitter promptu | Bölüm 10.4 |
| `concept_selection_prompt.txt` | Kavram seçim promptu | Bölüm 10.5 |
| `concept_content_prompt.txt` | Kavram içerik promptu | Bölüm 10.6 |

**12.2 Çıktı:** Tüm prompt dosyaları hazır.

---

### ADIM 13: TEST VE DOĞRULAMA

**Amaç:** Her modülü test etmek.

**13.1 Test Sırası**

| # | Test | Komut | Beklenen Çıktı |
|---|------|-------|----------------|
| 1 | Veritabanı | `python -c "from modules.storage import init_database; init_database()"` | data/scout.db oluşur |
| 2 | Kaynak yükleme | `python -c "from modules.scanner import NewsScanner; s=NewsScanner(); print(len(s.load_sources()))"` | 300+ |
| 3 | RSS tarama | `python -c "..."` | Makale listesi |
| 4 | Claude CLI | `echo "test" \| claude` | Yanıt gelir |
| 5 | Filtreleme | `python -c "..."` | Skorlanmış makaleler |
| 6 | Makale üretimi | `python -c "..."` | Markdown içerik |
| 7 | Dosya kaydetme | `python -c "..."` | content/ klasörüne dosya yazılır |
| 8 | Kavram seçimi | `python -c "..."` | Günün kavramı seçilir |
| 9 | İstek havuzu | `python -c "..."` | Bekleyen istekler listelenir |
| 10 | Tam akış | `python main.py` | Menü görünür, akışlar çalışır |

**13.2 Çıktı:** Tüm testler geçer, uygulama hazır.

---

### ADIM 14: ENTEGRASYONLAR (Opsiyonel)

**14.1 Typefully Entegrasyonu**
- PRD Bölüm 15'te detaylı tanım mevcut
- MVP sonrası eklenecek

**14.2 Cron/Zamanlama**
- Günlük otomatik tarama
- MVP sonrası eklenecek

---

### GELİŞTİRME SIRASI ÖZETİ

```
┌─────────────────────────────────────────────────────────────────┐
│                    GELİŞTİRME SIRASI                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ADIM 1: Proje İskeleti                                         │
│     └─→ Klasörler, boş dosyalar, config, requirements          │
│                                                                 │
│  ADIM 2: Veritabanı (storage.py)                                │
│     └─→ Tüm tablolar, CRUD fonksiyonları                       │
│                                                                 │
│  ADIM 3: Kaynak Yönetimi (sources.yaml)                         │
│     └─→ 300+ kaynak yapılandırması                             │
│                                                                 │
│  ADIM 4: Tarama (scanner.py)                                    │
│     └─→ RSS + Web scraping                                     │
│                                                                 │
│  ADIM 5: Filtreleme (filter.py)                                 │
│     └─→ Claude CLI entegrasyonu                                │
│                                                                 │
│  ADIM 6: İçerik Üretimi (generator.py)                          │
│     └─→ 3 format + anti-halüsinasyon                           │
│                                                                 │
│  ADIM 7: Günlük Kavram (concept_manager.py)                     │
│     └─→ Sözlük yönetimi + seçim + üretim                       │
│                                                                 │
│  ADIM 8: İstek Havuzu (request_manager.py)                      │
│     └─→ Manuel istek işleme                                    │
│                                                                 │
│  ADIM 9: Dosya Kaydetme (storage.py ek)                         │
│     └─→ BEIREK klasörlerine kaydetme                           │
│                                                                 │
│  ADIM 10: Terminal UI (ui.py)                                   │
│     └─→ Rich kütüphanesi ile arayüz                            │
│                                                                 │
│  ADIM 11: Ana Uygulama (main.py)                                │
│     └─→ Tüm modülleri birleştirme                              │
│                                                                 │
│  ADIM 12: Prompt Dosyaları                                      │
│     └─→ 6 prompt dosyası                                       │
│                                                                 │
│  ADIM 13: Test ve Doğrulama                                     │
│     └─→ Her modül için test                                    │
│                                                                 │
│  ADIM 14: Entegrasyonlar (Opsiyonel)                            │
│     └─→ Typefully, Cron                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 14. TEST SENARYOLARI

### 14.1 Unit Test Senaryoları
- RSS feed parse edilebilmeli
- Web scraping çalışmalı
- Claude CLI çağrısı başarılı olmalı
- Dosya yazma/okuma çalışmalı
- Veritabanı CRUD işlemleri çalışmalı

### 14.2 Integration Test Senaryoları
- Tarama → Filtreleme → Kaydetme akışı
- Seçim → Üretim → Kaydetme akışı
- Hata durumunda graceful degradation

### 14.3 Manuel Test Senaryoları
- [ ] Uygulama açılışı
- [ ] Menü navigasyonu
- [ ] 5 kaynaktan tarama
- [ ] Filtreleme sonuçları
- [ ] İçerik üretimi (3 format)
- [ ] Dosya kaydetme ve kontrol

---

## 15. TYPEFULLY API ENTEGRASYONU

### 15.1 Genel Bilgi
Typefully API v2 (Aralık 2025) ile içerikleri doğrudan uygulama içinden yayınlayabilirsin.

**Desteklenen Platformlar:**
- X (Twitter)
- LinkedIn
- Threads
- Bluesky
- Mastodon

### 15.2 Kurulum
```bash
# API Key alma:
# 1. Typefully.com → Settings → API
# 2. "Generate API Key" tıkla
# 3. config.yaml'a ekle
```

### 15.3 API Endpoints

**Base URL:** `https://api.typefully.com/v2`

**Authentication:**
```
Header: Authorization: Bearer YOUR_API_KEY
```

**Social Sets Listele (Hesapları Getir):**
```bash
GET /v2/social-sets

# Response:
{
  "results": [
    {
      "id": 12345,
      "username": "beirek",
      "name": "BEIREK"
    }
  ]
}
```

**Draft Oluştur:**
```bash
POST /v2/social-sets/{social_set_id}/drafts

# Body (Sadece X/Twitter):
{
  "platforms": {
    "x": {
      "enabled": true,
      "posts": [
        {"text": "Tweet 1"},
        {"text": "Tweet 2"}
      ]
    }
  }
}

# Body (Multi-platform):
{
  "platforms": {
    "x": {
      "enabled": true,
      "posts": [{"text": "Short for X"}]
    },
    "linkedin": {
      "enabled": true,
      "posts": [{"text": "Professional LinkedIn content..."}]
    }
  }
}
```

**Zamanlanmış Yayın:**
```bash
POST /v2/social-sets/{social_set_id}/drafts

{
  "platforms": {
    "x": {"enabled": true, "posts": [{"text": "Scheduled!"}]}
  },
  "publish_at": "2026-01-30T10:00:00Z"
}
```

**Hemen Yayınla:**
```bash
{
  "publish_at": "now"
}
```

**Media Upload:**
```bash
# 1. Upload URL al
POST /v2/social-sets/{social_set_id}/media/upload
{"file_name": "image.jpg"}

# Response: media_id ve upload_url döner

# 2. Dosyayı yükle (upload_url'e PUT)

# 3. Draft'ta kullan
{
  "platforms": {
    "x": {
      "enabled": true,
      "posts": [{"text": "With image!", "media_ids": ["<media_id>"]}]
    }
  }
}
```

### 15.4 Python Modülü: typefully.py

```python
"""
Typefully API v2 Entegrasyonu
"""

import requests
import json

class TypefullyClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.typefully.com/v2"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.social_set_id = None
    
    def get_social_sets(self) -> list:
        """Bağlı hesapları listele"""
        response = requests.get(
            f"{self.base_url}/social-sets",
            headers=self.headers
        )
        return response.json().get("results", [])
    
    def set_default_social_set(self, social_set_id: int):
        """Varsayılan hesabı ayarla"""
        self.social_set_id = social_set_id
    
    def create_draft(
        self,
        content: str | list,
        platforms: list = ["x"],
        publish_at: str = None,
        tags: list = None
    ) -> dict:
        """
        Draft oluştur
        
        Args:
            content: str (tek post) veya list (thread)
            platforms: ["x", "linkedin", "threads", "bluesky", "mastodon"]
            publish_at: ISO datetime veya "now" veya None (draft olarak kaydet)
            tags: ["marketing", "energy"] gibi etiketler
        """
        if isinstance(content, str):
            posts = [{"text": content}]
        else:
            posts = [{"text": p} for p in content]
        
        payload = {
            "platforms": {}
        }
        
        for platform in platforms:
            payload["platforms"][platform] = {
                "enabled": True,
                "posts": posts
            }
        
        if publish_at:
            payload["publish_at"] = publish_at
        
        if tags:
            payload["tags"] = tags
        
        response = requests.post(
            f"{self.base_url}/social-sets/{self.social_set_id}/drafts",
            headers=self.headers,
            json=payload
        )
        return response.json()
    
    def create_twitter_thread(self, tweets: list, publish_at: str = None) -> dict:
        """Twitter thread oluştur"""
        return self.create_draft(
            content=tweets,
            platforms=["x"],
            publish_at=publish_at
        )
    
    def create_linkedin_post(self, content: str, publish_at: str = None) -> dict:
        """LinkedIn post oluştur"""
        return self.create_draft(
            content=content,
            platforms=["linkedin"],
            publish_at=publish_at
        )
    
    def publish_now(self, content: str, platforms: list = ["x", "linkedin"]) -> dict:
        """Hemen yayınla"""
        return self.create_draft(
            content=content,
            platforms=platforms,
            publish_at="now"
        )
    
    def get_tags(self) -> list:
        """Mevcut etiketleri listele"""
        response = requests.get(
            f"{self.base_url}/social-sets/{self.social_set_id}/tags",
            headers=self.headers
        )
        return response.json().get("results", [])
    
    def create_tag(self, name: str) -> dict:
        """Yeni etiket oluştur"""
        response = requests.post(
            f"{self.base_url}/social-sets/{self.social_set_id}/tags",
            headers=self.headers,
            json={"name": name}
        )
        return response.json()
```

### 15.5 Kullanım Örneği

```python
from modules.typefully import TypefullyClient

# Client oluştur
client = TypefullyClient(api_key="your_api_key")

# Hesapları al ve varsayılanı ayarla
social_sets = client.get_social_sets()
client.set_default_social_set(social_sets[0]["id"])

# LinkedIn post oluştur (draft olarak)
client.create_linkedin_post(
    content="🔋 Energy storage market to triple by 2030...",
    publish_at=None  # Draft olarak kaydet
)

# Twitter thread oluştur ve zamanla
client.create_twitter_thread(
    tweets=[
        "1/ 🧵 Big news in the BESS market...",
        "2/ BloombergNEF predicts 3x growth...",
        "3/ Key drivers include...",
        "4/ What this means for developers...",
        "5/ Follow @BEIREK for more insights!"
    ],
    publish_at="2026-01-31T09:00:00Z"
)

# Hemen yayınla (X + LinkedIn)
client.publish_now(
    content="Breaking: Texas solar project reaches financial close!",
    platforms=["x", "linkedin"]
)
```

---

## 15. ANTİ-HALÜSİNASYON STRATEJİSİ

### 15.1 Problem Tanımı

LLM'ler içerik üretirken şu hataları yapabilir:
- ❌ Olmayan istatistikler uydurma ("Pazar %47 büyüdü")
- ❌ Var olmayan şirket/proje adları üretme
- ❌ Yanlış tarihler ve rakamlar verme
- ❌ Gerçekleşmemiş olayları anlatma

### 15.2 Temel Prensip: REAL DATA + ORIGINAL INSIGHT

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│   VERİLER & FAKTLAR  ──────▶  %100 GERÇEK (kaynaklardan)        │
│                                                                  │
│   YORUMLAR & ANALİZ  ──────▶  %100 BEIREK PERSPEKTİFİ (özgün)   │
│                                                                  │
│   LİNK & ATIF        ──────▶  GEREKMEZ                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Amaç:**
- Veriler gerçek olmalı (500 MW, $450M, Ocak 2026 gibi)
- Yorumlar BEIREK'in thought leadership perspektifinden
- Kaynak linki veya "...göre" ifadeleri GEREKMEZ
- Sanki BEIREK uzmanları bu verileri değerlendirip yazıyor

### 15.3 Üç Aşamalı Doğrulama Sistemi

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  AŞAMA 1     │     │  AŞAMA 2     │     │  AŞAMA 3     │
│  Extraction  │────▶│  Generation  │────▶│  Verification│
│  (Çıkarım)   │     │  (Üretim)    │     │  (Doğrulama) │
└──────────────┘     └──────────────┘     └──────────────┘
     │                     │                     │
     ▼                     ▼                     ▼
  Kaynaktan            Sadece çıkarılan      Üretilen içerik
  fact'leri çıkar      fact'leri kullan      kaynak ile karşılaştır
```

### 15.4 AŞAMA 1: Fact Extraction (Çıkarım)

İçerik üretmeden ÖNCE, kaynak metinden tüm doğrulanabilir bilgileri çıkar:

**extraction_prompt.txt:**
```
Sen bir fact-checker'sın. Aşağıdaki kaynak metinden TÜM doğrulanabilir bilgileri çıkar.

KURALLAR:
- Sadece metinde AÇIKÇA belirtilen bilgileri çıkar
- Hiçbir şey yorumlama veya çıkarım yapma
- Her fact için kaynak cümleyi belirt
- Belirsiz ifadeleri "belirsiz" olarak işaretle

ÇIKARILACAK BİLGİ TÜRLERİ:
1. RAKAMLAR: MW, $, %, yıl, tarih
2. İSİMLER: Şirket, proje, kişi, lokasyon
3. OLAYLAR: Ne oldu, ne zaman, nerede
4. KAYNAKLAR: Kim söyledi, hangi rapor

FORMAT:
---
FACT_ID: F1
TYPE: [rakam/isim/olay/kaynak]
CONTENT: [çıkarılan bilgi]
SOURCE_QUOTE: "[orijinal cümle]"
CONFIDENCE: [high/medium/low]
---

KAYNAK METİN:
{source_content}
```

**Örnek Çıktı:**
```
---
FACT_ID: F1
TYPE: rakam
CONTENT: Proje kapasitesi 500 MW
SOURCE_QUOTE: "The 500 MW solar project..."
CONFIDENCE: high
---
FACT_ID: F2
TYPE: rakam
CONTENT: Yatırım tutarı $450 milyon
SOURCE_QUOTE: "...secured $450 million in financing"
CONFIDENCE: high
---
FACT_ID: F3
TYPE: isim
CONTENT: Geliştirici: Longroad Energy
SOURCE_QUOTE: "Longroad Energy announced..."
CONFIDENCE: high
---
FACT_ID: F4
TYPE: olay
CONTENT: Financial close Ocak 2026'da tamamlandı
SOURCE_QUOTE: "reached financial close in January 2026"
CONFIDENCE: high
---
```

### 15.5 AŞAMA 2: Grounded Generation (Bağlı Üretim)

**article_prompt_grounded.txt:**
```
Sen BEIREK için içerik yazarısın. Aşağıdaki ÇIKARILMIŞ FACT'LER ve KAYNAK METİN kullanarak bir makale yaz.

⚠️ KRİTİK KURALLAR - İHLAL ETME:

1. SADECE aşağıdaki fact listesindeki bilgileri kullan
2. Fact listesinde OLMAYAN hiçbir:
   - Rakam (%, $, MW, tarih)
   - Şirket/proje/kişi adı
   - İstatistik veya veri
   - Alıntı veya söylem
   UYDURAMAZ veya EKLEYEMEZSIN

3. BEIREK perspektifinden özgün yorum ekle:
   - "Bu gelişme, proje geliştiricileri için X anlamına geliyor..."
   - "Biz bu trendi Y olarak değerlendiriyoruz..."

4. Kaynak atıfı veya link KULLANMA:
   - ❌ "Bloomberg'e göre..."
   - ❌ "Rapora göre..."
   - ✅ Verileri doğrudan yaz

ÇIKARILMIŞ GERÇEK VERİLER:
{extracted_facts}

KAYNAK METİN:
{source_content}

YAZIM FORMATI:
- Profesyonel thought leadership tonu
- 1500-2500 kelime
- Veriler doğal şekilde entegre
- BEIREK özgün yorumları ile zenginleştirilmiş
```

### 15.6 AŞAMA 3: Verification (Doğrulama)

**verification_prompt.txt:**
```
Sen bir fact-checker editörsün. ÜRETİLEN METNİ, KAYNAK METİN ile karşılaştır.

KONTROL LİSTESİ:
□ Tüm rakamlar (MW, $, %, tarih) kaynak ile eşleşiyor mu?
□ Tüm şirket/proje isimleri doğru yazılmış mı?
□ Kaynak metinde OLMAYAN veri uydurulmuş mu?
□ Tarihler tutarlı mı?
□ "...göre", "...raporuna göre" gibi atıf ifadeleri var mı? (OLMAMALI)

NOT: Yorumlar ve analizler özgün olabilir, sadece VERİLER kontrol edilecek.

FORMAT:
Her sorunlu ifade için:
---
ISSUE_ID: I1
SEVERITY: [critical/warning/info]
GENERATED_TEXT: "[üretilen metin]"
SOURCE_TEXT: "[kaynak metin]" veya "UYDURMA - KAYNAK YOK"
PROBLEM: [açıklama]
SUGGESTION: [düzeltme önerisi]
---

Sorun yoksa:
✅ VERIFIED - Tüm veriler kaynak ile tutarlı

ÜRETİLEN METİN:
{generated_content}

KAYNAK METİN:
{source_content}

ÇIKARILMIŞ FACT'LER:
{extracted_facts}
```

### 15.7 Python Implementasyonu

**modules/generator.py (güncellenmiş):**

```python
"""
Anti-Hallucination Content Generator
"""

import subprocess
import json
import re

class GroundedGenerator:
    def __init__(self):
        self.extraction_prompt = self._load_prompt("extraction_prompt.txt")
        self.article_prompt = self._load_prompt("article_prompt_grounded.txt")
        self.linkedin_prompt = self._load_prompt("linkedin_prompt_grounded.txt")
        self.twitter_prompt = self._load_prompt("twitter_prompt_grounded.txt")
        self.verification_prompt = self._load_prompt("verification_prompt.txt")
    
    def _load_prompt(self, filename: str) -> str:
        with open(f"prompts/{filename}", "r") as f:
            return f.read()
    
    def _call_claude(self, prompt: str) -> str:
        """Claude CLI çağrısı"""
        result = subprocess.run(
            ["claude"],
            input=prompt,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    
    def extract_facts(self, source_content: str) -> dict:
        """
        AŞAMA 1: Kaynak metinden fact'leri çıkar
        """
        prompt = self.extraction_prompt.replace("{source_content}", source_content)
        response = self._call_claude(prompt)
        
        # Parse facts
        facts = self._parse_facts(response)
        return {
            "raw_response": response,
            "facts": facts,
            "fact_count": len(facts)
        }
    
    def _parse_facts(self, response: str) -> list:
        """Fact response'unu parse et"""
        facts = []
        current_fact = {}
        
        for line in response.split("\n"):
            line = line.strip()
            if line.startswith("FACT_ID:"):
                if current_fact:
                    facts.append(current_fact)
                current_fact = {"id": line.split(":")[1].strip()}
            elif line.startswith("TYPE:"):
                current_fact["type"] = line.split(":")[1].strip()
            elif line.startswith("CONTENT:"):
                current_fact["content"] = line.split(":", 1)[1].strip()
            elif line.startswith("SOURCE_QUOTE:"):
                current_fact["source_quote"] = line.split(":", 1)[1].strip().strip('"')
            elif line.startswith("CONFIDENCE:"):
                current_fact["confidence"] = line.split(":")[1].strip()
        
        if current_fact:
            facts.append(current_fact)
        
        return facts
    
    def generate_content(
        self,
        source_content: str,
        content_type: str,  # "article", "linkedin", "twitter"
        extracted_facts: dict = None
    ) -> dict:
        """
        AŞAMA 2: Grounded içerik üret
        """
        # Fact extraction yapılmadıysa yap
        if not extracted_facts:
            extracted_facts = self.extract_facts(source_content)
        
        # Fact'leri string'e çevir
        facts_str = self._facts_to_string(extracted_facts["facts"])
        
        # Uygun prompt seç
        if content_type == "article":
            prompt_template = self.article_prompt
        elif content_type == "linkedin":
            prompt_template = self.linkedin_prompt
        else:
            prompt_template = self.twitter_prompt
        
        # Prompt hazırla
        prompt = prompt_template.replace("{extracted_facts}", facts_str)
        prompt = prompt.replace("{source_content}", source_content)
        
        # Generate
        generated = self._call_claude(prompt)
        
        return {
            "content": generated,
            "content_type": content_type,
            "facts_used": extracted_facts,
            "verified": False
        }
    
    def _facts_to_string(self, facts: list) -> str:
        """Fact listesini prompt için string'e çevir"""
        result = ""
        for f in facts:
            result += f"[{f.get('id', 'F?')}] {f.get('content', '')} "
            result += f"(Kaynak: \"{f.get('source_quote', '')}\")\n"
        return result
    
    def verify_content(
        self,
        generated_content: str,
        source_content: str,
        extracted_facts: dict
    ) -> dict:
        """
        AŞAMA 3: Üretilen içeriği doğrula
        """
        facts_str = self._facts_to_string(extracted_facts["facts"])
        
        prompt = self.verification_prompt.replace("{generated_content}", generated_content)
        prompt = prompt.replace("{source_content}", source_content)
        prompt = prompt.replace("{extracted_facts}", facts_str)
        
        response = self._call_claude(prompt)
        
        # Parse verification result
        is_verified = "✅ VERIFIED" in response
        issues = self._parse_issues(response) if not is_verified else []
        
        return {
            "verified": is_verified,
            "issues": issues,
            "issue_count": len(issues),
            "raw_response": response
        }
    
    def _parse_issues(self, response: str) -> list:
        """Verification issue'larını parse et"""
        issues = []
        current_issue = {}
        
        for line in response.split("\n"):
            line = line.strip()
            if line.startswith("ISSUE_ID:"):
                if current_issue:
                    issues.append(current_issue)
                current_issue = {"id": line.split(":")[1].strip()}
            elif line.startswith("SEVERITY:"):
                current_issue["severity"] = line.split(":")[1].strip()
            elif line.startswith("PROBLEM:"):
                current_issue["problem"] = line.split(":", 1)[1].strip()
            elif line.startswith("SUGGESTION:"):
                current_issue["suggestion"] = line.split(":", 1)[1].strip()
        
        if current_issue:
            issues.append(current_issue)
        
        return issues
    
    def generate_verified(
        self,
        source_content: str,
        content_type: str,
        max_iterations: int = 3
    ) -> dict:
        """
        Tam pipeline: Extract → Generate → Verify → Fix (loop)
        """
        # Aşama 1: Extract
        print("📋 Fact'ler çıkarılıyor...")
        extracted = self.extract_facts(source_content)
        print(f"   ✓ {extracted['fact_count']} fact bulundu")
        
        # Aşama 2 & 3: Generate & Verify loop
        for iteration in range(max_iterations):
            print(f"\n🔄 İterasyon {iteration + 1}/{max_iterations}")
            
            # Generate
            print("✍️  İçerik üretiliyor...")
            result = self.generate_content(
                source_content=source_content,
                content_type=content_type,
                extracted_facts=extracted
            )
            
            # Verify
            print("🔍 Doğrulanıyor...")
            verification = self.verify_content(
                generated_content=result["content"],
                source_content=source_content,
                extracted_facts=extracted
            )
            
            if verification["verified"]:
                print("✅ Doğrulama başarılı!")
                result["verified"] = True
                result["verification"] = verification
                return result
            
            print(f"⚠️  {verification['issue_count']} sorun bulundu")
            for issue in verification["issues"]:
                print(f"   - [{issue.get('severity', '?')}] {issue.get('problem', '')}")
            
            # Son iterasyon değilse, sorunları düzelt
            if iteration < max_iterations - 1:
                print("🔧 Düzeltme isteniyor...")
                result = self._fix_issues(
                    result["content"],
                    verification["issues"],
                    source_content,
                    extracted
                )
        
        # Max iteration'a ulaşıldı
        print("⚠️  Max iterasyon - manuel kontrol gerekli")
        result["verified"] = False
        result["verification"] = verification
        result["needs_manual_review"] = True
        return result
    
    def _fix_issues(
        self,
        content: str,
        issues: list,
        source_content: str,
        extracted_facts: dict
    ) -> dict:
        """Bulunan sorunları düzelt"""
        issues_str = "\n".join([
            f"- {i.get('problem', '')}: {i.get('suggestion', '')}"
            for i in issues
        ])
        
        fix_prompt = f"""
Aşağıdaki içerikte SORUNLAR bulundu. Düzelt.

SORUNLAR:
{issues_str}

KURALLAR:
- SADECE sorunlu kısımları düzelt
- Yeni bilgi EKLEME
- Kaynak metinde olmayan bilgi KULLANMA

MEVCUT İÇERİK:
{content}

KAYNAK METİN:
{source_content}

DÜZELTİLMİŞ İÇERİK:
"""
        fixed = self._call_claude(fix_prompt)
        
        return {
            "content": fixed,
            "verified": False
        }
```

### 15.8 Prompt Güvenlik Katmanları

**linkedin_prompt_grounded.txt:**
```
Sen BEIREK için LinkedIn içerik yazarısın.

⛔ YASAK LİSTESİ - ASLA KULLANMA:
- "Araştırmalara göre..." (spesifik kaynak olmadan)
- "Uzmanlar belirtiyor ki..." (isim olmadan)
- "İstatistikler gösteriyor..." (kaynak olmadan)
- "%XX büyüme/artış/düşüş" (veri listesinde yoksa)
- Herhangi bir şirket/kişi adı (veri listesinde yoksa)
- "...göre", "...raporuna göre" gibi atıf ifadeleri

✅ İZİN VERİLEN:
- Veri listesindeki TÜM rakamlar ve isimler
- BEIREK perspektifinden özgün yorumlar
- "Bu gelişme gösteriyor ki..." gibi bağlayıcılar
- Pratik çıkarımlar ve öngörüler

GERÇEK VERİLER (SADECE BUNLARI KULLAN):
{extracted_facts}

KAYNAK METİN:
{source_content}

FORMAT:
- 150-300 kelime
- Gerçek veri ile hook
- BEIREK perspektifinden insight
- Engagement sorusu ile bitir
- 3-5 hashtag
- Link/atıf YOK
```

### 15.9 Verification Checklist UI

```
╔══════════════════════════════════════════════════════════════╗
║  🔍 DOĞRULAMA SONUÇLARI                                      ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Kaynak: "Texas 500MW Solar Project Reaches Close"           ║
║  Üretilen: Research Article (2,145 kelime)                   ║
║                                                              ║
║  ─────────────────────────────────────────────────────────   ║
║                                                              ║
║  ✅ VERİ KONTROLÜ                                            ║
║     500 MW .................. ✓ Kaynak ile eşleşiyor        ║
║     $450 milyon ............. ✓ Kaynak ile eşleşiyor        ║
║     Ocak 2026 ............... ✓ Kaynak ile eşleşiyor        ║
║     Longroad Energy ......... ✓ İsim doğru                  ║
║                                                              ║
║  ⚠️  SORUNLAR                                                ║
║     Satır 45: "...sektörde %30 büyüme bekleniyor"           ║
║     → UYDURMA VERİ - Kaynak metinde yok, KALDIRILDI          ║
║                                                              ║
║  ✅ FORMAT KONTROLÜ                                          ║
║     "...göre" ifadesi ....... ✓ Yok (doğru)                 ║
║     Kaynak linki ............ ✓ Yok (doğru)                 ║
║                                                              ║
║  ─────────────────────────────────────────────────────────   ║
║  SONUÇ: ✅ DOĞRULANDI - Yayına hazır                         ║
║                                                              ║
║  [K] Kaydet  [D] Düzenle  [İ] İptal  [M] Ana menü           ║
╚══════════════════════════════════════════════════════════════╝
```

### 15.10 Ek Güvenlik Önlemleri

**1. Sayı Formatı Kontrolü:**
```python
def validate_numbers(generated: str, facts: list) -> list:
    """Üretilen içerikteki sayıları fact'lerle karşılaştır"""
    import re
    
    # Üretilendeki tüm sayıları bul
    generated_numbers = re.findall(r'\$?[\d,]+\.?\d*\s*(?:MW|%|million|billion)?', generated)
    
    # Fact'lerdeki sayıları al
    fact_numbers = [f['content'] for f in facts if f['type'] == 'rakam']
    
    # Eşleşmeyenleri bul
    suspicious = []
    for num in generated_numbers:
        normalized = num.replace(',', '').replace('$', '').strip()
        if not any(normalized in fn.replace(',', '') for fn in fact_numbers):
            suspicious.append(num)
    
    return suspicious
```

**2. Quote Validation:**
```python
def validate_quotes(generated: str, source: str) -> list:
    """Alıntıların gerçekten kaynakta olup olmadığını kontrol et"""
    import re
    
    # Tırnak içindeki alıntıları bul
    quotes = re.findall(r'"([^"]+)"', generated)
    
    invalid_quotes = []
    for quote in quotes:
        # 5 kelimeden uzun alıntılar için kontrol
        if len(quote.split()) > 5:
            if quote.lower() not in source.lower():
                invalid_quotes.append(quote)
    
    return invalid_quotes
```

**3. Entity Validation:**
```python
def validate_entities(generated: str, facts: list) -> list:
    """Şirket/kişi isimlerini kontrol et"""
    import re
    
    # Fact'lerdeki entity'ler
    fact_entities = [f['content'] for f in facts if f['type'] == 'isim']
    
    # Potansiyel entity pattern'leri (büyük harfle başlayan 2+ kelime)
    potential_entities = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b', generated)
    
    # Bilinen güvenli terimler
    safe_terms = {'United States', 'North America', 'New York', 'Project Finance'}
    
    suspicious = []
    for entity in potential_entities:
        if entity not in safe_terms:
            if not any(entity.lower() in fe.lower() for fe in fact_entities):
                suspicious.append(entity)
    
    return suspicious
```

### 15.11 Confidence Scoring

```python
def calculate_content_confidence(verification_result: dict) -> dict:
    """İçerik güvenilirlik skoru hesapla"""
    
    score = 100
    
    # Her sorun için puan düş
    for issue in verification_result.get('issues', []):
        if issue['severity'] == 'critical':
            score -= 30
        elif issue['severity'] == 'warning':
            score -= 15
        else:
            score -= 5
    
    # Minimum 0
    score = max(0, score)
    
    # Kategori
    if score >= 90:
        category = "🟢 HIGH - Yayına hazır"
    elif score >= 70:
        category = "🟡 MEDIUM - Gözden geçir"
    elif score >= 50:
        category = "🟠 LOW - Düzenleme gerekli"
    else:
        category = "🔴 CRITICAL - Yeniden üret"
    
    return {
        "score": score,
        "category": category,
        "recommendation": "publish" if score >= 90 else "review" if score >= 70 else "edit" if score >= 50 else "regenerate"
    }
```

### 15.12 Final Checklist (Manuel)

Her içerik yayınlanmadan önce:

```
VERİ DOĞRULUĞU:
□ Tüm rakamlar (MW, $, %, tarih) kaynak ile eşleşiyor mu?
□ Tüm şirket/proje isimleri doğru yazılmış mı?
□ Tarihler ve zaman dilimleri tutarlı mı?
□ Uydurulmuş veri var mı? (OLMAMALI)

THOUGHT LEADERSHIP KALİTESİ:
□ BEIREK perspektifi net mi?
□ Pratik çıkarımlar ve öngörüler var mı?
□ "Ne anlama geliyor?" sorusu cevaplanmış mı?
□ Özgün analiz ve yorum var mı?

BEIREK ÇÖZÜMÜ:
□ Doğru hizmet alanı seçilmiş mi?
□ Çözüm konuyla alakalı mı?
□ Soft sell mi? (Hard sell OLMAMALI)
□ CTA net ve actionable mı?

FORMAT KONTROLÜ:
□ "...göre", "...raporuna göre" ifadeleri YOK mu? (OLMAMALI)
□ Kaynak linki/atıf YOK mu? (OLMAMALI)
□ Veriler doğal şekilde entegre edilmiş mi?
□ Ton profesyonel ve thought leadership'e uygun mu?
```

### BEIREK HİZMET DOĞRULAMA

| Haber Konusu | Doğru Hizmet | Yanlış Örnekler |
|--------------|--------------|-----------------|
| Proje finansmanı | Development Finance | ❌ Asset Management |
| EPC kontratı | Engineering & Delivery | ❌ Digital Platforms |
| M&A / Yatırım | Deal & Contract Advisory | ❌ O&M hizmetleri |
| İşletme/Performans | Asset Management | ❌ Project Development |

---

## 16. GOOGLE SCHOLAR ENTEGRASYONU

### 16.1 Genel Bilgi
Google Scholar'ın resmi API'si yok (telif hakkı sorunları nedeniyle). Ancak `scholarly` Python paketi ile akademik araştırma yapılabilir.

**Neden Kullanıyoruz:**
- Ek istatistik ve trend verisi bulmak
- Rakamları ve verileri doğrulamak
- Sektör trendleri hakkında ek bilgi edinmek
- Thought leadership içeriği gerçek verilerle zenginleştirmek

**⚠️ ÖNEMLİ: Atıf/Referans DEĞİL**
- Scholar'dan alınan veriler içeriğe entegre edilir
- AMA kaynak linki veya atıf EKLENMEZ
- Veriler "kendi bilgimiz" gibi kullanılır

### 15.2 Kurulum
```bash
pip install scholarly --break-system-packages
```

### 15.3 Python Modülü: scholar.py

```python
"""
Google Scholar Entegrasyonu (scholarly paketi ile)
"""

from scholarly import scholarly
from typing import List, Dict, Optional
import time

class ScholarClient:
    def __init__(self, proxy: str = None):
        """
        Google Scholar client
        
        Args:
            proxy: Opsiyonel proxy (rate limit için)
        """
        if proxy:
            scholarly.use_proxy(proxy)
    
    def search_publications(
        self,
        query: str,
        limit: int = 10,
        year_low: int = None,
        year_high: int = None
    ) -> List[Dict]:
        """
        Akademik makale ara
        
        Args:
            query: Arama sorgusu ("solar energy storage", "BESS grid")
            limit: Maksimum sonuç sayısı
            year_low: Minimum yıl filtresi
            year_high: Maksimum yıl filtresi
        
        Returns:
            Liste: Makale bilgileri
        """
        results = []
        search_query = scholarly.search_pubs(query)
        
        for i, pub in enumerate(search_query):
            if i >= limit:
                break
            
            # Yıl filtresi
            pub_year = pub.get('bib', {}).get('pub_year')
            if pub_year:
                try:
                    year = int(pub_year)
                    if year_low and year < year_low:
                        continue
                    if year_high and year > year_high:
                        continue
                except:
                    pass
            
            results.append({
                'title': pub.get('bib', {}).get('title', ''),
                'authors': pub.get('bib', {}).get('author', ''),
                'year': pub_year,
                'abstract': pub.get('bib', {}).get('abstract', ''),
                'venue': pub.get('bib', {}).get('venue', ''),
                'citations': pub.get('num_citations', 0),
                'url': pub.get('pub_url', ''),
                'pdf_url': pub.get('eprint_url', ''),
            })
            
            # Rate limiting
            time.sleep(1)
        
        return results
    
    def search_author(self, name: str) -> Optional[Dict]:
        """
        Yazar ara ve profil bilgilerini getir
        
        Args:
            name: Yazar adı
        
        Returns:
            Dict: Yazar bilgileri
        """
        search_query = scholarly.search_author(name)
        
        try:
            author = next(search_query)
            author_filled = scholarly.fill(author)
            
            return {
                'name': author_filled.get('name', ''),
                'affiliation': author_filled.get('affiliation', ''),
                'email': author_filled.get('email_domain', ''),
                'citations': author_filled.get('citedby', 0),
                'h_index': author_filled.get('hindex', 0),
                'interests': author_filled.get('interests', []),
                'publications_count': len(author_filled.get('publications', []))
            }
        except StopIteration:
            return None
    
    def get_citations(self, publication: Dict, limit: int = 10) -> List[Dict]:
        """
        Bir makaleyi kaynak gösteren makaleleri getir
        
        Args:
            publication: search_publications'dan dönen makale
            limit: Maksimum atıf sayısı
        
        Returns:
            Liste: Atıf yapan makaleler
        """
        results = []
        pub_filled = scholarly.fill(publication)
        
        for i, citation in enumerate(scholarly.citedby(pub_filled)):
            if i >= limit:
                break
            
            results.append({
                'title': citation.get('bib', {}).get('title', ''),
                'authors': citation.get('bib', {}).get('author', ''),
                'year': citation.get('bib', {}).get('pub_year', ''),
                'url': citation.get('pub_url', '')
            })
            
            time.sleep(1)
        
        return results
    
    def search_by_topic(self, topic: str, recent_years: int = 5) -> List[Dict]:
        """
        BEIREK ilgi alanlarına göre konusal arama
        
        Args:
            topic: Konu ("utility scale solar", "BESS", "project finance")
            recent_years: Son kaç yılı ara
        
        Returns:
            Liste: İlgili akademik makaleler
        """
        from datetime import datetime
        current_year = datetime.now().year
        
        return self.search_publications(
            query=topic,
            limit=15,
            year_low=current_year - recent_years
        )
```

### 15.4 BEIREK İçin Önerilen Arama Sorguları

```python
SCHOLAR_TOPICS = {
    "solar": [
        "utility scale solar PV project finance",
        "solar farm construction management",
        "photovoltaic grid integration",
        "solar power purchase agreement PPA"
    ],
    "wind": [
        "offshore wind project development",
        "wind farm EPC contract",
        "wind energy transmission infrastructure"
    ],
    "storage": [
        "battery energy storage systems BESS grid",
        "utility scale battery storage economics",
        "energy storage project finance"
    ],
    "datacenter": [
        "data center power infrastructure",
        "hyperscale data center energy efficiency",
        "data center renewable energy procurement"
    ],
    "project_finance": [
        "infrastructure project finance IFI",
        "renewable energy project financing",
        "development finance institution energy"
    ],
    "project_management": [
        "mega project management best practices",
        "EPC project delivery optimization",
        "construction project risk management"
    ]
}
```

### 15.5 Kullanım Örneği

```python
from modules.scholar import ScholarClient

# Client oluştur
scholar = ScholarClient()

# BESS konusunda son 3 yılın makalelerini ara
bess_papers = scholar.search_by_topic(
    topic="battery energy storage grid scale",
    recent_years=3
)

for paper in bess_papers:
    print(f"📄 {paper['title']}")
    print(f"   👥 {paper['authors']}")
    print(f"   📅 {paper['year']} | 🔗 Citations: {paper['citations']}")
    print()

# Spesifik sorgu
solar_finance = scholar.search_publications(
    query="utility scale solar project finance",
    limit=5,
    year_low=2022
)

# Yazar ara
author = scholar.search_author("Daniel Kammen")
if author:
    print(f"H-Index: {author['h_index']}")
    print(f"Citations: {author['citations']}")
```

### 15.6 Research Article'a Entegrasyon

```python
def enrich_article_with_scholar(topic: str, article_content: str) -> dict:
    """
    Makaleyi akademik verilerle zenginleştir (atıf/link YOK)
    
    Amaç: Ek istatistik ve trend verisi bulmak
    NOT: Referans listesi EKLENMEZ, sadece veriler kullanılır
    """
    scholar = ScholarClient()
    
    # İlgili akademik makaleleri bul
    papers = scholar.search_by_topic(topic, recent_years=3)
    
    # En çok atıf alan makalelerdeki VERİLERİ çıkar
    top_papers = sorted(papers, key=lambda x: x['citations'], reverse=True)[:5]
    
    # Akademik kaynaklardan ek veri/istatistik çıkar
    additional_data = []
    for paper in top_papers:
        if paper.get('abstract'):
            # Abstract'tan potansiyel veri noktaları
            additional_data.append({
                'source_title': paper['title'],
                'year': paper['year'],
                'abstract': paper['abstract'],
                'citations': paper['citations']  # Güvenilirlik göstergesi
            })
    
    # NOT: Bu veriler içerik üretiminde KULLANILIR
    # ama makaleye referans olarak EKLENMEZ
    return {
        'original_content': article_content,
        'additional_data': additional_data,
        'data_count': len(additional_data)
    }
```

**Kullanım Örneği:**
```python
# Scholar'dan ek veri al
enriched = enrich_article_with_scholar("BESS grid storage", article)

# Bu verileri prompt'a ekle (atıf olarak DEĞİL, veri olarak)
prompt = f"""
Aşağıdaki makaleyi zenginleştir.

MEVCUT MAKALE:
{enriched['original_content']}

EK VERİLER (kullanabilirsin, ATIF YAPMA):
{enriched['additional_data']}

Kurallar:
- Ek verileri doğal şekilde entegre et
- "Araştırmalara göre..." gibi ifadeler KULLANMA
- Verileri kendi bilgin gibi yaz
- Referans/link EKLEME
"""
```

### 15.7 Rate Limiting ve Dikkat Edilmesi Gerekenler

| Konu | Öneri |
|------|-------|
| İstek hızı | Her istek arası min 1-2 saniye bekle |
| Günlük limit | ~100 sorgu/gün güvenli |
| CAPTCHA | Çok fazla istek = CAPTCHA, proxy kullan |
| Proxy | ScraperAPI, Luminati gibi servisler |
| Cache | Sonuçları cache'le, tekrar sorma |

```python
# Cache örneği
import json
import os
from datetime import datetime, timedelta

CACHE_FILE = "data/scholar_cache.json"
CACHE_EXPIRY_HOURS = 24

def get_cached_or_fetch(query: str, fetch_func):
    """Cache'den al veya fetch et"""
    cache = load_cache()
    
    cache_key = query.lower().strip()
    
    if cache_key in cache:
        cached = cache[cache_key]
        cached_time = datetime.fromisoformat(cached['timestamp'])
        
        if datetime.now() - cached_time < timedelta(hours=CACHE_EXPIRY_HOURS):
            return cached['data']
    
    # Fetch et ve cache'le
    data = fetch_func(query)
    cache[cache_key] = {
        'timestamp': datetime.now().isoformat(),
        'data': data
    }
    save_cache(cache)
    
    return data
```

---

## 16. GÜNCELLENMİŞ DOSYA YAPISI

```
beirek-content-scout/
│
├── main.py
├── config.yaml
├── sources.yaml
├── requirements.txt
├── README.md
│
├── modules/
│   ├── __init__.py
│   ├── scanner.py              # RSS/Web tarama
│   ├── filter.py               # Claude filtreleme
│   ├── generator.py            # İçerik üretimi
│   ├── storage.py              # Dosya kaydetme
│   ├── ui.py                   # Terminal arayüzü
│   ├── typefully.py            # 🆕 Typefully API
│   └── scholar.py              # 🆕 Google Scholar
│
├── prompts/
│   ├── filter_prompt.txt
│   ├── article_prompt.txt
│   ├── linkedin_prompt.txt
│   └── twitter_prompt.txt
│
├── data/
│   ├── scout.db
│   ├── scholar_cache.json      # 🆕 Scholar cache
│   └── cache/
│
└── outputs/
    ├── articles/
    ├── linkedin/
    ├── twitter/
    └── archive/
```

---

## 17. GÜNCELLENMİŞ REQUIREMENTS.TXT

```
# Temel
feedparser>=6.0.0
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
pyyaml>=6.0.0
rich>=13.0.0

# Google Scholar
scholarly>=1.7.0

# Typefully (requests zaten var)
# Ek bağımlılık yok
```

---

## 18. GÜNCELLENMİŞ CONFIG.YAML

```yaml
# BEIREK Content Scout Configuration

app:
  name: "BEIREK Content Scout"
  version: "1.0.0"

scanning:
  max_articles_per_source: 10
  lookback_hours: 48
  batch_size: 10
  timeout_seconds: 30

filtering:
  min_relevance_score: 7
  claude_model: "default"

generation:
  article_min_words: 1500
  article_max_words: 2500
  linkedin_min_words: 150
  linkedin_max_words: 300
  twitter_min_tweets: 5
  twitter_max_tweets: 10
  
  # Research grade içerik için Scholar kullan
  enrich_with_scholar: true
  scholar_max_references: 3

storage:
  base_path: "./outputs"
  archive_after_days: 30
  
database:
  path: "./data/scout.db"

# 🆕 Typefully API
typefully:
  api_key: "YOUR_TYPEFULLY_API_KEY"
  default_platforms: ["x", "linkedin"]
  auto_publish: false  # true = hemen yayınla, false = draft
  default_tags: ["energy", "infrastructure"]

# 🆕 Google Scholar
scholar:
  enabled: true
  cache_expiry_hours: 24
  max_results_per_query: 10
  recent_years: 5
  proxy: null  # Opsiyonel: "http://proxy:port"

ui:
  show_emojis: true
  color_output: true
```

---

## 19. GÜNCELLENMİŞ KULLANICI AKIŞI

```
┌─────────────────────────────────────────────────────────────────┐
│                         BAŞLANGIÇ                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ANA MENÜ                                                        │
│  ─────────                                                       │
│  [1] 🔍 Yeni Tarama Başlat                                       │
│  [2] 📋 Bekleyen İçerikleri Gör                                  │
│  [3] ✍️  İçerik Üret                                             │
│  [4] 🎓 Scholar Araştırma                    ← 🆕                │
│  [5] 📤 Typefully'e Gönder                   ← 🆕                │
│  [6] 📊 İstatistikler                                            │
│  [7] ⚙️  Ayarlar                                                 │
│  [8] 🚪 Çıkış                                                    │
└─────────────────────────────────────────────────────────────────┘
```

### Yeni Menü: Scholar Araştırma
```
╔══════════════════════════════════════════════════════════════╗
║  🎓 GOOGLE SCHOLAR ARAŞTIRMA                                 ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  [1] 🔍 Konu Ara (serbest metin)                             ║
║  [2] 📚 BEIREK Konularında Ara                               ║
║  [3] 👤 Yazar Ara                                            ║
║  [4] 📖 Cache'lenmiş Sonuçları Gör                           ║
║                                                              ║
║  [M] Ana menü                                                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Yeni Menü: Typefully
```
╔══════════════════════════════════════════════════════════════╗
║  📤 TYPEFULLY                                                ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Bağlı Hesap: @beirek (X, LinkedIn)                          ║
║                                                              ║
║  [1] 📝 Üretilmiş İçeriği Gönder                             ║
║  [2] 📅 Zamanlanmış Yayın Oluştur                            ║
║  [3] 🚀 Hemen Yayınla                                        ║
║  [4] 🏷️  Etiketleri Yönet                                    ║
║                                                              ║
║  [M] Ana menü                                                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 21. SONUÇ

Bu doküman, BEIREK Content Scout uygulamasının tüm gereksinimlerini ve teknik detaylarını içermektedir. 

### İÇERİK YAKLAŞIMI: VERİ → YORUM → ÇÖZÜM

```
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│  GERÇEK VERİ   │────▶│ BEIREK YORUMU  │────▶│ BEIREK ÇÖZÜMÜ  │
│  (kaynaktan)   │     │ (özgün analiz) │     │ (lead gen)     │
└────────────────┘     └────────────────┘     └────────────────┘
   Halüsinasyon         "Ne anlama            "Biz bu konuda
   YASAK                 geliyor?"             ne yapıyoruz?"
```

### TEMEL ÖZELLİKLER

**İçerik Üretimi:**
- ✅ 300+ kaynaktan RSS/Web tarama
- ✅ Claude CLI ile akıllı filtreleme
- ✅ 3 format: Article, LinkedIn, Twitter
- ✅ Anti-halüsinasyon sistemi (veri doğrulama)

**İçerik Türleri:**
- ✅ Haber bazlı içerik (günlük tarama)
- ✅ Günlük kavram tanıtımı (7000+ terimlik sözlükten dinamik seçim)
- ✅ İstek havuzu (manuel konular)

**BEIREK Çalışma Alanları (8 Alan):**
- ✅ Deal & Contract Advisory
- ✅ CEO Office & Governance
- ✅ Development Finance & Compliance
- ✅ Project Development & Finance
- ✅ Engineering & Delivery
- ✅ Asset Management (O&M)
- ✅ GTM & JV Management
- ✅ Digital Platforms

**Thought Leadership:**
- ✅ Gerçek veriler + özgün BEIREK yorumu
- ✅ Her içerikte BEIREK çözümü/hizmeti
- ✅ Soft CTA ile lead generation
- ✅ Hizmet-konu eşleştirme tablosu

**Entegrasyonlar:**
- ✅ Typefully API (direkt yayın)
- ✅ Google Scholar (veri zenginleştirme)

**Klasör Yapısı:**
- ✅ BEIREK alanlarına göre organize içerik
- ✅ 31 alt klasör (8 ana alan + alt başlıklar)
- ✅ daily-concepts (günlük kavram - 7000+ sözlükten)
- ✅ istek-havuzu (manuel talepler)

### ÖRNEK ÇIKTI

```
HABER: "Texas'ta 500MW Solar Proje Financial Close'a Ulaştı"

↓ İÇERİK ÜRETİMİ ↓

1. VERİ: 500MW, $450M, Texas, 2027 COD
2. YORUM: Neden hızlı kapandı? Sektör için ne anlama geliyor?
3. ÇÖZÜM: Development Finance hizmetimizle siz de hızlandırabilirsiniz
```

### TAHMİNİ GELİŞTİRME SÜRESİ

| Faz | Süre | Kapsam |
|-----|------|--------|
| MVP | 3-4 gün | Tarama + Filtreleme + Temel üretim |
| v1.0 | 5-6 gün | + Anti-halüsinasyon + Typefully |
| v1.1 | 7-8 gün | + Scholar + Tam UI |

---

*Doküman Versiyonu: 2.0*
*Son Güncelleme: 30 Ocak 2026*

---

## EK-A: GÜNLÜK KAVRAM SEÇİM SİSTEMİ

### Sözlük Havuzu

Günlük kavram tanıtımı için **7000+ terimlik sözlük** kullanılır:
- Kaynak: `proje-sozlugu.md` dosyası
- İçerik: Finans, hukuk, mühendislik, yönetim terimleri
- Dil: İngilizce-Türkçe

### Dinamik Seçim Mantığı

Her gün sistem sözlükten **1 kavram** seçer. Seçim kriterleri:

```
┌─────────────────────────────────────────────────────────────────┐
│  KAVRAM SEÇİM KRİTERLERİ                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. BEIREK UYUMU                                                │
│     → 8 çalışma alanından birine doğrudan bağlı olmalı          │
│                                                                 │
│  2. ÇARPICILIK                                                  │
│     → Sektörde dikkat çekici, tartışmalı veya güncel            │
│     → "Bu kavramı herkes biliyor mu?" değil                     │
│     → "Bu kavram hakkında söylenecek ilginç şey var mı?"        │
│                                                                 │
│  3. İLGİ ÇEKİCİLİK                                              │
│     → C-level yöneticilerin ilgisini çekebilir                  │
│     → Karar verici seviyesinde tartışılabilir                   │
│                                                                 │
│  4. GÜNCEL BAĞLANTI                                             │
│     → O günkü haberlerle bağlantı kurulabilir (tercih)          │
│     → Sektördeki aktif tartışmalarla ilişkili                   │
│                                                                 │
│  5. TEKRARSIZLIK                                                │
│     → Daha önce seçilmemiş olmalı (is_used = 0)                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Seçim Akışı

```
SÖZLÜK HAVUZU (7000+ terim)
         │
         ▼
┌─────────────────────┐
│  Claude Analizi     │
│  ─────────────────  │
│  • BEIREK uyumu?    │
│  • Çarpıcı mı?      │
│  • Güncel bağlantı? │
│  • Daha önce kullanıldı mı? │
└──────────┬──────────┘
           │
           ▼
    GÜNÜN KAVRAMI
           │
           ▼
┌─────────────────────┐
│  3 Format Üretimi   │
│  ─────────────────  │
│  • Makale           │
│  • LinkedIn         │
│  • Twitter          │
└─────────────────────┘
```

### Yıllık Hedef

- **365 gün = 365 farklı kavram**
- Her kavram sadece 1 kez kullanılır
- Sözlük yeterince büyük (7000+), tükenmez

---

## EK-B: İSTEK HAVUZU KULLANIMI

### Kullanım Adımları

1. `content/10-istek-havuzu/` klasörüne yeni alt klasör oluştur
2. Klasör adı = konu başlığı (kebab-case)
3. (Opsiyonel) `brief.md` dosyası ekle
4. Sistem içeriği üretir ve kaydeder
5. İçerik ilgili BEIREK alanına kopyalanır

### Brief Dosyası Formatı (Opsiyonel)

```markdown
# Konu
[Detaylı konu başlığı]

# Odak
- [Vurgulanacak nokta 1]
- [Vurgulanacak nokta 2]

# Hedef Kitle
- [Kitle 1]
- [Kitle 2]

# BEIREK Alanı
[ana-alan/alt-alan]
```

### Örnek

```
content/10-istek-havuzu/
└── neom-hydrogen-project/
    ├── brief.md
    ├── makale.md      (üretilen)
    ├── linkedin.md    (üretilen)
    └── twitter.md     (üretilen)
```
