from flask_restful import Resource


class Ping(Resource):
    """Resource represent ping functionality for this application.

    If ping does not return the expected 'I am alive message' with a
    HTTP 200, then we know something is wrong with application and we
    can try and restart it.
    """

    def get(self):
        """Ping endpoint"""
        return {"message": "I am alive"}
