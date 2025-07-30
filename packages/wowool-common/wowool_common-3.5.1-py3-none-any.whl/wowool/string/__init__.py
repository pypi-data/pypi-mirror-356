import re
from wowool.document.analysis.document import AnalysisDocument
from typing import cast

_URI_WORDS = re.compile(r"\w+")


def normalize(name: str):
    try:
        import unidecode

        """Remove accented characters"""
        return unidecode.unidecode(name)
    except ModuleNotFoundError:
        return name


def to_text(annotations: list) -> str:
    """Convert a list of annotations into a string taking care of offset.
    But will remove duplicate spaces or convert whitespace into spaces."""
    prev_end_offset = None
    text = ""
    for a in annotations:
        if a.is_token:
            if prev_end_offset:
                if prev_end_offset != a.begin_offset:
                    text += " "

            text += a.literal
            prev_end_offset = a.end_offset
        elif a.is_sentence:
            if len(text) > 0:
                text += " "
            text += to_text(a.annotations)
    return text


def _camelize(name, separator=""):
    """
    Capitalize the first letter of every part of a multiword.
    remove spaces and replace with the separator
    """
    parts = _URI_WORDS.findall(name)
    for idx in range(len(parts)):
        parts[idx] = parts[idx].capitalize()
    return separator.join(parts).strip()


def camelize(name: str, separator: str = ""):
    """
    Camelize but first remove accents if any.
    """
    return _camelize(normalize(name), separator)


def initial_caps(name):
    """
    Capitalize the first letter of every part of a multiword.
    """
    return camelize(name, separator=" ")


def to_uri(name: str, separator="") -> str:
    """
    same as camelize but also remove spaces.
    """
    return camelize(name, separator)


GUESSER_PROPERTIES = {"cleanup", "guess", "typo"}


def canonicalize(obj, lemmas: bool = False, dates=True, spelling=True) -> str:
    """
    replace the literal or the lemmas by there canonical.

    :param obj: the annotation to be converted.
    :type obj: Annotation
    :param stem: replace using the stem or the literal.
    :type stem: bool

    :rtype: str
    """
    from io import StringIO
    from wowool.annotation import Sentence, Entity, Token

    if isinstance(obj, Sentence):
        annotations_range = obj.annotations
    elif isinstance(obj, Entity):
        concept = obj
        annotations_range = concept.annotations
    else:
        raise RuntimeError("obj type can not be wowool.utility.canonicalize")

    with StringIO() as output:
        skip_until_offset = 0
        annotation_count = len(annotations_range)
        prev_token = None
        for annotation_idx in range(annotation_count):
            annotation = annotations_range[annotation_idx]
            if annotation.begin_offset < skip_until_offset:
                prev_token = annotation
                continue
            else:
                skip_until_offset = 0

            if annotation.is_token:
                token = cast(Token, annotation)
                # print(f"T:[{annotation.begin_offset},{annotation.end_offset}]:{annotation.literal} prev:{prev_token}")
                if prev_token:
                    # print(f"  -- pe:{prev_token.end_offset} != ab:{annotation.begin_offset}")
                    if prev_token.end_offset != annotation.begin_offset:
                        output.write(" ")
                if lemmas:
                    output.write(token.lemma)
                elif spelling and bool(GUESSER_PROPERTIES.intersection(token.properties)):
                    output.write(token.lemma)
                else:
                    output.write(token.literal)

                prev_token = token

            elif annotation.is_concept:
                concept = cast(Entity, annotation)
                if "canonical" in concept.attributes:
                    if prev_token:
                        if prev_token.end_offset != concept.begin_offset:
                            output.write(" ")
                    output.write((concept.attributes["canonical"][0]))
                    skip_until_offset = concept.end_offset
                elif dates and concept.uri == "Date" and "abs_date" in concept.attributes:
                    if prev_token:
                        if prev_token.end_offset != concept.begin_offset:
                            output.write(" ")
                    output.write((concept.attributes["abs_date"][0]))
                    skip_until_offset = concept.end_offset

        return output.getvalue()


def search_and_replace(document: AnalysisDocument, expression: str, replacestring: str) -> str:
    from io import StringIO
    from wowool.annotation import Entity

    with StringIO() as strm:
        assert isinstance(document.text, str), "document.text should be a string"
        dtext = document.text
        offset_ = 0
        for concept in Entity.iter(document, lambda c: c.uri == expression):
            strm.write(dtext[offset_ : concept.begin_offset])
            strm.write(replacestring)
            offset_ = concept.end_offset

        strm.write(dtext[offset_:])
        return strm.getvalue()
