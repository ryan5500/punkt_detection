import kenlm
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


class PunktDetector:

    def __init__(self, lm):
        self.model = kenlm.Model(lm)
        self.order = self.model.order
        self.punkts = ['、', '。']
        self.wd = WordDivider(is_normalize=True)

    def punkt_insert(self, sentence, punkt='。', debug=False):
        window = self.order
        words = sentence.split(' ')
        punkt_pos = []
        for i in range(len(words)-window+1):
            prob = self.model.score(' '.join(words))
            sent_p = ' '.join(words[:i+window] + [punkt] + words[i+window:])
            prob_p = self.model.score(sent_p)
            if prob_p > prob:
                if debug:
                    print(prob_p, prob, words[i:i+window])
                punkt_pos.append(i+window)
        return punkt_pos

    def punkt_decode(self, sentence, punkt_pos, punkt='。'):
        words = sentence.split(' ')
        pnkt_sent = []
        for i in range(len(words)):
            pnkt_sent.append(words[i])
            if i+1 in punkt_pos:
                pnkt_sent.append(punkt)
        return ' '.join(pnkt_sent)

    # 句読点付き文から句点挿入位置を抽出
    def extract_positions(self, sentence, punkt='。'):
        true_positions = []
        c_pos = 0
        for w in sentence.split(' '):
            if w in self.punkts:
                if w == punkt:
                    true_positions.append(c_pos)
            else:
                c_pos += 1
        return true_positions

    # 句読点無し文に対する句点挿入位置の予測結果から精度と再現率を計算
    def prf(self, punkt_pred, punkt_true):
        tp = set.intersection(set(punkt_pred), set(punkt_true))
        recall = len(tp) / len(punkt_true) if len(punkt_true) > 0 else 0
        precision = len(tp) / len(punkt_pred) if len(punkt_pred) > 0 else 0
        fval = 2 / (1/precision + 1/recall) if precision and recall else 0.
        return precision, recall, fval

    def prf_from_sentences(self, sentence_pred, sentence_true):
        punkt_pred = self.extract_positions(sentence_pred)
        punkt_true = self.extract_positions(sentence_true)
        print(punkt_pred, punkt_true)
        return self.prf(punkt_pred, punkt_true)

    def wakati(self, line):
        words = self.wd.extract_words(line, with_pos=False)
        return ' '.join(filter(None, words))

    def analyze(self, sentence_true):
        # sentence_true = '今日も、いい天気だ。明日の天気も晴れらしい。'
        sentence_true_w = self.wakati(sentence_true)
        print('入力文:')
        print(sentence_true_w)
        sentence_raw = ''.join(filter(lambda x: x not in self.punkts,
                                      sentence_true_w))
        sentence_raw_w = self.wakati(sentence_raw)
        punkt_position = self.punkt_insert(sentence_raw_w)
        sentence_pred_w = self.punkt_decode(sentence_raw_w, punkt_position)

        print('予測結果:')
        print(sentence_pred_w)
        sentence_pred = ''.join(sentence_pred_w.split(' '))
        p,r,f = self.prf_from_sentences(sentence_pred_w, sentence_true_w)
        print('Precision:{0:.5g}, Recall:{1:.5g}, F-value:{2:.5g}'.format(p,r,f))
        return sentence_pred


if __name__ == '__main__':
    LM='data/model.100K.klm'
    model = PunktDetector(LM)
    model.analyze('今日も、いい天気だ。明日の天気も晴れらしい。')
