#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       pvg_acquire.py
#
#       Copyright 2011 Giorgio Gilestro <giorgio@gilest.ro>
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
#
#

__author__ = "Giorgio Gilestro <giorgio@gilest.ro>"
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2011/08/16 21:57:19 $"
__copyright__ = "Copyright (c) 2011 Giorgio Gilestro"
__license__ = "Python"

#       Revisions by Caitlin Laughrey and Loretta E Laughrey in 2016.

# ----------------------------------------------------------------------------

pgm = 'pvg_acquire.py'
# ----------------------------------------------------------------------------

import wx, os, sys, datetime
from win32api import GetSystemMetrics    # to get screen resolution
import optparse
from wx.lib.filebrowsebutton import FileBrowseButton
import wx.grid as gridlib
import operator

from pvg_common import DEFAULT_CONFIG, root_dir, data_dir, start_dt, zero_dt
from pvg_common import pvg_config, acquireThread
from pvg_panel_one import panelOne
from pvg_options import pvg_OptionsPanel
from pvg_panel_two import panelLiveView
from pysolovideo import pySoloVideoVersion

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Global Variables
## get root dir name for all file operations
##
#import ctypes.wintypes
#CSIDL_PERSONAL = 5       # My Documents
#SHGFP_TYPE_CURRENT = 0   # Get current, not default value
#buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)  # get user document folder path
#ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
#root_dir = buf.value + '\\GitHub\\LL-DAM-Analysis\\'
#
#
#data_dir = root_dir + 'Data\\Working_files\\'
#DEFAULT_CONFIG = 'pysolo_video.cfg'
#pgm = 'pvg_acquire.py'
#start_dt = datetime.datetime(2016,8,23,13,52,17)
#t = datetime.time(19, 1, 00)                    # get datetime for adjusting from 31 Dec 1969 at 19:01:00
#d = datetime.date(1969, 12, 31)
#zero_dt = datetime.datetime.combine(d, t)
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# Not present in dev version
class customDataTable(gridlib.PyGridTableBase):
    def __init__(self, colLabels, dataTypes, useValueCleaner=True):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        gridlib.PyGridTableBase.__init__(self)
        self.useValueCleaner = useValueCleaner
        self.colLabels = colLabels
        self.dataTypes = dataTypes
        self.data = [['']*len(self.dataTypes)]
        debugprt(self,currentframe(),pgm,'end   ')
    #--------------------------------------------------
    # required methods for the wxPyGridTableBase interface

    def GetNumberRows(self):
        debugprt(self,currentframe(),pgm,'begin     ')                                           # debug

        try:
            print('$$$$$$  acquire customdatatable getnumberrows returns: ',len(self.data))
            debugprt(self,currentframe(),pgm,'end   ')
            return len(self.data)
        except:
            print('$$$$$$  acquire customdatatable getnumberrows returns: ',+str(0))
            debugprt(self,currentframe(),pgm,'end   ')
            return 0

    def GetNumberCols(self):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        # customdatatable getnumbercols')
        a = len (self.colLabels)
        debugprt(self,currentframe(),pgm,'end   ')
        return a

    def IsEmptyCell(self, row, col):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        # customdatatable isemptycell')
        try:
            a = not self.data[row][col]
            debugprt(self,currentframe(),pgm,'end   ')
            return a
        except IndexError:
            not self.data[row][col]
            debugprt(self,currentframe(),pgm,'end   ')
            return True

    def Reset(self, colLabels, dataTypes):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Re-initialise the table
        reset(colLabels, dataTypes)
        """
        n_col = self.GetNumberCols()-len(colLabels)
        if n_col > 0:
            self.GetView().ProcessTableMessage(
                        gridlib.GridTableMessage(self,
                        gridlib.GRIDTABLE_NOTIFY_COLS_DELETED,
                        1, n_col ))

            self.colLabels = colLabels
            self.dataTypes = dataTypes

        self.ClearTable()
        debugprt(self,currentframe(),pgm,'end   ')

    def ClearTable(self):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Clear the table
        """
        self.GetView().ProcessTableMessage(
                gridlib.GridTableMessage(self,
                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,
                0, self.GetNumberRows() ))
        self.data = []
        debugprt(self,currentframe(),pgm,'end   ')


    def GetValue(self, row, col):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        # customdatatable getvalue')                        # debug
        """
        (row, col)
        Get value at given coordinates
        """
        try:
            not self.data[row][col]
            a = self.data[row][col]
            debugprt(self,currentframe(),pgm,'end   ')
            return a
        except IndexError:
            not self.data[row][col]
            debugprt(self,currentframe(),pgm,'end   ')
            return ''

    def InsertColumn(self, col_pos, col_type=gridlib.GRID_VALUE_FLOAT+':6,2', col_label=''):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Add one grid column before col_pos, with type set to col_type and label col_label
        """
        debugprt(self,currentframe(),pgm,'end   ')

    def transpose(whole_table):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        a = map(lambda *row: list(row), *whole_table)
        debugprt(self,currentframe(),pgm,'%%% REMAINDER OF TRANSPOSE NOT DONE.    end   ')
        return a

        empty_col = [''] * self.GetNumberCols()                                   #  What's This ????

        if self.GetNumberRows() > 0:
            t_data = transpose(self.data)
            t_data.insert(col_pos, empty_col)
            self.data = transpose(t_data)

        self.dataTypes.insert(col_pos, col_type)
        self.colLabels.insert(col_pos, col_label)


        self.GetView().ProcessTableMessage(
                gridlib.GridTableMessage(self,
                gridlib.GRIDTABLE_NOTIFY_COLS_INSERTED,
                col_pos, 1         ))
        debugprt(self,currentframe(),pgm,'end   ')


    def Sort(self, bycols, descending=False):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        sort the table by multiple columns
            bycols:  a list (or tuple) specifying the column numbers to sort by
                   e.g. (1,0) would sort by column 1, then by column 0
            descending: specify sorting order
        """

        table = self.data

        for col in reversed(bycols):
            table = sorted(table, key=operator.itemgetter(col))

        if descending:
           table.reverse()

        self.data = table

        msg=wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        self.GetView().ProcessTableMessage(msg)
        debugprt(self,currentframe(),pgm,'end   ')

    def AddRow (self, rows):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Add one or more rows at the bottom of the table / sheet
        row can be an array of values or a 2-dimenstional array of rows and values
        """
        rows = self.cleanFromMask(rows)
        print('$$$$$$  rows = ',rows)

        if type(rows[0]) == list:
            n_rows = len (rows)
            for row in rows: self.data.append(row)
        else:
            self.data.append(rows)
            n_rows = 1

        self.GetView().ProcessTableMessage(
                gridlib.GridTableMessage(self,
                gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED,
                n_rows         ))

        print('$$$$$$ rows appended')
        debugprt(self,currentframe(),pgm,'end   ')

    def RemRow (self, rows):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Remove one or more rows
        """

        [self.data.pop(int(x)-1) for x in rows]

        self.GetView().ProcessTableMessage(
                gridlib.GridTableMessage(self,
                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,
                len(rows)         ))
        debugprt(self,currentframe(),pgm,'end   ')

    def SetData(self, data=None):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Set the whole content of the table to data
        """
        data = self.cleanFromMask(data)
        self.ClearTable()
        self.data = data
        n_rows = self.GetNumberRows()
        self.GetView().ProcessTableMessage(
                gridlib.GridTableMessage(self,
                gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED,
                n_rows ))

        self.GetView().ProcessTableMessage(
                gridlib.GridTableMessage(None,
                gridlib.GRIDTABLE_REQUEST_VIEW_GET_VALUES))
        debugprt(self,currentframe(),pgm,'end   ')

    def SetRow (self, row, data):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        data = self.cleanFromMask(data)
        try:
            self.data[row] = data
        except:
            self.AddRow(data)
        debugprt(self,currentframe(),pgm,'end   ')

    def SetValue(self, row, col, value):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        # setvalue')                                             # debug
        """
        (row, col, value)
        Set Value for cell at given coordinates
        """
        try:
            self.data[row][col] = value
        except IndexError:
            # add a new row
            self.data.append([''] * self.GetNumberCols())
            self.SetValue(row, col, value)

            # tell the grid we've added a row
            self.GetView().ProcessTableMessage(
                    gridlib.GridTableMessage(self,
                    gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED,
                    1                    ) )
        debugprt(self,currentframe(),pgm,'end   ')

    #--------------------------------------------------
    # Some optional methods

    def GetColLabelValue(self, col):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        # getcollabelvalue')
        """
        Called when the grid needs to display labels
        """
        a = self.colLabels[col]
        print('$$$$$$  colLabels[col] = ',self.colLabels[col])
        debugprt(self,currentframe(),pgm,'end   ')
        return self.colLabels[col]


    def GetTypeName(self, row, col):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        # customdatatable gettypename')                         # debug
        """
        Called to determine the kind of editor/renderer to use by
        default, doesn't necessarily have to be the same type used
        natively by the editor/renderer if they know how to convert.
        """
        a = self.dataTypes[col]
        debugprt(self,currentframe(),pgm,'end   ')
        print('\n\t\t returns: ',a)
        return a


    def CanGetValueAs(self, row, col, typeName):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        # cangetvalueas')                           # debug
        """
        Called to determine how the data can be fetched and stored by the
        editor and renderer.  This allows you to enforce some type-safety
        in the grid.
        """
        colType = self.dataTypes[col].split(':')[0]
        if typeName == colType:
            debugprt(self,currentframe(),pgm,'end   ')
            print('$$$$$$ CamGetValueAs returns: True')
            return True
        else:
            debugprt(self,currentframe(),pgm,'end   ')
            print('$$$$$$ CamGetValueAs returns: False')
            return False

    def CanSetValueAs(self, row, col, typeName):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        # cansetvalueas')                                             # debug
        a = self.CanGetValueAs(row, col, typeName)
        debugprt(self,currentframe(),pgm,'end   ')
        return a

    def cleanFromMask(self, l):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Goes through the list l and make sure it doesn't contain
        any masked value
        """
        if self.useValueCleaner:
            try:
                if type(l[0]) == list:

                    for r in range(len(l)):
                        l[r] = self.cleanFromMask(l[r])
                else:

                    for c in range (len(l)):
                        if np.ma.getmask(l[c]): l[c] = '--'
                        if type(l[c]) != str and l[c] >= 999999: l[c] = '--'
            except:
                pass

        debugprt(self,currentframe(),pgm,'end   ')
        return l


