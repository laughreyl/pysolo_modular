import wx
import os
import wx.grid as gridlib
from configurator import Configuration
from doTrack import doTrack
from filebrowsebutton_LL import FileBrowseButton, DirBrowseButton

class acquirePanel(wx.Panel):

    def __init__(self, parent, cfg):

        wx.Panel.__init__(self, parent)

        self.cfg_dict = cfg.cfg_dict
        self.n_mons = self.cfg_dict[0]['monitors']
        self.colLabels = ['Monitor', 'Source', 'Mask', 'Output', 'Track type', 'Track']

    # create the table
        self.acqGrid = gridlib.Grid(self)
        self.acqGrid.CreateGrid(self.n_mons,len(self.colLabels))
        self.acqGrid.SetRowLabelSize(0)                          # no need to show row numbers
        for colnum in range(0, len(self.colLabels)):
            self.acqGrid.SetColLabelValue(colnum, self.colLabels[colnum])     # apply labels to columns

        self.updateTable()                        # fill the table using config info

        acqSizer = wx.BoxSizer(wx.VERTICAL)
        acqSizer.Add(self.acqGrid, 1, wx.EXPAND)
        self.SetSizer(acqSizer)

    def updateTable(self):

        colKeys = ['source', 'maskfile', 'datafolder', 'tracktype', 'track']

        for mon_num in range(1, self.n_mons +1):                        # mon_num is 1-indexed
            for colnum in range(0, len(self.colLabels)):

                if self.colLabels[colnum] == 'Output':
                    value = 'Monitor%d.txt' % mon_num
                else:
                    value = str(self.cfg_dict[mon_num][colKeys[colnum]])

                self.acqGrid.SetCellValue(mon_num-1, colnum, value)   # row numbers are 0-indexed

# ------------------------------------------------------------------------------------------ Stand alone test code
#  insert other classes above and call them in mainFrame
#
class mainFrame(wx.Frame):

    def __init__(self, *args, **kwds):

        wx.Frame.__init__(self, *args, **kwds)

        cfg = Configuration(self)
        acquirePanel(self, cfg)





        print('done.')

if __name__ == "__main__":

    app = wx.App()
    wx.InitAllImageHandlers()


    frame_1 = mainFrame(None, 0, "")           # Create the main window.
    app.SetTopWindow(frame_1)                   # Makes this window the main window
    frame_1.Show()                              # Shows the main window

    app.MainLoop()                              # Begin user interactions.

#
