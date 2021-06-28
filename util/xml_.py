import os
import xml.dom.minidom

from gift import entity, urls
from util import path_

TAG_GIFT_LIST = "giftList"

# 配置参数
TAG_CONFIG = "config"
ATTRIBUTE_TARGET = "target"
ATTRIBUTE_START_INDEX = "index"
ATTRIBUTE_COUNT = "count"
ATTRIBUTE_LIMIT = "limit"
# 配置参数target的值
TARGET_WALL = "wall"
TARGET_RATE = "rate"
TARGET_LIST = "list"
TARGET_DIALOG = "dialog"
TARGET_CAROUSEL = "carousel"
TARGET_SIDEBAR = "sidebar"
TARGET_INTERSTITIAL = "interstitial"

# gift参数
TAG_GIFT = "gift"
ATTRIBUTE_ID = "id"
TAG_TITLE = "title"
TAG_DETAILED = "detailed"
TAG_ICON_PATH = "icon_imagePath"
TAG_POSTER_PATH = "posterPath"
TAG_PACKAGE_NAME = "packageName"
TAG_MARKET_URL = "marketUrl"
TAG_APP_TYPE = "apptype"
TAG_PROJECT_NAME = "projectName"


def analysis_overall_gift_xml(path):
    if not os.path.exists(path):
        return None
    dom = xml.dom.minidom.parse(path)
    root = dom.documentElement
    overall_gift_entity = entity.OverallGiftEntity()

    overall_gift_item_list = root.getElementsByTagName(TAG_GIFT)
    for item in overall_gift_item_list:
        overall_gift_item = entity.OverallGiftItem()
        overall_gift_item.id = item.getAttribute(ATTRIBUTE_ID)
        # 元素
        overall_gift_item.title = analysis_xml_item(item, TAG_TITLE)
        overall_gift_item.detailed = analysis_xml_item(item, TAG_DETAILED)
        overall_gift_item.icon_image_path = analysis_xml_item(item, TAG_ICON_PATH)
        overall_gift_item.package_name = analysis_xml_item(item, TAG_PACKAGE_NAME)
        overall_gift_item.market_url = analysis_xml_item(item, TAG_MARKET_URL)
        overall_gift_item.poster_path = analysis_xml_item(item, TAG_POSTER_PATH)
        overall_gift_item.app_type = analysis_xml_item(item, TAG_APP_TYPE)
        overall_gift_item.project_name = analysis_xml_item(item, TAG_PROJECT_NAME)
        overall_gift_entity.item_list.append(overall_gift_item)
    return overall_gift_entity


def analysis_gift_xml(path):
    if not os.path.exists(path):
        return None
    try:
        gift_entity = entity.GiftEntity()
        dom = xml.dom.minidom.parse(path)
        root = dom.documentElement
        # 解析gift配置参数
        gift_config_list = root.getElementsByTagName(TAG_CONFIG)
        for config in gift_config_list:
            gift_config = entity.GiftConfig()
            gift_config.target = config.getAttribute(ATTRIBUTE_TARGET)
            gift_config.index = config.getAttribute(ATTRIBUTE_START_INDEX)
            gift_config.count = config.getAttribute(ATTRIBUTE_COUNT)
            gift_config.limit = config.getAttribute(ATTRIBUTE_LIMIT)
            gift_entity.config_list[gift_config.target] = gift_config
        # 解析gift数据
        gift_item_list = root.getElementsByTagName(TAG_GIFT)
        for item in gift_item_list:
            gift_item = entity.GiftItem()
            gift_item.id = item.getAttribute(ATTRIBUTE_ID)
            # 元素
            gift_item.title = analysis_xml_item(item, TAG_TITLE)
            gift_item.detailed = analysis_xml_item(item, TAG_DETAILED)
            gift_item.icon_image_path = analysis_xml_item(item, TAG_ICON_PATH)
            gift_item.package_name = analysis_xml_item(item, TAG_PACKAGE_NAME)
            gift_item.market_url = analysis_xml_item(item, TAG_MARKET_URL)
            gift_item.poster_path = analysis_xml_item(item, TAG_POSTER_PATH)
            gift_item.app_type = analysis_xml_item(item, TAG_APP_TYPE)
            gift_entity.item_list.append(gift_item)
        return gift_entity
    except Exception as e:
        print(e)
    return None


