import re


class AudioImageFilePathError(Exception):
    pass


def get_file_path(base_content_path, key):
    """Get the location for the file"""
    if key.startswith("audio"):
        return f"{base_content_path}audio/"
    elif key.startswith("image"):
        return f"{base_content_path}images/"
    else:
        raise AudioImageFilePathError(f"Cannot determine file path based on: {key}")


def get_file_name(tour_id, content_type, filename, extension):
    parsed_content_type = "-".join(content_type.split("/"))
    location_no_whitespace = re.sub(
        "\s+", "", f"{tour_id}{parsed_content_type}{filename}".strip()
    )  # remove whitespace
    location_no_special_charaters = "".join(
        c for c in location_no_whitespace if c.isalnum()
    )  # remove special characters
    return f"{location_no_special_charaters}{extension}"
