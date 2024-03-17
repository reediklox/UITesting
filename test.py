from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep

# Инициализируем драйвер
driver = webdriver.Chrome()

# Открываем веб-страницу
driver.get("https://yandex.by/search/?text=keep_alive+selenium&clid=2270470&banerid=0401004991%3ASW-55b1398556c1&win=628&lr=157")

# Найдем элемент, в который хотим вставить текст
element = driver.find_element(By.XPATH, '//input[contains(@name, "text")]')

# Получаем текст из буфера обмена
text_to_paste = "Текст для вставки из буфера обмена"

# Нажимаем комбинацию клавиш для вставки (Ctrl + V)
element.clear()
element.send_keys(Keys.CONTROL, 'v')

# Можно также просто вставить текст, используя метод send_keys
# element.send_keys(text_to_paste)
sleep(10)
# Закрываем драйвер
driver.quit()



