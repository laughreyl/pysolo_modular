import wx
import os
import wx.grid as gridlib
from configurator import Configuration
from doTrack import doTrack
from filebrowsebutton_LL import FileBrowseButton, DirBrowseButton

class acquirePanel(wx.Panel):

    def __init__(self, parent, cfg, size=(800,200)):

        wx.Panel.__init__(self, parent, size=size)

        self.cfg_dict = cfg.cfg_dict
        self.n_mons = self.cfg_dict[0]['monitors']
        self.colLabels = ['Monitor', 'Track type', 'Track', 'Source', 'Mask', 'Output']

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

#        columns are: 'monitor', 'source', 'maskfile', 'output', 'tracktype', 'track'

        for mon_num in range(1, self.n_mons +1):                                # mon_num is 1-indexed
            # monitor name
            self.acqGrid.SetCellValue(mon_num - 1, 0, 'Monitor %d' % mon_num)   # row numbers are 0-indexed

            sourcefile = os.path.split(self.cfg_dict[mon_num]['source'])[1]
            self.acqGrid.SetCellValue(mon_num - 1, 3, sourcefile)

            maskfile = os.path.split(self.cfg_dict[mon_num]['maskfile'])[1]
            self.acqGrid.SetCellValue(mon_num - 1, 4, maskfile)

            # output file name
            outfolder = os.path.join(self.cfg_dict[mon_num]['datafolder'], ('Monitor%d.txt' % mon_num))
            self.acqGrid.SetCellValue(mon_num - 1, 5, outfolder)

            # track type
            tracktype = self.cfg_dict[mon_num]['tracktype']
            if tracktype == 0: tracktype = 'Distance'
            elif tracktype == 1: tracktype = 'Virtual BM'
            elif tracktype == 2: tracktype = 'Position'
            self.acqGrid.SetCellValue(mon_num - 1, 1, tracktype)

            # track
            track = self.cfg_dict[mon_num]['track']
            self.acqGrid.SetCellValue(mon_num - 1, 2, str(track))

            self.acqGrid.AutoSizeColumns(setAsMin=True)                     # set column width automatically
            self.acqGrid.EnableEditing(False)                               # user should not make changes here TODO: allow changes from Acquire?
            self.acqGrid.Fit()

# ------------------------------------------------------------------------------------------ Stand alone test code
#  insert other classes above and call them in mainFrame
#
class mainFrame(wx.Frame):

    def __init__(self, *args, **kwds):

        wx.Frame.__init__(self, None, id=wx.ID_ANY, size=(1000,200))

        cfg = Configuration(self)
        acquirePanel(self, cfg, size=(1000, 300))





        print('done.')

if __name__ == "__main__":

    app = wx.App()
    wx.InitAllImageHandlers()


    frame_1 = mainFrame(None, 0, "")           # Create the main window.
    app.SetTopWindow(frame_1)                   # Makes this window the main window
    frame_1.Show()                              # Shows the main window

    app.MainLoop()                              # Begin user interactions.

#
