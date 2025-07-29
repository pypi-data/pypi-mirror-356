import json

def read_json(path):
    data = json.load(open(path, 'r', encoding='UTF-8'))
    return data

def translatable_to_list(data, language=None):
    values = []
    for d in data:
        s = []
        if language is not None:
            if d['code'] != language:
                continue
        else:
            s.append("[%s] " % d['code'])
        for p in d['parts']:
            s.append(p['str'])
        values.append(' '.join(s))
    return values        
