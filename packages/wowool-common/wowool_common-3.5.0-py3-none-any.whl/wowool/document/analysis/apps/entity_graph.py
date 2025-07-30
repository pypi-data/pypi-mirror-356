from dataclasses import dataclass


@dataclass
class Link:
    from_: dict
    to: dict
    relation: dict


def convert_entity_graph(jo: list):
    """Convert a list of entity graph links from JSON format to a list of Link objects."""
    return [Link(from_=link["from"], to=link["to"], relation=link["relation"]) for link in jo]
