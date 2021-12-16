import json
from dmtools import Metadata


def get_metadata():
    """Return a Metadata object from label and description."""
    label = json.load(open("label.json"))
    description = open("description.md").read()
    description = f'({label["date"]}) [{label["medium"]}]\n\n{description}\n'

    return Metadata(title=label["title"],
                    author=label["author"],
                    description=description)
