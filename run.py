import giftdata

if __name__ == '__main__':
    var = giftdata.gift_entity_list[giftdata.urls.XML_NAME_LIST[0]]
    print(var.item_list[0].title)
