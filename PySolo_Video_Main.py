import wx
from win32api import GetSystemMetrics           # to get screen resolution
from configurator import Configuration
from configPanel import configPanel
from acquirePanel import acquirePanel


class maskPanel(wx.Panel):                                  # temporary class
    """
    panel for creating a mask of ROIs
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        mainSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        tempText2 = wx.StaticText(self, wx.ID_ANY, "Mask Making Tool Panel")
        mainSizer2.Add(tempText2)
        self.SetSizer(mainSizer2)

class binningPanel(wx.Panel):                                 # temporary class
    """
    panel for creating a mask of ROIs
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        mainSizer4 = wx.BoxSizer(wx.HORIZONTAL)
        tempText4 = wx.StaticText(self, wx.ID_ANY, "Binning Panel")
        mainSizer4.Add(tempText4)
        self.SetSizer(mainSizer4)

class SCAMPPanel(wx.Panel):                                     # temporary class
    """
    panel for creating a mask of ROIs
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        mainSizer5 = wx.BoxSizer(wx.HORIZONTAL)
        tempText5 = wx.StaticText(self, wx.ID_ANY, "SCAMP Panel")
        mainSizer5.Add(tempText5)
        self.SetSizer(mainSizer5)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Main Notebook
class mainNotebook(wx.Notebook):
    """
    The main notebook containing all the panels for data displaying and analysis
    """

    def __init__(self, parent):

        wx.Notebook.__init__(self, parent, id=-1, style=wx.NB_LEFT, name='NotebookNameStr')       # initialize notebook

        self.cfg = Configuration(self)                         # get default configuration settings
        self.configPanel = configPanel(self, mon_num=1, cfg=self.cfg)                        # create configuration page
        self.AddPage(self.configPanel, 'Configuration')

        self.maskPanel = maskPanel(self)                            # create mask maker page
        self.AddPage(self.maskPanel, 'Masks')

        self.acquirePanel = acquirePanel(self, self.cfg)                      # create acquire page
        self.AddPage(self.acquirePanel, 'Acquire')

        self.binningPanel = binningPanel(self)                      # create binning page
        self.AddPage(self.binningPanel, 'DAM File Scan 110X')

        self.SCAMPPanel = SCAMPPanel(self)                          # create SCAMP page
        self.AddPage(self.SCAMPPanel, 'SCAMP')


#        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)

        self.Layout()


# ------------------------------------------------------------------------------------------ Stand alone test code
#  insert other classes above and call them in mainFrame
#
class mainFrame(wx.Frame):

    def __init__(self, *args, **kwds):

        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        thenotebook = mainNotebook(self)

        self.__set_properties("pySolo Video", 0.9)  # set title and frame/screen ratio
#        self.__menubar__()
#        self.__do_layout()
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(thenotebook, 1, wx.EXPAND, 0)
        self.SetSizer(mainSizer)

        print('done.')

# %%                                                      Set window properties
    def __set_properties(self, window_title, size_ratio):
        """
        Set the title of the main window.
        Set the size of the main window relative to the size of the user's display.
        Center the window on the screen.
        # %%                                                                            get screen height & width

        Get screen_width & screen_height:   Screen resolution information
              Allows all object sizes to be sized relative to the display.
        """
        screen_width = GetSystemMetrics(0)  # get the screen resolution of this monitor
        screen_height = GetSystemMetrics(1)

        # begin wxGlade: mainFrame.__set_properties
        self.SetTitle(window_title)  # set window title
        self.SetSize((screen_width * size_ratio,
                      screen_height * size_ratio))  # set size of window
        self.Center()  # center the window

        # %%                                                  Put notebook in window.

    def __do_layout(self):
        """
        Puts a notebook in the main window.
        """
        self.videoNotebook = mainNotebook(self, -1)

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(self.videoNotebook, 1, wx.EXPAND, 0)
        self.SetSizer(mainSizer)


# ------------------------------------------------------------------------------------- Main Program
if __name__ == "__main__":

    app = wx.App()
    wx.InitAllImageHandlers()

    frame_1 = mainFrame(None, -1, '')           # Create the main window.
    app.SetTopWindow(frame_1)                   # Makes this window the main window
    frame_1.Show()                              # Shows the main window
    app.MainLoop()                              # Begin user interactions.


