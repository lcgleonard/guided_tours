from ..models.tour_content import TourContentModel
from ..models import db
from ._repository import _Repository


class ContentRepository(_Repository):
    @classmethod
    def delete(cls, data):
        """Delete an image or audio content from the repo."""
        content_object = TourContentModel.find_content(data["tour_id"], data["key"])

        if content_object:
            content_dict = {
                "key": content_object.key,
                "name": content_object.name,
                "content_type": content_object.content_type,
                "extension": content_object.extension,
                "tour_id": content_object.tour_id,
            }
            cls._remove(content_object)
            return content_dict
        else:
            return {}
