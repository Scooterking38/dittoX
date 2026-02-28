import re
import builtins

ANY = "*"

def phrase(template):
    rules = []

    def parse_placeholder(match):
        content = match.group(1).strip()
        if not content:
            rules.append((ANY, None))
            return "{}"
        content = content.split(',')[0:2]
        type_name, length_part = [p.strip() for p in content]

        if type_name == "*":
            expected_type = ANY
        else:
            expected_type = getattr(builtins, type_name, None)
            if expected_type is None:
                error(1, type_name)

        if length_part == "*":
            length_rule = None
        elif ":" in length_part:
            start, end = length_part.split(":")
            length_rule = range(int(start), int(end) + 1)
        else:
            error(2, length_part)

        rules.append((expected_type, length_rule))
        return "{}"

    clean_template = re.sub(r"\{([^}]*)\}", parse_placeholder, template)

    def call(*args):
        if len(args) != len(rules):
            error(3, len(rules), len(args))

        for value, (expected_type, length_rule) in zip(args, rules):
            if expected_type is not ANY and not isinstance(value, expected_type):
                error(4, expected_type.__name__, type(value).__name__)
            if length_rule is not None:
                actual_len = len(value) if hasattr(value, "__len__") else len(str(value))
                if actual_len not in length_rule:
                    error(5, actual_len, length_rule.start, length_rule.stop - 1)

        exec(clean_template.format(*args), globals())

    return call

def error(code, *args):
    match code:
        case 1: raise TypeError(f"'{args[0]}' is not a recognised built-in type")
        case 2: raise ValueError(f"Length rule '{args[0]}' must be 'min:max' or '*'")
        case 3: raise ValueError(f"Expected {args[0]} argument(s), got {args[1]}")
        case 4: raise TypeError(f"Expected {args[0]}, got {args[1]}")
        case 5: raise ValueError(f"Length {args[0]} must be between {args[1]} and {args[2]}")
