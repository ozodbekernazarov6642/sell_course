from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = '6989708033:AAElDGLT2t9nNObxPeBS-yohs5_k646yHzE'  # Bot toekn
ADMINS = [6642693329] # adminlar ro'yxati

DB_USER = 'sell_course'
DB_PASS = '6DOGuMv2aPco'
DB_NAME = 'downloader'
DB_HOST = 'ep-patient-term-a5d8qhcl.us-east-2.aws.neon.tech'