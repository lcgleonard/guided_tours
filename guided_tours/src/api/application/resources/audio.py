from http import HTTPStatus

from flask_restful import Resource

from ..repositories import ContentRepository


class TourAudio(Resource):
    """Class representing the tour audio resource."""

    def delete(self, tour_id):
        """Delete the audio"""
        key = "audioContent"
        result = ContentRepository.delete({"tour_id": tour_id, "key": key})

        if not result:
            return {"message": "Not found"}, HTTPStatus.NOT_FOUND

        return result
