import re
import builtins

class Ditto:
    ANY = "*"

    def __init__(self):
        # Shared environment for exec
        self.env = {"__builtins__": __builtins__}

    def error(self, code, ctx):
        match code:
            case 1:
                raise TypeError(f"'{ctx['name']}' is not a recognised built-in type")
            case 2:
                raise ValueError(f"Length rule '{ctx['part']}' must be 'min:max' or '*'")
            case 3:
                raise ValueError(f"Expected {ctx['expected_count']} argument(s), got {ctx['actual_count']}")
            case 4:
                expected = ctx.get("exp", ctx.get("expected_count"))
                got_type = type(ctx.get("val", ctx.get("value"))).__name__
                raise TypeError(f"Expected {expected}, got {got_type}")
            case 5:
                raise ValueError(f"Length {ctx['actual_val']} must be between {ctx['start']} and {ctx['stop']}")

    def phrase(self, template):
        rules = []

        def parse_placeholder(match):
            content = match.group(1).strip()

            # Empty braces → accept anything
            if not content:
                rules.append((self.ANY, None))
                return "{}"

            # Split type and length
            parts = [p.strip() for p in content.split(",")[0:2]]
            type_name = parts[0]
            length_part = parts[1] if len(parts) > 1 else self.ANY

            # Determine expected type
            if type_name == self.ANY:
                expected_type = self.ANY
            else:
                expected_type = getattr(builtins, type_name, None)
                if expected_type is None:
                    self.error(1, {"name": type_name})

            # Determine length rule
            if length_part == self.ANY:
                length_rule = None
            elif ":" in length_part:
                start, end = map(int, length_part.split(":"))
                length_rule = range(start, end + 1)
            else:
                self.error(2, {"part": length_part})

            rules.append((expected_type, length_rule))
            return "{}"

        # Preprocess template
        clean_template = re.sub(r"\{([^}]*)\}", parse_placeholder, template)

        def call(*args):
            # Argument count check
            expected_count = len(rules)
            actual_count = len(args)
            if actual_count != expected_count:
                self.error(3, {"expected_count": expected_count, "actual_count": actual_count})

            # Validate each argument
            for value, (expected_type, length_rule) in zip(args, rules):
                try:
                    actual_len = len(value)
                except TypeError:
                    actual_len = len(str(value))

                # Type check
                if expected_type != self.ANY and not isinstance(value, expected_type):
                    self.error(4, {"val": value, "exp": expected_type})

                # Length check
                if length_rule is not None and actual_len not in length_rule:
                    self.error(5, {"actual_val": actual_len, "start": length_rule.start, "stop": length_rule.stop - 1})

            # Execute template in shared environment
            exec(clean_template.format(*args), self.env)

        return call

# Module-level convenience so user calls phrase() directly
_ditto = Ditto()
phrase = _ditto.phrase
