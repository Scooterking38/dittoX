# ditto.py

`ditto.py` is a minimal builder-style template executor for Python.
It allows you to define a template with placeholders (`{}`) and rules for type and length, then dynamically insert values and execute Python code.

---

## Features

- Template strings with `{type,length}` placeholders
- Type and length validation
- Optional skipping of type/length checks using `*`
- Simple execution using `exec`
- Supports passing lists to expand over multiple values

---

## Installation

You can simply download `ditto.py` and import it in your project:

from ditto import ditto

No dependencies besides Python 3.8+.

---

## Usage

### Basic Example

from ditto import ditto

d = ditto("{str,5:7} = {}")
d("hello", "5**2")

print(hello)  # 25

### Skipping Checks with `*`

d = ditto("{*,3:4} = {}")
d([1,2,3], "sum([1,2,3])")  # type ignored, length checked

### Type Validation Against Allowed Types

from ditto import allowed_types
allowed_types  # e.g., [str, int, float, list]

- The type in `{}` must be in allowed_types unless you use `*`.

---

## Template Rules

- `{type,length}`  
  - `type` = type name (str, int, float, list)  
  - `length` = exact number (e.g., 5) or range (e.g., 2:7)  
  - Use `*` to skip a check  

- `{}` placeholders in the template are replaced in order with the arguments you pass when calling the `ditto` object.

---

## Example with List Expansion

d = ditto("var{} = {}")
d(["x", "y", "z"], "5**2")

print(x)  # 25
print(y)  # 25
print(z)  # 25

- Passing a list will execute the template for each element of the list.

---

## Notes

- Minimal, safe usage relies on controlling your template and arguments.  
- Designed for learning and simple dynamic template execution.  

---

## License

MIT
