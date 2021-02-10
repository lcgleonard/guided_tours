import re


def is_email_address(maybe_email):
    """Test if input is a vliad email address"""
    # regular expression is taken from:
    # http://emailregex.com/#crayon-5c5b38b70414e961047986
    email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    return email_regex.match(maybe_email)
