from scrapy.exceptions import DropItem

from goscrape.database.models import Category, Application


class ValidationPipeline(object):
    def process_item(self, item, spider):
        if not type(item) is dict \
                or not item.get("status", None) or not item.get("item"):
            raise DropItem("Invalid item format in %s" % item)

        return item


class DuplicateCheckPipeline(object):
    def process_item(self, item, spider):
        tp = item.get("status")
        if tp == "cat":
            if self.is_category_duplicate(item.get("item")):
                raise DropItem("Duplicate Category: %s" % item.get("item").get("slug"))
        elif tp == "app":
            if self.is_app_duplicate(item.get("item")):
                raise DropItem("Duplicate app")

        return item

    def is_category_duplicate(self, item):
        slug = item.get("slug")
        category = Category.query.filter_by(slug=slug).first()

        return category is not None

    def is_app_duplicate(self, item):
        app = Application.query.filter_by(component_name=item.get("component")).first()

        return app is not None
