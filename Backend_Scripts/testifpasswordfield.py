import requests
from bs4 import BeautifulSoup
from time import sleep


def has_password_field(urlPassed):
    url = f'https://iprorouter.everlong.smisc.net/#/login'
    # url = f'http://localhost/login.htm'
    url = urlPassed
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            sleep(1)
            soup = BeautifulSoup(response.text, 'html.parser')
            # Search for input elements with type="password"
            if soup.find('input', {'type': 'password'}):
                print("I found apassword", url)
                return True
            else:
                print("NO PASSWORD FIELD", url)
                return False

    except requests.exceptions.RequestException:
        print("EXCEPTION with", url)
        return False

has_password_field('https://iprorouter.everlong.smisc.net/#/login')
has_password_field('google.com')
has_password_field('https://semantic-ui.com/examples/login.html')
has_password_field('192.168.68.1')
has_password_field('http://192.168.68.1')
has_password_field('http://192.168.68.1')