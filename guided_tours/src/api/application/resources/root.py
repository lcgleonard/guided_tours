from flask_restful import Resource


class Root(Resource):
    """Class representing root '/' resource"""

    def get(self):
        """Get generic hello world message."""
        return {"message": "Hello World"}
