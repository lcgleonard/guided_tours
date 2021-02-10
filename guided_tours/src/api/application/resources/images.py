from http import HTTPStatus

from flask_restful import Resource

from ..repositories import ContentRepository


class TourImages(Resource):
    """Class representing the tour images resource."""

    def delete(self, tour_id, image_number):
        """Delete the image"""
        key = f"image{image_number}"
        result = ContentRepository.delete({"tour_id": tour_id, "key": key})

        if not result:
            return {"message": "Not found"}, HTTPStatus.NOT_FOUND

        return result
