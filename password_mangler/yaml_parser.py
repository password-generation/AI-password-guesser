import yaml
from commons import ManglingEpochType, LabelType
import password_rules


def parse_yaml(filename: str):
    with open(filename, "r") as file:
        user_config = yaml.safe_load(file)

    for epoch in user_config['mangling_schedule']:
        epoch['type'] = ManglingEpochType.UNARY if epoch['type'] == 'unary'\
            else ManglingEpochType.BINARY

        rules = []
        for rule in epoch['rules']:
            rules.append(getattr(password_rules, rule))
        epoch['rules'] = rules

        labels = []
        for label in epoch['labels']:
            labels.append(LabelType[label])
        epoch['labels'] = labels

    return user_config
