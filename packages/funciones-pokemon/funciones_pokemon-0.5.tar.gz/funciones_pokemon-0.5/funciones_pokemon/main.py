import pandas as pd

def get_grupos_pokemon(data):
    return data['egg_group'].tolist()

def get_altura_media_grupo(data, grupo):
    return data[data['egg_group'] == grupo]['height']

def get_peso_medio_grupo(data, grupo):
    return data[data['egg_group'] == grupo]['weight']