class GiftEntity:
    def __init__(self, *args, **kwargs):
        self.title = kwargs["title"] if "title" in kwargs else None
        self.detailed = kwargs["detailed"] if "detailed" in kwargs else None
        self.icon_image_path = kwargs["icon_image_path"] if "icon_image_path" in kwargs else None
        self.package_name = kwargs["package_name"] if "package_name" in kwargs else None
        self.poster_path = kwargs["poster_path"] if "poster_path" in kwargs else None
        self.app_type = kwargs["app_type"] if "app_type" in kwargs else None
        self.market_url = kwargs["market_url"] if "market_url" in kwargs else None

    def __str__(self):
        return "GiftEntity = {\n" \
               "    title = %s;\n" \
               "    detailed = %s;\n" \
               "    icon_image_path = %s;\n" \
               "    package_name = %s;\n" \
               "    poster_path = %s;\n" \
               "    app_type = %s;\n" \
               "    market_url = %s;\n" \
               "} " % (self.title, self.detailed, self.icon_image_path,
                       self.package_name, self.poster_path, self.app_type, self.market_url)


class OverallGiftEntity(GiftEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.project_name = kwargs["project_name"] if "project_name" in kwargs else None

    def __str__(self):
        return "OverallGiftEntity = {\n" \
               "    title = %s;\n" \
               "    detailed = %s;\n" \
               "    icon_image_path = %s;\n" \
               "    package_name = %s;\n" \
               "    poster_path = %s;\n" \
               "    app_type = %s;\n" \
               "    market_url = %s;\n" \
               "    project_name = %s;\n" \
               "} " % (self.title, self.detailed, self.icon_image_path, self.package_name,
                       self.poster_path, self.app_type, self.market_url, self.project_name)
