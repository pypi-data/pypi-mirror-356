from tkinter import filedialog
from tkinter import *
from tkinter import simpledialog
import tkinter
import kspice
import networkx as nx
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


class _askTimeline(simpledialog.Dialog): 
    """
    Dialog for selecting a timeline from a list of available timelines.
    
    Args:
        root (Tk): Parent Tkinter window.
        title (str): Dialog title.
        timelines (list): List of timeline objects to choose from.
    """
    def __init__(self, root, title, timelines= []):
        self.timelines = timelines
        self.tl = IntVar(root)
        super().__init__(root, title)
    
    def body(self, master):


        tkinter.Label(master, text="Please select the timeline to run").pack()

        for i, timeline in enumerate(self.timelines):
            tkinter.Radiobutton(master, text = timeline.name, value=i, variable = self.tl, indicator = 0).pack()


        return master

    def apply(self):
        pass
        
class _askFiles(simpledialog.Dialog):
    """
    Dialog for selecting model, parameter, and initial condition files.

    Args:
        root (Tk): Parent Tkinter window.
        title (str): Dialog title.
        models (list): List of available model file names.
        parameters (list): List of available parameter file names.
        ics (list): List of available initial condition file names.
    """
    def __init__(self, root, title, models, parameters, ics):
        self.models = models
        self.parameters = parameters
        self.ics = ics
        self.m = IntVar(root, 0)
        self.p = IntVar(root, 0)
        self.i = IntVar(root, 0)
        super().__init__(root, title)

    def body(self, master):

        

       

        tkinter.Label(master, text="Models").grid(column=0, row=0, sticky=tkinter.W, padx=5, pady=5)
        for i, model in enumerate(self.models):
            tkinter.Radiobutton(master, text=model, value=i, variable = self.m).grid(column=0, 
                                                                                                     row=1+i,
                                                                                                     sticky=tkinter.W,
                                                                                                     padx=5,
                                                                                                     pady=5)

        tkinter.Label(master, text="Parameters").grid(column=1, row=0, sticky=tkinter.W, padx=5, pady=5)        
        for i, param in enumerate(self.parameters):
            tkinter.Radiobutton(master, text=param, value=i, variable = self.p).grid(column=1, 
                                                                                                     row=1+i,
                                                                                                     sticky=tkinter.W,
                                                                                                     padx=5,
                                                                                                     pady=5)
        tkinter.Label(master, text="Initial Conditions").grid(column=2, row=0, sticky=tkinter.W, padx=5, pady=5)
        for i, ic in enumerate(self.ics):
            tkinter.Radiobutton(master, text=ic, value=i, variable = self.i).grid(column=2, 
                                                                                                     row=1+i,
                                                                                                     sticky=tkinter.W,
                                                                                                     padx=5,
                                                                                                     pady=5)

        return master

    def apply(self):
        pass
        
        
