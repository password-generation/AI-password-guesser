from yaml import safe_load
from functools import partial
from commons import ManglingEpochType, LabelType
import password_rules


def parse_yaml(filename: str):
    with open(filename, "r") as file:
        user_config = safe_load(file)

    for epoch in user_config['mangling_schedule']:
        epoch['type'] = ManglingEpochType.UNARY if epoch['type'] == 'unary'\
            else ManglingEpochType.BINARY

        rules = []
        for rule in epoch['rules']:
            if isinstance(rule, dict):
                rule_name, parameter = next(iter(rule.items()))
                func = getattr(password_rules, rule_name)

                if isinstance(parameter, list):
                    rules.append(partial(func, *parameter))
                else:
                    rules.append(partial(func, parameter))
            else:
                func = getattr(password_rules, rule)
                rules.append(func)

        epoch['rules'] = rules

        labels = []
        for label in epoch['labels']:
            labels.append(LabelType[label])
        epoch['labels'] = labels

    return user_config
