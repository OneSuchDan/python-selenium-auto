import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import NoSuchElementException, ElementNotInteractableException

URL = "https://public.ciudadanosenmovimiento.org" #En este caso especifico se utilizo esta url, se puede pasar por parametro

class StoreSele(webdriver.Chrome):

    def __init__(self, teardown=False):
        self.teardown = teardown
        super(StoreSele, self).__init__()
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    # Obtener URL
    def get_url(self):
        self.get(URL)
    #Obtener error de Servidor
    def get_error(self,full_name=""):
        try:
            conditional = self.find_element(By.XPATH,
                                        ('//p[contains(text(),"Server error: `GET https://mcuniversoapi-app.wittycoast-aad90e96.southcentralus.azurecontainerapps.io/api/PerfilPrecandidatura/perfil?alias=salvadormaciasmaestro` resulted in a `500 Internal Server Error` response")][1]'))
        except NoSuchElementException:
            pass
        else:
            print("Server error al subir: "+full_name)


    # Rellenar formulario buscando XPATH en el dom
    def rellenar_form(self, full_name="", section="", code="", number="", email="correo@yahoo.com"):
        self.maximize_window() #Expande ventana
        self.implicitly_wait(2) #Da dos segundos para que espere a cargar la pagina
        xpathInfo = '//span[contains(text(), "Quiero respaldar la candidatura de Ayuntamiento")]'
        boton = self.find_element(By.XPATH, xpathInfo) 
        boton.click()   #Selecciona en el dom el {xpathInfo} para dar click
        names = self.find_element(By.XPATH,
                                  "//div[@class='flex flex-col gap-4'][1]/div[@class='MuiFormControl-root MuiFormControl-fullWidth MuiTextField-root css-feqhe6'][1]/div[@class='MuiInputBase-root MuiOutlinedInput-root MuiInputBase-colorPrimary MuiInputBase-fullWidth MuiInputBase-formControl css-1gjzvlw'][1]/input")
        names.send_keys(full_name)
        seccion = self.find_element(By.XPATH, "//input[@id='Sección'][1]")
        seccion.send_keys(section)
        clave = self.find_element(By.XPATH, "//input[@id='clave']")
        clave.send_keys(code)
        phone = self.find_element(By.XPATH,
                                  "//div[@class='flex flex-col gap-4'][2]/div[@class='MuiFormControl-root MuiFormControl-fullWidth MuiTextField-root css-feqhe6'][1]/div[@class='MuiInputBase-root MuiOutlinedInput-root MuiInputBase-colorPrimary MuiInputBase-fullWidth MuiInputBase-formControl css-1gjzvlw'][1]/input")
        phone.send_keys(number)
        mail = self.find_element(By.XPATH,
                                 "//div[@class='flex flex-col gap-4'][2]/div[@class='MuiFormControl-root MuiFormControl-fullWidth MuiTextField-root css-feqhe6'][2]/div[@class='MuiInputBase-root MuiOutlinedInput-root MuiInputBase-colorPrimary MuiInputBase-fullWidth MuiInputBase-formControl css-1gjzvlw'][1]/input")
        mail.send_keys(email)
        # check_info = self.find_element(By.XPATH,
        #                                "//label[@class='MuiFormControlLabel-root MuiFormControlLabel-labelPlacementEnd css-1jaw3da'][1]/span[@class='MuiButtonBase-root MuiCheckbox-root MuiCheckbox-colorPrimary MuiCheckbox-sizeMedium PrivateSwitchBase-root MuiCheckbox-root MuiCheckbox-colorPrimary MuiCheckbox-sizeMedium MuiCheckbox-root MuiCheckbox-colorPrimary MuiCheckbox-sizeMedium css-1yatoyc'][1]/input[@class='PrivateSwitchBase-input css-1m9pwf3'][1]")
        # check_info.click()
        check_privacity = self.find_element(By.XPATH,
                                            "//label[@class='MuiFormControlLabel-root MuiFormControlLabel-labelPlacementEnd css-1jaw3da'][2]/span[@class='MuiButtonBase-root MuiCheckbox-root MuiCheckbox-colorPrimary MuiCheckbox-sizeMedium PrivateSwitchBase-root MuiCheckbox-root MuiCheckbox-colorPrimary MuiCheckbox-sizeMedium MuiCheckbox-root MuiCheckbox-colorPrimary MuiCheckbox-sizeMedium css-1yatoyc'][1]/input[@class='PrivateSwitchBase-input css-1m9pwf3'][1]")
        check_privacity.click()
        #Si se ingresan los datos correctamente se activa el boton
        try:
            confirm_button = self.find_element(By.XPATH,'//*[@id="app"]/div/div/div[2]/main/div/div[4]/div/div[2]/div[4]/button')
            confirm_button.click()
        except:
            logging.error(f"{full_name} no se envio por informacion incorrecta")
        else:
            logging.info(f"{full_name} registrado")
            time.sleep(1)