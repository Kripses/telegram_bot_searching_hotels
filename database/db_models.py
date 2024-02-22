from peewee import AutoField, CharField, IntegerField, Model, SqliteDatabase

DB_PATH = "database/database.db"
db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField(primary_key=True)
    username = CharField(null=True)
    first_name = CharField(null=True)


db.create_tables([User])


class Search(BaseModel):
    user_id = AutoField()
    city_search = CharField()
    country_search = CharField()
    hotel_amt_search = IntegerField()
    search_mode = CharField()
    arrival_date = CharField(null=True)
    departure_date = CharField(null=True)
    guest_qty = CharField()
    search_func = CharField()
    high_value = CharField(null=True)
    low_value = CharField(null=True)


# class SearchState(StatesGroup):

db.create_tables([Search])


def create_models():
    db.create_tables(BaseModel.__subclasses__())


def create_user(message):
    user_id = message.from_user.id
    try:
        username = message.from_user.username
        first_name = message.from_user.first_name
    except Exception:
        username = "None"
        first_name = message.from_user.first_name

    User.create(user_id=user_id, username=username, first_name=first_name)

    Search.create(
        user_id=user_id,
        city_search="",
        country_search="",
        hotel_amt_search=0,
        search_mode="",
        arrival_date="",
        departure_date="",
        guest_qty="",
        search_func="",
        high_value="",
        low_value="",
    )
