# Audio Recording Paradigm

The **Audio Recording Paradigm** was developed using PsychoPy and then modified in order to store the data as a simple .csv in one line. It starts with an instructional window, providing guidance on how to proceed. To initiate the recording, press the spacebar. Then, it records audio until the spacebar is pressed again. And finally, there is a Thank You Window.

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
   - Ensure that the required Python libraries are installed. You can install them using
     ```bash
     pip install -r requirements.txt.

   - In the code component or the script file, configure the Arduino port (`port`) and baud rate (`baud_rate`) as per your setup, and set the sampling frequency for your microphone.

3. **Execution:**

   For the typical day narrative in English:
      
   ```bash
   python typicalDayNarrative_script.py
   ```
   
   For the typical day narrative in Spanish:
   
   ```bash
   python typicalDayNarrativeSpanish_script.py
   ```
   
      - NOTE: The Psychopy file (.psyexp) was uploaded as an example, it does not save the .csv or the log data


## Contributions

This project is open to contributions and enhancements. If you wish to contribute or report issues, please feel free to open a pull request or issue on GitHub.


## Credits

The Audio Recording Paradigm was developed by Agustina Selser, IT Coordinator of the Cognitive Neuroscience Center at the University of San Andrés, Argentina.

## Citations

Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y
