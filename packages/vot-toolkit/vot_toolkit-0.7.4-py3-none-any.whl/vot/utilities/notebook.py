""" This module contains functions for visualization in Jupyter notebooks. """

import io
from threading import Thread, Condition
import typing

from vot.utilities import Progress

def is_notebook():
    """ Returns True if the current environment is a Jupyter notebook. 
    
    Returns:
        bool: True if the current environment is a Jupyter notebook.    
    """
    try:
        from IPython import get_ipython
        if get_ipython() is None:
            raise ImportError("console")
        if 'IPKernelApp' not in get_ipython().config:  # pragma: no cover
            raise ImportError("console")
    except ImportError:
        return False
    else:
        return True

class SequenceView(object):
    """ A widget for visualizing a sequence. """

    def __init__(self):
        """ Initializes a new instance of the SequenceView class. 
        
        Args:
            sequence (Sequence): The sequence to visualize.
        """

        try:
            from IPython.display import display
            from ipywidgets import widgets
        except ImportError:
            raise ImportError("The IPython and ipywidgets packages are required for visualization.")
        
        from vot.utilities.draw import ImageDrawHandle
        
        self._handle = ImageDrawHandle(sequence.frame(0).image())

        self._button_restart = widgets.Button(description='Restart')
        self._button_next = widgets.Button(description='Next')
        self._button_play = widgets.Button(description='Run')
        self._frame = widgets.Label(value="")
        self._frame.layout.display = "none"
        self._frame_feedback = widgets.Label(value="")
        self._image = widgets.Image(value="", format="png", width=sequence.size[0] * 2, height=sequence.size[1] * 2)

        state = dict(frame=0, auto=False, alive=True, region=None)
        condition = Condition()

        self._buttons = widgets.HBox(children=(frame, self._button_restart, self._button_next, button_play, frame2))

    def _push_image(handle):
        """ Pushes an image to the widget. 

        Args:
            handle (ImageDrawHandle): The image handle.
        """
        with io.BytesIO() as output:
            handle.snapshot.save(output, format="PNG")
            return output.getvalue()
        

def visualize_tracker(tracker: "Tracker", sequence: "Sequence"):
    """ Visualizes a tracker in a Jupyter notebook.

    Args:
        tracker (Tracker): The tracker to visualize.
        sequence (Sequence): The sequence to visualize.
    """
    
    if not is_notebook():
        raise ImportError("The Jupyter notebook environment is required for visualization.")
    
    try:
        from IPython.display import display
        from ipywidgets import widgets
    except ImportError:
        raise ImportError("The IPython and ipywidgets packages are required for visualization.")
    
    from vot.utilities.draw import ImageDrawHandle

    def encode_image(handle):
        """ Encodes an image so that it can be displayed in a Jupyter notebook.
        
        Args:
            handle (ImageDrawHandle): The image handle.
        
        Returns:
            bytes: The encoded image."""
        with io.BytesIO() as output:
            handle.snapshot.save(output, format="PNG")
            return output.getvalue()

    handle = ImageDrawHandle(sequence.frame(0).image())

    button_restart = widgets.Button(description='Restart')
    button_next = widgets.Button(description='Next')
    button_play = widgets.Button(description='Run')
    frame = widgets.Label(value="")
    frame.layout.display = "none"
    frame2 = widgets.Label(value="")
    image = widgets.Image(value=encode_image(handle), format="png", width=sequence.size[0] * 2, height=sequence.size[1] * 2)

    state = dict(frame=0, auto=False, alive=True, region=None)
    condition = Condition()

    buttons = widgets.VBox(children=(frame, button_restart, button_next, button_play, frame2))

    image.value = encode_image(handle)

    def run():
        """ Runs the tracker. """

        runtime = tracker.runtime()

        while state["alive"]:

            if state["frame"] == 0:
                state["objects"], _ = runtime.initialize(sequence.frame(0), sequence.groundtruth(0))
            else:
                state["objects"], _ = runtime.update(sequence.frame(state["frame"]))

            update_image()

            with condition:
                condition.wait()

                if state["frame"] == len(sequence):
                    state["alive"] = False
                    continue

                state["frame"] = state["frame"] + 1


    def update_image():
        """ Updates the image. """
        handle.image(sequence.frame(state["frame"]).image())
        handle.style(color="green").region(sequence.frame(state["frame"]).groundtruth())
        if state["objects"]:
            for obj in state["objects"]:
                handle.style(color="red").region(obj.region)
        image.value = encode_image(handle)
        frame.value = "Frame: " + str(state["frame"] - 1)

    def on_click(button):
        """ Handles a button click. """
        if button == button_next:
            with condition:
                state["auto"] = False
                condition.notify()
        if button == button_restart:
            with condition:
                state["frame"] = 0
                condition.notify()
        if button == button_play:
            with condition:
                state["auto"] = not state["auto"]
                button.description = "Stop" if state["auto"] else "Run"
                condition.notify()

    button_next.on_click(on_click)
    button_restart.on_click(on_click)
    button_play.on_click(on_click)
    widgets.jslink((frame, "value"), (frame2, "value"))

    def on_update(_):
        """ Handles a widget update."""
        with condition:
            if state["auto"]:
                condition.notify()

    frame2.observe(on_update, names=("value", ))

    thread = Thread(target=run)
    display(widgets.Box([widgets.HBox(children=(image, buttons))]))
    thread.start()
    with condition:
        condition.notify()

