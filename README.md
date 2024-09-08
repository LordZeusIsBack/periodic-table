# Elemental Combinator - Periodic Table

This project is an interactive educational tool named **Elemental Combinator**, designed to teach users about the periodic table of elements by allowing them to combine elements to form compounds. The project combines Python with graphical elements to create a dynamic and engaging experience.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Key Scripts](#key-scripts)
- [Contributing](#contributing)
- [License](#license)

## Overview
The Elemental Combinator project allows users to drag elements into a merge box and visualize the resulting compounds. This interactive experience provides an engaging way to learn about chemistry and the periodic table.

## Features
- **Drag-and-Drop Functionality**: Drag elements into a merge box to combine them.
- **Real-Time Feedback**: Visualize compounds as they are formed.
- **Educational Tool**: Provides information about the elements and their combinations.
- **Customizable Settings**: Adjust configurations to suit your preferences.

## Installation
To run this project, you'll need Python installed along with the required dependencies. You can install the necessary packages using the following command:

```bash
pip install -r requirements.txt


## Usage
1. **Clone the Repository**: Clone this repository to your local machine.
2. **Install Dependencies**: Use the command above to install all necessary dependencies.
3. **Run the Application**: Execute the main script to start the application.

```bash
python main.py
```

## Project Structure
The project includes the following main components:
- **`main.py`**: The main script to run the application.
- **`chemistry_constants.py`**: Contains constants related to the periodic table and chemical elements.
- **`ai_model/`**: Contains the model and session scripts, which handle the logic for combining elements and generating feedback.
- **`config/settings.py`**: Configuration settings for the project.
- **`requirements.txt`**: Lists all required Python libraries.

## Key Scripts
### `main.py`
The main entry point of the application. It initializes the game environment and handles user interactions.

### `chemistry_constants.py`
Defines constants and data related to the elements, such as atomic numbers, symbols, and properties.

### `ai_model/model.py`
Contains the logic for validating and combining elements to form compounds.

### `config/settings.py`
Contains adjustable settings for the application, including visual and operational configurations.

## Contributing
If you wish to contribute to this project, please fork the repository and create a feature branch. Pull requests are welcome!

## License
This project is licensed under the MIT License - see the LICENSE file for more details.
