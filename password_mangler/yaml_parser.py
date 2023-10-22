import yaml
from commons import ManglingEpochType
import password_rules


def parse_yaml(filename):
    with open(filename, "r") as file:
        rules = yaml.safe_load(file)

    unary_names, binary_names, mangling_schedule = (
        rules["unary_rules"],
        rules["binary_rules"],
        rules["mangling_schedule"],
    )

    unary, binary = (
        get_funcs(unary_names),
        get_funcs(binary_names),
    )

    schedule = get_schedule(mangling_schedule)

    return unary, binary, schedule


def get_schedule(names):
    schedule = []
    for name in names:
        if name == "unary":
            schedule.append(ManglingEpochType.UNARY)
        elif name == "binary":
            schedule.append(ManglingEpochType.BINARY)

        # TODO handling other cases

    return schedule


def get_funcs(names, module=password_rules):
    funcs = []
    for name in names:
        func = getattr(module, name)
        funcs.append(func)
    return funcs


if __name__ == "__main__":
    unary, binary, schedule = parse_yaml("config.yaml")
    print(unary, binary, schedule)

    print("--- unary ---")
    s1 = "p@ssW0rD"
    s2 = "ha$eLko"
    for u in unary:
        s1 = u(s1)
        print(s1)

    print("--- binary ---")
    double = ""
    for b in binary:
        double = b(s1, s2)
        print(double)
