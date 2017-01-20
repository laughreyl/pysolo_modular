import wx                               # GUI controls


class saveOrNot(wx.Dialog):
    """
    True:  Yes, save!
    False: No, go on without saving.
    None: Oops! pretend I didn't try to do that.
    """

    def __init__(self, parent, message='      Do you want to save changes to this \n     Monitor Configuration?'):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title='Save Monitor Configuration',
                           size=(100,400), style=wx.TAB_TRAVERSAL, name='saveOrNot')

        self.answer = None

        bmp = wx.ArtProvider.GetBitmap(wx.ART_WARNING, wx.ART_OTHER, (30, 30))
        warningIco = wx.StaticBitmap(self, wx.ID_ANY, bmp)

        messageToUser = wx.StaticText(self, wx.ID_ANY, message)

        self.btnSave = wx.Button( self, wx.ID_ANY, label='Save')
        self.Bind(wx.EVT_BUTTON, self.onSaveConfig, self.btnSave)

        self.btnDontSave = wx.Button( self, wx.ID_ANY, label='Don\'t Save')
        self.Bind(wx.EVT_BUTTON, self.onDontSave, self.btnDontSave)

        self.btnCancel = wx.Button( self, wx.ID_ANY, label='Cancel')
        self.Bind(wx.EVT_BUTTON, self.onCancel, self.btnCancel)

        self.wholeSizer = wx.BoxSizer(wx.VERTICAL)
        self.sbSizer_message = wx.BoxSizer(wx.HORIZONTAL)
        self.sbSizer_buttons = wx.BoxSizer(wx.HORIZONTAL)

        self.sbSizer_message.Add(warningIco,     1, wx.ALIGN_CENTER)
        self.sbSizer_message.Add(messageToUser,  4, wx.ALL | wx.ALIGN_CENTER, 2)

        self.sbSizer_buttons.Add(self.btnSave,    1, wx.ALL, 2)
        self.sbSizer_buttons.Add(self.btnDontSave,1, wx.ALL, 2)
        self.sbSizer_buttons.Add(self.btnCancel,  1, wx.ALL, 2)

        self.wholeSizer.AddSpacer(20)
        self.wholeSizer.Add(self.sbSizer_message,  1, wx.ALL | wx.ALIGN_CENTER, 2)
#        self.wholeSizer.AddSpacer(10)
        self.wholeSizer.Add(self.sbSizer_buttons, 1, wx.ALL | wx.ALIGN_CENTER, 2)

        self.SetSizer(self.wholeSizer)

    def onSaveConfig(self, event):
        print('$$$$$$ Save Configuration')
        self.answer = True

    def onDontSave(self, event):
        print('$$$$$$ Don''t save configuration')
        self.answer = False

    def onCancel(self, event):
        print('$$$$$$ Cancel')
        self.answer = None


# ------------------------------------------------------------------------------------------ Stand alone test code
#  insert other classes above and call them in mainFrame
#
class mainFrame(wx.Frame):

    def __init__(self, *args, **kwds):

        wx.Frame.__init__(self, *args, **kwds)

        toSaveOrNotToSave = saveOrNot(self)








        print('done.')

if __name__ == "__main__":

    app = wx.App()
    wx.InitAllImageHandlers()

    frame_1 = mainFrame(None, 0, "")           # Create the main window.
    app.SetTopWindow(frame_1)                   # Makes this window the main window
    frame_1.Show()                              # Shows the main window

    app.MainLoop()                              # Begin user interactions.

#
