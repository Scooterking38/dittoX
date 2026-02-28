import re

allowed_types = [str, int, float, list]

class ditto:
    def __init__(self, phrase):
        self.rules = []
        def r(m):
            text = m.group(1).strip()
            if text == "":
                self.rules.append((None,None))
                return "{}"
            t,l = text.split(",")
            self.rules.append((t,l))
            return "{}"
        self.template = re.sub(r"\{([^}]*)\}", r, phrase)

    def __call__(self, *args):
        # find the first arg that is a list to expand
        expanded = None
        new_args = []
        for v in args:
            if isinstance(v, list):
                expanded = v
            else:
                new_args.append(v)

        # if no list, just normal formatting
        if not expanded:
            for v,(t,l) in zip(args,self.rules):
                if t != "*" and not any(isinstance(v,typ) and typ.__name__==t for typ in allowed_types):
                    raise TypeError
            exec(self.template.format(*args))
            return

        # if list, run once per element in the list
        for item in expanded:
            current_args = [item] + new_args
            for v,(t,l) in zip(current_args,self.rules):
                if t != "*" and not any(isinstance(v,typ) and typ.__name__==t for typ in allowed_types):
                    raise TypeError
            exec(self.template.format(*current_args))
