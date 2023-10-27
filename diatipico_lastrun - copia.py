#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2023.2.3),
    on octubre 26, 2023, at 19:06
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---

from psychopy import plugins
plugins.activatePlugins()
from psychopy import  gui, visual, core, data, logging, event
from psychopy.tools import environmenttools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER, priority)

import os  # handy system and path functions
import sys  # to get file system encoding
from audioRecorder import AudioRecorder
import psychopy.iohub as io
from psychopy.hardware import keyboard

# Connecting to the board
puerto_arduino='COM16'
baud_rate=115200

# Variable para rastrear si estamos grabando
recording = False
sample_rate = 44100  # Sample rate (adjust as needed)

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
    ioConfig = {}
    
    # Setup iohub keyboard
    ioConfig['Keyboard'] = dict(use_keymap='psychopy')
    
    ioSession = '1'
    if 'session' in expInfo:
        ioSession = str(expInfo['session'])
    ioServer = io.launchHubServer(window=win, **ioConfig)
    
    # create a default keyboard (e.g. to check for escape)
    defaultKeyboard = keyboard.Keyboard(backend='iohub')
    # return inputs dict
    return {
        'ioServer': ioServer,
        'defaultKeyboard': defaultKeyboard
    }


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
        image='resources/microphone-png-16.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), size=(0.5, 0.5),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    
    # --- Initialize components for Routine "Agradecimiento" ---
    text = visual.TextStim(win=win, name='text',
        text='¡Muchas gracias por participar!\n\nPresion ESPACIO para terminar el experimento',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    exit_exp = keyboard.Keyboard()
    
    # Crear una instancia de la grabadora con los parámetros adecuados
    mi_grabadora = AudioRecorder(filepath=filename[:-4]+'.wav', mic_id=0, 
        sample_rate=sample_rate, channels=1, arduino_port=puerto_arduino, baud_rate=baud_rate)
    stop_rec = keyboard.Keyboard()
    
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
    thisExp.addData('t_start', globalClock.getTime())

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
    
    # check responses
    if start_rec.keys in ['', [], None]:  # No response was made
        start_rec.keys = None
    
    # the Routine "Instrucciones" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "Respuesta" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('start_recording', globalClock.getTime())
    
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
    thisExp.addData('stop_recording', globalClock.getTime())
    
    # Run 'End Routine' code from code
    mi_grabadora.stop_recording()
    
    # check responses
    if stop_rec.keys in ['', [], None]:  # No response was made
        stop_rec.keys = None
    
    # the Routine "Respuesta" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "Agradecimiento" ---
    continueRoutine = True
    
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
    thisExp.addData('t_end', globalClock.getTime())
    
    # check responses
    if exit_exp.keys in ['', [], None]:  # No response was made
        exit_exp.keys = None

    
    # the Routine "Agradecimiento" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    # Run 'End Experiment' code from code
    # Cierra la conexión serie
    mi_grabadora._serial.close()
    try:
        # Detener la grabación
        mi_grabadora.stop_recording()
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
    thisExp.saveAsWideText()


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
    # Initialize a data file to record events
    # ---
    output_filename = f'data/{expInfo["Nombre"]}_{expInfo["date"]}/{expInfo["Nombre"]}_{expInfo["date"]}'  # Output file name
    thisExp = data.ExperimentHandler(
        name='TypicalDayNarrative',
        extraInfo=expInfo,
        dataFileName=output_filename,  # Data file name
        savePickle=False,
        saveWideText=True
    )
    win = setupWindow(expInfo=expInfo)
    inputs = setupInputs(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo,
        thisExp=thisExp,
        win=win,
        inputs=inputs
    )
    saveData(thisExp)
    quit(thisExp=thisExp, win=win, inputs=inputs)
