import re
import builtins

def phrase(template):
    rules = []

    def parse_placeholder(match):
        content = match.group(1).strip()
        if not content:
            rules.append((object, None))
            return "{}"

        parts       = content.split(",")
        type_name   = parts[0].strip()
        length_part = parts[1].strip()

        if type_name == '*':
            expected_type = object
        else:
            expected_type = getattr(builtins, type_name, None)
            if expected_type is None:
                raise TypeError(f"'{type_name}' is not a recognised built-in type")

        if length_part == "*":
            length_rule = None
        elif ":" not in length_part:
            raise ValueError(
                f"Length rule '{length_part}' is invalid — "
                f"use 'min:max' format or '*' to skip the length check"
            )
        else:
            start, end = map(int, length_part.split(":"))
            length_rule = range(start, end + 1)

        rules.append((expected_type, length_rule))
        return "{}"

    clean_template = re.sub(r"\{([^}]*)\}", parse_placeholder, template)

    def call(*args):
        for value, (expected_type, length_rule) in zip(args, rules):
            if expected_type is not object and not isinstance(value, expected_type):
                raise TypeError(
                    f"Expected {expected_type.__name__}, got {type(value).__name__}"
                )
            if length_rule is not None:
                actual_len = len(str(value))
                if actual_len not in length_rule:
                    raise ValueError(
                        f"Length {actual_len} must be between "
                        f"{length_rule.start} and {length_rule.stop - 1}"
                    )
        exec(clean_template.format(*args), globals())

    return call