class On_Off_Valve:
    """
    Wrapper for operating block-valves and motor-operated-valves in the Yggdrasil Engineering Simulator.

    Args:
        tag (str): Tag name of the valve.
        model (YggLCS): Reference to the YggLCS simulation object.
        app (str, optional): Application name. Automatically inferred if not provided.
    """    
    def __init__(self, tag, model, app=False):  
        self.sim = model.sim
        self.tl = model.timeline
        self.tag = tag
        
        if not app:

            applications = [x.name for x in self.tl.applications]
            
            if tag[0] in "DEFNS":
                app = "HuginA" if "HuginA" in applications else self._search_application_(tag)
            
            elif tag[0] in "ACVWYZ":
                app = "Munin" if "Munin" in applications else self._search_application_(tag)

            elif tag[0] in "G":
                app = "HuginB" if "HuginB" in applications else self._search_application_(tag)
            else:
                app = self._search_application_(tag)
        

        self.app = app
        
        if self.app:
            try:
                self.v = self.tl.get_block(app, tag)
            except:
                print("No valve with tag {} found in application {}".format(tag, self.app))
        else:
            print("No valve with tag {} found in any of the simulator applications".format(tag))
            self.v = False

        if self.v:
            if self.v.type not in ["MotorOperatedValve", "BlockValve", "LedaValve", "PulseControlledValve", "ControlValve"]:
                print("Object is not a Leda-Valve, Motor-Operated_Valve, PulseControlledValve, ControlValve or Block-Valve. Object is of type {}.\nNo further operations on object allowed.".format(self.v.type))
                self.v = False
    
    def set(self, prop, value, unit=False):
        self.tl.set_value(self.app, self.v.name + ":" + prop, value, unit=unit)

    def get(self, prop, unit=False):
        return self.tl.get_value(self.app, self.v.name + ":" + prop, unit=unit)
        
    
    def _search_application_(self, tag):
        """ Returns the application name where tag can be found """
        for application in self.tl.applications:
            try:
                temp = self.tl.get_block(application.name, tag)
                print("{} found in application {}".format(tag, application.name))
                return application.name
                
            except:
                return False    
    
    def get_valve(self):
        """ Return the BlockValve object """
        return self.v
    

    def close(self):    
        """ Wrapper that closes the valve regardless of type """
        if self.v:
            if self.v.type == "MotorOperatedValve":
                self.tl.set_value(self.app, self.v.name + ":LocalClose", True)
            elif self.v.type == "BlockValve":
                self.tl.set_value(self.app, self.v.name + ":LocalInput", False)
            elif self.v.type in ["LedaValve", "ControlValve"]:
                self.tl.set_value(self.app, self.v.name + ":LocalControlSignalIn", 0, unit="%")
                # get and operate keyswitch if exists
                try:
                    ks = self.tl.get_block(self.app, self.tag + "_KS")
                    self.tl.set_value(self.app, self.tag + "_KS:RequestedPosition", False)
                except:
                    pass
                
            
                
            elif self.v.type == "PulseControlledValve":
                self.tl.set_value(self.app, self.v.name + ":LocalSetClosed", True)
        else:
            print("Unvaild valve object")

    def open(self):
        """ Wrapper that open the valve regardless of type """
        if self.v:
            if self.v.type == "MotorOperatedValve":
                self.tl.set_value(self.app, self.v.name + ":LocalOpen", True)
            elif self.v.type == "BlockValve":
                self.tl.set_value(self.app, self.v.name + ":LocalInput", True)
            elif self.v.type in ["LedaValve", "ControlValve"]:
                self.tl.set_value(self.app, self.v.name + ":LocalControlSignalIn", 100, unit="%")
                # get and operate keyswitch if exists
                try:
                    ks = self.tl.get_block(self.app, self.tag + "_KS")
                    self.tl.set_value(self.app, self.tag + "_KS:RequestedPosition", True)
                except:
                    pass
            elif self.v.type == "PulseControlledValve":
                self.tl.set_value(self.app, self.v.name + ":LocalSetOpen", True)
        else:
            print("Unvaild valve object")
            
    def get_pos(self):
        """ Wrapper that returns the stem position of the valve in percentage """
        if self.v:
            return self.tl.get_value(self.app, self.v.name + ":ValveStemPosition", unit="%")
        else:
            print("Unvaild valve object")
            
    def is_open(self):
        """ Wrapper that returns True if valve is defined as open """
        if self.v:
            return self.tl.get_value(self.app, self.v.name + ":IsDefinedOpen")
        else:
            print("Unvaild valve object")
            
    def is_closed(self):
        """ Wrapper that returns True if valve is defined as closed """
        if self.v:
            return self.tl.get_value(self.app, self.v.name + ":IsDefinedClosed")
        else:
            print("Unvaild valve object")        
    
