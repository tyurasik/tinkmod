import argparse
import re
import pickle
import random

class Model():
    def __init__(self, filename):
        self.train = filename

    def fit(self):
        #считывание и форматирование текста
        with open(self.train, 'r', encoding='utf-8') as file:
            text = file.read()
        lower_text = text.lower()
        ru_letters_text = re.sub('[^а-яё]', ' ', lower_text)
        splitted_text = re.split('\s+', ru_letters_text)
        text_len = len(splitted_text)

        word_dict = {}
        #создание би-граммной модели
        for i in range(0, text_len - 1):
            if splitted_text[i] != splitted_text[i + 1]:
                if splitted_text[i] not in word_dict:
                    word_dict[splitted_text[i]] = [splitted_text[i + 1]]
                else:
                    if splitted_text[i + 1] not in word_dict[splitted_text[i]]:
                        word_dict[splitted_text[i]].append(splitted_text[i + 1])

        return pickle.dumps(word_dict)

    def generate(self, length: int, prefix):
        bigrams = pickle.loads(self.fit())
        generated_text = []
        
        #форматирование начала генерируемого текста
        lower_prefix = prefix.lower()
        ru_letters_prefix = re.sub('[^а-яё]', ' ', lower_prefix)
        splitted_prefix = re.split('\s+', ru_letters_prefix)
        prefix_len = len(splitted_prefix)
        
        #выбор начала генерируемого текста
        init_word = max(bigrams, key=lambda element: len(bigrams[element]))
        #проверка наличия заданного начала генерируемого текста
        if prefix_len != 0 and splitted_prefix[prefix_len - 1] in bigrams:
            init_word = splitted_prefix[prefix_len - 1]
            generated_text = splitted_prefix
        else:
            generated_text = [init_word]
        
        cur = init_word
        #добавление слов в генерируемый текст
        for i in range(length - 1):
            next = random.choice(bigrams[cur])
            generated_text.append(next)
            cur = next
        
        with open('generated.txt', 'w') as F:
            F.write(' '.join(generated_text))
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Путь к файлу, из которого загружается модель")
    parser.add_argument("--prefix", help="Необязательный аргумент. Начало предложения (одно или несколько слов). ")
    parser.add_argument("--length", type=int, help="Длина генерируемой последовательности")
    args = parser.parse_args()
    filename = args.file
    length = args.length
    prefix = args.prefix
    text = Model(filename)
    text.generate(length, prefix)

if __name__ == '__main__':
    main()
