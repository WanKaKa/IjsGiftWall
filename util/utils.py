import os
import shutil

from PyQt5.QtWidgets import QCheckBox, QRadioButton

import release
from database import json_ex
from app.edit_gift.core import urls
from util import path_ex, icon


def delete_dir(dir_path):
    del_list = os.listdir(dir_path)
    for f in del_list:
        file_path = os.path.join(dir_path, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


def get_outputs_dir_list():
    dir_list = [urls.LANGUAGE_LIST[0]]
    file_list = os.listdir(path_ex.get_outputs())
    for file_name in file_list:
        if os.path.isdir(path_ex.get_outputs() + file_name):
            dir_list.append(file_name)
    return dir_list


def compare_entity(entity1, entity2):
    title1 = entity1.title if entity1.title else ""
    package_name1 = entity1.package_name if entity1.package_name else ""
    title2 = entity2.title if entity2.title else ""
    package_name2 = entity2.package_name if entity2.package_name else ""
    return title1 == title2 and package_name1 == package_name2


def is_entity_added(entity_, entity_list):
    title1 = entity_.title if entity_.title else ""
    package_name1 = entity_.package_name if entity_.package_name else ""
    for value in entity_list:
        title2 = value.title if value.title else ""
        package_name2 = value.package_name if value.package_name else ""
        if title1 == title2 and package_name1 == package_name2:
            return True
    return False


def copy_res():
    res_list = os.listdir(path_ex.get_res())
    icon_version = json_ex.get_icon_version()
    for item in os.listdir(icon.resource_path("./ico")):
        if item not in res_list or icon_version != release.version:
            shutil.copyfile(icon.resource_path(os.path.join("ico", item)), os.path.join(path_ex.get_res(), item))
    if icon_version != release.version:
        json_ex.put_icon_version(release.version)


CHECK_BOX_STYLE = """
QCheckBox{
    background-color: rgb(255, 255, 255);
    font: 12pt \"微软雅黑\";
}
QCheckBox::indicator {
    width:25px;
    height:25px;
}
QCheckBox::indicator:unchecked  {
    image: url(C:/IJoySoft/Kevin/IjsGiftWall/res/check_box_unchecked.png);
}
QCheckBox::indicator:unchecked:hover {
    image: url(C:/IJoySoft/Kevin/IjsGiftWall/res/check_box_unchecked_hover.png);
}
QCheckBox::indicator:checked {
    image: url(C:/IJoySoft/Kevin/IjsGiftWall/res/check_box_checked.png);
}
"""


def set_check_box_style(check_box):
    if isinstance(check_box, QCheckBox):
        check_box.setStyleSheet(CHECK_BOX_STYLE)


RADIO_BUTTON_STYLE_RED = """
QRadioButton{
    background-color: rgb(255, 255, 255);
    font: 10pt \"微软雅黑\";
    color: rgb(255, 0, 0);
}
QRadioButton::indicator {
    width:25px;
    height:25px;
}
QRadioButton::indicator:unchecked  {
    image: url(C:/IJoySoft/Kevin/IjsGiftWall/res/radio_button_normal_unchecked.png);
}
QRadioButton::indicator:unchecked:hover {
    image: url(C:/IJoySoft/Kevin/IjsGiftWall/res/radio_button_normal_unchecked_hover.png);
}
QRadioButton::indicator:checked {
    image: url(C:/IJoySoft/Kevin/IjsGiftWall/res/radio_button_normal_checked.png);
}
"""

RADIO_BUTTON_STYLE_BLACK = """
QRadioButton{
    background-color: rgb(255, 255, 255);
    font: 10pt \"微软雅黑\";
    color: rgb(0, 0, 0);
}
QRadioButton::indicator {
    width:25px;
    height:25px;
}
QRadioButton::indicator:unchecked  {
    image: url(C:/IJoySoft/Kevin/IjsGiftWall/res/radio_button_normal_unchecked.png);
}
QRadioButton::indicator:unchecked:hover {
    image: url(C:/IJoySoft/Kevin/IjsGiftWall/res/radio_button_normal_unchecked_hover.png);
}
QRadioButton::indicator:checked {
    image: url(C:/IJoySoft/Kevin/IjsGiftWall/res/radio_button_normal_checked.png);
}
"""


def set_radio_button_style(check_box, error):
    if isinstance(check_box, QRadioButton):
        if error:
            check_box.setStyleSheet(RADIO_BUTTON_STYLE_RED)
        else:
            check_box.setStyleSheet(RADIO_BUTTON_STYLE_BLACK)
