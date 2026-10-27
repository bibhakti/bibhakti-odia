from bibhakti import case_of, segment, split


def test_ablative():
    assert split("କଟକରୁ") == ("କଟକ", "ରୁ")


def test_locative_with_conjunct():
    assert split("ଭୁବନେଶ୍ୱରରେ") == ("ଭୁବନେଶ୍ୱର", "ରେ")


def test_honorific_dative():
    assert split("ରାମଙ୍କୁ") == ("ରାମ", "ଙ୍କୁ")


def test_stem_ending_in_ra_is_kept():
    assert split("ଭୁବନେଶ୍ୱର") == ("ଭୁବନେଶ୍ୱର", "")


def test_short_word_not_cut():
    assert split("ଗୁରୁ") == ("ଗୁରୁ", "")


def test_ambiguous_genitive_opt_in():
    assert split("କଟକର", include_ambiguous=True) == ("କଟକ", "ର")


def test_protected_word():
    assert split("କଟକରୁ", protected={"କଟକରୁ"}) == ("କଟକରୁ", "")


def test_case_lookup():
    assert case_of("ରୁ") == "ablative"


def test_sentence():
    tokens = segment("ମୋ ଠିକଣା କଟକରୁ ଭୁବନେଶ୍ୱରକୁ ବଦଳିଛି")
    assert tokens == ["ମୋ", "ଠିକଣା", "କଟକ", "ରୁ", "ଭୁବନେଶ୍ୱର", "କୁ", "ବଦଳିଛି"]
