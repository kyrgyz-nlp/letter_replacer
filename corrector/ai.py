import fasttext
from fasttext import FastText


kloop_model = FastText.load_model('kloop_with_books_model.bin')
u_umlaut_model = fasttext.load_model('u_and_u_umlaut_dataset.bin')
o_umlaut_model = fasttext.load_model('o_and_o_umlaut_dataset.bin')
n_umlaut_model = fasttext.load_model('n_and_n_umlaut_dataset.bin')


def contains_exception_subwords(w, exc):
    return any(ex in w.lower() for ex in exc)


def contains_exceptional_endings(w, exc_endings):
    return any(w.lower().endswith(ex) for ex in exc_endings)


def get_sentence_vector_sum(sent):
    # Kloop's model
    return sum(kloop_model.get_sentence_vector(sent))
    # Facebook's model
    # return sum(m.get_sentence_vector(sent))


def get_indices(word, letter):
    indices = [ind for ind, x in list(enumerate(word)) if x == letter]
    return indices


def get_candidates(word, letter, indices):
    candidates = []
    for i in range(len(indices)):
        l_w = list(word)
        l_w[indices[i]] = letter
        candidates.append(''.join(l_w))
    if len(indices) > 1:
        seek_letter = word[indices[0]]
        candidates.append(word.replace(seek_letter, letter))
    return list(set(candidates))


o_exceptions = [
    'ова',  # family name ending,
    'ов',  # family name ending,
    'фото',
    'соц',
    'макро',
    'сүткор',
    'авто',
    'аэро',
    'түрколог'
]

o_exceptional_endings = [
    'бүбү'
]

o_uml_exceptions = [
    'ов',  # family name ending
    'ова',  # family name ending
    'кумтөр',
    'жөлөкпул',
    'көмөкчордон',
    'кулмүнөз'
]

o_uml_exceptional_endings = [
    'кул'
]

n_uml_exceptions = [
]

n_uml_exceptional_endings = [
]


def _should_skip(word, exc, exc_end):
    is_corr = any([
        contains_exception_subwords(word, exc),
        contains_exceptional_endings(word, exc_end)
    ])
    return is_corr


def is_correct_u_uml_and_o(word, exc, exc_end):
    is_corr = _should_skip(word, exc, exc_end)
    if is_corr:
        return is_corr
    # "о" appears in a word together with "ү" if there are "и" or "e"
    rule_1 = True
    if 'о' in word and 'ү' in word:
        rule_1 = 'и' in word or 'е' in word
    rule_2 = True
    if 'ө' in word and 'ү' in word:
        rule_2 = 'у' not in word
    rule_3 = True
    if 'ү' in word:
        rule_3 = 'у' not in word
    rule_4 = True
    if 'ү' in word:
        rule_4 = 'о' not in word
    return rule_1 and rule_2 and rule_3 and rule_4


def is_correct_o_uml_and_u(word, exc, exc_end):
    is_corr = _should_skip(word, exc, exc_end)
    if is_corr:
        return is_corr
    # "ө" never appears with "у" with
    # small exceptions like "кулмүнөздүү" or "Өмүркуловдуку"
    rule_1 = True
    if 'ө' in word:
        rule_1 = 'у' not in word
    rule_2 = True
    if 'ө' in word and 'ү' in word:
        rule_2 = 'у' not in word
    rule_3 = True
    if 'ө' in word:
        rule_3 = 'о' not in word
    rule_4 = True
    if 'ү' in word:
        rule_4 = 'о' not in word
    return rule_1 and rule_2 and rule_3 and rule_4


def is_correct_n_uml(word, exc, exc_end):
    # is_corr = _should_skip(word, exc, exc_end)
    rule_1 = True
    if 'ө' in word and 'ң' in word and 'ү' in word:
        rule_1 = 'у' not in word
    return rule_1


