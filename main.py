import time
import cv2
import pyautogui
import numpy as np
import time
from PIL import ImageGrab
import pyautogui
import random
import requests
from bs4 import BeautifulSoup
from pynput.keyboard import Controller

keyboard = Controller()
unlock_chest = cv2.imread('templates/unlock_chest.png')
unlock_code = cv2.imread('templates/unlock_code.png')
flip = cv2.imread('templates/flip.png')
done = cv2.imread('templates/done.png')
already_used = cv2.imread('templates/already_used.png')
ok = cv2.imread('templates/ok.png')
exit = cv2.imread('templates/exit.png')


def template_match(image, template):
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    threshold = 0.4  # Adjust the threshold as needed
    if max_val >= threshold:
        return max_loc

    return None


def match_location(temp):
    found = True
    time.sleep(2)
    while found:
        screenshot = np.array(ImageGrab.grab())
        location = template_match(screenshot, temp)
        if location is not None:
            click_x = location[0] + temp.shape[1] // 2
            click_y = location[1] + temp.shape[0] // 2
            pyautogui.moveTo(click_x, click_y)
            time.sleep(0.1)
            pyautogui.click()
            found = False


# Make a GET request to the website
url = "https://incendar.com/idlechampions_codes.php"  # Replace with the URL of the website you want to scrape
lista = []
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find all the <strong> tags
textarea_element = soup.find('textarea', {'id': 'i11'})

# Extract the value from the textarea element
if textarea_element:
    textarea_value = textarea_element.text

    # Split the lines based on the newline character
    lines = textarea_value.rstrip().split('\n')

    # Print each line
    for line in lines:
        cleaned_line = line.replace('-', '').replace('\r', '')
        if len(cleaned_line) > 13:
            continue
        else:
            lista.append(cleaned_line)

print(lista)

time.sleep(3)


def used(temp):
    time.sleep(1)
    screenshot = np.array(ImageGrab.grab())
    location = template_match(screenshot, temp)
    if location is not None:
        return True
    else:
        return False


lista = ['ODAHRIFEHIZZ', 'SUNNY&CASUAL', 'DEVSFANKMERI', 'NEALCHASNABS', 'SHIMMAXIWAKE', 'DEIFPOLEOLES',
         'VACATIONSOON', 'SKEOINBYOMER']

for code in lista:
    time.sleep(2)
    match_location(unlock_chest)
    time.sleep(1)
    keyboard.type(code)
    time.sleep(1)
    match_location(unlock_code)
    if used(already_used):
        match_location(ok)
        match_location(exit)
        continue
    time.sleep(5)
    match_location(flip)
    match_location(done)
