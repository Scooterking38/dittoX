import re
import builtins

ANY = "*"


def phrase(template):
    rules = []

    def parse_placeholder(match):
        content = match.group(1).strip()

        # Empty braces → accept anything
        if not content:
            rules.append((ANY, None))
            return "{}"

        # Split type and length
        parts = [p.strip() for p in content.split(",")[0:2]]
        type_name = parts[0]
        length_part = parts[1] if len(parts) > 1 else ANY

        # Prepare locals for error reporting
        name, part = type_name, length_part

        # Determine expected type
        if type_name == ANY:
            expected_type = ANY
        else:
            expected_type = getattr(builtins, type_name, None)
            if expected_type is None:
                error(1, locals())

        # Determine length rule
        if length_part == ANY:
            length_rule = None
        elif ":" in length_part:
            start, end = map(int, length_part.split(":"))
            length_rule = range(start, end + 1)
        else:
            error(2, locals())

        rules.append((expected_type, length_rule))
        return "{}"

    # Preprocess the template and build rules
    clean_template = re.sub(r"\{([^}]*)\}", parse_placeholder, template)

    def call(*args):
        # Argument count check
        expected_count = len(rules)
        actual_count = len(args)
        if actual_count != expected_count:
            error(3, locals())

        # Unified type and length checks
        for value, (expected_type, length_rule) in zip(args, rules):
            # Determine actual length
            try:
                actual_len = len(value)
            except TypeError:
                actual_len = len(str(value))

            # Type validation
            if expected_type is not ANY and not isinstance(value, expected_type):
                val, exp = value, expected_type
                error(4, locals())

            # Length validation
            if length_rule is not None and actual_len not in length_rule:
                actual_val, start, stop = actual_len, length_rule.start, length_rule.stop - 1
                error(5, locals())

        # Execute the template with validated arguments
        exec(clean_template.format(*args), globals())

    return call


def error(code, ctx):
    match code:
        case 1:
            raise TypeError(f"'{ctx['name']}' is not a recognised built-in type")
        case 2:
            raise ValueError(f"Length rule '{ctx['part']}' must be 'min:max' or '*'")
        case 3:
            raise ValueError(
                f"Expected {ctx['expected_count']} argument(s), got {ctx['actual_count']}"
            )
        case 4:
            expected = ctx.get("exp", ctx.get("expected_count"))
            got_type = type(ctx.get("val", ctx.get("value"))).__name__
            raise TypeError(f"Expected {expected}, got {got_type}")
        case 5:
            raise ValueError(
                f"Length {ctx['actual_val']} must be between {ctx['start']} and {ctx['stop']}"
            )