def apply_u_uml_filters(candidates):
    wrong_endings = [
        'өдум'
    ]

    def not_end_with(x):
        return all([not x.endswith(ending) for ending in wrong_endings])
    candidates = filter(not_end_with, candidates)
    u_replacement_candidates = filter(
        lambda x: is_correct_u_uml_and_o(
            x, o_exceptions, o_exceptional_endings),
        candidates
    )
    return list(u_replacement_candidates)


def get_o_uml_replacement_candidate(word):
    o_indices = get_indices(word, 'о')
    o_replacement_candidates = get_candidates(word, 'ө', o_indices)
    o_replacement_candidates = filter(
        lambda x: is_correct_o_uml_and_u(
            x, o_uml_exceptions, o_uml_exceptional_endings),
        o_replacement_candidates
    )
    return o_replacement_candidates


def get_u_uml_replacement_candidate(word):
    u_indices = get_indices(word, 'у')
    u_replacement_candidates = get_candidates(word, 'ү', u_indices)
    u_replacement_candidates = apply_u_uml_filters(u_replacement_candidates)
    return u_replacement_candidates


def get_n_uml_replacement_candidate(word):
    indices = get_indices(word, 'н')
    candidates = get_candidates(word, 'ң', indices)
    candidates = filter(
        lambda x: is_correct_n_uml(
            x, n_uml_exceptions, n_uml_exceptional_endings),
        candidates
    )
    return candidates


def apply_filters(candidates):
    """
    Apply some rules to exclude unlikely candidates
    """
    wrong_endings = [
        'улор',
        'үлор',
        'өдум',
        'юшот'
    ]

    def not_end_with(x):
        return all([not x.endswith(ending) for ending in wrong_endings])
    candidates = filter(not_end_with, candidates)
    return candidates


def apply_n_uml_filters(candidates):
    wrong_endings = [
        'ңдың',
        'ңындын',
        'ңыңдың',
        'ңдуң',
        'ңдагаң',
    ]

    def not_end_with(x):
        return all([not x.endswith(ending) for ending in wrong_endings])
    candidates = filter(not_end_with, candidates)
    return list(candidates)


def get_letter_predictions_from_separate_models(word):
    """
    u_umlaut_model is used for classifying
        if there should be "у" or "ү" in the given word
    o_umlaut_model is used for classifying
        if there should be "о" or "ө" in the given word
    n_umlaut_model is used for classifying
        if there should be "н" or "ң" in the given word
    """
    pred_letters = []
    if 'у' in word:
        letter = u_umlaut_model.predict(' '.join(list(word)))[0][0][-1]
        pred_letters.append(letter)
    if 'о' in word:
        letter = o_umlaut_model.predict(' '.join(list(word)))[0][0][-1]
        pred_letters.append(letter)
    if 'н' in word:
        letter = n_umlaut_model.predict(' '.join(list(word)))[0][0][-1]
        pred_letters.append(letter)
    return pred_letters


