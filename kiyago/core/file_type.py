import yaml


def langsrc2filetype(lang:str):

    with open("./kiyago/core/lang_config.yaml") as f:
        X = yaml.load(f, Loader=yaml.FullLoader)
        if lang in X["src"]:
            return(X["src"][lang])
        else:
            return ""
    
    return ""

def langbin2filetype(lang:str):

    with open("./kiyago/core/lang_config.yaml") as f:
        X = yaml.load(f, Loader=yaml.FullLoader)
        if lang in X["bin"]:
            return(X["bin"][lang])
        else:
            return ""
    
    return ""

