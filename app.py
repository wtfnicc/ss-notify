import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage

URL = 'https://www.ss.lv/lv/real-estate/flats/jelgava-and-reg/jelgava/filter/'

HEADERS = {
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'application/x-www-form-urlencoded'
}

PAYLOAD = {
    'topt[8][min]': '30000',
    'topt[8][max]': '50000',
    'topt[1][min]': '2',
    'topt[1][max]': '2',
    'topt[3][min]': '40',
    'topt[3][max]': '55',
    'topt[4][max]': '3',
    'sid': '/lv/real-estate/flats/jelgava-and-reg/jelgava/filter/'
}

# Store known ad IDs in memory
known_ads = set()

# Email config
EMAIL_ADDRESS = 'your_email@gmail.com'
EMAIL_PASSWORD = 'your_app_password'
RECIPIENT = 'niks1315@gmail.com'

def send_email(subject, body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def check_for_new_ads():
    session = requests.Session()
    response = session.post(URL, data=PAYLOAD, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.select('tr[id^=tr_]')

    new_ads_found = False

    for row in rows:
        ad_id = row.get('id')
        if ad_id and ad_id not in known_ads:
            known_ads.add(ad_id)
            title_elem = row.select_one('td.msga2-o.pp0 a')
            if title_elem:
                title = title_elem.text.strip()
                link = "https://www.ss.lv" + title_elem['href']
                print(f"🆕 New ad: {title} → {link}")

                # Send email notification
                send_email(
                    subject='🆕 Jauns dzīvokļa sludinājums Jelgavā',
                    body=f'{title}\n{link}'
                )

                new_ads_found = True

    if not new_ads_found:
        print("✅ No new ads.")

# Only run once (Render runs scheduled jobs like this)
if __name__ == "__main__":
    print("🔎 Checking for new listings...")
    check_for_new_ads()
