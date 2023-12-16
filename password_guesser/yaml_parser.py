from yaml import safe_load
from functools import partial
from .commons import ManglingEpochType, LabelType
from . import password_rules


def parse_yaml(filename: str):
    with open(filename, "r") as file:
        user_config = safe_load(file)
    
    user_config['mangling_schedule'] = parse_schedule(user_config['mangling_schedule'])
    user_config['pre_generation_schedule'] = parse_schedule(user_config['pre_generation_schedule'])

    return user_config


def parse_schedule(schedule):
    for epoch in schedule:
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

    return schedule


def get_model_props_from_config(filename: str):
    with open(filename, "r") as file:
        user_config = safe_load(file)
    return user_config['std_dev'], user_config['samples_count']