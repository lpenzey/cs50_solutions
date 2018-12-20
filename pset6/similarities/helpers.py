from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""
    # split each string into lines
    linesa = a.splitlines()
    linesb = b.splitlines()

    # instantiate results list
    lines = []

    # compare lines
    for a_line in linesa:
        for b_line in linesb:
            # if both lines match append to results
            if a_line == b_line:
                lines.append(a_line)
    # convert to set to remove duplicates
    uniquelines = set(lines)
    return uniquelines


def sentences(a, b):
    """Return sentences in both a and b"""

    # TODO
    # split each string into sentences
    sentences_a = sent_tokenize(a)
    sentences_b = sent_tokenize(b)

    sentences = []

    # compare lines
    for a_sentence in sentences_a:
        for b_sentence in sentences_b:
            # if both lines match append to results
            if a_sentence == b_sentence:
                sentences.append(a_sentence)

    # convert to set to remove duplicates
    unique_sentences = set(sentences)

    return unique_sentences


def get_substrings(string, n):
    subs = []
    for i in range(len(string) - n + 1):
        subs.append(string[i:i+n])
    return subs


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    # generate all substrings of length n
    sub_a = get_substrings(a, n)
    sub_b = get_substrings(b, n)

    substrings = []

    # compare substrings
    for a_sub in sub_a:
        for b_sub in sub_b:
            # if both substrings match append to results
            if a_sub == b_sub:
                substrings.append(a_sub)

    # convert to set to remove duplicates
    unique_substrings = set(substrings)

    return unique_substrings
