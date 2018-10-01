from django.template.defaulttags import register

from transliterate import translit


@register.filter
def name_to_tag_part(name: str) -> str:
    transliterated = translit(name, 'ru', reversed=True)
    filtered = ''.join([x for x in transliterated if x.isalnum()])
    result = filtered.lower()

    return result
