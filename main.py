import time
import requests
from bs4 import BeautifulSoup
import telegram

# ---------------------------
# CONFIGURATION
# ---------------------------
FIRST_NUMBER = "282099018490"
SECOND_NUMBER = "109991022018490007"
URL = "https://minha.anem.dz/pre_inscription"

TELEGRAM_TOKEN = "7695653978:AAGjNDXcfjxW9xTJf8ZBWzg5SUZcV6mFIww"
CHAT_ID = "1906111091"

NO_DATE_TEXTS = [
    "نعتذر منكم",  # Arabic
    "Nous sommes désolés",  # French
    "We are sorry"  # English (if available)
]

# ---------------------------
# FUNCTION
# ---------------------------
def check_dates():
    session = requests.Session()
    
    # Step 1: Access the initial page
    response = session.get(URL)
    if response.status_code != 200:
        print("Failed to load page.")
        return False

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find hidden fields or tokens if needed
    try:
        csrf_token = soup.find('input', {'name': '_token'})['value']
    except:
        csrf_token = None

    # Step 2: Submit the two numbers
    payload = {
        "_token": csrf_token,
        "numero_nin": FIRST_NUMBER,
        "numero_anem": SECOND_NUMBER,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    post_response = session.post(URL, data=payload, headers=headers)

    if post_response.status_code != 200:
        print("Failed to submit numbers.")
        return False

    time.sleep(10)  # Wait for popup simulation time

    # Step 3: Access the second step page
    soup = BeautifulSoup(post_response.text, 'html.parser')
    page_text = soup.get_text()

    # Step 4: Check if dates available
    if any(word in page_text for word in NO_DATE_TEXTS):
        print("No dates available.")
        return False
    else:
        print("Dates available!")
        send_alert()
        return True

def send_alert():
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    bot.send_message(
        chat_id=CHAT_ID,
        text="⚡ Good news! Dates are available! Go fast: https://minha.anem.dz/pre_inscription"
    )

if __name__ == "__main__":
    check_dates()
