
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz

BOT_TOKEN = '7624103848:AAGxyyzQOZorYzCZJYkaW1198IvF4HKs_qQ'
CHAT_ID = '1741470483'

def obtener_titulares_gestion(fecha_obj):
    print("🟣 Scrapeando Gestión...")
    URL = "https://gestion.pe"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(URL, headers=headers)
    if response.status_code != 200:
        print(f"❌ Error Gestión: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    articulos = soup.select('h2 a')
    noticias = []
    for a in articulos[:10]:
        titulo = a.get_text(strip=True)
        link = a['href']
        if not link.startswith('http'):
            link = 'https://gestion.pe' + link
        noticias.append(f"- {titulo} ({link})")
        print(f"✔️ Gestión: {titulo}")
    return noticias

def obtener_titulares_comercio(fecha_obj):
    print("🔵 Scrapeando El Comercio...")
    URL = "https://elcomercio.pe"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(URL, headers=headers)
    if response.status_code != 200:
        print(f"❌ Error El Comercio: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    articulos = soup.select('h2 a')
    noticias = []
    for a in articulos[:10]:
        titulo = a.get_text(strip=True)
        link = a['href']
        if not link.startswith('http'):
            link = 'https://elcomercio.pe' + link
        noticias.append(f"- {titulo} ({link})")
        print(f"✔️ El Comercio: {titulo}")
    return noticias

def enviar_resumen():
    tz = pytz.timezone('America/Lima')
    ahora = datetime.now(tz)
    fecha_str = ahora.strftime("%d/%m/%Y")
    
    gestion = obtener_titulares_gestion(ahora)
    mensaje_gestion = f"🗞️ Titulares de Gestión - {fecha_str}\n\n" + "\n".join(gestion) if gestion else f"No se encontraron titulares de Gestión ({fecha_str})"
    
    comercio = obtener_titulares_comercio(ahora)
    mensaje_comercio = f"🗞️ Titulares de El Comercio - {fecha_str}\n\n" + "\n".join(comercio) if comercio else f"No se encontraron titulares de El Comercio ({fecha_str})"
    
    for mensaje in [mensaje_gestion, mensaje_comercio]:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        datos = {
            'chat_id': CHAT_ID,
            'text': mensaje,
            'disable_web_page_preview': True
        }
        r = requests.post(url, data=datos)
        print(f"📤 Enviado a Telegram: {r.status_code} - {r.text}")

enviar_resumen()
