#!/bin/bash
#
# BEIREK Content Scout - Tıkla Çalıştır
# =====================================
# Bu dosyaya çift tıklayarak uygulamayı başlatabilirsiniz.
#

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script'in bulunduğu dizine git
cd "$(dirname "$0")"

echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     BEIREK Content Scout - Başlatılıyor      ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════╝${NC}"
echo ""

# Python kontrolü
echo -e "${YELLOW}[1/4]${NC} Python kontrol ediliyor..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo -e "${GREEN}✓${NC} $PYTHON_VERSION bulundu"
else
    echo -e "${RED}✗ Python3 bulunamadı!${NC}"
    echo ""
    echo "Python'u yüklemek için: https://www.python.org/downloads/"
    echo "veya Homebrew ile: brew install python3"
    echo ""
    read -p "Çıkmak için Enter'a basın..."
    exit 1
fi

# Virtual environment kontrolü
echo -e "${YELLOW}[2/4]${NC} Virtual environment kontrol ediliyor..."
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}→${NC} venv oluşturuluyor..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ Virtual environment oluşturulamadı!${NC}"
        read -p "Çıkmak için Enter'a basın..."
        exit 1
    fi
    echo -e "${GREEN}✓${NC} venv oluşturuldu"
else
    echo -e "${GREEN}✓${NC} venv mevcut"
fi

# venv'i aktive et
echo -e "${YELLOW}[3/4]${NC} Virtual environment aktive ediliyor..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Virtual environment aktive edilemedi!${NC}"
    read -p "Çıkmak için Enter'a basın..."
    exit 1
fi
echo -e "${GREEN}✓${NC} venv aktif"

# Bağımlılıkları kontrol et ve yükle
echo -e "${YELLOW}[4/4]${NC} Bağımlılıklar kontrol ediliyor..."
pip install -q --upgrade pip 2>/dev/null

# requirements.txt'den eksik paketleri kontrol et
MISSING_PACKAGES=false
while IFS= read -r line || [[ -n "$line" ]]; do
    # Boş satırları ve yorumları atla
    [[ -z "$line" || "$line" =~ ^# ]] && continue

    # Paket adını al (>=, ==, vb. önce)
    PACKAGE=$(echo "$line" | sed 's/[>=<].*//')

    # Paket yüklü mü kontrol et
    if ! pip show "$PACKAGE" &> /dev/null; then
        MISSING_PACKAGES=true
        break
    fi
done < requirements.txt

if [ "$MISSING_PACKAGES" = true ]; then
    echo -e "${YELLOW}→${NC} Eksik paketler yükleniyor..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ Paket yükleme başarısız!${NC}"
        read -p "Çıkmak için Enter'a basın..."
        exit 1
    fi
    echo -e "${GREEN}✓${NC} Tüm paketler yüklendi"
else
    echo -e "${GREEN}✓${NC} Tüm paketler mevcut"
fi

# Uygulamayı başlat
echo ""
echo -e "${GREEN}════════════════════════════════════════════════${NC}"
echo -e "${GREEN}           Uygulama başlatılıyor...             ${NC}"
echo -e "${GREEN}════════════════════════════════════════════════${NC}"
echo ""

python3 main.py

# Uygulama kapandığında
echo ""
echo -e "${BLUE}Uygulama kapatıldı.${NC}"
read -p "Pencereyi kapatmak için Enter'a basın..."
