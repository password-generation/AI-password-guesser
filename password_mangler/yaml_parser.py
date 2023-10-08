import yaml
import password_rules


def parse_yaml(filename):
    with open(filename, "r") as file:
        rules = yaml.safe_load(file)

    unary_names, binary_names = rules["unary_rules"], rules["binary_rules"]

    unary, binary = get_funcs(unary_names), get_funcs(binary_names)

    return unary, binary


def get_funcs(names, module=password_rules):
    funcs = []
    for name in names:
        func = getattr(module, name)
        funcs.append(func)
    return funcs


if __name__ == "__main__":
    unary, binary = parse_yaml("config.yaml")
    print(unary, binary)

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
