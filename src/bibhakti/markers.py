"""Odia case markers (bibhakti) and a simple rule-based splitter.

This is an early, deliberately simple baseline. It strips one fused case
marker from the end of a word using longest-match rules, with two guards:

* a minimum stem length counted in aksharas (syllable units), so short
  words such as ଗୁରୁ are not cut; and
* the bare genitive ର is off by default, because many Odia stems already
  end in ର (ଘର, ନଗର, ଭୁବନେଶ୍ୱର).
"""

import unicodedata

VIRAMA = "୍"

# Fused case markers, grouped by case. Longer forms come first so that
# longest-match wins (ଙ୍କୁ before କୁ, ଠାରୁ before ରୁ).
MARKERS = {
    "plural_case": ["ମାନଙ୍କଠାରୁ", "ମାନଙ୍କଠାରେ", "ମାନଙ୍କୁ", "ମାନଙ୍କର", "ମାନଙ୍କ", "ମାନେ"],
    "ablative": ["ଙ୍କଠାରୁ", "ଠାରୁ", "ରୁ"],
    "locative": ["ଙ୍କଠାରେ", "ଠାରେ", "ରେ"],
    "accusative_dative": ["ଙ୍କୁ", "କୁ"],
    "genitive": ["ଙ୍କର", "ଙ୍କ"],
}

# The bare genitive ର is ambiguous with stem-final ର, so it is opt-in.
AMBIGUOUS_MARKERS = {"genitive": ["ର"]}


def _is_odia_letter(ch):
    cp = ord(ch)
    return 0x0B05 <= cp <= 0x0B39 or 0x0B5C <= cp <= 0x0B5F or cp == 0x0B71


def akshara_count(text):
    """Count aksharas: Odia letters not joined to the previous one by a virama."""
    count = 0
    prev = ""
    for ch in text:
        if _is_odia_letter(ch) and prev != VIRAMA:
            count += 1
        prev = ch
    return count


def _suffix_list(include_ambiguous):
    pairs = [(m, case) for case, ms in MARKERS.items() for m in ms]
    if include_ambiguous:
        pairs += [(m, case) for case, ms in AMBIGUOUS_MARKERS.items() for m in ms]
    return sorted(pairs, key=lambda p: len(p[0]), reverse=True)


def split(word, min_stem=2, include_ambiguous=False, protected=None):
    """Split one fused case marker off an Odia word.

    Returns (stem, marker). The marker is "" when nothing is split.

    >>> split("କଟକରୁ")
    ('କଟକ', 'ରୁ')
    """
    word = unicodedata.normalize("NFC", word)
    if protected and word in protected:
        return word, ""
    for marker, _case in _suffix_list(include_ambiguous):
        if word.endswith(marker):
            stem = word[: -len(marker)]
            if akshara_count(stem) >= min_stem:
                return stem, marker
    return word, ""


def case_of(marker):
    """Return the case name for a marker, or None if unknown."""
    for case, ms in {**MARKERS, **AMBIGUOUS_MARKERS}.items():
        if marker in ms:
            return case
    return None


def segment(text, **kwargs):
    """Split every whitespace word in a sentence; return a flat token list."""
    tokens = []
    for word in text.split():
        stem, marker = split(word, **kwargs)
        tokens.append(stem)
        if marker:
            tokens.append(marker)
    return tokens
