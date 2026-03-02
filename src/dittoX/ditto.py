import re
import builtins

class Ditto:

    ANY = '*'

    def __init__(self):
        self.env = {"__builtins__": builtins}
        self.customrules = {}
        self.skip = 0
        
    def error(self, code, mandatory=0, inserts=None):
        inserts = inserts or []
        match mandatory, code:
            # mandatory=0 → always raise
            case 0, 1:
                raise TypeError(f"'{inserts[0]}' is not a recognised built-in type")
            case 0, 2:
                raise ValueError(f"Length rule '{inserts[0]}' must be 'min:max' or '*'")
            case 0, 3:
                raise ValueError(f"Expected {inserts[0]} argument(s), got {inserts[1]}")
            case 0, 4:
                raise ValueError("Must be data in template")
            case 0, 5:
                raise ValueError(f"Length {inserts[0]} must be between {inserts[1]} and {inserts[2]}")
            case 0, 7:
                raise ValueError("Value must fit rule")
            # mandatory=1 → raise only if skip flag is not set
            case 1, 1:
                if not self.skip:
                    raise TypeError(f"Expected {inserts[1]}, got {type(inserts[0]).__name__}")
            case 1, 5:
                if not self.skip:
                    raise ValueError(f"Length {inserts[0]} must be between {inserts[1]} and {inserts[2]}")
            case 1, 7:
                if not self.skip:
                    raise ValueError("Value must fit rule")

    def skipErrors(self):
        self.skip = 1
    
    def customrule(self, name, text):
        func = eval(text)
        self.customrules[name] = func

    def phrase(self, template):
        rules = []

        def parse_placeholder(match):
            content = match.group(1).strip()
            parts = content.split(",") + [self.ANY]*3
            type_name, length_part, custom_part = map(str.strip, parts[:3])
            
            type_name = type_name or self.ANY
            length_part = length_part or self.ANY
            custom_part = custom_part or self.ANY

            if type_name == self.ANY:
                expected_type = self.ANY
            else:
                expected_type = getattr(builtins, type_name, None)
                if expected_type is None:
                    self.error(1, 0, [type_name])

            if length_part == self.ANY:
                length_rule = None
            elif ":" in length_part:
                start, end = map(int, length_part.split(":", 1))
                length_rule = range(start, end + 1)
            else:
                self.error(2, 0, [length_part])

            rules.append((expected_type, length_rule, custom_part))
            return "{}"

        clean_template = re.sub(r"\{([^}]*)\}", parse_placeholder, template)

        def call(*args):
            if len(args) != len(rules):
                self.error(3, 0, [len(rules), len(args)])

            for value, (expected_type, length_rule, custom_part) in zip(args, rules):
                actual_len = len(value) if hasattr(value,'__len__') else len(str(value))

                if expected_type != self.ANY and not isinstance(value, expected_type):
                    self.error(1, 1, [value, expected_type])

                if length_rule is not None and actual_len not in length_rule:
                    self.error(5, 1, [actual_len, length_rule.start, length_rule.stop-1])

                if custom_part != self.ANY:
                    func = self.customrules.get(custom_part)
                    if func is None:
                        raise ValueError(f"Unknown custom rule '{custom_part}'")
                    if func(value) is not True:
                        self.error(7, 1)

            exec(clean_template.format(*args), self.env)
        return call

_ditto = Ditto()
Phrase,Rule,skipErrors = _ditto.phrase,_ditto.customrule,_ditto.skipErrors
