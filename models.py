from peewee import Model, SqliteDatabase, CharField, TextField

my_database = SqliteDatabase("translations.db") #Creating and initializing the database with name "translations.db"

class TranslationModel(Model):
    """
    - Define a database table and the columns in that table.
    - We will have _ columns in the table which are initialized below.
    - When ew create a new record in the table, the client will send text to be translated, the base language of the
      text and the final language to which the text has be translated. The translation field will be empty initially,
      because it is us who need to generate the translation. The client won't be doing it.
    """
    text = TextField()
    base_lang = CharField()
    final_lang = CharField()
    translation = TextField(null = True)

    class Meta:
        """
        Tells which database to be used so as to store the model
        """
        database = my_database

my_database.create_tables([TranslationModel])



