from tortoise import Model, fields
from setting import settings

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=100)

class KVStore(Model):
    id = fields.IntField(pk=True)
    key = fields.CharField(max_length=50, unique=True)
    value = fields.CharField(max_length=100)

def get_mysql_db_config() -> dict:
    return {
        "connections": {"default": {'engine': 'tortoise.backends.mysql',
                "credentials": {
                    'host': settings.DB_HOST,
                    'user': settings.DB_USER,
                    'password': settings.DB_PASS,  # password of mysql server
                    'port': settings.DB_PORT,
                    'database': settings.DB_NAME,  # name of mysql database server
                }
            },
        },
        "apps": {
            "models": {
                "models": ["model"],
                "default_connection": "default"
            },
        }
    }