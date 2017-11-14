import MeCab


class WordDivider:

    def __init__(self, dictionary=".mecabrc", is_normalize=False):
        self.dictionary = dictionary
        self.tagger = MeCab.Tagger(self.dictionary)
        self.tagger.parse("") # necessary in Python3
        self.is_normalize = is_normalize

    def extract_words(self, text, with_pos=True):
        if not text:
            return []

        words = []
        # normalize text before MeCab processing
        if self.is_normalize:
            text = text.lower()

        node = self.tagger.parseToNode(text)
        while node:
            features = node.feature.split(',')
            # extract word surface (configurable)
            word_to_append = node.surface
            if with_pos:
                pos = features[0]
                word_to_append = '{}/{}'.format(word_to_append, pos)
            words.append(word_to_append)
            node = node.next

        return words


def filter_punctuations(filepath, outpath, batch_sentences_size=10):
    # one line contains batch_sentences_size sentences
    # '、', '。'を両方含む行だけ抽出(同一文は複数行にまたがらないと仮定)
    lines_to_add = []
    with open(filepath, encoding='utf-8', errors='ignore') as ifp, \
         open(outpath, 'w', encoding='utf-8') as ofp:
        for line in ifp:
            if '、' in line and '。' in line:
                lines = line.strip().split('。')[:-1]
                if len(list(filter(None, lines))) > 1:
                    lines_to_add += lines
                if len(lines_to_add) > batch_sentences_size:
                    ofp.write('。'.join(lines_to_add) + '。\n')
                    lines_to_add = []


def make_wakati_from_corpus(filepath, outpath):
    wd = WordDivider(is_normalize=True)
    docs = []
    with open(filepath, encoding='utf-8', errors='ignore') as ifp, \
         open(outpath, 'w', encoding='utf-8') as ofp:
        for line in ifp:
            words = wd.extract_words(line)
            line_to_write = ' '.join(words)
            ofp.write(line_to_write + '\n')

def replace_pnct(filepath, outpath):
    with open(filepath, encoding='utf-8', errors='ignore') as ifp, \
         open(outpath, 'w', encoding='utf-8') as ofp:
        for line in ifp:
            words_to_append = []
            unigrams = line.split(' ')
            bigrams = [b for b in zip(unigrams[:-1], unigrams[1:])]
            for w, wn in bigrams:
                if len(w.split('/')) == 2 and len(wn.split('/')) == 2:
                    surface, pos = w.split('/')
                    if surface != '、' and surface != '。':
                        sn, _ = wn.split('/')
                        yomi = '0'
                        if sn == '。':
                            yomi = '1'
                        elif sn == '、':
                            yomi = '2'
                        words_to_append.append('{}/{}'.format(w, yomi))
            line_to_write = ' '.join(words_to_append)
            ofp.write(line_to_write + '\n')

if __name__ == '__main__':
    print('filtering puncuations')
    filter_punctuations('input.txt', 'sentences.txt')
    print('making wakati from raw sentences')
    make_wakati_from_corpus('sentences.txt', 'wakati.txt')
    print('attaching punctuation labels to each previous words')
    replace_pnct('wakati.txt', 'X.txt')
