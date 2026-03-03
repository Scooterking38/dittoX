<!-- ===================================================== -->
<!--                    🧬 DITTO ENGINE                     -->
<!-- ===================================================== -->

<h1 align="center">
  <span style="color:#7C3AED;">Ditto</span>
</h1>

<p align="center">
  <b style="color:#22D3EE;">Tiny</b> • 
  <b style="color:#A3E635;">Expressive</b> • 
  <b style="color:#F472B6;">Rule-Driven</b> • 
  <b style="color:#FACC15;">Template Execution</b>
</p>

<p align="center">
  <i>A lightweight Python templating engine with built-in validation and custom rules.</i>
</p>

---

## ✨ What is Ditto?

**Ditto** lets you write small executable templates that:

✅ Accept typed arguments  
✅ Validate lengths  
✅ Enforce custom rules  
✅ Execute formatted Python code  
✅ Stay compact and readable  

Think:

> *“Format strings + validation + execution = one clean call.”*

---

## 🎯 Quick Example

```python
from ditto import Phrase, Rule

Rule("is_even", "lambda x: x % 2 == 0")

hello = Phrase("""
print("User:", {})
print("Score:", {})
""")

hello("Alice", 42)
```

---

## 🧠 Core Idea

### Template → Rules → Callable → Execute

```text
"{type, length, rule}"
```

Each `{}` becomes:

```
(type, length constraint, custom rule)
```

Then:

```python
Phrase(template)(args...)
```

---

## 📦 Installation

Just drop the file in your project:

```bash
ditto.py
```

No dependencies. Pure stdlib.

---

## 🚀 Usage

### 1️⃣ Create a phrase

```python
say = Phrase('print("Hello", {})')
say("world")
```

---

### 2️⃣ Add type checking

```python
say = Phrase('print({int})')
say(10)      # ✅
say("10")    # ❌ TypeError
```

---

### 3️⃣ Length rules

```python
Phrase('print({str,3:6})')("hello")
```

Allowed:

```
length 3 → 6
```

Wildcard:

```
*
```

---

### 4️⃣ Custom rules

```python
Rule("positive", lambda x: x > 0)

test = Phrase("print({int,*,positive})")
test(5)   # ✅
test(-1)  # ❌
```

---

## 🧩 Placeholder Syntax

```text
{ type , length , custom }
```

All parts optional.

| Part | Meaning | Example |
|-------|-----------|-------------|
| type | built-in type | `int` |
| length | range | `3:8` |
| custom | rule name | `positive` |
| any | wildcard | `*` |

---

### Examples

```python
{}
{int}
{str,5:10}
{int,*,positive}
{*,3:6,*}
```

---

## 🛠 API

### Phrase(template)

Compiles a template into a callable.

```python
run = Phrase("print({})")
run("hi")
```

---

### Rule(name, func)

Register validation rules.

```python
Rule("even", lambda x: x % 2 == 0)
```

---

### skipErrors()

Suppress non-mandatory errors.

```python
skipErrors()
```

Useful when skipping invalid insertions.

---

## ⚡ How It Works

### Step 1
Regex extracts `{placeholders}`

### Step 2
Each placeholder becomes:

```python
(expected_type, length_range, custom_rule)
```

### Step 3
Arguments validated

### Step 4
Template executed with:

```python
exec(...)
```

---

## 🎨 Design Goals

- 🧼 minimal syntax
- ⚡ fast setup
- 🧠 expressive rules
- 🪶 zero dependencies
- 🔧 hackable core

---

## 🔍 Why Use Ditto?

Instead of:

```python
if not isinstance(x, int): ...
if len(x) < 3 or len(x) > 8: ...
if not rule(x): ...
```

You write:

```python
"{int,3:8,myrule}"
```

Cleaner. Smaller. Reusable.

---

## 💡 Patterns

### Generate variables

```python
Phrase("a={}, b={}, print(a+b)")(3, 4)
```

---

### Quick validation

```python
Phrase("pass")("text")
```

Use just for checking.

---

### Mini DSL

Build small structured commands with rules.

---

## 📁 File Layout

```text
ditto.py
```

Single file. Nothing else.

---

## ⚠️ Notes

- Uses `exec()` → trusted input only
- Types must be built-ins
- Custom rules must return `True`

---

## 🧪 Mini Playground

```python
Rule("short", lambda s: len(s) < 5)

demo = Phrase("""
print("Name:", {})
print("Age:", {})
""")

demo("Eli", 13)
```

---

## 🌈 Philosophy

> Tiny tools > big frameworks

Ditto keeps logic:
- visible
- explicit
- composable

No magic. Just clean mechanics.

---

## 📜 License

MIT — use freely, modify freely.

---

<p align="center">
  <b style="color:#7C3AED;">Made for builders who like small, sharp tools.</b>
</p>
