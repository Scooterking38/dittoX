# ditto.py
import re
from itertools import product

allowed_types = [str, int, float, list]

class ditto:
    def __init__(self, phrase):
        self.rules = []

        def r(m):
            text = m.group(1).strip()
            if not text:
                self.rules.append((object, None))
                return "{}"
            
            parts = [p.strip() for p in text.split(",")]
            if len(parts) == 2:
                t_str, label = parts
                t = next((typ for typ in allowed_types if typ.__name__ == t_str), object)
            else:
                t, label = object, None
            self.rules.append((t, label))
            return "{}"

        self.template = re.sub(r"\{([^}]*)\}", r, phrase)

    def __call__(self, *args):
        lists = [v for v in args if isinstance(v, list)]
        scalars = [v for v in args if not isinstance(v, list)]

        if not lists:
            self._check_types(args)
            print(self.template.format(*args))
            return

        for combo in product(*lists):
            current_args = combo + tuple(scalars)
            self._check_types(current_args)
            print(self.template.format(*current_args))

    def _check_types(self, args):
        for v, (t, _) in zip(args, self.rules):
            if t is object:
                continue
            if not isinstance(v, t):
                raise TypeError(f"Expected type {t.__name__} but got {type(v).__name__}")
