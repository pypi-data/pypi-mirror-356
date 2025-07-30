import re
import json
import urllib.request
import sanakirja.tag_parser as tag_parser
from enum import IntEnum
from urllib.parse import quote
from typing import Dict, List, Optional, Tuple, TypedDict, Union

# Custom type aliases for improved readability
StrDictList = List[Dict[str, Optional[str]]]
TranslationEntry = Dict[str, Optional[Union[str, List[str], StrDictList]]]

ExampleResult = Dict[str, List[str]]
DefinitionResult = List[Optional[Union[str, List[str]]]]
PronunciationResult = Dict[str, StrDictList]
TranslationResult = Dict[str, List[TranslationEntry]]

class SanakirjaResult(TypedDict):
    """Result dictionary with type annotated individual fields."""
    id: int
    source_language: Optional[str]
    target_language: Optional[str]
    word: str
    transliteration: Optional[str]
    additional_source_languages: List[str]
    relations: List[str]
    similar_words: List[str]
    alternative_spellings: StrDictList
    multiple_spellings: List[str]
    synonyms: StrDictList
    pronunciations: PronunciationResult
    abbreviations: StrDictList
    inflections: Dict[str, str]
    definitions: DefinitionResult
    examples: ExampleResult
    categories: List[str]
    translations: TranslationResult

class LangCodes(IntEnum):
    """Map ISO 3166-2 format country codes to integer values used by sanakirja.org."""
    bg = 1
    et = 2
    en = 3
    es = 4
    eo = 5
    it = 6
    el = 7
    la = 8
    lv = 9
    lt = 10
    no = 11
    pt = 12
    pl = 13
    fr = 14
    sv = 15
    de = 16
    fi = 17
    da = 18
    cs = 19
    tr = 20
    hu = 21
    ru = 22
    nl = 23
    jp = 24

class LanguageCodeError(ValueError):
    """Exception class for invalid language codes."""

    def __init__(self, lang: str) -> None:
        """
        Initialize the invalid language code exception.

        :param lang: The invalid language code.
        :type lang: str
        """
        super().__init__(f"Invalid language code: '{lang}'")