from vot.experiment import Experiment

def visualize_results(experiment: "Experiment", sequence: "Sequence", trackers: typing.List["Tracker"]):
    """ Visualizes the results of an experiment in a Jupyter notebook.
    
    Args:
        experiment (Experiment): The experiment to visualize.
        sequence (Sequence): The sequence to visualize.
        trackers (List[Tracker]): The trackers to visualize.
        
    """
    
    if not is_notebook():
        raise ImportError("The Jupyter notebook environment is required for visualization.")

    try:
        from IPython.display import display
        from ipywidgets import widgets
    except ImportError:
        raise ImportError("The IPython and ipywidgets packages are required for visualization.")
    
    from vot.utilities.draw import ImageDrawHandle

    def encode_image(handle):
        """ Encodes an image so that it can be displayed in a Jupyter notebook.
        
        Args:
            handle (ImageDrawHandle): The image handle.
        
        Returns:
            bytes: The encoded image.
        """

        with io.BytesIO() as output:
            handle.snapshot.save(output, format="PNG")
            return output.getvalue()

    handle = ImageDrawHandle(sequence.frame(0).image())

    button_restart = widgets.Button(description='Restart')
    button_next = widgets.Button(description='Next')
    button_play = widgets.Button(description='Run')
    frame = widgets.Label(value="")
    frame.layout.display = "none"
    frame2 = widgets.Label(value="")
    image = widgets.Image(value=encode_image(handle), format="png", width=sequence.size[0] * 2, height=sequence.size[1] * 2)

    state = dict(frame=0, auto=False, alive=True, region=None)
    condition = Condition()

    buttons = widgets.HBox(children=(frame, button_restart, button_next, button_play, frame2))

    image.value = encode_image(handle)

    state["data"] = [(tracker, experiment.results(tracker, sequence)) for tracker in trackers]

    sequence = experiment.transform([sequence])[0]

    def run():
        """ Runs the tracker. """

        while state["alive"]:

            for tracker in trackers:
                pass


            update_image()

            with condition:
                condition.wait()

                if state["frame"] == len(sequence):
                    state["alive"] = False
                    continue

                state["frame"] = state["frame"] + 1


    def update_image():
        """ Updates the image. """
        handle.image(sequence.frame(state["frame"]).image())
        handle.style(color="green").region(sequence.frame(state["frame"]).groundtruth())
        if state["region"]:
            handle.style(color="red").region(state["region"])
        image.value = encode_image(handle)
        frame.value = "Frame: " + str(state["frame"] - 1)

    def on_click(button):
        """ Handles a button click. """
        if button == button_next:
            with condition:
                state["auto"] = False
                condition.notify()
        if button == button_restart:
            with condition:
                state["frame"] = 0
                condition.notify()
        if button == button_play:
            with condition:
                state["auto"] = not state["auto"]
                button.description = "Stop" if state["auto"] else "Run"
                condition.notify()

    button_next.on_click(on_click)
    button_restart.on_click(on_click)
    button_play.on_click(on_click)
    widgets.jslink((frame, "value"), (frame2, "value"))

    def on_update(_):
        """ Handles a widget update."""
        with condition:
            if state["auto"]:
                condition.notify()

    frame2.observe(on_update, names=("value", ))

    thread = Thread(target=run)
    display(widgets.Box([widgets.VBox(children=(image, buttons))]))
    thread.start()
    

def run_experiment(experiment: "Experiment", sequences: typing.List["Sequence"], trackers: typing.List["Tracker"], force: bool = False, persist: bool = False):
    """ Runs an experiment with Jupiter notebook interface. """
    
    if not is_notebook():
        raise ImportError("The Jupyter notebook environment is required for visualization.")

    from collections.abc import Iterable    

    try:
        from IPython.display import display
        from ipywidgets import widgets
    except ImportError:
        raise ImportError("The IPython and ipywidgets packages are required for visualization.")
        
    # Ensure that the sequences are a list
    if not isinstance(sequences, Iterable):
        sequences = [sequences]
        
    # Ensure that the trackers are a list
    if not isinstance(trackers, Iterable):
        trackers = [trackers]
        
    from vot.experiment import run_experiment
    
    try:
    
        for tracker in trackers:
            run_experiment(experiment, tracker, sequences, force=force, persist=persist)    
        
    except InterruptedError:
        return False
    
    return True

def run_analysis(workspace: "Workspace", trackers: typing.List["Tracker"]):
    """ Runs an analysis with Jupiter notebook interface. """
    
    if not is_notebook():
        raise ImportError("The Jupyter notebook environment is required for visualization.")

    from collections.abc import Iterable    

    try:
        from IPython.display import display
        from ipywidgets import widgets
    except ImportError:
        raise ImportError("The IPython and ipywidgets packages are required for visualization.")
        
    # Ensure that the sequences are a list
    if not isinstance(sequences, Iterable):
        sequences = [sequences]
        
    # Ensure that the trackers are a list
    if not isinstance(trackers, Iterable):
        trackers = [trackers]
        
    from vot.analysis import process_stack_analyses
    
    try:
    
        for tracker in trackers:
            process_stack_analyses(workspace, trackers)    
        
    except InterruptedError:
        return False
    
    return True