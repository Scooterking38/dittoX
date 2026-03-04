# 🦜 Ditto

Tiny 🐍 Python templating + validation DSL.

---

## 🚀 Quick Example

```python id="q1x9dk"
_ditto = Ditto()
Phrase = _ditto.phrase
Rule = _ditto.customrule

Rule("even", lambda x: x % 2 == 0)
say = Phrase("print({int,1:3,even})")

say(24)  # ✅ OK
```

---

## 📋 Feature Table

| 🧩 Feature             | ✍ Syntax       | ✅ What It Does                    | 📝 Example                 |
| ---------------------- | -------------- | --------------------------------- | -------------------------- |
| Type check             | `{int}`        | Ensures argument is built-in type | `{str}`                    |
| Length rule 📏         | `{str,3:10}`   | Length must be between `min:max`  | `{list,1:5}`               |
| Ignore field           | `*`            | Skips that validation             | `{*,*,rule}`               |
| Custom rule 🔧         | `{int,*,even}` | Runs registered rule              | `Rule("even", fn)`         |
| Arg count check        | Auto           | Args must match placeholders      | —                          |
| Error override ⚠       | `failrule=`    | Custom error handler              | `Phrase(..., failrule=fn)` |
| Executable template 🔥 | `exec()`       | Runs validated template           | `"print({int})"`           |

---

## 🧩 Placeholder Format

```python id="l2z8mw"
{type, min:max, custom_rule}
```

All fields optional. Use `*` to ignore.

---

## ❌ Errors

Raises `ValueError` by default.

```python id="d4k7sq"
def handler(exc):
    print("⚠", exc)
    return False
```

---

## 🔥 Security Warning

Uses `eval()` + `exec()` 💣
**Never use with untrusted input.**

---

🧪 Experimental
🚫 Not production-safe
🛠 Built for DSL exploration
