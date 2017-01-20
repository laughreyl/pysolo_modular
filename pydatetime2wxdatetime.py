import datetime, wx

def pydatetime2wxdatetime(pydt):
    dt_iso = pydt.isoformat()
    wxdt = wx.DateTime()
    wxdt.ParseISOCombined(dt_iso, sep='T')
    return wxdt


def wxdatetime2pydatetime(wxdt):
    dt_iso = wxdt.formatISOcombined()
    pydt = datetime.datetime.strptime(dt_iso, '%Y-%m-%dT%H:%M:%S.%fZ')
    return pydt

def string2wxdatetime(self, strdt):
    wxdt = wx.DateTime()
    wxdt.ParseDatetime(strdt)
