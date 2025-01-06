from flask import Flask, request, render_template
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
import os
import requests
from datetime import datetime

app = Flask(__name__)

# XML dosyasına veri eklemek için bir fonksiyon
def log_to_xml(data):
    xml_file_path = "site_data_log.xml"

    if os.path.exists(xml_file_path):
        # XML dosyasını yükle
        tree = ElementTree()
        tree.parse(xml_file_path)
        root = tree.getroot()
    else:
        # Yeni bir XML dosyası oluştur
        root = Element("Sites")
        tree = ElementTree(root)

    # Yeni bir site elemanı ekle
    site = SubElement(root, "Site")

    for key, value in data.items():
        element = SubElement(site, key)
        element.text = value

    # XML dosyasını kaydet
    tree.write(xml_file_path, encoding="utf-8", xml_declaration=True)

@app.route('/', methods=['GET', 'POST'])
def check_site():
    result = None
    if request.method == 'POST':
        kaynak_id = request.form['kaynakID']
        kaynak_adi = request.form['kaynakAdi']
        kaynak_detay = request.form['kaynakDetay']
        kaynak_url = request.form['kaynakURL']
        zaman_damgasi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            response = requests.get(kaynak_url, timeout=5)
            if response.status_code >= 200 and response.status_code < 400:
                result = "Erişilebilir"
            else:
                result = f"Erişilemez (HTTP Kod: {response.status_code})"
        except requests.exceptions.RequestException:
            result = "Erişim sağlanamadı (Bağlantı hatası)"

        # XML'e kaydedilecek veri
        data = {
            "KaynakID": kaynak_id,
            "KaynakAdi": kaynak_adi,
            "KaynakDetay": kaynak_detay,
            "KaynakURL": kaynak_url,
            "KaynakZamanDamgasi": zaman_damgasi,
            "Durum": result
        }

        log_to_xml(data)

    return render_template("form.html", result=result)

if __name__ == '__main__':
    app.run(debug=True)
