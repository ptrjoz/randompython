#Multiple string replacement
#replace = { ":": "", ";": "", " ": "-", ".": "", ",": "", "?": "", "'": "", "/": ""}
#stringo = "AAAA:BBB;CCC DDD.EEE,FFF?GGG'HHH/III"
def replace_multiple(text, replace):
    for k, v in replace.items():
        text = text.replace(k, v)
    return text
