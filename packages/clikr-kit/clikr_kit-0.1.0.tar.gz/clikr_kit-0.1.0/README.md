# clikr_kit

**clikr_kit** is a simple Python GUI toolkit designed to help you build clicker-style games using `tkinter`. It provides a single powerful function, `compile_kit`, that builds a clicker window with customizable visuals and behavior in just one call.

## 🔧 Features

- Create a clicker game window in seconds
- Customize button text, colors, fonts, and positions
- Supports fullscreen mode
- Built using the standard `tkinter` module
- No dependencies required

## 🚀 Installation

Once published to PyPI:

```
pip install clikr-kit
```

## 🧪 Example Usage

```python
from clikr_kit import compile_kit

compile_kit(
    button_text="Click Me!",
    x=150, y=200,
    button_bg="lightblue",
    button_fg="black",
    x_1=170, y_1=100,
    label_bg="white",
    label_fg="green",
    bg="white",
    fullscreen=False,
    geo="400x400",
    title="My Clicker Game",
    dev_clicks=0
)
```

## 📦 Planned Features

- Add click sound support
- Add score save/load
- Auto-clicker support
- Theme presets
- PyPI publishing

## 🤖 Requirements

- Python 3.x
- tkinter (included with standard Python)

## 🧑‍💻 Author

Made with ❤️ by [Stup 4400]

## 📄 License

MIT License
