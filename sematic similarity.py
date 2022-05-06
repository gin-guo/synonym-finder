import random
import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    '''Return the cosine similarity between the sparse vectors vec1 and vec2,
    stored as dictionaries with the same number of keys
    '''
    prod_sum, sum_1sqr, sum_2sqr = 0, 0, 0

    for i in vec1:
        if i in vec2:
            prod_sum += vec1[i] * vec2[i]
        sum_1sqr += vec1[i] ** 2

    for j in vec2:
        sum_2sqr += vec2[j] ** 2

    sim = prod_sum / math.sqrt(sum_1sqr * sum_2sqr)

    return sim


def build_semantic_descriptors(sentences):
    big_dict = {}
    for sentence in sentences:
        dict_sentence = dict.fromkeys(sentence) #get rid of duplicate words
        sent = list(dict_sentence.keys())
        for word in sent:
            if word not in big_dict:
                big_dict[word] = {}

        for i in range(len(sent) - 1):
            for j in range(i+1, len(sent)):
                if sent[j] not in big_dict[sent[i]]:
                    big_dict[sent[i]][sent[j]] = 1
                    big_dict[sent[j]][sent[i]] = 1
                else:
                    big_dict[sent[i]][sent[j]] += 1
                    big_dict[sent[j]][sent[i]] += 1

    return big_dict

def build_semantic_descriptors_from_files(filenames):
    big_list = []
    punctuation = [",", "--", ":", ";", "(", ")", '"', "*", "â€", "â€™", "â€œ", "â€˜", "'"]
    sentence_ends = ["!", "?"]
    for filename in filenames:
        f = open(filename, "r", encoding="latin1")#"UTF-8")
        text = f.read()
        text = text.lower()

        text = text.replace("-", " ")
        text = text.replace("â€”", " ")
        # text = text.replace("'", " ")
        for i in punctuation:
            text = text.replace(i, "")

        for j in sentence_ends:
            text = text.replace(j, ".")

        text = text.split(".")#creates list of sentences
        for k in text:
            k = k.split()
            big_list.append(k)

        # big_list.append(text)

    big_dict = build_semantic_descriptors(big_list)

    return big_dict

# ["war_and_peace.txt", "swanns_way.txt", "gutenberg_pride.txt"]


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    max_similarity = [-1000, ""]
    if word not in semantic_descriptors:
        # print("ERROR")
        max_similarity[0] = -1
        max_similarity[1] = choices[0]
        # print(word, max_similarity[1])
    else:
        v1 = semantic_descriptors[word]

        for choice in choices:
            if choice not in semantic_descriptors:
                # print(choice)
                similarity = -1
            else:
                v2 = semantic_descriptors[choice]
                similarity = similarity_fn(v1, v2)

            if similarity > max_similarity[0]:
                max_similarity = [similarity, choice]

    return max_similarity[1]


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    percentage = 0
    correct_answers = 0
    total_answers = 0

    f = open(filename)
    text = f.read()
    text = text.split("\n")
    total_answers = len(text)

    for line in text:
        line = line.split()
        estimated_answer = most_similar_word(line[0], line[2:], semantic_descriptors, similarity_fn)
        answer = line[1]

        if estimated_answer == answer:
            correct_answers += 1
        # else:
            # print(line, estimated_answer)

    percentage = correct_answers / total_answers * 100
    return percentage