class Motor_Heater:
    """
    Wrapper for operating motors and electric heaters in the Yggdrasil Engineering Simulator.

    Args:
        tag (str): Tag name of the motor or heater.
        model (YggLCS): Reference to the YggLCS simulation object.
        app (str, optional): Application name. Automatically inferred if not provided.
    """

    def __init__(self, tag, model, app=False):  

        self.sim = model.sim
        self.tl = model.timeline
        
        if not app:

            applications = [x.name for x in self.tl.applications]
            
            if tag[0] in "DEFNS":
                app = "HuginA" if "HuginA" in applications else self._search_application_(tag)
            
            elif tag[0] in "ACVWYZ":
                app = "Munin" if "Munin" in applications else self._search_application_(tag)

            elif tag[0] in "G":
                app = "HuginB" if "HuginB" in applications else self._search_application_(tag)
            else:
                app = self._search_application_(tag)
        

        self.app = app
        
        if self.app:
            try:
                self.m = self.tl.get_block(app, tag)
            except:
                print("No motor with tag {} found in application {}".format(tag, self.app))
        else:
            print("No motor with tag {} found in any of the simulator applications".format(tag))
            self.m = False

        if self.m:
            if self.m.type not in ["ControlledAsynchronousMachine", "ControlledElectricHeater"]:
                print("Object is not a Motor or Heater. Object is of type {}.\nNo further operations on object allowed.".format(self.m.type))
                self.m = False

    def _search_application_(self, tag):
        """ Returns the application name where tag can be found """
        for application in self.tl.applications:
            try:
                temp = self.tl.get_block(application.name, tag)
                print("{} found in application {}".format(tag, application.name))
                return application.name
                
            except:
                return False       
    
    def set(self, prop, value, unit=False):
        self.tl.set_value(self.app, self.m.name + ":" + prop, value, unit=unit)

    def get(self, prop, unit=False):
        return self.tl.get_value(self.app, self.m.name + ":" + prop, unit=unit)
    
    def start(self):
        
        """ Switch on the motor/element """
        if self.m:
            if self.tl.get_value(self.app, self.m.name + ":OnOffOption") == 0:
                self.tl.set_value(self.app, self.m.name + ":LocalInput", True)
            else:
                self.tl.set_value(self.app, self.m.name + ":LocalSetOn", True)
        else:
            print("Unvaild heater or motor object")   
    def stop(self):
        
        """ Switch off the motor/element """
        if self.m:
            if self.tl.get_value(self.app, self.m.name + ":OnOffOption") == 0:
                self.tl.set_value(self.app, self.m.name + ":LocalInput", False)
            else:
                self.tl.set_value(self.app, self.m.name + ":LocalSetOff", True)
        else:
            print("Unvaild heater or motor object")
    def is_on(self):
        """ Returns True if motor/element is switched on """
        if self.m.type == "ControlledAsynchronousMachine":
            return self.tl.get_value(self.app, self.m.name + ":MachineState") == 1
        else:
            return self.tl.get_value(self.app, self.m.name + ":Running") == True
    def is_off(self):
        """ Returns True if motor/element is switched off """
        if self.m.type == "ControlledAsynchronousMachine":
            return self.tl.get_value(self.app, self.m.name + ":MachineState") == 0
        return self.tl.get_value(self.app, self.m.name + ":Running") == False

class PID:
    """
    Wrapper for operating PID controllers in the Yggdrasil Engineering Simulator.

    Args:
        tag (str): Tag name of the PID controller.
        model (YggLCS): Reference to the YggLCS simulation object.
        app (str, optional): Application name. Automatically inferred if not provided.
    """
    def __init__(self, tag, model, app=False):  



        self.sim = model.sim
        self.tl = model.timeline
        
        if not app:

            applications = [x.name for x in self.tl.applications]
            
            if tag[0] in "DEFNS":
                app = "HuginA" if "HuginA" in applications else self._search_application_(tag)
            
            elif tag[0] in "ACVWYZ":
                app = "Munin" if "Munin" in applications else self._search_application_(tag)

            elif tag[0] in "G":
                app = "HuginB" if "HuginB" in applications else self._search_application_(tag)
            else:
                app = self._search_application_(tag)
        

        self.app = app
        
        if self.app:
            try:
                self.c = self.tl.get_block(app, tag)
            except:
                print("No PID controller with tag {} found in application {}".format(tag, self.app))
        else:
            print("No PID controller with tag {} found in any of the simulator applications".format(tag))
            self.c = False

        if self.c:
            if self.c.type not in ["PidController"]:
                print("Object is not a PID Controller. Object is of type {}.\nNo further operations on object allowed.".format(self.v.type))
                self.c = False

    def _search_application_(self, tag):
        """ Returns the application name where tag can be found """
        for application in self.tl.applications:
            try:
                temp = self.tl.get_block(application.name, tag)
                print("{} found in application {}".format(tag, application.name))
                return application.name
                
            except:
                return False   
    
    
    def set(self, prop, value, unit=False):
        self.tl.set_value(self.app, self.c.name + ":" + prop, value, unit=unit)

    def get(self, prop, unit=False):
        return self.tl.get_value(self.app, self.c.name + ":" + prop, unit=unit)
        
    def get_mode(self):
        """
        Returns text representation of the current mode
        """
        m = self.tl.get_value(self.app, self.c.name + ":Mode")
        if m == 0:
            return ("Auto")
        elif m == 1:
            return ("Manual")
        else: 
            return("External")
    
    def get_sp_selection(self):
        s = self.tl.get_value(self.app, self.c.name + ":SetpointSelection")
        if s == 0:
            return("Internal")
        else:
            return("External")

    def to_auto(self):
        """
        Set controller mode to Auto
        """
        self.tl.set_value(self.app, self.c.name + ":Mode", 0)

    def to_man(self):
        """
        Set controller mode to Manual
        """
        self.tl.set_value(self.app, self.c.name + ":Mode", 1)

    def to_external(self):
        """
        Set controller mode to External SP
        """
        self.tl.set_value(self.app, self.c.name + ":Mode", 2) 

    def set_tracking(self, state):
        """
        Set tracking mode on or off
        """
        self.tl.set_value(self.app, self.c.name + ":Tracking", state)

    def get_tracking(self):
        """
        Get state of tracking
        """
        return self.tl.get_value(self.app, self.c.name + ":Tracking")

    def set_tracking_value(self, value):
        """ 
        Set the output used when tracking
        """
        self.tl.set_value(self.app, self.c.name + ":Feedback", value)

    def set_output(self, out):
        """
        Change output of controller if controller is in manual mode
        """
        if self.get_mode() == "Manual":
            self.tl.set_value(self.app, self.c.name + ":ControllerOutput", out)
    def get_output(self):
        """
        Get output of controller
        """        
        return self.tl.get_value(self.app, self.c.name + ":ControllerOutput")

    def set_setpoint(self, sp):
        """
        Change internal setpoint of controller if controller is in manual or auto with internal setpoint selection
        """
        if self.get_mode() == "Manual" or (self.get_mode() == "Auto" and self.get_sp_selection() == "Internal"):
            self.tl.set_value(self.app, self.c.name + ":InternalSetpoint", sp)

