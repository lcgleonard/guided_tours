from ..models import db


class _Repository(object):
    @staticmethod
    def _add(entity):
        """Add an entity to the repo"""
        db.session.add(entity)
        db.session.commit()
        return entity.id

    @staticmethod
    def _remove(entity):
        """Add an remove to the repo"""
        db.session.delete(entity)
        db.session.commit()
