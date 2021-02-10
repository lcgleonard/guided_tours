from guided_tours_lib.distance import get_distances_nsew_from_starting_point
from ..models.tour_content import TourContentModel
from ..models.tour_details import TourDetailsModel
from ..models import db
from ._repository import _Repository


class ToursRepository(_Repository):
    @classmethod
    def add(cls, user_id, data):
        """Add new tour details to the repo."""

        new_tour_details = TourDetailsModel(
            title=data["title"],
            description=data["description"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            user_id=user_id,
        )

        return cls._add(new_tour_details)

    @classmethod
    def upsert(cls, tour_id, data):
        """Upsert tour content to the repo."""

        tour_content_data = []

        for _data in data:
            new_tour_content = TourContentModel(
                key=_data["key"],
                name=_data["name"],
                content_type=_data["content_type"],
                extension=_data["extension"],
                tour_id=tour_id,
            )
            tour_content_data.append(new_tour_content)

        db.session.bulk_save_objects(tour_content_data)
        db.session.commit()

    @classmethod
    def update(cls, tour_id, data):
        tour = TourDetailsModel.find_object_by_id(tour_id)

        tour.title = data["title"]
        tour.description = data["description"]
        tour.latitude = data["latitude"]
        tour.longitude = data["longitude"]

        return cls._add(tour)

    @staticmethod
    def _build_tours_datastructure(tours):
        return {
            "tours": [
                {
                    "title": tour.title,
                    "latitude": str(tour.latitude),
                    "longitude": str(tour.longitude),
                    "tour_id": tour.id,
                }
                for tour in tours
            ]
        }

    @classmethod
    def get_many(cls, data):
        """Get tours based on input data"""

        if "user_id" in data:
            return cls._handle_get_by_user_id(data["user_id"])
        elif "latitude" in data and "longitude" in data:
            return cls._handle_get_by_coordinates(data["latitude"], data["longitude"])
        else:
            # I'm failing silently here, raising an exception may be a better
            # approach
            return []

    @classmethod
    def _handle_get_by_user_id(cls, user_id):
        """Search for tours based on the user id provided"""
        tours = TourDetailsModel.find_by_user_id(user_id)
        return cls._build_tours_datastructure(tours)

    @classmethod
    def _handle_get_by_coordinates(cls, latitude, longitude):
        """Search for nearby tours based on the latitude and longitude provided"""

        return TourDetailsModel.find_tours_by_coordinates(latitude, longitude)

    @classmethod
    def get_one(cls, tour_id):
        """Get a tour by it's id"""
        tour = TourDetailsModel.find_dict_by_id(tour_id)
        return tour

    @classmethod
    def remove(cls, tour_id):
        tour = TourDetailsModel.find_dict_by_id(tour_id)
        TourDetailsModel.remove_by_id(tour_id)
        return tour
