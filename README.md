# Typical Day Paradigm

The **Typical Day Paradigm** was developed using PsychoPy Builder. It is designed to record audio of a patient describing a typical day while they have an implanted iEEG. The paradigm also sends markers to the recording device to coordinate the timing of the signals.

The paradigm follows these steps:
1. **Instructions**: Instructions are presented for testing the pulses.
2. **Pulse Presentation**: 5 pulses are presented with Arduino signals and sound.
3. **Confirmation**: A screen appears to confirm the perception of the pulses.
4. **Instructions**: The paradigm continues with instructions for the patient.
4. **Recording**: The patient's voice is recorded; at least 5 seconds must pass before the spacebar can be pressed to stop the recording.
6. **Acknowledgments**: A thank you screen is displayed at the end.

## Interaction with Arduino
Upon both the initiation and termination of the recording, the program sends the character 'P' to an Arduino device. The Arduino processes this character and responds by generating a pulse. This design choice allows the Arduino to be controlled via serial communication from both Python and MATLAB without the need for reprogramming based on the development language. The paradigm won't work if it can't establish serial communication.

## Requirements

Before utilizing this paradigm, ensure that you have the necessary requirements in place:

- Python 3.x
- Required Python libraries found in the requirements.txt
- Arduino Uno or a similar device
- Arduino IDE (for uploading code to the Arduino, if needed)

## Usage

1. **Arduino Setup (if applicable):**
   - Connect your Arduino Uno to the USB port of your computer.
   - Upload the provided code located in the `resources` folder to your Arduino using the Arduino IDE. This code allows the Arduino to generate pulses in response to a command.

2. **Python Configuration:**
   - Ensure that the required Python libraries are installed. You can install them using
     ```bash
     pip install -r requirements.txt.

   - In the code component (`code`) you can configure baud rate (`baud_rate`) and set the sampling frequency (`sample_rate`) for your microphone (probably won't need it).

3. **Execution:**

   For the typical day narrative in Spanish:
   
   ```bash
   python typicalDayNarrativeSpanish_lastrun.py
   ```
   
      - NOTE: The Psychopy file (.psyexp) was uploaded so you can run it from the builder


## Contributions

This project is open to contributions and enhancements. If you wish to contribute or report issues, please feel free to open a pull request or issue on GitHub.


## Credits

The Audio Recording Paradigm was developed by Agustina Selser, IT Coordinator of the Cognitive Neuroscience Center at the University of San Andrés, Argentina.

## Citations

Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y