class Choke:
    """
    Wrapper for operating choke and control valves in the Yggdrasil Engineering Simulator.

    Args:
        tag (str): Tag name of the choke valve.
        model (YggLCS): Reference to the YggLCS simulation object.
        app (str, optional): Application name. Automatically inferred if not provided.
    """
    def __init__(self, tag, model, app=False):  



        self.sim = model.sim
        self.tl = model.timeline
        
        if not app:

            applications = [x.name for x in self.tl.applications]
            
            if tag[0] in "DEFNS":
                app = "HuginA" if "HuginA" in applications else self._search_application_(tag)
            
            elif tag[0] in "ACVWYZ":
                app = "Munin" if "Munin" in applications else self._search_application_(tag)

            elif tag[0] in "G":
                app = "HuginB" if "HuginB" in applications else self._search_application_(tag)
            else:
                app = self._search_application_(tag)
        

        self.app = app
        
        if self.app:
            try:
                self.c = self.tl.get_block(app, tag)
            except:
                print("No choke with tag {} found in application {}".format(tag, self.app))
        else:
            print("No choke with tag {} found in any of the simulator applications".format(tag))
            self.c = False

        if self.c:
            if self.c.type not in ["ControlValve", "LedaValve"]:
                print("Object is not a Control Valve. Object is of type {}.\nNo further operations on object allowed.".format(self.c.type))
                self.c = False

    def _search_application_(self, tag):
        """ Returns the application name where tag can be found """
        for application in self.tl.applications:
            try:
                temp = self.tl.get_block(application.name, tag)
                print("{} found in application {}".format(tag, application.name))
                return application.name
                
            except:
                return False       
    
    def set(self, prop, value, unit=False):
        self.tl.set_value(self.app, self.c.name + ":" + prop, value, unit=unit)

    def get(self, prop, unit=False):
        return self.tl.get_value(self.app, self.c.name + ":" + prop, unit=unit)    
    
    def move_to(self, pos):
        """
        Wrapper that moves a choke object to a desired position.  
        If LocalControlSignalIn is connected from an external source, the choke will be set in Manual Mode
        """
        connections = self.tl.get_block(self.app, self.c.name).input_connections
        if len(connections) > 0:
            for conn in connections:
                if "LocalControlSignalIn" in str(conn):
                    self.direct_control()
        self.tl.set_value(self.app, self.c.name + ":LocalControlSignalIn", pos, unit="%")
        self.tl.set_value(self.app, self.c.name + ":TargetPosition", pos, unit="%")

    def direct_control(self):
        """
        Set object in manual mode
        """
        self.tl.set_value(self.app, self.c.name + ":InputSwitch",2)

    def reset_control(self):
        """
        If object has defined connection to LocalControlSignalIn, set mode to Local
        """
        connections = self.tl.get_block(self.app, self.c.name).input_connections
        if len(connections) > 0:
            for conn in connections:
                if "LocalControlSignalIn" in str(conn):
                    self.tl.set_value(self.app, self.c.name + ":InputSwitch", 0)      
    
    def get_pos(self):
        return self.tl.get_value(self.app, self.c.name + ":ValveStemPosition", unit="%")

