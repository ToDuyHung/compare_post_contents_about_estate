import requests
import json

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
            if content["type"] == "addr_street" and data_attrs["attr_addr_street"] == "":
                data_attrs["attr_addr_street"] = content["content"]

            elif content['type'] == "addr_ward" and data_attrs["attr_addr_ward"] == "":
                data_attrs["attr_addr_ward"] = content["content"]

            elif content['type'] == "addr_district" and data_attrs["attr_addr_district"] == "":
                data_attrs["attr_addr_district"] = content["content"]

            elif content['type'] == "addr_city" and data_attrs["attr_addr_city"] == "":
                data_attrs["attr_addr_city"] = content["content"]

            elif content['type'] == "surrounding":
                if data_attrs["attr_surrounding_name"] == "":
                    data_attrs["attr_surrounding_name"] = content["content"]
                else:
                    data_attrs["attr_surrounding_name"] = data_attrs["attr_surrounding_name"] + " " + content["content"]

            elif content["type"] == "surrounding_characteristics":
                if data_attrs["attr_surrounding_characteristics"] == "":
                    data_attrs["attr_surrounding_characteristics"] = content["content"]
                else:
                    data_attrs["attr_surrounding_characteristics"] = \
                        data_attrs['attr_surrounding_characteristics'] + " " + content["content"]
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


# Compare 2 features regardless of accents and higher letters
# if different return 1, otherwise return 0
def compare_features(feature1, feature2):
    new_feature1 = remove_accents(feature1).lower()
    new_feature2 = remove_accents(feature2).lower()
    bagOfWord1 = set(new_feature1.split(' '))
    bagOfWord2 = set(new_feature2.split(' '))
    if bagOfWord1 != bagOfWord2:
        return 1
    return 0


# print(compare_features("Hoàng Hoa Thám", "hoàng hoa thám"))


with open('data.json', 'rb') as json_data:
    data_set = json.loads(json_data.read())
    print(len(data_set), "datas loaded succesfully")
    for data_i in data_set:
        for data_j in data_set:
            if data_j["id"] > data_i["id"]:
                data1 = get_from_api(data_i["content"])
                data2 = get_from_api(data_j["content"])
                check = 0
                for feature in data1:
                    check += compare_features(data1[feature], data2[feature])
                    if check == 1:
                        break
                if check == 0:
                    print("Two posts:", data_i["id"], "and", data_j["id"], "are identical.")
                else:
                    print("Two posts:", data_i["id"], "and", data_j["id"], "are different.")

#   Test case:
#   text1 = "Em cần nhượng phòng gấpĐịa chỉ: 242Hoàng Hoa Thám,p5, Q. Bình Thạnh. Phòng e ở được từ 2-3 người. Phòng có giá 2tr5, có nhà vệ sinh riêng, nước 50k/người, điện 3,5k/kwh. Sát chợ nên rất nhộn nhịp, ăn uống thoải mái, gần hồ về đêm rất yên tĩnh. Sdt 0944296412 "
#   text2 = "Vì đang kẹt tiền nên em có một căn nhà ở hoàng hoa thám ,p5, quận bình thạnh cần bán gấp. Phòng giá 5 triệu. Gần hồ và chợ nên rất yên tĩnh, nhộn nhịp . Liên hệ: 0944296412 "
#   data1 = get_from_api(text1)
#   data2 = get_from_api(text2)
#   print(data1)
#   print(data2)
#   check = 0
#   for feature in data1:
#       check += compare_features(data1[feature], data2[feature])
#       if check == 1:
#           break
#   if check == 0:
#       print("Two posts are identical.")
#   else:
#       print("Two posts are different.")
