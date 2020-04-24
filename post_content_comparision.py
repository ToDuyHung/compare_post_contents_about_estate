import requests
import json
import hashlib

url = "http://127.0.0.1:3005/api/v1/real-estate-extraction"


def get_from_api(post_content):
    request = requests.Session()
    data_list = [post_content]
    # print("*** \ndata_list:{}\n ***".format(data_list))
    headers = {}

    response = request.post(
        url=url,
        headers=headers,
        json=data_list
    )

    data_attrs = {
        "attr_addr_street": "",
        "attr_addr_district": "",
        "attr_addr_ward": "",
        "attr_addr_city": "",
        "attr_surrounding_name": "",
        "attr_surrounding_characteristics": "",
    }

    try:
        json_response = response.json()
        # print("\n\n\n === json_response:{} === \n\n\n".format(json_response))
        for content, i in zip(
                json_response[0]["tags"],
                range(len(
                    json_response[0]["tags"]
                ))
        ):
            if content["type"] == "addr_street":
                data_attrs["attr_addr_street"] += content["content"] + ", "

            elif content['type'] == "addr_ward":
                data_attrs["attr_addr_ward"] += content["content"] + ", "

            elif content['type'] == "addr_district":
                data_attrs["attr_addr_district"] += content["content"] + ", "

            elif content['type'] == "addr_city":
                data_attrs["attr_addr_city"] += content["content"] + ", "

            elif content['type'] == "surrounding":
                data_attrs["attr_surrounding_name"] += content["content"] + ", "

            elif content["type"] == "surrounding_characteristics":
                data_attrs['attr_surrounding_characteristics'] += content["content"] + ", "

    except:
        pass
    return data_attrs


s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'


def remove_accents(input_str):
    s = ''
    for c in input_str:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    return s


def requestToString(data):
    stringRequest = ""
    for feature in data:
        new_feature = remove_accents(data[feature]).lower()
        bagOfWord = set(new_feature.split(', '))
        bagOfWord.discard('')

        new_bagOfWord = sorted(bagOfWord)
        # print(new_bagOfWord)

        for word in new_bagOfWord:
            stringRequest += word + " "

    return stringRequest


def hashMap(string):
    string = string.replace(" ", "")
    return hashlib.md5(string.encode('utf-8')).hexdigest()


with open('data.json', 'rb') as json_data:
    data_set = json.loads(json_data.read())
    print(len(data_set), "data loaded successfully")

    requestDict = {}
    for data in data_set:
        content = get_from_api(data["content"])
        # print(content)
        request = requestToString(content)
        key = hashMap(request)

        if not requestDict.get(key):  ## O(1)
            requestDict[key] = data['id']
        else:
            print("Two posts:", data['id'], "and", requestDict.get(key), "are identical.")

    print(requestDict)

