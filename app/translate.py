
import deepl,requests
from flask_babel import _
from app import app, translator

def translate(text,source_language,dest_language):
   
    if not translator:
        return _('Error: the translation service is not configured.')
    result = translator.translate_text(text,source_lang=source_language,
    target_lang = dest_language)

    if result.text =='':
        return _('Error: the translation service has failed')
    else:
        return result.text

