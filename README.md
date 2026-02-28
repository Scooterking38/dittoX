# 🚀 Ditto.py

**Ditto** is a **Python mini-engine** for generating and executing **dynamic code templates** — fast, readable, and incredibly flexible.  

---

## ✨ Key Features

- 📝 **Dynamic templates** — insert variables, data, or text directly into code blocks.  
- 🔀 **Wildcards & multi-types** — `*` for any type, `[int;float]` for multiple types.  
- ⚡ **Sequential generation** — create `var1…var10`, functions, logs, or repetitive code effortlessly.  
- 💎 **Readable & reusable** — templates clearly separate static text from dynamic values.  

---

## ⚡ Quick Demo

```python
from ditto import phrase

# Dynamic print statements
log = phrase("print('User {} scored {} points')")
log("Alice", 10)
log("Bob", 15)

# Generate sequential variables
v = phrase("var{} = {}")
for i in range(1, 6):
    v(i, i**2)
print(var3)  # 9

# Multi-type & wildcard
g = phrase("process({[int;float],*}, {str,*})")
g(3.14, "data")
```

---

## 🔥 Why Ditto?

Some repetitive Python code is **messy to compress** with loops or functions, especially when:

- Variable names or functions change per line  
- Literal text is mixed with dynamic data  
- You want **executed templates** instead of just strings  

Ditto makes it **easy, readable, and beautiful**.  

---

## ⚡ Installation

```bash
# Just copy ditto.py into your project
```

MIT License
