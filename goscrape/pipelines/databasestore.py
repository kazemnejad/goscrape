from sqlalchemy import or_

from goscrape.database.connection import db_session
from goscrape.database.models import Category, Application, Developer


class DatabaseStorePipeline(object):
    def process_item(self, item, spider):
        tp = item.get("status")
        if tp == "cat":
            self.save_category(item.get("item"))
        elif tp == "app":
            self.save_app(item.get("item"))

        return item

    def save_category(self, item):
        category = Category(
            item.get("slug"),
            item.get("name")
        )

        db_session.add(category)
        db_session.commit()

        return category

    def save_developer(self, slug, name):
        developer = Developer(
            slug,
            name
        )

        db_session.add(developer)
        db_session.commit()

        return developer

    def save_app(self, item):
        cat_slug = item.get("cat_slug")
        cat_name = item.get("cat_name")

        category = Category.query.filter_by(slug=cat_slug).first()
        if category is None:
            category = Category(
                cat_slug,
                cat_name
            )

        developer = Developer.query.filter(
            or_(Developer.slug == item.get("dev_slug"), Developer.name == item.get("dev_name"))
        ).first()
        if not developer:
            developer = self.save_developer(item.get("dev_slug"), item.get("dev_name"))

        app = Application(item.get("component"))
        db_session.add(app)

        app.name = item.get("name")
        app.size = item.get("size")
        app.price = item.get("price")
        app.active_installs = item.get("act_install")
        app.version = item.get("version")
        app.rate = item.get("rate")
        app.icon = item.get("icon")

        app.developer = developer
        app.categories.append(category)

        db_session.commit()