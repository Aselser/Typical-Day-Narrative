# Audio Recording Paradigm

The **Audio Recording Paradigm** was developed using PsychoPy. It commences with an instructional window, providing guidance on how to proceed. To initiate the recording, press the spacebar. Then, it records audio until spacebar is pressed again. And finally, there is a Thank You Window.

## Interaction with Arduino

Upon both the initiation and termination of the recording, the program sends the character 'P' to an Arduino device. The Arduino processes this character and responds by generating a pulse. This design choice allows the Arduino to be controlled via serial communication from both Python and MATLAB without the need for reprogramming based on the development language.

## Requirements

Before utilizing this paradigm, ensure that you have the necessary requirements in place:

- Python 3.x
- Required Python libraries found in the requirements.txt
- Arduino Uno or a similar device (if applicable)
- Arduino IDE (for uploading code to the Arduino, if needed)

## Usage

1. **Arduino Setup (if applicable):**
   - Connect your Arduino Uno to the USB port of your computer.
   - Upload the provided code located in the `resources` folder to your Arduino using the Arduino IDE. This code allows the Arduino to generate pulses in response to a command.

2. **Python Configuration:**
   - Ensure that the required Python libraries are installed. You can install them using `pip`.
   - In the code component, configure the Arduino port (`puerto_arduino`) and baud rate (`baud_rate`) as per your setup.

3. **Execution:**
   - Run the `diatipico_lastrun.py` file to initiate the paradigm.

4. **Termination:**
   - To stop the recording and pulses, simply terminate the program's execution or follow specific application instructions.

## Contributions

This project is open to contributions and enhancements. If you wish to contribute or report issues, please feel free to open a pull request or issue on GitHub.


## Credits

The Audio Recording Paradigm was developed by Agustina Selser, IT Coordinator of the Cognitive Neuroscience Center at the University of San Andrés, Argentina.
