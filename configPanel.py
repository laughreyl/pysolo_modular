import wx
import os
import datetime as dt
import wx.lib.masked as masked
from filebrowsebutton_LL import FileBrowseButton, DirBrowseButton
from configurator import Configuration
from SavePrompt import saveOrNot


class configPanel(wx.Panel):
    """
    The lower half of panel one with the configuration settings
    """
    def __init__(self, parent, mon_num, cfg):

        wx.Panel.__init__(self, parent, wx.ID_ANY, pos=(20,20), size=(-1,250),
            style=wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL)

        self.parent = parent
        self.cfg = cfg
        self.cfg_dict = self.cfg.cfg_dict
        self.n_cams = self.cfg_dict[0]['webcams']
        self.n_mons = self.cfg_dict[0]['monitors']
        self.mon_num = mon_num                             # TODO: do webcams have configurations?

        self.update_cfgpanel(self.mon_num)                      # update fields from cfg_dict

    #  ###########################################################         Create items for configuration panel display
    # ---------------------------------------------------------------------------  monitor selection combobox
        self.txt_source = wx.StaticText(self, wx.ID_ANY, "Source:  ")

        if self.cfg_dict[0]['monitors'] >0 :                        # there are monitors in the config file
            self.n_mons = self.cfg_dict[0]['monitors']                   # how many?
            self.monitorList = ['Monitor %s' % (int(m)) for m in range( 1, self.n_mons+1 )]    # make list

            self.currentSource = wx.TextCtrl (self, wx.ID_ANY, self.source,            # os.path.split(self.source)[1],
                                              style=wx.TE_READONLY, size=(350, -1))    # get current source

        else:
            # if there are no monitors in the config file, create an empty monitor 1
            self.monitorList = ['Monitor 1']
            self.currentSource = wx.TextCtrl (self, wx.ID_ANY, 'No source selected',
                                              style=wx.TE_READONLY, size=(350, -1))

        self.mon_choice = wx.ComboBox(self, wx.ID_ANY, choices=self.monitorList, size=(150,-1),
                                         style=wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)   # mon_num should be 1-indexed
        self.mon_choice.Selection = self.mon_num -1                                             # initial selection is monitor 1
        self.Bind (wx.EVT_COMBOBOX, self.onChangeMonitor, self.mon_choice)

    # -----------------------------------------------------------------------------  Play & Stop Buttons
        self.btnPlay = wx.Button( self, wx.ID_FORWARD, label="Play")
        self.Bind(wx.EVT_BUTTON, self.onPlay, self.btnPlay)
        if self.currentSource != '': self.btnPlay.Enable(True)
        else: self.btnPlay.Enable(False)

        self.btnStop = wx.Button( self, wx.ID_STOP, label="Stop")
        self.Bind(wx.EVT_BUTTON, self.onStop, self.btnStop)
        self.btnStop.Enable(False)

    # ---------------------------------------------------------------------------------  Add & Remove Monitor Buttons
        self.btnAdd = wx.Button( self, wx.ID_ANY, label='Add Monitor')
        self.Bind(wx.EVT_BUTTON, self.onAddMonitor, self.btnAdd)
        if self.n_mons <9: self.btnAdd.Enable(True)
        else: self.btnAdd.Enable(False)

        self.btnDel = wx.Button( self, wx.ID_ANY, label='Remove Monitor')
        self.Bind(wx.EVT_BUTTON, self.onRemoveMonitor, self.btnDel)
        if self.n_mons >0: self.btnDel.Enable(True)
        else: self.btnDel.Enable(False)

    # ------------------------------------------------------------------------------  Video Input Selectors
        # Select source Sizer named section

        self.rb1 = wx.RadioButton(self, wx.ID_ANY, 'Camera', style=wx.RB_GROUP)          # select camera source
        self.rb2 = wx.RadioButton(self, wx.ID_ANY, 'File')                               # select video file source
        self.rb3 = wx.RadioButton(self, wx.ID_ANY, 'Folder')

        # Webcam selection combobox
        self.WebcamsList = ['Webcam %s' % (int(w) + 1) for w in range(self.n_cams)]

        self.source1 = wx.ComboBox(self, wx.ID_ANY, size=(300,-1), choices=self.WebcamsList,
                              style= wx.EXPAND | wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)

        self.source2 = FileBrowseButton(self, id=wx.ID_ANY,
                                labelText='', buttonText='Browse',
                                toolTip='Type filename or click browse to choose video file',
                                dialogTitle='Choose a video file',
                                size=(300, -1),
                                startDirectory=os.path.split(self.cfg_dict[self.mon_num]['source'])[0],
                                initialValue=self.source,                                # os.path.split(self.source)[1],
                                fileMask='*.*', fileMode=wx.ALL,
                                changeCallback=self.onChangeSource, name='videoBrowseButton')

        self.source3 = DirBrowseButton(self, id=wx.ID_ANY,                  # TODO: does this start in right directory?
                               labelText='',
                               size=(300, -1),
                               style=wx.DD_DIR_MUST_EXIST,
                               startDirectory=os.path.split(self.cfg_dict[self.mon_num]['source'])[0],
                               changeCallback=self.onChangeSource, name = 'dirBrowseButton')

        self.Bind(wx.EVT_BUTTON, self.onChangeSource, self.rb1)
        self.Bind(wx.EVT_BUTTON, self.onChangeSource, self.rb2)
        self.Bind(wx.EVT_BUTTON, self.onChangeSource, self.rb3)


        self.Bind(wx.EVT_COMBOBOX,  self.onChangeSource, self.source1)
        self.Bind(wx.EVT_TEXT,      self.onChangeSource, self.source2)
        self.Bind(wx.EVT_TEXT,      self.onChangeSource, self.source3)

        # select folder containing 2D images

        self.controls = []                                                                  # list of radio buttons and sources
        self.controls.append((self.rb1, self.source1))
        self.controls.append((self.rb2, self.source2))
        self.controls.append((self.rb3, self.source3))

        for radio, source in self.controls:
            self.Bind(wx.EVT_RADIOBUTTON, self.onChangeSource, radio)
            self.Bind(wx.EVT_TEXT, self.onChangeSource, source)
            radio.Enable(True)
            source.Enable(True)



        # ------------------------------------------------------------------------  apply to monitor button
        self.applyButton = wx.Button( self, wx.ID_APPLY)
        self.applyButton.SetToolTip(wx.ToolTip("Apply to Monitor"))
        self.Bind(wx.EVT_BUTTON, self.onApplySource, self.applyButton)

        # ----------------------------------------------------------------------------------- start date
        self.txt_date = wx.StaticText(self, wx.ID_ANY, "Date:")
        self.start_date = wx.DatePickerCtrl(self, wx.ID_ANY, dt=self.start_datetime,
                                            style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
#        self.Bind(wx.EVT_DATE_CHANGED, self.onDateTimeChanged, self.start_date)


        # ----------------------------------------------------------------------------------- start time
        self.txt_time = wx.StaticText(self, wx.ID_ANY, "Time: (24-hr)")
        self.spinbtn = wx.SpinButton(self, wx.ID_ANY, wx.DefaultPosition, (-1, 20), wx.SP_VERTICAL)
        self.start_time = masked.TimeCtrl(self, wx.ID_ANY,
                                          value=self.start_datetime,
                                          name='time: \n24 hour control', fmt24hr=True,
                                          spinButton=self.spinbtn)
#        self.Bind(masked.EVT_TIMEUPDATE, self.onDateTimeChanged, self.start_time)                                                                            # $$$$$$ - set default date to start_datetime

        # ----------------------------------------------------------------------------------- frame rate
        self.fpsTxt = wx.StaticText(self, wx.ID_ANY, 'Speed in frames per second:')
        self.fps = wx.TextCtrl(self, 0, style=wx.EXPAND | wx.ALIGN_RIGHT, size=(30, -1), value=str(self.fps))          # get current source

        # ------------------------------------------------------------------------------------- activate tracking
        self.track = wx.CheckBox(self, wx.ID_ANY, 'Activate Tracking')
#         self.track.Bind (wx.EVT_CHECKBOX, self.ontrack)

        # --------------------------------------------------------------------------------- sleep deprivation monitor
        """
        self.isSDMonitor = wx.CheckBox(self, wx.ID_ANY, 'Sleep Deprivation Monitor')
#        self.isSDMonitor.Bind ( wx.EVT_CHECKBOX, self.onSDMonitor)
        self.isSDMonitor.Enable(True)
        """

        # -------------------------------------------------------------------------------------------- tracking type
        self.trackDistance = wx.RadioButton(self, wx.ID_ANY, 'Activity as distance traveled', style=wx.RB_GROUP)
        self.trackVirtualBM = wx.RadioButton(self, wx.ID_ANY, 'Activity as midline crossings count')
        self.trackPosition = wx.RadioButton(self, wx.ID_ANY, 'Only position of flies')

        # ------------------------------------------------------------------------------------------choose mask file
        wildcard = 'PySolo Video mask file (*.msk)|*.msk|' \
                   'All files (*.*)|*.*'                # adding space in here will mess it up!
        self.pickMaskBrowser = FileBrowseButton(self,id =  wx.ID_ANY,
                                        labelText = 'Select Mask File:', buttonText = 'Browse',
                                        toolTip = 'Type filename or click browse to choose mask file',
                                        dialogTitle = 'Choose a mask file',
                                        startDirectory = os.path.split(self.cfg_dict[self.mon_num]['maskfile'])[0],
                                        initialValue = self.source[1][0:-4] + '.msk',  # os.path.split(self.source)[1][0:-4] + '.msk',
                                        fileMask = wildcard, fileMode = wx.ALL,
                                        changeCallback = None,
                                        name = 'maskBrowseButton')

        # ------------------------------------------------------------------------------------------choose output folder
        self.pickOutputBrowser = DirBrowseButton(self,id =  wx.ID_ANY,
                                        style=wx.TAB_TRAVERSAL,
                                        dialogTitle = 'Choose an output folder',
                                        startDirectory = os.path.split(self.cfg_dict[self.mon_num]['output_folder'])[0],
                                        name = 'OutputBrowseButton')

        # ---------------------------------------------------------------------------------  Save Button
        self.btnSave = wx.Button( self, wx.ID_ANY, label='Save Settings', size=(200,50))
        self.Bind(wx.EVT_BUTTON, self.onSaveSettings, self.btnSave)
        if self.currentSource != '': self.btnSave.Enable(True)
        else: self.btnSave.Enable(False)


    # ######################################################        make  Labelled boxes
        sb_selectmonitor = wx.StaticBox(self, wx.ID_ANY, 'Select Monitor')             # monitor selection box
        sbSizer_selectmonitor = wx.StaticBoxSizer(sb_selectmonitor, wx.VERTICAL)
        selectmonitorSizer_row1 = wx.BoxSizer(wx.HORIZONTAL)
        selectmonitorSizer_row2 = wx.BoxSizer(wx.HORIZONTAL)
        selectmonitorSizer_row3 = wx.BoxSizer(wx.HORIZONTAL)

        sb_videofile = wx.StaticBox(self, wx.ID_ANY, "Select Video Source")             # input video selection box
        sbSizer_videofile = wx.StaticBoxSizer(sb_videofile, wx.VERTICAL)
        sourceGridSizer = wx.FlexGridSizer(0, 2, 5, 5)

        sb_datetime = wx.StaticBox(self, wx.ID_ANY, "Video Start Date and Time")        # date time fps (top-left)
        sbSizer_datetime = wx.StaticBoxSizer (sb_datetime, wx.VERTICAL)
        dt_Sizer = wx.FlexGridSizer(3, 2, 5, 5)

        sb_track_txt = wx.StaticBox(self, wx.ID_ANY, "Set Tracking Parameters")         # tracking (top-right)
        sbSizer_trackoptions = wx.StaticBoxSizer (sb_track_txt, wx.HORIZONTAL)

        sb_calcbox = wx.StaticBox( self, wx.ID_ANY, 'Calculate fly activity as...')     # tracking type
        calcbox_sizer = wx.StaticBoxSizer(sb_calcbox, wx.VERTICAL)

        sb_mask_txt = wx.StaticBox(self, wx.ID_ANY, "Select Files")                     # mask file and output folder
        sb_mask_sizer = wx.StaticBoxSizer (sb_mask_txt, wx.VERTICAL)

        sb_Save_sizer = wx.BoxSizer(wx.VERTICAL)


    # ##################################       Put items in boxes
    # ------------------------------------------------------------------------------- Put items in select monitor box
        selectmonitorSizer_row1.Add(self.mon_choice,    2, wx.ALIGN_TOP | wx.ALL, 2)           # monitor dropdown box
        selectmonitorSizer_row1.Add(self.btnPlay,       1, wx.ALIGN_TOP | wx.ALL, 2)                 # play
        selectmonitorSizer_row1.Add(self.btnStop,       1, wx.ALIGN_TOP | wx.ALL, 2)                 # stop

        selectmonitorSizer_row2.Add(self.btnAdd,        2, wx.ALL, 2)
        selectmonitorSizer_row2.Add(self.btnDel,        2, wx.ALL, 2)
        selectmonitorSizer_row2.AddStretchSpacer(2)

        selectmonitorSizer_row3.Add(self.txt_source,        0, wx.EXPAND | wx.ALIGN_CENTER, 2)
        selectmonitorSizer_row3.Add(self.currentSource,     3, wx.EXPAND | wx.ALIGN_CENTER, 2)        # current source

        sbSizer_selectmonitor.Add(selectmonitorSizer_row1,  1, wx.EXPAND | wx.ALIGN_LEFT, 2)                                     # monitor selection box
        sbSizer_selectmonitor.Add(selectmonitorSizer_row2,  1, wx.EXPAND | wx.ALIGN_LEFT, 2)
        sbSizer_selectmonitor.AddSpacer(10)
        sbSizer_selectmonitor.Add(selectmonitorSizer_row3,  1, wx.EXPAND | wx.ALIGN_LEFT, 2)

    # ------------------------------------------------------------------------------ Put items in video source box
        for radio, source in self.controls:                                                     # video source selections
            sourceGridSizer.Add(radio,  0, wx.ALL, 2)
            sourceGridSizer.Add(source, 0, wx.ALL | wx.EXPAND, 5)

        sbSizer_videofile.Add(sourceGridSizer,  0, wx.ALL | wx.ALIGN_RIGHT, 2)
        sbSizer_videofile.Add(self.applyButton, 0, wx.ALL | wx.ALIGN_RIGHT, 2)                  # apply source button

    # ------------------------------------------------------------------------------ Put items in date time fps box
        dt_Sizer.Add(self.txt_date,   0, wx.ALL, 2)                                       # calendar
        dt_Sizer.Add(self.start_date, 0, wx.ALL, 2)

        dt_Sizer.Add(self.txt_time,   0, wx.ALL, 2)
        self.addWidgets(dt_Sizer, [self.start_time, self.spinbtn])             # clock

        dt_Sizer.Add(self.fpsTxt,   0, wx.EXPAND | wx.ALL, 2)
        dt_Sizer.Add(self.fps,      0, wx.EXPAND | wx.ALL, 2)

        sbSizer_datetime.Add(dt_Sizer, 0, wx.ALL, 2)

        # ------------------------------------------------------------------------------- Tracking Type
        calcbox_sizer.Add (self.trackDistance, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 2 )
        calcbox_sizer.Add (self.trackVirtualBM, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 2 )
        calcbox_sizer.Add (self.trackPosition, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 2 )

        # ------------------------------------------------------------------------------- Put items in tracking box
        sbSizer_trackoptions.Add (self.track, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 2 )
#        sbSizer_trackoptions.Add (self.isSDMonitor, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 2 )

        # -------------------------------------------------------------------------------- Mask file
        sb_mask_sizer.Add ( self.pickMaskBrowser , wx.EXPAND | wx.BOTTOM | wx.ALL, 2 )
        sb_mask_sizer.Add( self.pickOutputBrowser, wx.EXPAND | wx.BOTTOM | wx.ALL, 2)

        # -------------------------------------------------------------------------------- Save Add Remove buttons
        sb_Save_sizer.Add(self.btnSave, 0, wx.ALIGN_CENTER|wx.ALIGN_BOTTOM|wx.ALL, 2)

        # -------------------------------------------------------------------------------- assemble left side
        leftSideSizer = wx.BoxSizer(wx.VERTICAL)  # left side of main
        leftSideSizer.Add(sbSizer_selectmonitor, 0, wx.EXPAND | wx.TOP | wx.ALL, 2)
        leftSideSizer.AddSpacer(10)
        leftSideSizer.Add(sbSizer_videofile,     1, wx.EXPAND | wx.BOTTOM | wx.ALL, 2)

        # -------------------------------------------------------------------------------------  assemble right side top
        rightSideTopLeftSizer = wx.BoxSizer(wx.HORIZONTAL)  # top of right side
        rightSideTopLeftSizer.Add(sbSizer_datetime,         1, wx.EXPAND | wx.TOP | wx.ALL, 2)

        rightSideTopRightSizer = wx.BoxSizer(wx.VERTICAL)
        rightSideTopRightSizer.Add(sbSizer_trackoptions,    1, wx.EXPAND | wx.TOP  | wx.ALL, 2)
        rightSideTopRightSizer.Add(calcbox_sizer,           1, wx.EXPAND | wx.TOP  | wx.ALL, 2)

        rightSideTopSizer = wx.BoxSizer(wx.HORIZONTAL)
        rightSideTopSizer.Add(rightSideTopLeftSizer,        1, wx.EXPAND | wx.TOP | wx.ALL, 2)
        rightSideTopSizer.Add(rightSideTopRightSizer,       1, wx.EXPAND | wx.TOP | wx.ALL, 2)

        # -------------------------------------------------------------------------------------  assemble right side
        rightSideSizer = wx.BoxSizer(wx.VERTICAL)
        rightSideSizer.Add(rightSideTopSizer, 0, wx.EXPAND | wx.TOP | wx.ALL, 2)
        rightSideSizer.AddSpacer(15)
        rightSideSizer.Add(sb_mask_sizer, 0, wx.EXPAND | wx.TOP | wx.ALL, 2)
        rightSideSizer.AddSpacer(15)
        rightSideSizer.Add(sb_Save_sizer, 0, wx.EXPAND | wx.ALIGN_BOTTOM | wx.ALL, 2)

        # -------------------------------------------------------------------------------------- assemble whole panel
        configPanelSizer = wx.BoxSizer(wx.HORIZONTAL)  # main
        configPanelSizer.Add(leftSideSizer, 0, wx.EXPAND | wx.TOP | wx.ALL, 2)
        configPanelSizer.AddSpacer(15)
        configPanelSizer.Add(rightSideSizer, 0, wx.EXPAND | wx.TOP | wx.ALL, 2)

        self.SetSizer(configPanelSizer)
        self.Layout()



    #----------------------------------------------------------------------  used for datetime widgets
    def addWidgets(self, mainSizer ,widgets):
        """
        """
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        for widget in widgets:
            if isinstance(widget, wx.StaticText):
                sizer.Add(widget, 0, wx.ALL|wx.CENTER, 2),
            else:
                sizer.Add(widget, 0, wx.ALL, 2)
        mainSizer.Add(sizer)

    # -----------------------------------------------------------------------  Move displayed settings to the cfg_dict
    def cfg_dict_update(self):
        self.cfg_dict[self.mon_num]['mon_name'] = 'Monitor%d' % self.mon_num
        self.cfg_dict[self.mon_num]['issdmonitor'] = False  # not currently being used
        self.cfg_dict[self.mon_num]['source'] = self.source
        self.cfg_dict[self.mon_num]['fps_recording'] = self.fps.Value
        self.cfg_dict[self.mon_num]['start_datetime'] = self.start_date.Value + \
                                                        self.start_time.GetValue(as_wxTimeSpan = True)
        self.cfg_dict[self.mon_num]['track'] = self.track.Value
        self.cfg_dict[self.mon_num]['maskfile'] = self.pickMaskBrowser.GetValue()
        self.cfg_dict[self.mon_num]['output_folder'] = self.pickOutputBrowser.GetValue()

        if self.rb1.Value:
            self.cfg_dict[self.mon_num]['sourcetype'] = 0
        elif self.rb2.Value:
            self.cfg_dict[self.mon_num]['sourcetype'] = 1
        elif self.rb3.Value:
            self.cfg_dict[self.mon_num]['sourcetype'] = 2

        if self.trackDistance.Value:
            self.cfg_dict[self.mon_num]['tracktype'] = 0
        elif self.trackVirtualBM.Value:
            self.cfg_dict[self.mon_num]['tracktype'] = 1
        elif self.trackPosition.Value:
            self.cfg_dict[self.mon_num]['tracktype'] = 2

    # ---------------------------------------------------------------------- use cfg_dict to update displayed settings
    def update_cfgpanel(self,mon_num):

        self.currentSource = self.source = self.cfg_dict[self.mon_num]['source']
        self.start_datetime =   self.cfg_dict[self.mon_num]['start_datetime']
        self.fps =              self.cfg_dict[self.mon_num]['fps_recording']
        self.track =            self.cfg_dict[self.mon_num]['track']
        self.sourcetype =       self.cfg_dict[self.mon_num]['sourcetype']
        self.tracktype =        self.cfg_dict[self.mon_num]['tracktype']
        self.pickMaskBrowser =  self.cfg_dict[self.mon_num]['maskfile']
        self.pickOutputBrowser =self.cfg_dict[self.mon_num]['output_folder']
#        self.isSDMonitor =      self.cfg_dict[self.mon_num]['issdmonitor']

        try: self.start_time.SetValue(self.start_datetime)
        except: pass
        try: self.start_date.SetValue(self.start_datetime)
        except: pass

        self.rb1 = self.rb2 = self.rb3 = False
        if self.sourcetype == 0:
            self.rb1 = True
        elif self.sourcetype == 1:
            self.rb2 = True
        elif self.sourcetype == 2:
            self.rb3 == True

        self.trackDistance = self.trackVirtualBM = self.trackPosition = False
        if self.tracktype == 0:
            self.trackDistance = True
        elif self.tracktype == 1:
            self.trackVirtualBM = True
        elif self.tracktype == 2:
            self.trackPosition == True


    # -----------------------------------------------------------------------    Save cfg_dict to the Configuration obj and file
    def onSaveSettings(self, event):
        print('$$$$$$     Save the monitor cfg or revert?')
        self.cfg_dict_update()
        self.cfg.dict_to_cfgFile(self.cfg_dict)
        # update the configuration object with current settings
        self.cfg.cfgSaveAs()
    # -----------------------------------------------------------------------    Changing Monitor
    def onChangeMonitor(self, event):
        print('$$$$$$   the monitor changed')
        # ask user if should save this monitor cfg
        toSaveOrNotToSave = saveOrNot(self)

        # if cancelled, pretend this never happened,
        if not(toSaveOrNotToSave.answer):
            # otherwise...
            # if true, do onSaveSettings
            if toSaveOrNotToSave.answer:  self.onSaveSettings(event)           # true => save configuration

            # if true or none, change monitors     (none => don't save)
            self.mon_num = event + 1                            # mon_num is 1-indexed but event is 0-indexed
            self.update_cfgpanel(self.mon_num)


   # -----------------------------------------------------------------------    Changing Source
    def onChangeSource(self, event):
        print('$$$$$$    the source changed')
        # determine which rb should now be True
        # (most recently modified should be True)
    # -----------------------------------------------------------------------    Apply Source
    def onApplySource(self, event):
        print('$$$$$$     Apply the source')
        # update the currentSource
    # ------------------------------------------------------------------------   Play video
    def onPlay(self, event):
        print('$$$$$$     Play')
    # ------------------------------------------------------------------------    Stop video
    def onStop(self, event):
        print('$$$$$$     Stop')
    # ------------------------------------------------------------------------    Source Callback
    def onSourceCallback(self, event):
        print('$$$$$$     source callback')
    # ------------------------------------------------------------------------    Add monitor
    def onAddMonitor(self, event):
        print('$$$$$$     add monitor')
    # -------------------------------------------------------------------------   Remove monitor
    def onRemoveMonitor(self, event):
        print('$$$$$$     remove monitor')






# ------------------------------------------------------------------------------------------ Stand alone test code
#  insert other classes above and call them in mainFrame
#
class mainFrame(wx.Frame):

    def __init__(self, *args, **kwds):

        kwds['size'] = (1024,400)
        wx.Frame.__init__(self, *args, **kwds)


        cfg = Configuration(self, 'C:\Users\Lori\PyCharmProjects\pysolo_modular\Data\pysolo_config.cfg')
        cfg_dict = cfg.cfg_dict

        mon_num = 1

        configPanel(self, mon_num, cfg)


        print('done.')

if __name__ == "__main__":

    app = wx.App()
#    wx.InitAllImageHandlers()


    frame_1 = mainFrame(None, 0, "")           # Create the main window.
    app.SetTopWindow(frame_1)                   # Makes this window the main window
    frame_1.Show()                              # Shows the main window

    app.MainLoop()                              # Begin user interactions.

#
