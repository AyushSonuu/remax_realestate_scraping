import requests
zip_codes = ["80237","55125","80111","20016","92604"]


def urls_to_send(zip_codes:list):

    zip_dict_lst = []
    for zip in zip_codes:
        api_url = f"https://www.remax.com/api-v2/listings/autocomplete/?autocompleteValue={zip}&categories%5B0%5D=states&categories%5B1%5D=places&categories%5B2%5D=zips"
        a = ((requests.get(api_url).json()))
        zip_dict_lst.append(a)
    print(zip_dict_lst[0])

    url_lst = []
    for dic in zip_dict_lst:
        state = dic["zips"][0]["state"].lower()
        city = dic["zips"][0]["city"].lower()
        city = city.replace(" ","-")
        end_url = city+"-"+state
        url = f"https://www.remax.com/real-estate-agents/{end_url}"
        url_lst.append(url)
        print(city)

    return url_lst
# zip_dict_lst = []
# for zip in zip_codes:
#         api_url = f"https://www.remax.com/api-v2/listings/autocomplete/?autocompleteValue={zip}&categories%5B0%5D=states&categories%5B1%5D=places&categories%5B2%5D=zips"
#         a = ((requests.get(api_url).json()))
#         zip_dict_lst.append(a)
urls_to_send(zip_codes)
