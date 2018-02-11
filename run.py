import os
import re
from os import walk


def run():
    try:
        index = create_index(get_file_names())
        print("Index created with %s words." % len(index))
        search_words(index)
    except ValueError as e:
        print(str(e))


def search_words(index):
    while True:
        search_word = input('Input word (print exit to stop): ')
        if search_word == 'exit':
            return
        if search_word in index:
            print('Word found in:')
            for file_name in index[search_word]:
                print(file_name)
        else:
            print('Word not found')


def get_file_names():
    directory_path = input('Input directory with files: ')
    for (_, _, file_names) in walk(directory_path):
        return [os.path.join(directory_path, f) for f in file_names]


def create_index(file_names):
    if file_names is None:
        raise ValueError('Can not read from directory.')

    index = {}
    for file_name in file_names:
        index = merge_index(index, get_file_words(file_name), file_name)
    return index


def get_file_words(file_name):
    words = set()
    f = open(file_name, 'r')
    try:
        for line in f:
            for word in [w.lower() for w in re.split('[^a-zA-Z]+', line) if len(w) != 0]:
                words.add(word)
        print('Processed: %s. Words: %s' % (file_name, len(words)))
        return words
    except:
        print('Can not process file: %s' % file_name)
        return words
    finally:
        f.close()


def merge_index(index, words, file_name):
    for word in words:
        put_to_index(index, word, file_name)
    return index


def put_to_index(index, word, file_name):
    if word in index:
        index[word].add(file_name)
    else:
        index[word] = {file_name}


if __name__ == "__main__":
    run()
