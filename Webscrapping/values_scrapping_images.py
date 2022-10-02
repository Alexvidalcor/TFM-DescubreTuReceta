#Importación de librerías

import os

'''
        VARIABLES GENERALES
'''

# URL a scrapear y número de imágenes a tomar por producto
urlToScrap = "https://images.google.com/"
numberImagesTaken = 5

# Relacionadas con la ingesta de los productos a scrapear
pathToDF = ""
fileToDF = "https://www.dropbox.com/s/fsmrn97gbdmoznh/input_scrapping_images.csv?raw=1"
colTarget = 0

# Nombre del output final y de los checkpoints intermedios
nameOutput = "output_scrapping_images.csv"
nameInter = "inter_scrapping_images.csv"


# Webdriver a usar por Selenium. Se ha escrito soporte para Firefox (geckodriver) y para Chromium/Chrome(chromedriver)
webdriverToUse = "firefox"

# Rutas para almacenar logs
logPath = "webscrapping-resources/logs/"
imagesPath = "webscrapping-resources/images/"

# Variables extras que modifican la lógica del scrapping. 
deleteOldLogs = True
enableFullErrors = False
takeScreenshot = False
downloadImages = True
compressImages = True
linkWebCSV = True


# Variables que almacenan los xPath principales que necesitará Selenium para moverse entre páginas web.
# Se incluye soporte para Firefox y Chromium/Chrome
'''
        VARIABLES FIREFOX
'''

if webdriverToUse == "firefox":
    privacyButton = "/html/body/div[2]/div[2]/div[3]/span/div/div/div/div[3]/div[1]/button[2]/div"
    searchImageBar = "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input"
    selectImageSearched ="/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[1]/a[1]/div[1]/img"
    selectDefImage = '/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img'



'''
        VARIABLES CHROMIUM
'''

if webdriverToUse != "firefox":
    privacyButton = "/html/body/div[2]/div[2]/div[3]/span/div/div/div/div[3]/div[1]/button[2]/div"
    searchImageBar = "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input"
    selectImageSearched ="/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[1]/a[1]/div[1]/img"
    selectDefImage = "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img"