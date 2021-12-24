import requests


def get_similar_words(target):
    url = "https://twinword-word-associations-v1.p.rapidapi.com/associations/"
    querystring = {"entry": target}
    headers = {
        'x-rapidapi-host': "twinword-word-associations-v1.p.rapidapi.com",
        'x-rapidapi-key': "db7d4cf8b9msh568bdb5906cba3bp18c5a7jsnc6d234e61cde"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.status_code)
    return response.json()


def add_similar_words(keywords):
    master_dict = {}
    k_targets = 3
    for kw in keywords:
        related_words = get_similar_words(kw)
        for key in related_words.keys:
            if key in master_dict:
                master_dict[key] += related_words[key]
            else:
                master_dict[key] = related_words[key]

    target_keywords = sorted(master_dict, key=master_dict.get)[0:k_targets]
    sep = " "
    target_query = sep.join(target_keywords).append("gift")
    return target_query


