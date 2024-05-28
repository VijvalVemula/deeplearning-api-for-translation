"""
This file contains the tasks that we need to run at the backend in order to power all the routes.
"""
from models import TranslationModel
from transformers import T5Tokenizer, T5ForConditionalGeneration

# for larger models, t5-base and t5-large

# tokenizer to transform words to number
tokenizer = T5Tokenizer.from_pretrained("t5-small", model_max_length = 512)
# Translator to use the numbers from tokenizer and translate them
translator = T5ForConditionalGeneration.from_pretrained("t5-small")


"""
Task 1: store_translation
- take in a translation request and save it to database.
"""
def store_translation(translation):
    model = TranslationModel(
        text = translation.text,
        base_lang = translation.base_lang,
        final_lang = translation.final_lang
    )
    model.save()
    return model.id

"""
Task 2: run_translation
- Run a pretrained deep learning model.
"""
def run_translation(translation_id : int):
    model = TranslationModel.get_by_id(translation_id)

    prefix = f"translate {model.base_lang} to {model.final_lang} : {model.text}"
    input_ids = tokenizer(prefix, return_tensors = "pt").input_ids

    outputs = translator.generate(input_ids, max_new_tokens = 512)
    translation = tokenizer.decode(outputs[0], skip_special_tokens = True)
    model.translation = translation
    model.save()

"""
Task 3: find_translation
- Retrieve the translation for the database.
"""
def find_translation(translation_id : int):
    model = TranslationModel.get_by_id(translation_id)

    translation = model.translation
    if translation is None:
        translation = "Processing, check back later..."
    return translation


