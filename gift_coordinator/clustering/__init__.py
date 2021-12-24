import requests
from gift_coordinator.models import GiftPool, Contributor
from urllib.parse import quote


def get_similar_words(target):
    url = "https://twinword-word-associations-v1.p.rapidapi.com/associations/"
    querystring = {"entry": target}

    headers = {
        'x-rapidapi-host': "twinword-word-associations-v1.p.rapidapi.com",
        'x-rapidapi-key': "b3b4a1e5f6msh8f5a0a2c59457a4p1378cbjsnc00fe924215e"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.status_code)
    return response.json()["associations_scored"]


def query_from_kws(keywords):
    master_dict = {}
    k_targets = 3
    for kw in keywords:
        related_words = get_similar_words(kw)
        for key in related_words.keys():
            if key in master_dict:
                master_dict[key] += related_words[key]
            else:
                master_dict[key] = related_words[key]

    target_keywords = sorted(master_dict, key=master_dict.get)[0:k_targets]
    sep = " "
    target_keywords.append("gifts")
    target_query = quote(sep.join(target_keywords))  #encode URL string
    return target_query


def update_gift_product(pool_id):
    price_limit = GiftPool.objects.get(pk=pool_id).curr_val
    contributors = Contributor.objects.filter(gift_pool_id=pool_id)
    keywords = [c.keyword1 for c in contributors]
    keywords += [c.keyword2 for c in contributors]
    keywords += [c.keyword3 for c in contributors]
    query = query_from_kws(keywords)

    url = f"https://amazon-data-scraper15.p.rapidapi.com/search/{query}"

    querystring = {"api_key": "9eabdc7648052e4a9d19552920b60a7f"}

    headers = {
        'x-rapidapi-host': "amazon-data-scraper15.p.rapidapi.com",
        'x-rapidapi-key': "db7d4cf8b9msh568bdb5906cba3bp18c5a7jsnc6d234e61cde"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)
    print(response.json())
    return response.json()["results"][0]["url"]