def get_correction_candidates(word):
    pred_letters = get_letter_predictions_from_separate_models(word)
    if 'ү' in pred_letters and 'о' in pred_letters and 'ө' not in pred_letters:
        pred_letters.append('ө')
    if 'ө' in pred_letters and 'ү' in pred_letters and 'ң' in pred_letters:
        cands = apply_n_uml_filters(
            [word.replace('о', 'ө').replace('у', 'ү').replace('н', 'ң')])
        o_replacement_candidates = get_o_uml_replacement_candidate(word)
        u_replacement_candidates = get_u_uml_replacement_candidate(word)
        n_uml_candidates = apply_n_uml_filters(
            get_n_uml_replacement_candidate(word))
        cands = apply_u_uml_filters(apply_filters(
            list(cands) +
            list(o_replacement_candidates) +
            list(u_replacement_candidates) +
            list(n_uml_candidates)
        ))
        return list(set(cands))
    if 'ө' in pred_letters and 'ү' in pred_letters:
        cands = [word.replace('о', 'ө').replace('у', 'ү')]
        o_replacement_candidates = get_o_uml_replacement_candidate(word)
        u_replacement_candidates = get_u_uml_replacement_candidate(word)
        cands = apply_filters(
            cands +
            list(o_replacement_candidates) +
            list(u_replacement_candidates)
        )
        cands = apply_u_uml_filters(cands)
        return list(set(cands))
    if 'ө' in pred_letters and 'ң' in pred_letters:
        cands = [word.replace('о', 'ө').replace('н', 'ң')]
        o_replacement_candidates = get_o_uml_replacement_candidate(word)
        n_uml_candidates = apply_n_uml_filters(
            get_n_uml_replacement_candidate(word))
        cands = apply_u_uml_filters(apply_filters(
            list(cands) +
            list(o_replacement_candidates) +
            list(n_uml_candidates)
        ))
        return list(set(cands))
    if 'ү' in pred_letters and 'ң' in pred_letters:
        cands = [word, word.replace('у', 'ү').replace('н', 'ң')]
        u_replacement_candidates = apply_u_uml_filters(
            get_u_uml_replacement_candidate(word))
        n_uml_candidates = apply_n_uml_filters(
            get_n_uml_replacement_candidate(word))
        cands = apply_filters(
            list(cands) +
            list(u_replacement_candidates) +
            list(n_uml_candidates)
        )
        cands = apply_u_uml_filters(cands)
        return list(set(cands))
    if 'ң' in pred_letters:
        ca = [word, word.replace('н', 'ң')]
        n_uml_candidates = apply_n_uml_filters(
            get_n_uml_replacement_candidate(word))
        ca = apply_n_uml_filters(
            apply_filters(ca + list(n_uml_candidates)))
        return list(set(ca))
    if 'ү' in pred_letters:
        ca = [word.replace('у', 'ү')]
        u_replacement_candidates = get_u_uml_replacement_candidate(word)
        ca = apply_u_uml_filters(
            apply_filters(ca + list(u_replacement_candidates)))
        return list(set(ca))
    if 'ө' in pred_letters:
        ca = [word, word.replace('о', 'ө')]
        o_replacement_candidates = get_o_uml_replacement_candidate(word)
        ca = apply_u_uml_filters(
            apply_filters(ca + list(o_replacement_candidates)))
        return list(set(ca))
    return [word]


def get_case(cases, ind, word):
    cases_list = cases[ind]
    cased = ''.join(
        [l.upper() if cases_list[ind] else l for ind, l in enumerate(word)]
    )
    return cased


def correct_sentence(sent):
    words = sent.split(' ')
    cases = {}
    final_sent = []
    correction_candidates = {}
    for ind, word in enumerate(words):
        cases[ind] = [letter.isupper() for letter in word]
        word = word.lower()
        corr_words = get_correction_candidates(word)
        correction_candidates[ind] = corr_words
    is_single_word = len(correction_candidates.keys()) == 1
    for ind, cands in enumerate(correction_candidates.values()):
        if len(cands) > 1:
            vector_sums = []
            candidates_combinations_d = {}
            for c in cands:
                if is_single_word:
                    vector_sum = get_sentence_vector_sum(c)
                    candidates_combinations_d[vector_sum] = c
                    vector_sums.append(vector_sum)
                    continue
                next_word_candidates = correction_candidates.get(ind+1)
                ordering_format = '{0} {1}'
                if ind + 1 == len(correction_candidates.values()):
                    next_word_candidates = correction_candidates.get(ind-1)
                    ordering_format = '{1} {0}'
                if next_word_candidates:
                    for next_w in next_word_candidates:
                        combination = ordering_format.format(c, next_w)
                        vector_sum = get_sentence_vector_sum(combination)
                        candidates_combinations_d[vector_sum] = c
                        vector_sums.append(vector_sum)
            # We collected all combinations'
            # vector sums for the given candidate
            max_vector_sum = max(vector_sums)
            best_candidate = candidates_combinations_d[max_vector_sum]
            cased = get_case(cases, ind, best_candidate)
            final_sent.append(cased)
        else:
            w = cands[0]
            cased = get_case(cases, ind, w)
            final_sent.append(cased)
    return ' '.join(final_sent)