class Sanakirja:
    """Class for fetching information from sanakirja.org."""

    def __init__(self) -> None:
        """Initialize the Sanakirja object with the base URL."""

        self.__base_url = "https://www.sanakirja.org/search.php?q={}&l={}&l2={}"

    @staticmethod
    def _validate_lang_code(lang: Union[int, str, LangCodes]) -> Union[int, bool]:
        """
        Validate the given language code.

        :param lang: The language code to validate.
        :type lang: int | str | LangCodes
        :return: The validated language code in `int` format, or `False` if invalid.
        :rtype: int | bool
        """
        if lang == 0: return 0
        elif isinstance(lang, str): return LangCodes[lang.lower()] if hasattr(LangCodes, lang.lower()) else False
        elif isinstance(lang, int): return lang if lang in LangCodes._value2member_map_ else False
        return lang
    
    @staticmethod
    def _get_sk_var(html: str) -> Dict[str, Union[int, str, bool]]:
        """
        Resolve the SK object from the HTML of the webpage.

        :param html: The HTML of the webpage.
        :type html: str
        :return: The resolved SK object in `dict` format.
        :rtype: dict[str, int | str | bool]
        """
        body = tag_parser.find(html, "body")
        sk_var = tag_parser.find_text(body, "script")
        sk_var_dict = json.loads(sk_var.split("var SK=")[-1][:-1])

        return sk_var_dict
    
    @staticmethod
    def _get_multiple_spellings(html: str) -> List[str]:
        """
        Extract the multiple spellings from the HTML of the webpage.

        :param html: The HTML of the webpage.
        :type html: str
        :return: The multiple spellings as a list of strings.
        :rtype: list[str]
        """
        multiple_spellings_ul = tag_parser.find(html, "ul", {"class": "multiple_spellings"})
        multiple_spellings = tag_parser.find_all_text(multiple_spellings_ul, "a")

        return multiple_spellings
        
    @staticmethod
    def _get_alt_synonyms_and_pronunciations(html: str) -> Tuple[StrDictList, StrDictList, PronunciationResult]:
        """
        Extract the alternative spellings, synonyms and pronunciations from the HTML of the webpage.

        :param html: The HTML of the webpage.
        :type html: str
        :return: The alternative spellings and synonyms as :type:`StrDictList` type and pronunciations as :type:`PronunciationResult` type.
        :rtype: tuple[StrDictList, StrDictList, PronunciationResult]
        """
        lists_div = tag_parser.find(html, "div", {"class": "lists"})
        alternative_spellings_div = tag_parser.find(lists_div, "div", {"class": "alternative_spellings"})
        alternative_spellings = []

        for li in tag_parser.find_all(alternative_spellings_div, "li"):
            word = tag_parser.find_text(li, "a")
            context = tag_parser.find_text(li, "span").strip("() ") or None

            alternative_spellings.append({"word": word, "context": context})

        synonyms_div = tag_parser.find(lists_div, "div", {"class": "synonyms"})
        synonyms = []

        for li in tag_parser.find_all(synonyms_div, "li"):
            word = tag_parser.find_text(li, "a")
            context = tag_parser.find_text(li, "span").strip("() ") or None

            synonyms.append({"word": word, "context": context})

        pronunciations_div = tag_parser.find(lists_div, "div", {"class": "pronunciation"})
        pronunciations = {}

        for pronunciation in tag_parser.find_all(pronunciations_div, "li"):
            # Convert "Tuntematon aksentti" to "unknown" to unify key names
            abbr = tag_parser.find_text(pronunciation, "abbr").lower()
            if not abbr or abbr == "tuntematon aksentti": abbr = "unknown"

            url = tag_parser.find_attrs(pronunciation, "a", {"class": "audio"}).get("href", "").lstrip("//")
            pronunciation_ul = tag_parser.find(pronunciation, "ul")

            if pronunciation_ul:
                for li in tag_parser.find_all(pronunciation_ul, "li"):
                    text = tag_parser.find_text(li, "span")
                    pronunciations.setdefault(abbr, []).append({"text": text, "audio_url": url})
            else:
                pronunciations.setdefault(abbr, []).append({"text": "", "audio_url": url})

        return alternative_spellings, synonyms, pronunciations
    
    @staticmethod
    def _get_source_languages(html: str) -> List[str]:
        """
        Extract the additional source languages from the HTML of the webpage.

        :param html: The HTML of the webpage.
        :type html: str
        :return: The additional source languages as a list of strings.
        :rtype: list[str]
        """
        source_languages_div = tag_parser.find(html, "div", {"id": "source_languages"})
        source_languages = []

        # Omit the current language
        for li in tag_parser.find_all(source_languages_div, "li")[1:]:
            lang = int(tag_parser.find_attrs(li, "a").get("href", "").split("=")[-1] or 0)
            source_languages.append(LangCodes(lang).name)

        return source_languages
    
    @staticmethod
    def _get_abbreviations(html: str) -> StrDictList:
        """
        Extract the abbreviations from the HTML of the webpage.

        :param html: The HTML of the webpage.
        :type html: str
        :return: The abbreviations as :type:`StrDictList` type.
        :rtype: StrDictList
        """
        abbreviations_div = tag_parser.find(html, "div", {"class": "abbreviations"})
        abbreviations = []

        for li in tag_parser.find_all(abbreviations_div, "li"):
            word = tag_parser.find_text(li, "a")
            context = tag_parser.find_text(li, "li").rstrip(word).strip("() ") or None

            abbreviations.append({"word": word, "context": context})

        return abbreviations
    
    @staticmethod
    def _get_inflections(html: str) -> Dict[str, str]:
        """
        Extract the inflections from the HTML of the webpage.

        :param html: The HTML of the webpage.
        :type html: str
        :return: The inflections in `dict` format, with keys and values in `str` format.
        :rtype: dict[str, str]
        """
        inflections_table = tag_parser.find(html, "table", {"class": "inflections"})
        sk_rows_tr = tag_parser.find_all(inflections_table, "tr", {"class": r"sk-row[12]"})
        inflections_td = []

        for row in sk_rows_tr:
            inflections_td.extend([text for text in tag_parser.find_all_text(row, "td") if text])

        # Create a dictionary from a list alternating keys and values
        inflections = dict(zip([k.lower() for k in inflections_td[::2]], inflections_td[1::2]))

        return inflections
    
    @staticmethod
    def _get_translations(html: str, l2: int) -> TranslationResult:
        """
        Extract the translations to the target language from the HTML of the webpage.

        :param html: The HTML of the webpage.
        :type html: str
        :param l2: The target language.
        :type l2: int
        :return: The translations as :type:`TranslationResult` type.
        :rtype: TranslationResult
        """
        translations_table = tag_parser.find(html, "table", {"class": "translations"})

        if not l2:
            rows_tr = tag_parser.find_all(translations_table, "tr", {"class": r"sk-row[12]"})
            lang_dict = {}

            for row in rows_tr:
                rows_td = tag_parser.find_all(row, "td")
                lang_tag = tag_parser.find(rows_td[0], "a")
                lang = int(tag_parser.find_attrs(lang_tag, "a").get("href", "").split("=")[-1] or 0)
                words_and_transliterations = []

                for full_word in rows_td[1].split(","):
                    word = tag_parser.find_text(full_word, "a")
                    transliteration_match = re.search(r"\(([^)]+)\)", full_word)

                    words_and_transliterations.append((word, transliteration_match.group(1) if transliteration_match else None))

                lang_dict[LangCodes(lang).name] = [{
                    "word": word,
                    "transliteration": transliteration,
                    "gender": None,
                    "group": None,
                    "context": [],
                    "pronunciations": {}
                } for word, transliteration in words_and_transliterations]

            return lang_dict

        rows_tr = tag_parser.find_all(translations_table, "tr", {"class": r"(group_name|sk-row[12])"})
        current_group = None
        translations = []

        for row in rows_tr:
            if "group_name" in row:
                current_group = tag_parser.find_text(row, "td")
                continue

            rows_td = tag_parser.find_all(row, "td")
            word = tag_parser.find_text(rows_td[1], "a")
            
            gender_span = tag_parser.find_text(rows_td[1], "span")
            gender = gender_span.strip("{}") if gender_span else None

            transliterations = re.search(r"\(([^)]+)\)", tag_parser.find_text(rows_td[1], "td"))
            transliteration = transliterations.group(1) if transliterations else None

            # The 3rd "td" tag is *usually* reserved for context, however, sometimes it contains pronunciations instead
            # For this reason, we have to check if it contains nested tags
            context_td = tag_parser.find_text(rows_td[2] if len(rows_td) > 2 else "", "td")
            context = [part.strip() for part in context_td.split(",")] if context_td and "<" not in re.sub(r"^<td>|</td>$", "", rows_td[2]) else []

            pronunciation_ul = tag_parser.find(row, "ul", {"class": "audio"})
            pronunciation_li = tag_parser.find_all(pronunciation_ul, "li")
            abbrs = [abbr.lower() or "unknown" for abbr in tag_parser.find_all_text(pronunciation_ul, "li")]
            pronunciations = {}

            for abbr, li in zip(abbrs, pronunciation_li):
                url = tag_parser.find_attrs(li, "a", {"class": "audio"}).get("href", "").lstrip("//")
                pronunciations.setdefault(abbr, []).append(url)

            translations.append({
                "word": word,
                "transliteration": transliteration,
                "gender": gender,
                "group": current_group,
                "context": context,
                "pronunciations": pronunciations
            })

        return {LangCodes(l2).name: translations}
    
    @staticmethod
    def _get_transliteration(html: str) -> Optional[str]:
        """
        Extract the transliteration from the HTML of the webpage.

        :param html: The HTML of the webpage.
        :type html: str
        :return: The transliteration in `str` format, or None if not applicable.
        :rtype: str | None
        """
        transliteration_text = tag_parser.find_text(html, "p", {"class": "transliteration"})
        transliteration = transliteration_text.split("Translitterointi: ")[-1][:-1] if transliteration_text else None

        return transliteration
    
    @staticmethod
    def _get_relations(html: str) -> List[str]:
        """
        Extract the relations from the HTML of the webpage.

        :param html: The HTML of the webpage.
        :type html: str
        :return: The relations as a list of strings.
        :rtype: list[str]
        """
        relations_div = tag_parser.find(html, "ul", {"class": r"relations.*"})
        relations = tag_parser.find_all_text(relations_div, "a")

        return list(dict.fromkeys(relations))
    
    @staticmethod
    def _get_similar_words(html: str) -> List[str]:
        """
        Extract the similar words from the HTML of the webpage.

        :param html: The HTML of the webpage.
        :type html: str
        :return: The similar words as a list of strings.
        :rtype: list[str]
        """
        similar_words_div = tag_parser.find(html, "div", {"class": "similar_words"})
        similar_words = tag_parser.find_all_text(similar_words_div, "a")

        return similar_words
    
    @staticmethod
    def _get_definitions(html: str) -> DefinitionResult:
        """
        Extract the definitions from the HTML of the webpage.

        :param html: The HTML of the webpage.
        :type html: str
        :return: The definitions as :type:`DefinitionResult` type.
        :rtype: DefinitionResult
        """
        definitions_div = tag_parser.find(html, "div", {"class": "definitions"})
        current_group = None
        definitions = []

        for li in tag_parser.find_all(definitions_div, r"li|h4"):
            if "h4" in li:
                current_group = tag_parser.find_text(li, "h4")
                continue

            context_em = tag_parser.find_text(li, "em").strip("()")
            context = [part.strip() for part in context_em.split(",")] if context_em else []
            text_full = tag_parser.find_text(li, "li")

            # Account for the stripped parentheses and whitespace
            text = text_full[len(context_em) + 3:] if context_em else text_full

            definitions.append({"text": text, "group": current_group, "context": context})

        return definitions
    
    @staticmethod
    def _get_examples(html: str, l: int, l2: int) -> ExampleResult:
        """
        Extract the examples from the HTML of the webpage.

        :param html: The HTML of the webpage.
        :type html: str
        :return: The examples as :type:`ExampleResult` type.
        :rtype: ExampleResult
        """
        examples_div = tag_parser.find(html, "div", {"class": "examples"})
        examples_li = tag_parser.find_all(examples_div, "li")
        examples = tag_parser.find_all_text(examples_div, "li")
        translated_examples = [example for li in examples_li if (example := tag_parser.find_text(li, "ul"))]

        for i, translation in enumerate(translated_examples):
            examples[i] = examples[i].replace(translation, "")

        result = {}
        if examples: result[LangCodes(l).name] = examples
        if translated_examples: result[LangCodes(l2).name] = translated_examples

        return result
    
    @staticmethod
    def _get_categories(html: str) -> List[str]:
        """
        Extract the categories from the HTML of the webpage.

        :param html: The HTML of the webpage.
        :type html: str
        :return: The categories as a list of strings.
        :rtype: list[str]
        """
        categories_div = tag_parser.find(html, "div", {"class": "categories"})
        categories = tag_parser.find_all_text(categories_div, "a")

        return categories
    
    def search(self, q: str, l: Union[int, str, LangCodes] = 0, l2: Union[int, str, LangCodes] = 0) -> SanakirjaResult:
        """
        Search sanakirja.org for information on a given query.

        :param q: The search query to retrieve information for.
        :type q: str
        :param l: The source language.
        :type l: int | str | LangCodes
        :param l2: The target language.
        :type l2: int | str | LangCodes
        :return: The information dictionary as a :type:`SanakirjaResult` type.
        :rtype: SanakirjaResult
        :raises LanguageCodeError: If either of the given language codes is invalid.
        """
        if (valid_l := self._validate_lang_code(l)) is False: raise LanguageCodeError(str(l))
        l = valid_l

        if (valid_l2 := self._validate_lang_code(l2)) is False: raise LanguageCodeError(str(l2))
        l2 = valid_l2

        # Make a request to the percent-encoded URL
        with urllib.request.urlopen(self.__base_url.format(quote(q), l, l2)) as response:
            html = response.read().decode("utf-8")

        sk_var = self._get_sk_var(html)
        if not l: l = sk_var.get("source_language") or 0

        alternative_spellings, synonyms, pronunciations = self._get_alt_synonyms_and_pronunciations(html)
        additional_source_languages = self._get_source_languages(html)
        multiple_spellings = self._get_multiple_spellings(html)
        abbreviations = self._get_abbreviations(html)
        inflections = self._get_inflections(html)
        translations = self._get_translations(html, l2)
        transliteration = self._get_transliteration(html)
        relations = self._get_relations(html)
        similar_words = self._get_similar_words(html)
        definitions = self._get_definitions(html)
        examples = self._get_examples(html, int(l), l2 if not (keys := list(translations.keys())) else LangCodes[keys[0]])
        categories = self._get_categories(html)

        result: SanakirjaResult = {
            "id": int(sk_var.get("main_word_id") or 0),
            "source_language": (l if isinstance(l, str) else LangCodes(l).name) if l else None,
            "target_language": (l2 if isinstance(l2, str) else LangCodes(l2).name) if l2 else None,
            "word": str(sk_var.get("main_word_text") or q),
            "transliteration": transliteration,
            "additional_source_languages": additional_source_languages,
            "relations": relations,
            "similar_words": similar_words,
            "alternative_spellings": alternative_spellings,
            "multiple_spellings": multiple_spellings,
            "synonyms": synonyms,
            "pronunciations": pronunciations,
            "abbreviations": abbreviations,
            "inflections": inflections,
            "definitions": definitions,
            "examples": examples,
            "categories": categories,
            "translations": translations
        }
        return result
