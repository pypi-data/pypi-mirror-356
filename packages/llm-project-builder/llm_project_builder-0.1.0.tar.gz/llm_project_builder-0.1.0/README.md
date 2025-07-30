CapOv — Captain Obvious

Fixes the dumbest, most obvious Python code errors automatically.

CapOv corrects only the 100% safe stuff: missing imports, duplicate imports, unclosed brackets, and more — with zero assumptions.

---

🔧 Installation

    pip install capov

---

🚀 Example usage

    from capov.fixers import process

    code = '''
    import os
    import os
    x = [1, 2, 3,
    print(json.dumps(x)
    '''

    fixed = process(code)
    print(fixed)

Command-line:

    python -m capov your_script.py [options]

Options:
- --in-place → Overwrite the input file
- --output FILENAME → Write fixed code to a separate file
- --backup → Create a .bak backup before overwrite
- --verbose → Print debug messages
- --log FILE → Log to specified log file

---

🧪 Run tests

To verify installation and test functionality:

    python3 -m capov.tests

---

🗂 Project structure

- capov/ — main package
  - fixers.py — bug fixing logic
  - __main__.py — CLI entry point
  - example.py — example usage
  - tests/
    - test_cli_full.py — full run tests
    - test_cli_params.py — CLI parameter tests
    - test_module_usage.py — module usage tests
    - faulty_scripts/ — broken Python samples

---

CapOv is your cleanup butler. Let him sweep the dumb bugs so you don't have to.

Submit bugs or contribute: https://github.com/HansPeterRadtke/capov
