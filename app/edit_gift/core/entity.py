class GiftConfig:
    def __init__(self, **kwargs):
        self.target = kwargs["target"] if "target" in kwargs else None
        self.index = kwargs["index"] if "index" in kwargs else "0"
        self.count = kwargs["count"] if "count" in kwargs else "5"
        self.limit = kwargs["limit"] if "limit" in kwargs else "10"

    def __str__(self):
        return "GiftConfig = {\n" \
               "    target = %s;\n" \
               "    index = %s;\n" \
               "    count = %s;\n" \
               "    limit = %s;\n" \
               "} " % (self.target, self.index, self.count, self.limit)


class GiftItem:
    def __init__(self, **kwargs):
        self.id = kwargs["id"] if "id" in kwargs else None
        self.title = kwargs["title"] if "title" in kwargs else None
        self.detailed = kwargs["detailed"] if "detailed" in kwargs else None
        self.icon_image_path = kwargs["icon_image_path"] if "icon_image_path" in kwargs else None
        self.package_name = kwargs["package_name"] if "package_name" in kwargs else None
        self.poster_path = kwargs["poster_path"] if "poster_path" in kwargs else None
        self.app_type = kwargs["app_type"] if "app_type" in kwargs else None
        self.market_url = kwargs["market_url"] if "market_url" in kwargs else None

    def __str__(self):
        return "GiftEntity = {\n" \
               "    id = %s;\n" \
               "    title = %s;\n" \
               "    detailed = %s;\n" \
               "    icon_image_path = %s;\n" \
               "    package_name = %s;\n" \
               "    poster_path = %s;\n" \
               "    app_type = %s;\n" \
               "    market_url = %s;\n" \
               "} " % (self.id, self.title, self.detailed, self.icon_image_path,
                       self.package_name, self.poster_path, self.app_type, self.market_url)


class GiftEntity:
    def __init__(self, **kwargs):
        self.config_list = kwargs["config_list"] if "config_list" in kwargs else {}
        self.item_list = kwargs["item_list"] if "item_list" in kwargs else []


class OverallGiftItem(GiftItem):
    def __init__(self, **kwargs):
        super().__init__()
        self.project_name = kwargs["project_name"] if "project_name" in kwargs else None

    def __str__(self):
        return "OverallGiftEntity = {\n" \
               "    id = %s;\n" \
               "    title = %s;\n" \
               "    detailed = %s;\n" \
               "    icon_image_path = %s;\n" \
               "    package_name = %s;\n" \
               "    poster_path = %s;\n" \
               "    app_type = %s;\n" \
               "    market_url = %s;\n" \
               "    project_name = %s;\n" \
               "} " % (self.id, self.title, self.detailed, self.icon_image_path, self.package_name,
                       self.poster_path, self.app_type, self.market_url, self.project_name)


class OverallGiftEntity:
    def __init__(self, **kwargs):
        self.item_list = kwargs["item_list"] if "item_list" in kwargs else []
