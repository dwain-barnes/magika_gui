# Magika GUI by EryriLabs

Magika GUI is a simple user-friendly interface for interacting with the Magika CLI, Google’s AI-powered file-type identification system. It allows users to easily select files or directories and set various options for file analysis without needing to use the command line.

Here's a screenshot of the GUI in action:

[GUI Example](/assets/screenshot.png)


## Features

- File and Folder Browsing: Easily select the files or directories you want to analyze.
- Configurable Options: Set options such as recursive analysis, output format (JSON, JSONL), MIME type, and more directly from the GUI.
- Save Output: Conveniently save the analysis output to a file, with support for different formats based on your output settings.

## Installation

To use Magika GUI, you need to have Python installed on your system. It's recommended to use a virtual environment.

### Steps:

1. Clone this repository or download the source code.
2. Navigate to the project directory.
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```
Run the application:
```bash
python magika_gui.py
```

## Usage

1. Start the application using the command mentioned above.
2. Use the "Browse" button to select the file or directory you want to analyze.
3. Choose your desired options.
4. Click "Run Magika" to start the analysis.
5. After the analysis is complete, you can save the output using the "Save Output" button.

## License

This project is open-sourced under the MIT License. See the LICENSE file for more details.

## Contributions

Contributions are welcome! Please open an issue or submit a pull request for any bugs, features, or improvements.

## Contact

For any queries, please reach out to [queries@eryrilabs.com](mailto:queries@eryrilabs.com).

## Additional Information 

This is a GUI for Magika. For more inforamtion on Magika visit https://github.com/google/magika

```bibtex
@software{magika,
  author = {Fratantonio, Yanick and Bursztein, Elie and Invernizzi, Luca and Zhang, Marina and Metitieri, Giancarlo and Kurt, Thomas and Galilee, Francois and Petit-Bianco, Alexandre and Farah, Loua and Albertini, Ange},
  title = {{Magika content-type scanner}},
  url = {https://github.com/google/magika}
}

