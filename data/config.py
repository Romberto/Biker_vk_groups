import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = str(os.getenv('TOKEN'))
VK_TOKEN = str(os.getenv('VK'))
CHANAL_ID = str(os.getenv('CHANAL_ID'))

GROUP_IDs = ['-220310598'] # список групп
DEPLOY = 5 # задержка между обходом групп
DEPLOY_POST = 5 # задержка между постингов в групу( в нутри идущенго цикла)

PATH_TO_DB = "mydatapost.db"