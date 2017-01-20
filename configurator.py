# -*- coding: utf-8 -*-
#
#       pvg_common.py
#
#       Copyright 2011 Giorgio Gilestro <giorgio@gilest.ro>
#       revisions: 2016 Loretta Laughrey
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

#       Revisions by Caitlin Laughrey and Loretta E Laughrey in 2016.


# ----------------------------------------------------------------------------   Imports
import wx                               # GUI controls
import os                               # system controls
import ConfigParser                     # configuration file handler
import datetime                         # date and time handling functions
from os.path import expanduser          # get user's home directory
from dateutil import parser             # converts string version of datetime to datetime object

import wx.lib.newevent                  # mouse click event handling functions
ThumbnailClickedEvt, EVT_THUMBNAIL_CLICKED = wx.lib.newevent.NewCommandEvent()


""" ----------------------------------------------------------------------------------------  Config Object """
class Configuration(object):
    """
    Handles program configuration; Uses ConfigParser to store and retrieve


            options     section of configuration that pertains to program operation
            monitor#    section of configuration that pertains to video source #

        ----------  object attributes ---------------
            self.cfg_dict   list of dictionaries containing all config parameters and their values, indexed on 'section, key'
                                    cfg_dict[0] contains options
                                    cfg_dict[n] where n is > 0 contains parameters for monitor n
            self.filePathName   the name of the configuration file
            self.opt_keys       list of configuration option keys
            self.mon_keys       list of configration monitor keys

        ----------  functions -----------------------
            cfgOpen()                       reads configuration file
            cfgSaveAs()                     gets file path and name from user and saves
            default_cfg()                   creates a default configuration dictionary and saves it to a config file
            cfg_to_dicts(cfg)               creates a configuration dictionary for quicker access to configuration parameters
            dicts_to_cfg(cfg_dict)          saves dictionary to ConfigParser object
            getValue(section, key)          gets configuration value and converts it into the correct type
            setValue(section, key, value)   sets the value for a configuration parameter and updates dictionary
    """

    def __init__(self, parent, dirName=None, fileName=None):
        """
        Sets up a default configuration object and dictionary.
        """
        object.__init__(self)

        self.parent = parent


        """ -------------------------------------------------------------------------- configuration keywords """
        self.opt_keys = ['webcams', 'thumbnailsize', 'fullsize',  'fps_preview', 'monitors', 'cfgfolder']
        self.mon_keys = ['sourcetype','issdmonitor', 'source','fps_recording','start_datetime',
                         'track','tracktype','maskfile','datafolder']


        """ --------------------------------------------------------------------- create the ConfigParser object """
        self.cfg = ConfigParser.RawConfigParser()             # create the ConfigParser object
        self.default_cfg()                                  # start with a default configuration dictionary

        """ ------------------------------------- verify that provided filename exists or create default file name  """
        self.cfgGetFilePathName(self.parent, dirName, fileName)

        try:
            self.cfg.read(self.filePathName)                # read the selected configuration file
        except:                                             # otherwise make config object from cfg_dict
            print('$$$$$$ Invalid configuration file.  Creating default.')
            self.dict_to_cfgObject(self.cfg_dict)                        # apply the default configuration to the cfg object
            self.cfgSaveAs()                                # save the configuration

        self.cfg_to_dicts()                             # overwrites default cfg_dict with file cfg values if they exist

# -------------------------------------------------------------------------------- creates a default cfg dictionary
    def default_cfg(self):
        """
        Dictionary and cfg object will be created but NOT saved.
        """
        print('$$$$$$ Generating default configuration')
        self.defaultDir = os.path.join(expanduser('~'), 'Documents', 'PySolo_Files')

        if not(os.path.isdir(self.defaultDir)):
            os.mkdir(self.defaultDir)     # make sure default dir exists

        self.cfg_dict = [{                               # create the default config dictionary
            'webcams': 0,                                   # element 0 is the options dictionary
            'monitors': 1,
            'thumbnailsize': (320, 240),
            'fullsize': (640, 480),
            'fps_preview': 5,
            'cfgfolder': self.defaultDir
            },
            {                                       # all additional elements are the monitor dictionaries (1-indexed)
            'mon_name': 'Monitor1',  # include one default monitor
            'sourcetype': 1,
            'issdmonitor': False,
            'source': os.path.join(self.defaultDir, 'source.avi'),
            'fps_recording': 1,
            'start_datetime': wx.DateTime_Now(),
            'track': False,
            'tracktype': 0,
            'maskfile': os.path.join(self.defaultDir, 'mask.msk'),
            'datafolder': self.defaultDir
        }]


        self.dict_to_cfgObject(self.cfg_dict)                        # make cfg object from dictionary


