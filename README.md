# QuickDraw App

QuickDraw is a reference image viewer application designed for artists and creators who need to reference a variety of images in a timed manner. It allows users to load images from their directories, display them in fullscreen, and cycle through them for a set amount of time.

## Features

- Load images from any directory.
- Set the display time for each image.
- Fullscreen mode for distraction-free viewing.
- Pause, previous, and next controls for image navigation.
- Ability to save and load session configurations.
- Session logs that track time spent on each image.
- Customizable image display time and session names.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need Python installed on your system to run the QuickDraw app. You can download Python from [here](https://www.python.org/downloads/).

### Installing

1. Clone the repository or download the ZIP file and extract it.
2. Navigate to the project directory.
3. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Run the application:

    ```sh
    python QuickDraw.py
    ```

### Usage

1. Start the application using the command above.
2. Use the '+' button to add directories containing images you wish to view.
3. Set the time you want each image to be displayed.
4. Click 'Start Session' to begin cycling through the images.
5. You can pause and navigate through the images using the controls provided.

## Building the Application

To build the QuickDraw app into a standalone executable:

1. Activate your virtual environment.
2. Install PyInstaller:

    ```sh
    pip install pyinstaller
    ```

3. Run PyInstaller:

    ```sh
    pyinstaller --onefile --windowed QuickDraw.py
    ```

4. Find the built executable in the `dist` directory.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

- Erik Iuhas - *Initial work* - [Erik-Iuhas](https://github.com/Erik-Iuhas)

See also the list of [contributors](https://github.com/Erik-Iuhas/QuickDraw/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

- Hat tip to anyone whose code was used
- Inspiration
- etc
