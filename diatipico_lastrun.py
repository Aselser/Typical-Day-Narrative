#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2023.2.3),
    on octubre 25, 2023, at 11:38
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
prefs.hardware['audioLib'] = 'ptb'
prefs.hardware['audioLatencyMode'] = '3'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.tools import environmenttools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER, priority)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

# Run 'Before Experiment' code from code
import sounddevice as sd
import soundfile as sf
import threading
import time
from psychopy import core, event
#from pyfirmata import Arduino
from queue import Queue
from time import sleep
import serial

# Connecting to the board
puerto_arduino='COM16'
baud_rate=115200

# Variable para rastrear si estamos grabando
recording = False
sample_rate = 44100  # Sample rate (adjust as needed)


class Grabadora:
    def __init__(self, filepath, mic_id, sample_rate, channels, arduino_port, baud_rate):
        self.filepath = filepath
        self.mic_id = mic_id
        self.SAMPLE_RATE = sample_rate
        self.CHANNELS = channels
        self.mic_queue = Queue()
        self.recording = False
        self.stop_requested = False  # Variable de bandera para detener la grabación
        
        # Conectar a la placa Arduino
        # Configura la comunicación serie
        self._serial = serial.Serial(arduino_port, baud_rate)  # Reemplaza 'COM3' por el puerto serie correcto
        

    def callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        if self.recording:
            self.mic_queue.put(indata.copy())

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.enviarMarca()  # Llama a enviarMarca al inicio de la grabación
            self.mic_queue = Queue()  # Reinicia la cola
            self.recording_thread = threading.Thread(target=self._record)
            self.recording_thread.start()

    def stop_recording(self):
        if self.recording:
            self.stop_requested = True  # Establece la bandera de detención
            self.enviarMarca()
            

    def enviarMarca(self):
        # Mensaje a enviar a Arduino
        mensaje = "P"
        # Envía el mensaje a Arduino
        self._serial.write(mensaje.encode())
        
    
    def _record(self):
        with sf.SoundFile(self.filepath, mode='x', samplerate=self.SAMPLE_RATE, channels=self.CHANNELS, subtype=None) as file:
            with sd.InputStream(samplerate=self.SAMPLE_RATE, device=self.mic_id, channels=self.CHANNELS, callback=self.callback):
                try:
                    while not self.stop_requested:  # Verifica si se solicitó la detención
                        file.write(self.mic_queue.get())

                except RuntimeError as re:
                    print(f"{re}. If recording was stopped by the user, then this can be ignored")
                finally:
                    self.recording = False  # Asegura que la grabación se marque como detenida

# --- Setup global variables (available in all functions) ---
# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# Store info about the experiment session
psychopyVersion = '2023.2.3'
expName = 'diatipico'  # from the Builder filename that created this script
expInfo = {
    'Nombre': '',
    'Edad': '',
    'Lateralidad': ['Izquierda', 'Derecha'],
    'date': data.getDateStr(),  # add a simple timestamp
    'expName': expName,
    'psychopyVersion': psychopyVersion,
}


def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # temporarily remove keys which the dialog doesn't need to show
    poppedKeys = {
        'date': expInfo.pop('date', data.getDateStr()),
        'expName': expInfo.pop('expName', expName),
        'psychopyVersion': expInfo.pop('psychopyVersion', psychopyVersion),
    }
    # show participant info dialog
    dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # restore hidden keys
    expInfo.update(poppedKeys)
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = f'%s_data/%s_%s/%s_%s' % (expName, expInfo['Nombre'], expInfo['date'], expInfo['Nombre'], expInfo['date'])
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath='C:\\Users\\agust\\OneDrive\\Desktop\\CNC\\Paradigma_dia_tipico\\diatipico_lastrun.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # this outputs to the screen, not a file
    logging.console.setLevel(logging.EXP)
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log', level=logging.EXP)
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=[1536, 864], fullscr=True, screen=0,
            winType='pyglet', allowStencil=False,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height'
        )
        if expInfo is not None:
            # store frame rate of monitor if we can measure it
            expInfo['frameRate'] = win.getActualFrameRate()
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0,0,0]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    win.mouseVisible = False
    win.hideMessage()
    return win


