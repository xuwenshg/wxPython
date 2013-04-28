#!/usr/bin/env python

import wx

class MainWindow(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title = title, size = (200, 200))
		self.control = wx.TextCtrl(self, style = wx.TE_MULTILINE)
		self.CreateStatusBar()	# A Statusbar in the Bottom of the window

		# Setup the menu
		filemenu = wx.Menu()

		# wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided py wxWidgets.
		menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", "Information about this program")
		menuExit = filemenu.Append(wx.ID_EXIT, "&Exit", "Terminate the program")
			
		# Create a menubar
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu, "&File")	# Adding the "filemenu" to the MenuBar
		self.SetMenuBar(menuBar)

		# set events
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

		self.Show(True)
	
	def OnAbout(self, e):
		dlg = wx.MessageDialog(self, "A small text editor", "About Sample Editer", wx.OK)
		dlg.ShowModal()
		dlg.Destroy()

	def OnExit(self, e):
		self.Close()
	
if __name__ == "__main__":
	app = wx.App(False)
	frame = MainWindow(None, "Sample Editer")
	app.MainLoop()
