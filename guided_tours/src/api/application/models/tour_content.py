from . import db


class TourContentModel(db.Model):
    """Models for user tour cotent."""

    __tablename__ = "tour_content"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    content_type = db.Column(db.String(25), nullable=False)
    extension = db.Column(db.String(10), nullable=False)
    tour_id = db.Column(
        db.Integer, db.ForeignKey("tour_details.id", ondelete="CASCADE"), nullable=False
    )

    tour = db.relationship("TourDetailsModel", backref="tour_content")

    @classmethod
    def find_content(cls, tour_id, key):
        # using SELECT FOR UPDATE via the with_for_update method call
        # to lock the row so it can then be updated or deleted
        # https://docs.sqlalchemy.org/en/13/orm/query.html?highlight=update#sqlalchemy.orm.query.Query.with_for_update
        return cls.query.filter_by(key=key, tour_id=tour_id).with_for_update().first()