def setupInputs(expInfo, thisExp, win):
    """
    Setup whatever inputs are available (mouse, keyboard, eyetracker, etc.)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    dict
        Dictionary of input devices by name.
    """
    # --- Setup input devices ---
    inputs = {}
    ioConfig = {}
    
    # Setup iohub keyboard
    ioConfig['Keyboard'] = dict(use_keymap='psychopy')
    
    ioSession = '1'
    if 'session' in expInfo:
        ioSession = str(expInfo['session'])
    ioServer = io.launchHubServer(window=win, **ioConfig)
    eyetracker = None
    
    # create a default keyboard (e.g. to check for escape)
    defaultKeyboard = keyboard.Keyboard(backend='iohub')
    # return inputs dict
    return {
        'ioServer': ioServer,
        'defaultKeyboard': defaultKeyboard,
        'eyetracker': eyetracker,
    }

def pauseExperiment(thisExp, inputs=None, win=None, timers=[], playbackComponents=[]):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    inputs : dict
        Dictionary of input devices by name.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    playbackComponents : list, tuple
        List of any components with a `pause` method which need to be paused.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # pause any playback components
    for comp in playbackComponents:
        comp.pause()
    # prevent components from auto-drawing
    win.stashAutoDraw()
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # make sure we have a keyboard
        if inputs is None:
            inputs = {
                'defaultKeyboard': keyboard.Keyboard(backend='ioHub')
            }
        # check for quit (typically the Esc key)
        if inputs['defaultKeyboard'].getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win, inputs=inputs)
        # flip the screen
        win.flip()
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, inputs=inputs, win=win)
    # resume any playback components
    for comp in playbackComponents:
        comp.play()
    # restore auto-drawn components
    win.retrieveAutoDraw()
    # reset any timers
    for timer in timers:
        timer.reset()