def analysis_xml_item(content, name):
    items = content.getElementsByTagName(name)
    if not items or len(items) == 0:
        return None
    # print(items[0].nodeName, ":", items[0].childNodes[0].data)
    return items[0].childNodes[0].data


def create_gift_wall_files(file_name, language_list, config_list, entity_list):
    for language in language_list:
        if language:
            dir_path = path_.get_outputs() + (language + "\\" if urls.LANGUAGE_LIST[0] != language else "")
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            file = open(dir_path + file_name, mode='w', encoding='utf-8')
            file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
            file.write("\n")
            file.write("<" + TAG_GIFT_LIST + ">")
            file.write("\n")
            file.write("\n")

            write_config_item(file, config_list[TARGET_RATE])
            write_config_item(file, config_list[TARGET_INTERSTITIAL])
            write_config_item(file, config_list[TARGET_LIST])
            write_config_item(file, config_list[TARGET_DIALOG])
            write_config_item(file, config_list[TARGET_CAROUSEL])
            write_config_item(file, config_list[TARGET_SIDEBAR])
            write_config_item(file, config_list[TARGET_WALL])
            file.write("\n")

            for entity_value in entity_list:
                write_entity_item(file, entity_value)

            file.write("</" + TAG_GIFT_LIST + ">")
            file.write("\n")
            file.close()


def write_config_item(file, config):
    if config.target:
        value = "    <" + TAG_CONFIG
        value += " " + ATTRIBUTE_TARGET + "=\"" + config.target + "\""
        if config.index:
            value += " " + ATTRIBUTE_START_INDEX + "=\"" + config.index + "\""
        if config.count:
            value += " " + ATTRIBUTE_COUNT + "=\"" + config.count + "\""
        if config.limit:
            value += " " + ATTRIBUTE_LIMIT + "=\"" + config.limit + "\""
        value = value + "/>"
        file.write(value)
        file.write("\n")


def write_entity_item(file, entity_):
    value = "    <" + TAG_GIFT + " " + ATTRIBUTE_ID + "=\"" + entity_.id + "\">"
    value += "\n"
    if entity_.title:
        title = entity_.title
        if isinstance(title, str):
            title = title.replace("&", "&amp;")
        value += "        <" + TAG_TITLE + ">" + title + "</" + TAG_TITLE + ">"
        value += "\n"
    if entity_.detailed:
        value += "        <" + TAG_DETAILED + ">" + entity_.detailed + "</" + TAG_DETAILED + ">"
        value += "\n"
    if entity_.icon_image_path:
        value += "        <" + TAG_ICON_PATH + ">" + entity_.icon_image_path + "</" + TAG_ICON_PATH + ">"
        value += "\n"
    if entity_.package_name:
        value += "        <" + TAG_PACKAGE_NAME + ">" + entity_.package_name + "</" + TAG_PACKAGE_NAME + ">"
        value += "\n"
    if entity_.poster_path:
        value += "        <" + TAG_POSTER_PATH + ">" + entity_.poster_path + "</" + TAG_POSTER_PATH + ">"
        value += "\n"
    if entity_.market_url:
        value += "        <" + TAG_MARKET_URL + ">" + entity_.market_url + "</" + TAG_MARKET_URL + ">"
        value += "\n"
    if entity_.app_type:
        value += "        <" + TAG_APP_TYPE + ">" + entity_.app_type + "</" + TAG_APP_TYPE + ">"
        value += "\n"
    value += "    </" + TAG_GIFT + ">"
    value += "\n"
    file.write(value)
    file.write("\n")