class Transmitter:
    """
    Wrapper for reading transmitter values in the Yggdrasil Engineering Simulator.

    Args:
        tag (str): Tag name of the transmitter.
        model (YggLCS): Reference to the YggLCS simulation object.
        app (str, optional): Application name. Automatically inferred if not provided.
    """
    def __init__(self, tag, model, app=False):  

        self.sim = model.sim
        self.tl = model.timeline
        
        if not app:

            applications = [x.name for x in self.tl.applications]
            
            if tag[0] in "DEFNS":
                app = "HuginA" if "HuginA" in applications else self._search_application_(tag)
            
            elif tag[0] in "ACVWYZ":
                app = "Munin" if "Munin" in applications else self._search_application_(tag)

            elif tag[0] in "G":
                app = "HuginB" if "HuginB" in applications else self._search_application_(tag)
            else:
                app = self._search_application_(tag)
        

        self.app = app
        
        if self.app:
            try:
                self.t = self.tl.get_block(app, tag)
            except:
                print("No transmitter with tag {} found in application {}".format(tag, self.app))
        else:
            print("No transmitter with tag {} found in any of the simulator applications".format(tag))
            self.t = False

        if self.t:
            if self.t.type not in ["AlarmTransmitter"]:
                print("Object is not a Transmitter. Object is of type {}.\nNo further operations on object allowed.".format(self.t.type))
                self.t = False

    def _search_application_(self, tag):
        """ Returns the application name where tag can be found """
        for application in self.tl.applications:
            try:
                temp = self.tl.get_block(application.name, tag)
                print("{} found in application {}".format(tag, application.name))
                return application.name
                
            except:
                return False   

    def set(self, prop, value, unit=False):
        self.tl.set_value(self.app, self.t.name + ":" + prop, value, unit=unit)

    def get(self, prop, unit=False):
        return self.tl.get_value(self.app, self.t.name + ":" + prop, unit=unit)    
    
    def get_value(self, unit):
        return self.tl.get_value(self.app, self.t.name + ":MeasuredValue", unit=unit)

class YggLCS:
    """
    Wrapper for initializing and managing a Yggdrasil Engineering Simulator project.

    Args:
        run (bool, optional): If True, starts the simulation immediately after loading.
        model (string, optional): Path to model directory. If False, UI activates to select model directory.
        tl (string, optional): Timeline to be activated. If false, UI activates to allow user to select among available timelines
        mpc (list, optional): List with name of model, parameter and condition files to load.  If false, UI activates to allow user to select among available files.
    """
    def __init__(self, model = False, tl = False, mpc = False, run = False):

        root = Tk()
        root.withdraw()

        self.model = model or filedialog.askdirectory(**{"title":"Please select model directory"})
        self.sim = kspice.Simulator(self.model)
        self.tl = tl or _askTimeline(root, "Timelines", self.sim.timelines).tl.get()
        self.timeline = self.sim.timelines[self.tl]
        self.timeline.activate()
        if not mpc:
            files = _askFiles(root, "Files", self.timeline.models, self.timeline.parameters, self.timeline.initial_conditions)
            self.model = files.m.get()
            self.parameter = files.p.get()
            self.ic = files.i.get()
            self.timeline.load(self.timeline.models[self.model], self.timeline.parameters[self.parameter], self.timeline.initial_conditions[self.ic])
        else:
            self.timeline.load(self.timeline.models[mpc[0]], self.timeline.parameters[mpc[1]], self.timeline.initial_conditions[mpc[2]])
        self.timeline.initialize()
        if run:
            self.timeline.run()

    def get_timeline(self):
        """
        Returns the active timeline object
        """
        return self.timeline
    
    def on_off_valve(self, tag, app=False):
        """
        Creates and returns a on-off valve object
        """
        return On_Off_Valve(tag, self, app)

    def motor_heater(self, tag, app=False):
        """
        Creates and returns an electrical element, used for heaters and motors
        """
        return Motor_Heater(tag, self, app)

    def pid(self, tag, app=False):
        """
        Creates and returns a PID controller
        """
        return PID(tag, self, app)
    
    def choke(self, tag, app=False):
        """        
        Creates and returns a choke object
        """
        return Choke(tag, self, app)

    def transmitter(self, tag, app=False):
        """
        Creates and returns an AlarmTransmitter object
        """
        return Transmitter(tag, self, app)
    
    def run(self):
        self.timeline.run()
    def pause(self):
        self.timeline.pause()
    def close_project(self):
        self.sim.close_project()

    def set(self, tag, prop, value, unit=False):
        """ Set a property for a given tag. """
        app = self._search_application_(tag)
        self.tl.set_value(app, tag + ":" + prop, value, unit=unit)

    def get(self, tag, prop, unit=False):
        """ Get the value of a property of a given tag. """
        app = self._search_application_(tag)
        return self.tl.get_value(app, tag + ":" + prop, unit=unit)
    
    def _search_application_(self, tag):
        """ Returns the application name where tag can be found """
        for application in self.tl.applications:
            try:
                temp = self.tl.get_block(application.name, tag)
                #print("{} found in application {}".format(tag, application.name))
                return application.name
                
            except:
                return False