def run(expInfo, thisExp, win, inputs, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    inputs : dict
        Dictionary of input devices by name.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = inputs['ioServer']
    defaultKeyboard = inputs['defaultKeyboard']
    eyetracker = inputs['eyetracker']
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    
    # --- Initialize components for Routine "Instrucciones" ---
    texto_instrucciones = visual.TextStim(win=win, name='texto_instrucciones',
        text='A continuación, te pedimos que nos cuentes un día típico. Espera a que aparezca el microfono para empezar a hablar.\n\nPulse ESPACIO para empezar a grabar y ESPACIO nuevamente cuando termines.',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    start_rec = keyboard.Keyboard()
    
    # --- Initialize components for Routine "Respuesta" ---
    image = visual.ImageStim(
        win=win,
        name='image', 
        image='microphone-png-16.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), size=(0.5, 0.5),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    # Run 'Begin Experiment' code from code
    output_filename = f'%s_data/%s_%s/%s_%s.wav' % (expName, expInfo['Nombre'],
        expInfo['date'], expInfo['Nombre'], expInfo['date'])  # Output file name
    
    # Crear una instancia de la grabadora con los parámetros adecuados
    mi_grabadora = Grabadora(filepath=output_filename, mic_id=0, 
        sample_rate=sample_rate, channels=1, arduino_port=puerto_arduino, baud_rate=baud_rate)
    stop_rec = keyboard.Keyboard()
    
    # --- Initialize components for Routine "Agradecimiento" ---
    text = visual.TextStim(win=win, name='text',
        text='¡Muchas gracias por participar!\n\nPresion ESPACIO para terminar el experimento',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    exit_exp = keyboard.Keyboard()
    
    # create some handy timers
    if globalClock is None:
        globalClock = core.Clock()  # to track the time since experiment started
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6)
    
    # --- Prepare to start Routine "Instrucciones" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('Instrucciones.started', globalClock.getTime())
    start_rec.keys = []
    start_rec.rt = []
    _start_rec_allKeys = []
    # keep track of which components have finished
    InstruccionesComponents = [texto_instrucciones, start_rec]
    for thisComponent in InstruccionesComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Instrucciones" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *texto_instrucciones* updates
        
        # if texto_instrucciones is starting this frame...
        if texto_instrucciones.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            texto_instrucciones.frameNStart = frameN  # exact frame index
            texto_instrucciones.tStart = t  # local t and not account for scr refresh
            texto_instrucciones.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(texto_instrucciones, 'tStartRefresh')  # time at next scr refresh
            # update status
            texto_instrucciones.status = STARTED
            texto_instrucciones.setAutoDraw(True)
        
        # if texto_instrucciones is active this frame...
        if texto_instrucciones.status == STARTED:
            # update params
            pass
        
        # *start_rec* updates
        
        # if start_rec is starting this frame...
        if start_rec.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            start_rec.frameNStart = frameN  # exact frame index
            start_rec.tStart = t  # local t and not account for scr refresh
            start_rec.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(start_rec, 'tStartRefresh')  # time at next scr refresh
            # update status
            start_rec.status = STARTED
            # keyboard checking is just starting
            start_rec.clock.reset()  # now t=0
            start_rec.clearEvents(eventType='keyboard')
        if start_rec.status == STARTED:
            theseKeys = start_rec.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _start_rec_allKeys.extend(theseKeys)
            if len(_start_rec_allKeys):
                start_rec.keys = _start_rec_allKeys[-1].name  # just the last key pressed
                start_rec.rt = _start_rec_allKeys[-1].rt
                start_rec.duration = _start_rec_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, inputs=inputs, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in InstruccionesComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Instrucciones" ---
    for thisComponent in InstruccionesComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('Instrucciones.stopped', globalClock.getTime())
    # check responses
    if start_rec.keys in ['', [], None]:  # No response was made
        start_rec.keys = None
    thisExp.addData('start_rec.keys',start_rec.keys)
    if start_rec.keys != None:  # we had a response
        thisExp.addData('start_rec.rt', start_rec.rt)
        thisExp.addData('start_rec.duration', start_rec.duration)
    thisExp.nextEntry()
    # the Routine "Instrucciones" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "Respuesta" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('Respuesta.started', globalClock.getTime())
    # Run 'Begin Routine' code from code
    # Iniciar la grabación
    mi_grabadora.start_recording()
    
    stop_rec.keys = []
    stop_rec.rt = []
    _stop_rec_allKeys = []
    # keep track of which components have finished
    RespuestaComponents = [image, stop_rec]
    for thisComponent in RespuestaComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Respuesta" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *image* updates
        
        # if image is starting this frame...
        if image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            image.frameNStart = frameN  # exact frame index
            image.tStart = t  # local t and not account for scr refresh
            image.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(image, 'tStartRefresh')  # time at next scr refresh
            # update status
            image.status = STARTED
            image.setAutoDraw(True)
        
        # if image is active this frame...
        if image.status == STARTED:
            # update params
            pass
        
        # *stop_rec* updates
        
        # if stop_rec is starting this frame...
        if stop_rec.status == NOT_STARTED and t >= 5.0-frameTolerance:
            # keep track of start time/frame for later
            stop_rec.frameNStart = frameN  # exact frame index
            stop_rec.tStart = t  # local t and not account for scr refresh
            stop_rec.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stop_rec, 'tStartRefresh')  # time at next scr refresh
            # update status
            stop_rec.status = STARTED
            # keyboard checking is just starting
            stop_rec.clock.reset()  # now t=0
            stop_rec.clearEvents(eventType='keyboard')
        if stop_rec.status == STARTED:
            theseKeys = stop_rec.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _stop_rec_allKeys.extend(theseKeys)
            if len(_stop_rec_allKeys):
                stop_rec.keys = _stop_rec_allKeys[-1].name  # just the last key pressed
                stop_rec.rt = _stop_rec_allKeys[-1].rt
                stop_rec.duration = _stop_rec_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, inputs=inputs, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in RespuestaComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Respuesta" ---
    for thisComponent in RespuestaComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('Respuesta.stopped', globalClock.getTime())
    # Run 'End Routine' code from code
    mi_grabadora.stop_recording()
    
    # check responses
    if stop_rec.keys in ['', [], None]:  # No response was made
        stop_rec.keys = None
    thisExp.addData('stop_rec.keys',stop_rec.keys)
    if stop_rec.keys != None:  # we had a response
        thisExp.addData('stop_rec.rt', stop_rec.rt)
        thisExp.addData('stop_rec.duration', stop_rec.duration)
    thisExp.nextEntry()
    # the Routine "Respuesta" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "Agradecimiento" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('Agradecimiento.started', globalClock.getTime())
    exit_exp.keys = []
    exit_exp.rt = []
    _exit_exp_allKeys = []
    # keep track of which components have finished
    AgradecimientoComponents = [text, exit_exp]
    for thisComponent in AgradecimientoComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Agradecimiento" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text* updates
        
        # if text is starting this frame...
        if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text.frameNStart = frameN  # exact frame index
            text.tStart = t  # local t and not account for scr refresh
            text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
            # update status
            text.status = STARTED
            text.setAutoDraw(True)
        
        # if text is active this frame...
        if text.status == STARTED:
            # update params
            pass
        
        # *exit_exp* updates
        
        # if exit_exp is starting this frame...
        if exit_exp.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            exit_exp.frameNStart = frameN  # exact frame index
            exit_exp.tStart = t  # local t and not account for scr refresh
            exit_exp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(exit_exp, 'tStartRefresh')  # time at next scr refresh
            # update status
            exit_exp.status = STARTED
            # keyboard checking is just starting
            exit_exp.clock.reset()  # now t=0
            exit_exp.clearEvents(eventType='keyboard')
        if exit_exp.status == STARTED:
            theseKeys = exit_exp.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _exit_exp_allKeys.extend(theseKeys)
            if len(_exit_exp_allKeys):
                exit_exp.keys = _exit_exp_allKeys[-1].name  # just the last key pressed
                exit_exp.rt = _exit_exp_allKeys[-1].rt
                exit_exp.duration = _exit_exp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, inputs=inputs, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in AgradecimientoComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Agradecimiento" ---
    for thisComponent in AgradecimientoComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('Agradecimiento.stopped', globalClock.getTime())
    # check responses
    if exit_exp.keys in ['', [], None]:  # No response was made
        exit_exp.keys = None
    thisExp.addData('exit_exp.keys',exit_exp.keys)
    if exit_exp.keys != None:  # we had a response
        thisExp.addData('exit_exp.rt', exit_exp.rt)
        thisExp.addData('exit_exp.duration', exit_exp.duration)
    thisExp.nextEntry()
    # the Routine "Agradecimiento" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    # Run 'End Experiment' code from code
    # Cierra la conexión serie
    mi_grabadora._serial.close()
    try:
        # Detener la grabación
        mi_grabadora.stop_recording()
        print("Grabación detenida.")
    except:
        pass
    
    # mark experiment as finished
    endExperiment(thisExp, win=win, inputs=inputs)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, inputs=None, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    inputs : dict
        Dictionary of input devices by name.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # mark experiment handler as finished
    thisExp.status = FINISHED
    # shut down eyetracker, if there is one
    if inputs is not None:
        if 'eyetracker' in inputs and inputs['eyetracker'] is not None:
            inputs['eyetracker'].setConnectionState(False)
    logging.flush()


def quit(thisExp, win=None, inputs=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    inputs : dict
        Dictionary of input devices by name.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    if inputs is not None:
        if 'eyetracker' in inputs and inputs['eyetracker'] is not None:
            inputs['eyetracker'].setConnectionState(False)
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    inputs = setupInputs(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win, 
        inputs=inputs
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win, inputs=inputs)