class CustTableGrid(gridlib.Grid):
    """
    This class describes a CustomGrid. Data are handled thorough a table but
    functions for the table are proxied from here
    """
    def __init__(self, parent, colLabels, dataTypes, enableEdit = False, useValueCleaner=True, useMenu=True):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug

        gridlib.Grid.__init__(self, parent, -1)
        self.table = customDataTable(colLabels, dataTypes, useValueCleaner)
        self.SetTable(self.table, True)
        self.EnableEditing(enableEdit)
        self.SetColMinimalAcceptableWidth(0)
        self.SetRowMinimalAcceptableHeight(0)
        self.checkableItems = self.table.dataTypes.count('bool') > 0

        self.sortedColumn=1
        self.sortedColumnDescending=False
        self.CtrlDown = False

        # we draw the column headers
        # code based on original implementation by Paul Mcnett
        #wx.EVT_PAINT(self.GetGridColLabelWindow(), self.OnColumnHeaderPaint)

        self.SetRowLabelSize(30)
        self.SetMargins(0,0)
        self.Bind(gridlib.EVT_GRID_LABEL_LEFT_CLICK, self.OnSort)
        #self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnLeftClick)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        #self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnLeftDClick)

        if useMenu: self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.OnContextMenu)
        debugprt(self,currentframe(),pgm,'end   ')

    def OnColumnHeaderPaint(self, evt):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        w = self.GetGridColLabelWindow()
        dc = wx.PaintDC(w)
        clientRect = w.GetClientRect()
        font = dc.GetFont()

        # For each column, draw it's rectangle, it's column name,
        # and it's sort indicator, if appropriate:
        #totColSize = 0
        totColSize = -self.GetViewStart()[0]*self.GetScrollPixelsPerUnit()[0] # Thanks Roger Binns
        for col in range(self.GetNumberCols()):
            dc.SetBrush(wx.Brush("WHEAT", wx.TRANSPARENT))
            dc.SetTextForeground(wx.BLACK)
            colSize = self.GetColSize(col)
            rect = (totColSize,0,colSize,32)
            dc.DrawRectangle(rect[0] - (col<>0 and 1 or 0), rect[1],
                             rect[2] + (col<>0 and 1 or 0), rect[3])
            totColSize += colSize

            if col == self.sortedColumn:
                font.SetWeight(wx.BOLD)
                # draw a triangle, pointed up or down, at the
                # top left of the column.
                left = rect[0] + 3
                top = rect[1] + 3

                dc.SetBrush(wx.Brush("WHEAT", wx.SOLID))
                if self.sortedColumnDescending:
                    dc.DrawPolygon([(left,top), (left+6,top), (left+3,top+4)])
                else:
                    dc.DrawPolygon([(left+3,top), (left+6, top+4), (left, top+4)])
            else:
                font.SetWeight(wx.NORMAL)

            dc.SetFont(font)
            dc.DrawLabel("%s" % self.GetTable().colLabels[col],
                     rect, wx.ALIGN_CENTER | wx.ALIGN_TOP)
        debugprt(self,currentframe(),pgm,'end   ')



    def Reset(self, *args, **kwargs):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Reinitialize the table
        """

        self.table.Reset(*args, **kwargs)
        self.AutoSizeColumns()
        debugprt(self,currentframe(),pgm,'end   ')

    def InsertCol (self, *args, **kwargs):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        (self, col_pos, col_type=gridlib.GRID_VALUE_FLOAT+':6,2', col_label='')
        Add one grid column before col_pos, with type set to col_type and label col_label
        """

        self.table.InsertColumn (*args, **kwargs)
        self.AutoSizeColumns()
        debugprt(self,currentframe(),pgm,'end   ')


    def SetColsSize(self, cols_size):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        """
        for col in range(len(cols_size)):
            self.SetColSize(col, cols_size[col])
        debugprt(self,currentframe(),pgm,'end   ')

    def GetData (self):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Return a bidimensional array with a copy
        of the data in the spreadsheet
        """
        all_data = self.table.data
        for row in range(len(all_data)):
            for col in range (len(all_data[row])):
                try:
                    all_data[row][col] = all_data[row][col].strip()
                except:
                    pass

        a = all_data
        debugprt(self,currentframe(),pgm,'end   ')
        print('$$$$$$  GetData returns: ',a)
        return a

    def SetData(self, *kargs, **kwargs):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        (data)
        Set the data of the table to the given value
        data is a bidimensional array
        """
        self.table.SetData(*kargs, **kwargs)
        self.AutoSizeColumns()
        debugprt(self,currentframe(),pgm,'end   ')

    def GoToEnd(self):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Go to the end of the table
        """
        while self.MovePageDown():
            pass
        debugprt(self,currentframe(),pgm,'end   ')

    def AddRow(self, *kargs, **kwargs):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Add one or more rows at the bottom of the table / sheet
        row can be an array of values or a 2-dimenstional array of rows and values
        """

        self.table.AddRow(*kargs, **kwargs)
        self.AutoSizeColumns()
        #row = self.GetNumberRows()
        #self.GoToEnd()
        debugprt(self,currentframe(),pgm,'end   ')

    def RemRow(self, *kargs, **kwargs):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Add one or more rows at the bottom of the table / sheet
        row can be an array of values or a 2-dimenstional array of rows and values
        """

        self.table.RemRow(*kargs, **kwargs)
        self.AutoSizeColumns()
        row = self.GetNumberRows()
        debugprt(self,currentframe(),pgm,'end   ')

    def GetNumberRows(self, *kargs, **kwargs):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Return the number of Rows
        """
        a = self.table.GetNumberRows ()
        debugprt(self,currentframe(),pgm,'end   ')
        return a

    def GetNumberCols(self, *kargs, **kwargs):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Return the number of cols
        """
        a = self.table.GetNumberCols ()
        debugprt(self,currentframe(),pgm,'end   ')
        return a

    def HideCol(self, col):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        (col)
        Hide the specified column by setting its size to 0
        """
        self.SetColSize(col, 0)
        debugprt(self,currentframe(),pgm,'end   ')

    def OnKeyUp(self, event):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Records whether the Ctrl Key is up or down
        """
        if event.GetKeyCode() == 308:
            self.CtrlDown = False
        event.Skip()
        debugprt(self,currentframe(),pgm,'end   ')

    def OnKeyDown(self, event):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Responds to the following keys:
        Enter -> Jumps to next cell
        Ctrl-C -> Copy selected cells
        """

        if event.GetKeyCode() == 308:
            self.CtrlDown = True
            event.Skip()

        if self.CtrlDown and event.GetKeyCode() == 67:
            self.OnCopySelected(event)
            event.Skip()

        if event.GetKeyCode() != wx.WXK_RETURN:
            event.Skip()
            debugprt(self,currentframe(),pgm,'end   ')
            return

        if event.ControlDown():   # the edit control needs this key
            event.Skip()
            debugprt(self,currentframe(),pgm,'end   ')
            return

        self.DisableCellEditControl()

        while 1 == 1:
            success = self.MoveCursorRight(event.ShiftDown())
            size_of_current_col = self.GetColSize(self.GetGridCursorCol())
            if size_of_current_col != 0 or not success:
                 debugprt(self,currentframe(),pgm,'end   ')
                 break

        if not success:
            newRow = self.GetGridCursorRow() + 1

            if newRow < self.GetTable().GetNumberRows():
                self.SetGridCursor(newRow, 0)
                self.MakeCellVisible(newRow, 0)
            else:
                #Add a new row here?
                pass

        debugprt(self,currentframe(),pgm,'end   ')



    def OnLeftClick(self, event):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        On mouse click checks if the cell contain a checkbox and if it does
        will change its status
        """
        self.ForceRefresh()
        debugprt(self,currentframe(),pgm,'end   ')


    def OnSort(self, event):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Clicking on the label of the columns sorts data in one order, a second click reverses the order.
        """
        col = event.GetCol()
        if col >= 0:
            if col==self.sortedColumn:
                self.sortedColumnDescending=not self.sortedColumnDescending
            else:
                self.sortedColumn=col
                self.sortedColumnDescending=False

            sorting_order = range(self.GetNumberCols())
            sorting_order.pop(col)
            sorting_order = [col] + sorting_order

            self.table.Sort( sorting_order, self.sortedColumnDescending)
            self.Refresh()
            debugprt(self,currentframe(),pgm,'end   ')   #


    def OnContextMenu(self, event):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Creates and handles a popup menu
        """
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.popupID3 = wx.NewId()
            self.popupID4 = wx.NewId()
            self.popupID5 = wx.NewId()

            self.Bind(wx.EVT_MENU, self.OnCopyAll, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnCopyRow, id=self.popupID2)
            self.Bind(wx.EVT_MENU, self.OnCopyCol, id=self.popupID3)
            self.Bind(wx.EVT_MENU, self.OnCopySelected, id=self.popupID4)
            self.Bind(wx.EVT_MENU, self.OnExportToFile, id=self.popupID5)


        # make a menu
        menu = wx.Menu()
        menu.Append(self.popupID1, "Copy All")
        menu.Append(self.popupID2, "Copy Current Row")
        menu.Append(self.popupID3, "Copy Current Column")
        menu.Append(self.popupID4, "Copy Selected")
        menu.Append(self.popupID5, "Export All to file")

        #Add this voice only if the table has checkable items
        if self.checkableItems:
            self.popupID6 = wx.NewId()
            self.popupID7 = wx.NewId()
            self.Bind(wx.EVT_MENU, partial(self.OnCheckUncheckItems, True ), id=self.popupID6)
            self.Bind(wx.EVT_MENU, partial(self.OnCheckUncheckItems, False ), id=self.popupID7)
            menu.AppendSeparator()
            menu.Append(self.popupID6, "Check Selected")
            menu.Append(self.popupID7, "Uncheck Selected")
            #menu.Append(self.popupID8, "Remove Selected")


        self.PopupMenu(menu)
        menu.Destroy()
        debugprt(self,currentframe(),pgm,'end   ')   #

    def OnCopyCol(self, event):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Copy to clipboard the content of the entire currently
        selected column, including the column label
        """
        self.SelectCol(self.GetGridCursorCol())
        content = wx.TextDataObject()
        content.SetText(self.DataToCSV('\t', onlySel = True))
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(content)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Unable to open the clipboard", "Error")
        debugprt(self,currentframe(),pgm,'end   ')   #

    def OnCopyRow(self, event):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Copy to clipboard the content of the entire currently
        selected row
        """
        self.SelectRow(self.GetGridCursorRow())
        content = wx.TextDataObject()
        content.SetText(self.DataToCSV('\t', onlySel = True))
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(content)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Unable to open the clipboard", "Error")
        debugprt(self,currentframe(),pgm,'end   ')   #

    # I do this because I don't like the default behaviour of not starting the
    # cell editor on double clicks, but only a second click.
    def OnLeftDClick(self, evt):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        if self.CanEnableCellControl():
            self.EnableCellEditControl()
        debugprt(self,currentframe(),pgm,'end   ')   #

    def OnCopyAll(self, event):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Copy the all table to clipboard
        """
        content = wx.TextDataObject()
        content.SetText(self.DataToCSV('\t'))
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(content)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Unable to open the clipboard", "Error")
        debugprt(self,currentframe(),pgm,'end   ')   #

    def OnCopySelected(self, event):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Copy selected cells to system clipboard
        """
        content = wx.TextDataObject()
        content.SetText(self.DataToCSV('\t', onlySel = True))
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(content)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Unable to open the clipboard", "Error")
        debugprt(self,currentframe(),pgm,'end   ')   #

    def OnExportToFile(self, event):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Save away the content of the grid as CSV file
        """
        wildcard = 'CSV files (*.csv)|*.csv|All files (*.*)|*.*'
        dlg = wx.FileDialog(self, 'Choose a file', '', '', wildcard, wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            filename=dlg.GetFilename()
            dirname=dlg.GetDirectory()
            filehandle=open(os.path.join(dirname, filename),'w')
            filehandle.write(self.DataToCSV(','))
            filehandle.close()
        dlg.Destroy()
        debugprt(self,currentframe(),pgm,'end   ')   #

    def DataToCSV(self, separator=',', onlySel = False):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Convert the data in the grid to CSV value format (or equivalent)
        """
        csv = ''
        r, c = 0, 0

        all_content = [self.table.colLabels] + self.table.data

        for row in all_content:
            c = 0
            notEmptyLine = ''
            for cell in row:
                if not(onlySel) or self.IsInSelection(r-1, c):
                    csv += str(cell)+separator
                    notEmptyLine = '\n'
                c+=1
            csv += notEmptyLine
            r +=1
        debugprt(self,currentframe(),pgm,'end   ')   #
        return csv

    def OnCheckUncheckItems(self, check_value, event):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Check uncheck all checkable items in the selected rows
        """
        c = self.table.dataTypes.index('bool')
        r = 0

        for row in self.table.data:
            if self.IsInSelection(r,c):
                self.table.SetValue(r,c, check_value)
            r += 1
        self.ForceRefresh()
        debugprt(self,currentframe(),pgm,'end   ')   #

class pvg_AcquirePanel(wx.Panel):
    def __init__(self, parent):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug

        wx.Panel.__init__(self, parent, wx.ID_ANY)
        self.parent = parent

        print('$$$$$$  changing to dir: '+data_dir)                         # debug
        os.chdir(data_dir)                    # debug
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.FBconfig = FileBrowseButton(self, -1, labelText='Pick file', size=(300,-1), changeCallback = self.configCallback)

        print('$$$$$$   file browse button created')
        colLabels = ['Monitor', 'Source', 'Mask', 'Output', 'Track type', 'Track']

        dataTypes = [gridlib.GRID_VALUE_NUMBER,
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_BOOL,
                          ]

        self.grid = CustTableGrid(self, colLabels, dataTypes, enableEdit=True, useMenu=False)

        print('$$$$$$  grid created by custtablegrid')
        self.grid.Clear()

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.startBtn = wx.Button(self, wx.ID_ANY, 'Start')
        self.stopBtn = wx.Button(self, wx.ID_ANY, 'Stop')
        self.stopBtn.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.onStop, self.stopBtn)
        self.Bind(wx.EVT_BUTTON, self.onStart, self.startBtn)

        print('$$$$$$ start and stop buttons are bound')
        btnSizer.Add (self.startBtn, 0, wx.ALL, 5)
        btnSizer.Add (self.stopBtn, 0, wx.ALL, 5)


        mainSizer.Add(self.FBconfig, 0, wx.EXPAND|wx.ALL, 5)
        mainSizer.Add(self.grid, 1, wx.EXPAND, 0)
        mainSizer.Add(btnSizer, 0, wx.ALL, 5)
        self.SetSizer(mainSizer)

        print('$$$$$$ sizer completed')
        debugprt(self,currentframe(),pgm,'end   ')   #

    def configCallback(self, event):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        """
        self.loadFile( self.FBconfig.GetValue() )
        debugprt(self,currentframe(),pgm,'end   ')   #


    def loadFile(self, filename):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        """
        print('$$$$$$  filename = ',filename)
        self.options = pvg_config(filename)
        print("$$$$$$ options = ",self.options)
        self.updateTable()
        print("$$$$$$ table updated")
        self.parent.sb.SetStatusText('Loaded file %s' % filename)
        print("$$$$$$ status bar message changed")
        debugprt(self,currentframe(),pgm,'end   ')   #
        return True

    def updateTable(self):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        """
        monitorsData = self.options.getMonitorsData()

        self.grid.Clear()
        self.monitors = {}

        for mn in monitorsData:

            m = monitorsData[mn]

            try:
                s = os.path.split( m['source'] )[1]
            except:
                s = 'Camera %02d' % ( m['source'] + 1 )

            mf = os.path.split(m['mask_file'])[1]
            df = 'Monitor%02d.txt' % (mn+1)
            row = [mn, s, mf, df, m['track_type'], m['track'] ]
            self.grid.AddRow(row)


        for mn in monitorsData:    # collects specs for monitors from config
            m = monitorsData[mn]
            self.monitors[mn] = ( acquireThread(mn, m['source'],
                                                m['resolution'],
                                                m['mask_file'],
                                                m['track'],
                                                m['track_type'],
                                                m['dataFolder']) )
            print('$$$$$$ mm = ', mn, '\n options = ', self.monitors[mn], '\n m = ', m)                                                 # debug
        debugprt(self,currentframe(),pgm,'end   ')   #

    def isToTrack(self, monitor):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        """
        d = self.grid.GetData()

        print('$$$$$$  isToTrack  monitor = ',monitor)                                                              # debug
        for row in d:
            print ('$$$$$$ isToTrack row in d = ',row)                                                           # debug
            print('$$$$$$  istotrack row[0] = ',row[0])
            if monitor == row[0]:
                print('$$$$$$ isToTrack row[-1] = ',row[-1])
                debugprt(self,currentframe(),pgm,'end   ')   #
                return row[-1]
        debugprt(self,currentframe(),pgm,'end   ')   #

    def onStart(self, event=None):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        """
        print('$$$$$$  Start button clicked')
        self.acquiring = True
        self.stopBtn.Enable(self.acquiring)
        self.startBtn.Enable(not self.acquiring)
        c = 0

        print('$$$$$$  onStart monitors:  ',self.monitors)
        for mon in self.monitors:
            print('\n $$$$$$ c is ',c)
            print('\n $$$$$$      mon:   ',mon)
            if self.isToTrack(mon):

                print('\n$$$$$$            mon istotrack is true')
                self.monitors[mon].doTrack()

                print('\n $$$$$$ tracking done')
                c+=1

        self.parent.sb.SetStatusText('Tracking %s Monitors' % (str(int(c))))
        debugprt(self,currentframe(),pgm,'end   ')   #

    def onStop(self, event):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        """
        print('$$$$$$   stop clicked')
        self.acquiring = False
        self.stopBtn.Enable(self.acquiring)
        self.startBtn.Enable(not self.acquiring)
        for mon in self.monitors:
            self.monitors[mon].halt()

        self.parent.sb.SetStatusText('All tracking is now stopped')
        debugprt(self,currentframe(),pgm,'end   ')   #

class acquireFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        debugprt(self,currentframe(),pgm,'begin     ')        #
        kwargs["size"] = (800, 600)

        wx.Frame.__init__(self, *args, **kwargs)

        self.sb = wx.StatusBar(self, wx.ID_ANY)
        self.SetStatusBar(self.sb)

        self.acq_panel =  pvg_AcquirePanel(self)
        debugprt(self,currentframe(),pgm,'end   ')   #

    def loadConfig(self, filename=None):
        """
        """
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        # acquireframe loadConfig '+filename)                   # debug
        if ~os.path.isfile(filename):

            if filename is None:
                print(os.environ['HOME'])
                pDir = os.environ['HOME']
                filename = os.path.join (pDir, DEFAULT_CONFIG)
                filename = DEFAULT_CONFIG
        print('$$$$$$   loadconfig  filename = ',filename)
        self.acq_panel.loadFile(filename)
        debugprt(self,currentframe(),pgm,'end   ')   #
        return True

    def Start(self):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        """
        self.acq_panel.onStart()
        debugprt(self,currentframe(),pgm,'end   ')   #


if __name__ == '__main__':
    parser = optparse.OptionParser(usage='%prog [options] [argument]', version='%prog version 1.0')
    parser.add_option('-c', '--config', dest='config_file', metavar="CONFIG_FILE", help="The full path to the config file to open")
    parser.add_option('--acquire', action="store_true", default=False, dest='acquire', help="Start acquisition when the program starts")
    parser.add_option('--nogui', action="store_false", default=True, dest='showgui', help="Do not show the graphical interface")

    (options, args) = parser.parse_args()
#    app=wx.PySimpleApp(0)
    app=wx.App(0)
    frame_acq = acquireFrame(None, -1, "")           # Create the main window.
    app.SetTopWindow(frame_acq)
    frame_acq.Show(options.showgui)

    configfile = DEFAULT_CONFIG
    cfgloaded = frame_acq.loadConfig(configfile)

    if cfgloaded and options.acquire:
        frame_acq.Start()

    app.MainLoop()              # don't step into this