class Sequence:
    """
    A sequence of steps to be executed in order, with optional inhibit conditions.

    Args:
        name (str): Name of the sequence.
        seqs (dict): Dictionary of all step objects (name → Step).
        sim (YggLCS): Reference to the simulator object.
        inhibit_conditions (list of callables, optional): Conditions that must evaluate False for the sequence to run.
        verbose (bool, optional): If True, prints execution info.
    """

    def __init__(self, name, seqs, sim, inhibit_conditions=[], verbose = False):
        self.seqs = seqs
        self.steps = []
        self.inhibits = inhibit_conditions
        self.name = name
        self.sim = sim
        self.verbose = verbose

    def check_inhibits(self):
        """ Inhibit conditions must all evaluate to False to allow sequence to start"""
        ret = True
        if len(self.inhibits) > 0:            
            for inhibit in self.inhibits:
                if inhibit():
                    print("Inhibit condition prevents sequence start of " + self.name + ": " + str(inhibit))
                    ret = False
        return ret
    
    def start(self, verbose = False):
        """
        Executes the sequence, Step by Step according to Step configuration and logic
        """

        if self.name not in ["START", "END"]:
            print("\n" + str(self.sim.timeline.model_time) + ": *** Starting Sequence. Name: {}, number of Steps: {} ***".format(self.name, len(self.steps)))

        if self.check_inhibits():
            self.steps.sort()

            # Step 1 is the always the first step in a sequence.  Following steps dictated by Step property and logic.
            step = self.steps[0] 
            while True:
                if verbose:
                    print(str(self.sim.timeline.model_time) + ": Executing step {}".format(step.number), end="...")                                
                step.execute_actions()
                if verbose:
                    print(str(self.sim.timeline.model_time) + ": Executing {} action(s)".format(len(step.st)), end="...")
                start = self.sim.timeline.model_time
                while not step.check_trans():
                    time.sleep(1)
                    end = self.sim.timeline.model_time
                    if (end-start).seconds > step.tmax:
                        message = str(self.sim.timeline.model_time) + ": Sequence: {}, Step timeout in step {}.\n".format(self.name, step.number)
                        for trans in step.trans:
                            message += str(trans) +": " + str(trans()) + "\n"
                        raise Exception(message)
                if verbose:
                    print(str(self.sim.timeline.model_time) + ": Step {} executed successfully.".format(step.number))
                if step.next:
                    step = self.seqs[step.next()]
                else:
                    if self.name not in ["START", "END"]:
                        print(str(self.sim.timeline.model_time) + ": *** Sequence {} finished ***".format(self.name))
                    break
        else:
            raise Exception("Sequence cannot be started due to inhibit conditions")
        return self.name

    def add_step(self, step):
        self.steps.append(step)

    def add_steps(self, steps):
        for step in steps:
            self.add_step(step)

