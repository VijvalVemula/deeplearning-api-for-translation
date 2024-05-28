"""
We will be creating 3 routes.

Route 1: /
- This is the index route.
- Checks if everything is okay.
- returns as message if everything is okay:
    {
        "message" : "Hello World!!"
    }

Route 2: /translate
- Takes in a translation request, and stores it in the database.
- Translation will not take place here, as we may have large amount of text and may get timed out error.
- returns a translation_id

Route 3: /results
- Take in a translation id.
- return the translated text

Note: To support these routes we need couple of python files, namely tasks.py and models.py
"""


from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, validator
import tasks
"""
- FastAPI ==> To create webserver, BackgroundTasks ==> To perform translation tasks in the background
- Used to validate the data we get from the client as input to the api. Validations is important or otherwise we may 
  get into random error.
- import background the tasks from the tasks.py file.
"""

app = FastAPI() #Initialise the web application api

languages = ["English", "French", "Italian", "German", "Romanian", "Spanish"]

class Translation(BaseModel):
    text : str
    base_lang : str
    final_lang : str

    @validator("base_lang", "final_lang")
    def valid_lang(cls, lang):
        if lang not in languages:
            raise ValueError("Invalid Language")
        return lang


#Route 1: /index_route
@app.get("/")
def get_root():
    return {"message" : "Hello World!"}

#Route 2: /translate
@app.post("/translate")
def post_translation(translation : Translation, background_tasks : BackgroundTasks):
    # Store the translation
    # Run translation in background
    translation_id = tasks.store_translation(translation)
    background_tasks.add_task(tasks.run_translation,translation_id)
    return {"task_id" : translation_id}

# Route 3: /results
@app.get("/results")
def get_translations(translation_id : int):
    return {"translation" : tasks.find_translation(translation_id)}


# "loginServer": "dqdlapi.azurecr.io",


