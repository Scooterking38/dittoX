import re
import builtins

class Ditto:
    ANY = "*"

    def __init__(self):
        # shared environment for exec
        self.env = {"__builtins__": __builtins__}
        self.customrules = {}

    def error(self, code, ctx={}):
        match code:
            case 1: raise TypeError(f"'{ctx['name']}' is not a recognised built-in type")
            case 2: raise ValueError(f"Length rule '{ctx['part']}' must be 'min:max' or '*'")
            case 3: raise ValueError(f"Expected {ctx['expected_count']} argument(s), got {ctx['actual_count']}")
            case 4: if not self.skip:
                raise TypeError(
                    f"Expected {ctx.get('exp', ctx.get('expected_count'))}, "
                    f"got {type(ctx.get('val', ctx.get('value'))).__name__}"
                )
            case 5: if not self.skip: raise ValueError(f"Length {ctx['actual_val']} must be between {ctx['start']} and {ctx['stop']}")
            case 6: raise ValueError("Must be data in template")
            case 7: if not self.skip: raise ValueError(f"Value must fit rule")

    def skipErrors(self):
        self.skip = 1
    
    def customrule(self, name, text):
        func = eval(text)
        self.customrules[name] = func

    def phrase(self, template):
        rules = []

        def parse_placeholder(match):
            content = match.group(1).strip()
            if not content:
                rules.append((self.ANY, None, self.ANY))
                return "{}"
            parts = [x.strip() for x in content.split(',')]
            type_name = parts[0]
            length_part = parts[1] if len(parts) > 1 else self.ANY
            custom_part = parts[2] if len(parts) > 2 else self.ANY

            if type_name == self.ANY:
                expected_type = self.ANY
            else:
                expected_type = getattr(builtins, type_name, None)
                if expected_type is None:
                    self.error(1, {"name": type_name})

            if length_part == self.ANY:
                length_rule = None
            elif ":" in length_part:
                start, end = map(int, length_part.split(":", 1))
                length_rule = range(start, end + 1)
            else:
                self.error(2, {"part": length_part})

            rules.append((expected_type, length_rule, custom_part))
            return "{}"

        clean_template = re.sub(r"\{([^}]*)\}", parse_placeholder, template)

        def call(*args):
            if len(args) != len(rules):
                self.error(3, {"expected_count": len(rules), "actual_count": len(args)})

            for value, (expected_type, length_rule, custom_part) in zip(args, rules):
                try:
                    actual_len = len(value)
                except TypeError:
                    actual_len = len(str(value))

                if expected_type != self.ANY and not isinstance(value, expected_type):
                    self.error(4, {"val": value, "exp": expected_type})

                if length_rule is not None and actual_len not in length_rule:
                    self.error(5, {"actual_val": actual_len, "start": length_rule.start, "stop": length_rule.stop - 1})

                if custom_part != self.ANY:
                    func = self.customrules.get(custom_part)
                    if func is None:
                        raise ValueError(f"Unknown custom rule '{custom_part}'")
                    result = func(value)
                    if result is not True:
                        self.error(7, {})

            exec(clean_template.format(*args), self.env)

        return call

_ditto = Ditto()
Phrase = _ditto.phrase
Template = _ditto.customrule
skipErrors = _ditto.skipErrors
