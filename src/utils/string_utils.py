import re

def normalize_string(s:str)->str:
    characters_to_remove = "-/!()@ "

    pattern = "[" + characters_to_remove + "]"
    new_string = re.sub(pattern, "", s)
    return new_string.lower()