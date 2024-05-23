from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
    "tour_db": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "etlmysqlDM",
        "USER": "bigDM",
        "PASSWORD": "bigDM1234@",
        "HOST": "localhost",
        "PORT": "3306",
    }
}



# SECRET_KEY
# settings.py에서 복사하고 SECRET_KEY 주석 처리
# DATABASES 주석 처리
SECRET_KEY = 'django-insecure-$hkc4pab^ua_%10+1_9)5c@3e)^+kx149-)r(%w$1rdlts4_vt'