# ------------------------------------------------------------------------------  use config object to make dictionary
    def cfg_to_dicts(self):
        """
        Create list of dictionaries from cfg for easier lookup of configuration info.
        First element [0] contains Options.
        Remaining element's indices indicate monitor number.
        """

        self.cfg_dict = [{}]                                      # start with empty list of dictionaries
    # Options:  cfg_dict[0]

        if not self.cfg.has_section('Options'):                      # make sure the options section exists in the cfg object
            self.cfg.add_section('Options')


        for key in self.opt_keys:                                   # fill dictionary with parameters
            if not self.cfg.has_option('Options',key):               # make sure the parameters exist in the cfg object
                default_value = self.cfg_dict[0][key]                   # key missing in cfg object: add it from default dictionary
                self.cfg.set('Options', key, default_value)

            self.cfg_dict[0][key] = self.getValue('Options', key)    # getValue() converts value to correct type from string

    #Monitors

        if not self.cfg.has_option('Options','monitors'):
            n_mons = 0
        else:
            n_mons = int(self.cfg.get('Options','monitors'))

        for mon_num in range(1, n_mons+1 ):
            self.cfg_dict.append({})                                 # create dictionary in element mon_num
            mon_name = 'Monitor%d' % mon_num
            for key in self.mon_keys:                               # fill dictionary with parameters
                if not self.cfg.has_option(mon_name, key):               # make sure the parameters exist in the cfg object
                    default_value = self.cfg_dict[1][key]
                    self.setValue('Monitor1', key, default_value)

                self.cfg_dict[mon_num][key] = self.getValue(mon_name, key)   # getValue() converts value to correct type from string

# -------------------------------------------------------------------------------- use dictionary to build cfg object
    def dict_to_cfgObject(self, cfg_dict):
        """
        Creates ConfigParser object using cfg_dict values.
        """
    # update configuration object with current config dictionary
        if not self.cfg.has_section('Options'):                      # make sure the options section exists in the cfg object
            self.cfg.add_section('Options')

        for key in self.opt_keys:                                       # options section
            self.cfg.set('Options', key, cfg_dict[0][key])

        n_mons = self.cfg_dict[0]['monitors']
        for mon_num in range(1, n_mons+1):
            mon_name = 'Monitor%d' % mon_num
            if not self.cfg.has_section(mon_name):
                self.cfg.add_section(mon_name)                # make sure the monitor section exists

            for key in self.mon_keys:
                self.cfg.set(mon_name, key, cfg_dict[mon_num][key])                 # monitors section

