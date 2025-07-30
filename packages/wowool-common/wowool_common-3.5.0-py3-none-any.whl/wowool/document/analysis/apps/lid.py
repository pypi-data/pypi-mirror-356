from dataclasses import dataclass, field


@dataclass
class LanguageIdentifierSectionResult:
    """
    Language Identification results.
    """

    language: str
    begin_offset: int
    end_offset: int
    text: str | None = None


@dataclass
class LanguageIdentifierResults:
    """
    Language Identification results.
    """

    language: str = ""
    sections: list[LanguageIdentifierSectionResult] = field(default_factory=list)


def convert_lid(jo_data: dict) -> LanguageIdentifierResults:
    """
    Convert JSON object to LanguageIdentifierResults.

    :param jo_data: JSON object containing language identification results.
    :return: LanguageIdentifierResults instance with identified language.
    """
    retval = LanguageIdentifierResults()
    if "sections" in jo_data:
        sections = []
        languages = set()
        for section in jo_data["sections"]:
            section_result = LanguageIdentifierSectionResult(
                language=section["language"],
                begin_offset=section["begin_offset"],
                end_offset=section["end_offset"],
                text=section.get("text"),
            )
            languages.add(section_result.language)
            sections.append(section_result)
        retval.sections = sections
        if len(languages) == 1:
            retval.language = languages.pop()
        else:
            retval.language = "multiple"
    elif "language" in jo_data:
        retval.language = jo_data["language"]
    else:
        raise ValueError("Invalid JSON data for language identification.")
    return retval
