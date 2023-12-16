import tensorflow._api.v2.compat.v1 as tf
tf.logging.set_verbosity(tf.logging.ERROR)
import tensorflow_hub as hub
import numpy as np
import pickle
from tqdm import tqdm
from itertools import combinations
from copy import copy
from .commons import Token, LabelType
from .commons import WILDCARD_CHAR, CHARMAP_PATH, MODEL_PATH
from .rules_applier import apply_binary_rules_to_tokens
from .password_rules import join as join_rule


class TemplateBasedPasswordModel:
    def __init__(self, num_of_samples: int, stddev: float):
        tf.disable_v2_behavior()
        tf.reset_default_graph()
        tf.logging.set_verbosity(tf.logging.ERROR)
        self.MAX_LEN = 16

        self.num_of_samples = num_of_samples
        self.stddev = stddev
        self.char2id = None
        self.id2char = None
        self.x_placeholder = None
        self.prediction_tensor = None

        self.load_char2id_id2char()
        self.load_model()

    def load_char2id_id2char(self):
        with open(CHARMAP_PATH, 'rb') as f:
            char2id: dict[str, int] = pickle.load(f)

        id2char: list[str] = [''] * len(char2id)
        for char, id in char2id.items():
            id2char[id] = char

        self.char2id = char2id
        self.id2char = id2char

    def load_model(self):
        module = hub.Module(MODEL_PATH)
        x_placeholder = tf.placeholder(tf.int32, shape=(None, self.MAX_LEN))

        module_inputs = {'x': x_placeholder,
                         'stddev': (self.stddev,),
                         'n': (self.num_of_samples,)}

        module_dict = module(module_inputs, as_dict=True,
                             signature='sample_from_latent')
        prediction_tensor = module_dict['prediction']

        self.x_placeholder = x_placeholder
        self.prediction_tensor = prediction_tensor

    def template2vector(self, template: str) -> tf.Tensor:
        template_as_vector = np.zeros(self.MAX_LEN, dtype=np.int32)

        for i, c in enumerate(template):
            template_as_vector[i] = self.char2id.get(c, -1)

        template_as_vector = template_as_vector[None, :]
        return template_as_vector

    def vector2template(self, vector: tf.Tensor) -> str:
        return ''.join(self.id2char[i] for i in vector if i > 0)

    def tensor2templates(self, tensor: tf.Tensor) -> list[str]:
        return list(map(self.vector2template, tensor))

    def is_sample_valid(self, template: str, sample: str) -> bool:
        return len(sample) == len(template) \
            and all(sc == tc or tc == WILDCARD_CHAR
                    for sc, tc in zip(sample, template))

    def filterout_invalid_samples(self, template: str, samples: list[str]) -> list[str]:
        partial_is_sample_valid = lambda sample: self.is_sample_valid(template, sample)
        return list(set(filter(partial_is_sample_valid, samples)))

    def sample_model_based_on_templates(self, templates: list[Token]) -> list[Token]:
        produced_tokens = list[Token]()

        with tf.Session() as sess:
            sess.run(tf.initialize_all_variables())
            try:
                for template in tqdm(templates, desc='Generating passwords'):
                    template_as_vector = self.template2vector(template.text)
                    samples = sess.run(self.prediction_tensor,
                                    {self.x_placeholder: template_as_vector})

                    samples_as_strings = self.tensor2templates(samples)
                    samples_filtered = self.filterout_invalid_samples(template.text, samples_as_strings)

                    new_label = LabelType.remove_label_from_binary_mask(
                        LabelType.WILDCARD, template.binary_mask)
                    new_tokens = list(map(
                        lambda sample: Token(sample, new_label),
                        samples_filtered))

                    produced_tokens.extend(new_tokens)
            except KeyboardInterrupt:
                print("Early stopping")

        return produced_tokens

def poke_holes_in_tokens(tokens: list[Token]) -> list[Token]:
    wildcard_binary_mask = 1 << LabelType.WILDCARD.value
    tokens_with_holes = []
    for token in tokens:
        # Without holes
        tokens_with_holes.append(token)
        # With one hole
        for i in range(len(token)):
            tokens_with_holes.append(Token(token.text[:i] + WILDCARD_CHAR + token.text[i + 1 :], token.binary_mask | wildcard_binary_mask))
        # With two holes
        comb = combinations(list(range(len(token.text))), 2)
        for i, j in comb:
            token_text_list = list(copy(token.text))
            token_text_list[i] = WILDCARD_CHAR
            token_text_list[j] = WILDCARD_CHAR
            tokens_with_holes.append(Token(''.join(token_text_list), token.binary_mask | wildcard_binary_mask))
    return tokens_with_holes

def tokens_to_seeds(tokens, max_length) -> list[Token]:
    wildcard_binary_mask = 1 << LabelType.WILDCARD.value
    wildcard_tokens = [Token(WILDCARD_CHAR * n, wildcard_binary_mask)
              for n in range(1, 5)]
    tokens_with_holes = poke_holes_in_tokens(tokens)
    new_tokens = tokens_with_holes + wildcard_tokens
    total_num = len(new_tokens) * len(new_tokens)

    progress_bar = tqdm(desc=f'Mangling tokens with wildcards',
                        total=total_num)
    mangled_tokens = apply_binary_rules_to_tokens([join_rule], new_tokens, max_length, progress_bar)
    return mangled_tokens