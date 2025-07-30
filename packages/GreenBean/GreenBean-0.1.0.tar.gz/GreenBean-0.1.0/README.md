# MyLibrary

A simple Python library for multitasking.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [License](#license)

## Installation

To install this library, you can use pip:

```sh
pip install GreenBean
```

## Usage

Here's how you can use the library in your Python scripts:

### Importing the Library

```python
import GreenBean
```

### Usage

```python
filename = "game_data.json"
game_manager = GreenBean(filename)
    
# Load existing data
print("Current game data:", game_manager.data)
    
# Add new data
game_manager.add_data("score", 100)
print("Game data after adding score:", game_manager.data)
    
# Remove data
game_manager.remove_data("score")
print("Game data after removing score:", game_manager.data)
```
## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute.

## Authors

- **Bob Robertson** -
