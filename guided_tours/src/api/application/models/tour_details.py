from sqlalchemy.types import DECIMAL
from guided_tours_lib.distance import (
    get_distances_nsew_from_starting_point,
    check_coordinates_are_inside_given_km_radius,
)
from .tour_content import TourContentModel
from . import db


class TourDetailsModel(db.Model):
    """Models for user tour details."""

    __tablename__ = "tour_details"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=False)
    latitude = db.Column(DECIMAL, nullable=False)
    longitude = db.Column(DECIMAL, nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    user = db.relationship("UserModel", backref="tour_details")

    @classmethod
    def find_by_user_id(cls, user_id):
        """Find tour by its user_id."""

        results = cls.query.filter_by(user_id=user_id).all()
        return results

    @classmethod
    def find_tours_by_coordinates(cls, latitude, longitude):
        """Find tours within a given km radius of the coordinates."""
        distance_north, distance_south, distance_east, distance_west = get_distances_nsew_from_starting_point(
            latitude, longitude
        )
        tours = cls.query.filter(
            db.and_(
                cls.latitude <= distance_east,
                cls.latitude >= distance_west,
                cls.longitude <= distance_north,
                cls.longitude >= distance_south,
            )
        ).all()

        km_radius = 5  # TODO: move this value to config file

        return {
            "tours": [
                {
                    "title": tour.title,
                    "latitude": float(tour.latitude),
                    "longitude": float(tour.longitude),
                    "tour_id": tour.id,
                }
                for tour in tours
                if check_coordinates_are_inside_given_km_radius(
                    latitude, longitude, tour.latitude, tour.longitude, km_radius
                )
            ]
        }

    @classmethod
    def find_object_by_id(cls, tour_id):
        """Find tour object by its id."""

        return cls.query.filter_by(id=tour_id).first()

    @staticmethod
    def tour_to_dict(tour):
        return {
            "tour_id": tour.id,
            "title": tour.title,
            "description": tour.description,
            "latitude": float(tour.latitude),
            "longitude": float(tour.longitude),
        }

    @classmethod
    def find_dict_by_id(cls, tour_id):
        """Find tour dict by its id."""

        tour = cls.find_object_by_id(tour_id)
        tour_content = TourContentModel.query.filter_by(tour_id=tour_id).all()

        tour_dict = cls.tour_to_dict(tour)
        tour_dict["content"] = [
            {
                "key": content.key,
                "name": content.name,
                "content_type": content.content_type,
                "extension": content.extension,
            }
            for content in tour_content
        ]

        return tour_dict

    @classmethod
    def remove_by_id(cls, tour_id):
        cls.query.filter_by(id=tour_id).delete()
        db.session.commit()
