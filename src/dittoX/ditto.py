import re, builtins
class Ditto:
    ANY = '*'
    def __init__(self): self.env, self.customrules = {"__builtins__": builtins}, {}
    def error(self, code, mandatory=0, inserts=None, failrule=None):
        inserts = inserts or []
        mismatch = [
            f"Expected {inserts[1]}, got {type(inserts[0]).__name__}",
            f"Length {inserts[0]} must be between {inserts[1]} and {inserts[2]}",
            "Value must fit rule"]
        error = [
            f"'{inserts[0]}' is not a recognised built-in type",
            f"Length rule '{inserts[0]}' must be 'min:max' or '*'",
            f"Expected {inserts[0]} argument(s), got {inserts[1]}",
            "Must be data in template",
            f"Length {inserts[0]} must be between {inserts[1]} and {inserts[2]}",
            "Value must fit rule"]
        message = mismatch[code] if mandatory == 0 else error[code]
        exc = ValueError(message)
    
        if failrule: if failrule(exc) is False: return
        else: raise exc

    def customrule(self, name, text): self.customrules[name] = eval(text) if isinstance(text, str) else text
    def phrase(self, template, failrule=None):
        rules = []
    
        def parse_placeholder(match):
            type_name, length_part, custom_part = [x.strip() for x in (match.group(1).strip().split(",") + [self.ANY]*3)][:3]
            type_name = type_name or self.ANY
            length_part = length_part or self.ANY
            custom_part = custom_part or self.ANY
    
            if type_name == self.ANY: expected_type = self.ANY
            else:
                expected_type = getattr(builtins, type_name, None)
                if expected_type is None: self.error(0, 1, [type_name], failrule)
                    
            if length_part == self.ANY: length_rule = None
            elif ":" in length_part:
                start, end = map(int, length_part.split(":", 1))
                length_rule = range(start, end + 1)
            else: self.error(1, 1, [length_part], failrule)
    
            rules.append((expected_type, length_rule, custom_part))
            return "{}"
    
        clean_template = re.sub(r"\{([^}]*)\}", parse_placeholder, template)
        
        def call(*args):
            if len(args) != len(rules): self.error(2, 1, [len(rules), len(args)], failrule)
            for value, (expected_type, length_rule, custom_part) in zip(args, rules):
    
                actual_len = len(value) if hasattr(value,'__len__') else len(str(value))
    
                if expected_type != self.ANY and not isinstance(value, expected_type):
                    self.error(0, 0, [value, expected_type.__name__], failrule)
    
                if length_rule is not None and actual_len not in length_rule:
                    self.error(1, 0, [actual_len, length_rule.start, length_rule.stop-1], failrule)
    
                if custom_part != self.ANY:
                    func = self.customrules.get(custom_part)
                    if func is None: raise ValueError(f"Unknown custom rule '{custom_part}'")
                    if func(value) is not True: self.error(2, 0, [value, custom_part], failrule)
    
            exec(clean_template.format(*args), self.env)
        return call
_ditto = Ditto()
Phrase, Rule = _ditto.phrase, _ditto.customrule
