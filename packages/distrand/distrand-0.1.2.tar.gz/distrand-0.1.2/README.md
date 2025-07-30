# distrand

🎲 Generate random numbers with spacing constraints — no collisions, no clutter.

[![PyPI version](https://img.shields.io/pypi/v/distrand.svg)](https://pypi.org/project/distrand/)
[![License](https://img.shields.io/pypi/l/distrand.svg)](https://github.com/Eggman5800/distrand/blob/main/LICENSE)

## 📦 What is this?

`distrand` lets you generate random numbers (integers or floats) between two bounds, ensuring that all values are **at least `min_dist` apart**.

Perfect for:
- Spaced-out sampling
- Visualization
- Simulation
- Teaching randomness with constraints

## 🔧 Features

- 🧠 Smart spacing — every pair of values ≥ `min_dist`
- 🧮 Supports `int` and `float` generation
- 🚫 Automatically raises `ValueError` if impossible
- ⚡ Fast and NumPy-powered
- 📜 Apache 2.0 licensed

## 🚀 Installation

From [PyPI](https://pypi.org/project/distrand/):
```bash
pip install distrand
```

From source (for development):

```bash
git clone https://github.com/Eggman5800/distrand.git
cd distrand
pip install .
```
## 📚 Usage

```python
from distrand import distrand

# Integer mode
nums = distrand(low=0, high=100, size=5, min_dist=10, dtype=int)

# Float mode
floats = distrand(low=0.0, high=5.0, size=4, min_dist=1.2, dtype=float)
```
🧪 It guarantees that:

- `len(nums) == size`
- `abs(a - b) >= min_dist` for all `a, b` pairs


## 🧪 Testing

Run the tests using `pytest`:

```# Run tests (make sure PYTHONPATH is set to 'src')

# Windows (PowerShell)
$env:PYTHONPATH = "src"
pytest

# Unix/macOS
PYTHONPATH=src pytest

```

Tests cover:

* Integer & float mode
* Invalid inputs (e.g. not enough space)
* Type conversions



## 🧑‍💻 Example Run

```bash
python usage_demo.py
```

Output:

```
🎲 Integer Mode Example:
Generated integers: [10 40 20 60 0]

🌊 Float Mode Example:
Generated floats: [0.   3.6 1.2 2.4]

🚫 Invalid Parameters Example:
Caught expected error: Cannot select 10 values from range [0, 10] with min_dist=5
```

## 🛡️ License

Licensed under the [Apache License 2.0](LICENSE).

## 💡 Credits

Developed by [Syed Talha](https://github.com/Eggman5800).  
Feedback, issues, and pull requests welcome!

## 🌠 Roadmap

- [x] Publish to PyPI
- [ ] Add optional seed parameter (for reproducible results)
- [ ] Support output sorting (`sort=True`)
- [ ] Vectorized float optimization

---

## 🙌 Support

If you find this useful, give the repo a ⭐ or share it.  
Feel free to open [issues](https://github.com/Eggman5800/distrand/issues).
