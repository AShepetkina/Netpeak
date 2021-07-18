from os import getcwd
from selenium import webdriver
from time import sleep
import names
from selenium.webdriver.support.ui import Select
from random import randint

driver = webdriver.Chrome()

#1. Перейти по ссылке на главную страницу сайта Netpeak. (https://netpeak.ua/)

driver.get('https://netpeak.ua/')
sleep(1)

#2. Перейдите на страницу "Работа в Netpeak", нажав на кнопку "Карьера"

careerButton = driver.find_element_by_xpath('//*[@id="rec278727844"]/div/div/div/div[1]/div/nav/div[1]/div[1]/ul/li[4]/a')
careerButton.click()
sleep(2)

secondWindow = driver.window_handles[1]
driver.switch_to.window(secondWindow)

#3. Перейти на страницу заполнения анкеты, нажав кнопку - "Я хочу работать в Netpeak"

applicationForm = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[5]/div/a')
applicationForm.click()

#4. Загрузить файл с недопустимым форматом в блоке "Резюме", например png, и проверить 
# что на странице появилось сообщение, о том что формат изображения неверный.

cvButton = driver.find_element_by_xpath('//input[@name = "up_file"]')
file = getcwd() + '/2021-07-11.png'
cvButton.send_keys(file) 

errorMessage = driver.find_element_by_xpath('//*[@id="up_file_name"]')
sleep(5)
assert errorMessage.text == 'Ошибка: неверный формат файла (разрешённые форматы: doc, docx, pdf, txt, odt, rtf).'

#5. Заполнить случайными данными блок "3. Личные данные"

nameInput = driver.find_element_by_xpath('//*[@id = "inputName"]')
nameInput.send_keys(names.get_first_name())

lastNameInput = driver.find_element_by_xpath('//*[@id = "inputLastname"]')
lastNameInput.send_keys(names.get_last_name())

emailInput = driver.find_element_by_xpath('//*[@id = "inputEmail"]')

email = names.get_full_name().replace(" ", "") + "@gmail.com"
emailInput.send_keys(email)

yearSelect = Select(driver.find_element_by_xpath('//select[@name = "by"]'))
year = randint(1952, 2003)
yearSelect.select_by_visible_text(str(year))

monthSelect = Select(driver.find_element_by_xpath('//select[@name = "bm"]'))
month = randint(1,12)
monthSelect.select_by_index(month)

daySelect = Select(driver.find_element_by_xpath('//select[@name = "bd"]'))
day = randint(1,28)
daySelect.select_by_index(day)

phoneInput = driver.find_element_by_xpath('//*[@id = "inputPhone"]')
number = randint(79000000000, 79999999999)
phone = "+" + str(number)
phoneInput.send_keys(phone)

#6. Нажать на кнопку отправить резюме

submitButton = driver.find_element_by_xpath('//*[@id = "submit"]')
submitButton.click()

sleep(3)

#7. Проверить что сообщение на текущей странице  - "Все поля являются обязательными для 
# заполнения" - подсветилось красным цветом

requiredFieldsMessage = driver.find_element_by_xpath('//p[@class="warning-fields help-block"]')
assert requiredFieldsMessage.text == 'Все поля являются обязательными для заполнения'
realColor = requiredFieldsMessage.value_of_css_property('color')
assert realColor == 'rgba(255, 0, 0, 1)'

#8. Перейти на страницу "Курсы" нажав соответствующую кнопку в меню и убедиться 
# что открылась нужная страница.

coursesButton = driver.find_element_by_xpath(u'//a[text()="Курсы"]')
coursesButton.click()

assert driver.current_url == 'https://school.netpeak.group/'

driver.close()

