import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = str(os.getenv('TOKEN'))
VK_TOKEN = str(os.getenv('VK'))
CHANAL_ID = str(os.getenv('CHANAL_ID'))

GROUP_IDs = {'-215864608':'Модернизированные трактора',
             '-220310598': "Imperia's Wheels MCC", '-39710761': "Engels MOTO",
             '-107880833': '-Мотосообщество - Свободное Братство MCC',
             '-220151587': "Мото мастерская «Авангард»",
             '-153161312':"MotoBraZZers[64]МотоМУВ!",
             '-19471446':'Байк-клуб "Девятый Блок MC"'
             } # список групп
DEPLOY = 5 # задержка между обходом групп
DEPLOY_POST = 5 # задержка между постингов в групу( в нутри идущенго цикла)

PATH_TO_DB = "mydatapost.db"