class Step:
    """
    A single step in a sequence.

    Args:
        config (dict): Configuration dictionary containing:
        number (int): Step number.
        actions (list of callables): Actions to perform when the step starts.
        transitions (list of callables): Conditions that must evaluate to True to complete the step.
        tmax (int): Maximum allowed simulator time (in seconds) for the step.
        next (Callable[[], str] or None): Function returning the key of the next step.
    """
    def __init__(self, config):
        self.failed = False
        self.number = config["number"]
        self.st = config["actions"]
        self.trans = config["transitions"]
        self.tmax = config["tmax"]
        self.next = config["next"]
  
    def execute_actions(self):
        """
        Executes all actions
        """
        for st in self.st:
            st()

    def check_trans(self):
        """
        All transitions must evaluate to True to continue.
        """
        ret = True
        for trans in self.trans:
            if not trans():
                ret = False
        return ret

    def StepAction(self):
        """
        Returns the list of Step Actions
        """
        return self.st

    def transition(self):
        """
        Returns the list of Step Transitions
        """
        return self.trans

    def onFail(self):
        """
        To be implemented.  What to do on Step failure (conditions or transitions).  For now Exceptions are raised directly.
        """
        return False

    def __lt__(self, other):
        """
        To allow sorting
        """
        return self.number < other.number

    def __eq__(self, other):
        """
        To allow sorting
        """
        return self.number == other.number


class Admin:

    """
    Administrative controller for managing and executing multiple sequences with dependency resolution.

    Args:
        name (str): Name of the admin controller.
        sequences (list of Sequence): List of sequence objects.
        edges (list of tuples): Directed edges defining execution order between sequences.
        sim (YggLCS): Reference to the simulator object.
    """

    def __init__(self, name, sequences, edges, sim):
        self.name = name
        self.seq = {}
        for s in sequences:
            self.seq[s.name] = s
        # Initialise first step (START)
        dummy = {}
        dummy["start"] = Step({
            "number": 1,
            "conditions": [],
            "actions": [],
            "transitions": [],
            "tmax": 2,
            "next": None
        })
        start_seq = Sequence("START", 
               dummy,
               sim,
               []
               )
        start_seq.add_step(dummy["start"])
        self.seq["START"] = start_seq

        #Initialize the last step (END)
        end = Sequence("END", 
               dummy,
               sim,
               []
               )
        end.add_step(dummy["start"])
        self.seq["END"] = end
        
        self.edges = edges

        # Create a directed graph
        self.G = nx.DiGraph()
        # Create the nodes and connect the edges
        self.G.add_edges_from(edges)


    def start(self):
        """
        Starts the admin sequence execution
        """
        self.execute_tasks(self.G, self.seq)



    def start_sequence(self, seq, name):
        """
        Helper function to start a sequence and return the name of the sequence that was started.
        """
        seq.start()
        return name





# Execute the tasks based on the dependency graph
    def execute_tasks(self, graph, seq_objects):
        """
        Function that starts all the sequences which has no parent or whos parent has completed. 
        Parallel sequences are started in separate pseudo threads to enable paralell execution. 
        Edges in directed graph dicated when a sequence can be started.
        """
        # Find the start tasks (those that have no predecessors)
        initial_tasks = [n for n in graph.nodes if graph.in_degree(n) == 0]
    
        # Initialize an executor for parallel task execution
        with ThreadPoolExecutor() as executor:
            # Track futures
            task_futures = {}
    
            # Start initial tasks
            for task_name in initial_tasks:
                
                task_futures[task_name] = executor.submit(self.start_sequence, seq_objects[task_name], task_name)
    
            # As each task finishes, check if we can start dependent tasks
            while task_futures:
                for future in as_completed(task_futures.values()):
                    task_name = future.result()  # Get the result (task name)
                    
                    if task_name is None:
                        raise ValueError("Error: Task returned None!")
    
                    # Check if task has successors
                    if task_name in graph:
                        successors = list(graph.successors(task_name))
                        for successor in successors:
                            # Check if all predecessors of the successor have finished
                            predecessors = list(graph.predecessors(successor))
                            if all(p in task_futures and task_futures[p].done() for p in predecessors):
                                # Start successor task
                                
                                task_futures[successor] = executor.submit(self.start_sequence, seq_objects[successor], successor)
    
                    # Remove completed task from tracking
                    if task_name in task_futures:
                        del task_futures[task_name]