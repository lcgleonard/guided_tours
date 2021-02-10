from http import HTTPStatus

from flask_restful import Resource

from guided_tours_lib.validation.tours import ToursValidator
from guided_tours_lib.validation.flask import validate

from ..repositories import ToursRepository, UsersRepository


class Tours(Resource):
    """Class representing the tour details resource."""

    _validator = ToursValidator

    @staticmethod
    def _get_by_tour_id(tour_id):
        result = ToursRepository.get_one(tour_id)

        return result

    @staticmethod
    def _get_by_query_data(data):
        if "username" in data:
            user = UsersRepository.get(data)

            if user:
                data["user_id"] = user.id
            else:
                return {"message": "Not found"}, HTTPStatus.NOT_FOUND

        results = ToursRepository.get_many(data)

        if not results:
            return {"message": "No Tours Found"}, HTTPStatus.NOT_FOUND
        else:
            return results

    @validate
    def get(self, data, *args, **kwargs):
        """Get the search results"""

        if "tour_id" in kwargs:
            return self._get_by_tour_id(kwargs["tour_id"])
        else:
            return self._get_by_query_data(data)

    @validate
    def post(self, data, *args, **kwargs):
        """Post new tour data and store in repo."""

        user = UsersRepository.get({"username": data["username"]})

        if not user:
            return {"message": "Not Found"}, HTTPStatus.NOT_FOUND

        tour_id = ToursRepository.add(user.id, data)

        return {"message": "Tour created", "tour_id": tour_id}, HTTPStatus.CREATED

    @validate
    def put(self, data, tour_id):
        """Update tour content and store in repo."""

        ToursRepository.update(tour_id, data)

        return {"message": "Tour updated"}

    @validate
    def patch(self, data, tour_id):
        """Update tour content and store in repo."""

        ToursRepository.upsert(tour_id, data)

        return {"message": "Tour updated"}

    def delete(self, tour_id):
        tour = ToursRepository.remove(tour_id)

        return {"message": "Tour deleted", "tour": tour}