# --------------------------------------------------------------------------------------  get config file path & name
    def cfgGetFilePathName(self, parent, dirName='', fileName=''):
        """
        Lets user select or create a config file.
        """
        # if directory or file name are invalid, start file dialog
        if (dirName is None) or (fileName is None) or (not(os.path.isfile(os.path.join(dirName, fileName)))):

                wildcard = "PySolo Video config file (*.cfg)|*.cfg|" \
                           "All files (*.*)|*.*"                # adding space in here will mess it up!

                dlg = wx.FileDialog(parent,
                                    message="Open configuration file ...",
                                    defaultDir=os.getcwd(),
                                    wildcard=wildcard,
                                    style=wx.OPEN
                                    )

                if not(dlg.ShowModal() == wx.ID_OK):  # show the file browser window
                    return False
                else:
                    self.filePathName = dlg.GetPath()  # get the filepath from the save dialog

                dlg.Destroy()

        else:
            self.filePathName = os.path.join(dirName, fileName)

        return True


    # %%  ----------------------------------------------------------------------------  Save config file
    def cfgSaveAs(self):
        """
        Lets user select file and path where configuration will be saved. Saves using ConfigParser .write()
        """

        # set file types for find dialog
        wildcard = "PySolo Video config file (*.cfg)|*.cfg|" \
                   "All files (*.*)|*.*"  # adding space in here will mess it up!

        dlg = wx.FileDialog(self.parent,
                            message="Save configuration as file ...",
                            defaultDir=self.cfg_dict[0]['cfgfolder'],
                            wildcard=wildcard,
                            style=(wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        )

        if not(dlg.ShowModal() == wx.ID_OK):                     # show the file browser window
            return False

        else:
            self.filePathName = dlg.GetPath()               # get the path from the save dialog

            with open(self.filePathName, 'wb') as configfile:
                self.cfg.write(configfile)                          # ConfigParser write to file

        dlg.Destroy()
        return True

# ------------------------------------------------------------------------------  add or change cfg value in dictionary
    def setValue(self, section, key, value):
        """
        changes or adds a configuration value in config file
        """
        if not self.cfg.has_section(section):
            self.cfg.add_section(section)
        if not self.cfg.has_option(section, key):
            self.cfg.set(section, key)

        self.cfg.set(section, key, value)                   # get dictionary list index number from section name
        element_no = section[7:8]
        if element_no == '': element_no = '0'

        self.cfg_dict[int(element_no)][key] = value

# ---------------------------------------------------------- get cfg object string and convert into value of correct type
    def getValue(self, section, key):
        """
        get value from config file based on section and keyword
        Do some sanity checking to return tuple, integer and strings, datetimes, as required.
        """
        if  not self.cfg.has_option(section, key):                       # does option exist?
            r = None
            return r

        r = self.cfg.get(section, key)

        if key == 'start_datetime' :                            # order of conditional test is important! do this first!
            if type(r) == type(wx.DateTime.Now()):
                pass
            elif type(r) == type(''):                     # string -> datetime value
                try: r = self.string2wxdatetime(r)
                except: r = wx.DateTime.Now()
            elif type(r) == type(datetime.datetime.now()):
                try: r= self.pydatetime2wxdatetime(r)
                except: r = wx.DateTime.Now()
            else:
                r = wx.DateTime.Now()
                print('$$$$$$ could not interpret start_datetime value')
                return r


            return r

        if r == 'None' or r is None:                                                        # None type
            r = None
            return r

    # look for string characteristics to figure out what type they should be
        if r == 'True' or r == 'False' :                                         # boolean
            if r == 'False' :
                r = False
            elif r == 'True' :
                r = True

            return r

        try:
            int(r) == int(0)                                                   # int
            return int(r)
        except Exception:
            pass

        try:
            float(r) == float(1.1)                                              # float
            return float(r)
        except Exception:
            pass

        if ',' in r:                                                         # tuple of two integers
            if not '(' in r:
                r = '(' + r + ')'
            r = tuple(r[1:-1].split(','))
            r = (int(r[0]), int(r[1]))

            return r

        return r                                                             # all else has failed:  return as string

# --------------------------------------------------------------------- convert python datetime.datetime to wx.datetime
    def pydatetime2wxdatetime(self, pydt):
        dt_iso = pydt.isoformat()
        wxdt = wx.DateTime()
        wxdt.ParseISOCombined(dt_iso, sep='T')
        return wxdt

    def string2wxdatetime(self, strdt):
        wxdt = wx.DateTime()
        wxdt.ParseDateTime(strdt)
        return wxdt

# ------------------------------------------------------------------------------------------ Stand alone test code

class mainFrame(wx.Frame):

    def __init__(self, *args, **kwds):

        wx.Frame.__init__(self, *args, **kwds)

    # get configuration parameters and create dictionaries for each section
        cfg = Configuration(self)
        cfg_dict = cfg.cfg_dict

        print('done.')

if __name__ == "__main__":

    app = wx.App()
    wx.InitAllImageHandlers()


    frame_1 = mainFrame(None, 0, "")           # Create the main window.
    app.SetTopWindow(frame_1)                   # Makes this window the main window
    frame_1.Show()                              # Shows the main window

    app.MainLoop()                              # Begin user interactions.



