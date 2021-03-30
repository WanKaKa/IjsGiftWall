from giftdata import download, urls
from utils import gift_xml_utils, path_utils

gift_entity_list = {}

# 下载数据
download.load()
# 下载数据成功后解析数据
if download.get_update_time():
    # 总表数据
    overall_gift_entity = gift_xml_utils.analysis_overall_gift_xml(
        path_utils.get_download_path() + urls.OVERALL_XML_NAME)
    print("OverallGiftItem Count = %d" % len(overall_gift_entity.item_list))
    # 各项目数据
    gift_entity_list.clear()
    for path in urls.XML_NAME_LIST:
        gift_entity_list[path] = gift_xml_utils.analysis_gift_xml(path_utils.get_download_path() + path)
    print("GiftEntity Count = %d" % len(gift_entity_list))
