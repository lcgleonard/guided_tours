#!/usr/bin/env python
from application import make_app, db

app = make_app()


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
