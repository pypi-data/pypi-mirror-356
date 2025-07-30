RemoveBgPlus is a lightweight Python wrapper for the remove.bg API, allowing you to remove image backgrounds using local files, URLs, or base64 input.

## Installation

```bash
pip install RemoveBgPlus
```

## Usage

```python
import removebgplus

client = removebgplus.removebg.RemoveBg("your-api-key")

client.remove(
    url="https://example.com/image.jpg",
    output_path="output.png"
)

client.remove(
    input_path="input.jpg",
    output_path="output.png"
)

client.remove(
    base64_image="iVBORw0KGgoAAAANSUhEUg...",
    output_path="output.png"
)
```

## Features

- Supports file, URL, and base64 input
- Customizable output path (overwrites if not provided)

## License

MIT