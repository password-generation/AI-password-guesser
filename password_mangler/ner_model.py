from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from commons import Language, Token, LabelType, NotSupportedLabelType


class NERModel:
    def __init__(self, language: Language):
        if language == Language.ENGLISH:
            self.tokenizer = AutoTokenizer.from_pretrained('dslim/bert-base-NER')
            self.model = AutoModelForTokenClassification.from_pretrained('dslim/bert-base-NER')
        elif language == Language.POLISH:
            self.tokenizer = AutoTokenizer.from_pretrained('pietruszkowiec/herbert-base-ner')
            self.model = AutoModelForTokenClassification.from_pretrained('pietruszkowiec/herbert-base-ner')

        self.nlp = pipeline('ner', model=self.model, tokenizer=self.tokenizer)

    def predict(self, text):
        return self.nlp(text)

    def recognize_tokens(self, text):
        predictions = self.predict(text)
        tokens = list[Token]()

        start_idx = end_idx = -1

        for pred in predictions:
            if pred['entity'].startswith('B-'):
                if start_idx != -1:
                    try:
                        label = LabelType.parse_label(pred['entity'][2:])
                    except NotSupportedLabelType as e:
                        continue
                    txts = text[start_idx:end_idx].split()

                    for txt in txts:
                        tok = Token(txt, 1 << label.value)
                        tokens.append(tok)

                start_idx = pred['start']
                end_idx = pred['end']
            elif pred['entity'].startswith('I-'):
                end_idx = pred['end']

        return tokens
