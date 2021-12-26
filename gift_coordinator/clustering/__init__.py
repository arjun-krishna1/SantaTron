import requests
from gift_coordinator.models import GiftPool, Contributor
from urllib.parse import quote
from re import sub
from decimal import Decimal


def get_similar_words(target):
    url = "https://twinword-word-associations-v1.p.rapidapi.com/associations/"
    querystring = {"entry": target}

    headers = {
        'x-rapidapi-host': "twinword-word-associations-v1.p.rapidapi.com",
        'x-rapidapi-key': "b3b4a1e5f6msh8f5a0a2c59457a4p1378cbjsnc00fe924215e"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.status_code)
    if response.status_code == 200:
        return response.json()["associations_scored"]
    else:
        return -1


def query_from_kws(keywords):
    master_dict = {}
    k_targets = 3
    for kw in keywords:
        result = get_similar_words(kw)
        if result == -1:
            related_words = {}
        else:
            related_words = result
        for key in related_words.keys():
            if key in master_dict:
                master_dict[key] += related_words[key]
            else:
                master_dict[key] = related_words[key]
    print(master_dict)
    print(sorted(master_dict, key=master_dict.get))
    target_keywords = sorted(master_dict, key=master_dict.get)[-k_targets:]
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
    final_result = ''
    if response.status_code == 200:
        #print(type(response.json()["results"][0]["price"]))
        #print((response.json()["results"][0]["price"]))
        for index in range(20):
            #print(response.json()["results"][index]["price"])
            #print(type(response.json()["results"][index]["price"]))
            price = response.json()["results"][index]["price"]
            if price is not None and price <= price_limit:
                final_result = response.json()["results"][0]["url"]
                break
    return final_result





