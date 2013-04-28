#!/usr/bin/env python
import wx
import wx.media
import os
from os.path import basename, splitext

class PlayPanel(wx.Panel):
	""" Control media play. """
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, wx.ID_ANY, style = wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN)

		# Create Controls
		try:
			self.mc = wx.media.MediaCtrl(self, style = wx.SIMPLE_BORDER,
										# szBackend = wx.media.MEDIABACKEND_DIRECTSHOW
										# szBackend = wx.media.MEDIABACKEND_QUICKTIME
										# szBackend = wx.media.MEDIABACKEND_WMP10
										)
		except NotImplementedError:
			self.Destroy()
			raise

		# Create wigets
		self.musicName = wx.StaticText(self, wx.ID_ANY, size = (100, -1))
		self.loadButton = wx.Button(self, wx.ID_ANY, "Load")
		self.preButton = wx.Button(self, wx.ID_ANY, "Pre")
		self.playButton = wx.Button(self, wx.ID_ANY, "Play")
		self.nextButton = wx.Button(self, wx.ID_ANY, "Next")
		self.stopButton = wx.Button(self, wx.ID_ANY, "Stop")
		self.slider = wx.Slider(self, wx.ID_ANY, 0, 0, 0)
		self.slider.SetMinSize((150, -1))

		# Initial wigets and control var
		self.isPlaying = 0
		self.musicName.SetLabel("Choose a music")

		# Bind event,methed and wigets
		self.Bind(wx.EVT_BUTTON, self.OnLoadClicked, self.loadButton)
		self.Bind(wx.EVT_BUTTON, self.OnPlayClicked, self.playButton)
		self.Bind(wx.EVT_BUTTON, self.OnStopClicked, self.stopButton)
		self.Bind(wx.EVT_SLIDER, self.OnSeek, self.slider)
		self.Bind(wx.media.EVT_MEDIA_LOADED, self.OnMediaLOaded)

		# Set the layout
		sizer = wx.GridBagSizer(3, 5)
		sizer.Add(self.mc, (1, 1)) #, flag = wx.EXPAND)
		sizer.Add(self.musicName, (1, 2), span = (1, 3))
		sizer.Add(self.loadButton, (1, 5))
		sizer.Add(self.preButton, (2, 1))
		sizer.Add(self.playButton, (2, 2))
		sizer.Add(self.nextButton, (2, 3))
		sizer.Add(self.stopButton, (2, 5))
		sizer.Add(self.slider, (3, 1), span = (1, 5),  flag = wx.EXPAND)
		self.SetSizer(sizer)

	
	def OnLoadClicked(self, evt):
		dlg = wx.FileDialog(self, message = "choose a music", 
							defaultDir = os.getcwd(), 
							defaultFile = "", 
							style = wx.OPEN | wx.CHANGE_DIR)
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
			self.DoLoadFile(path)

		dlg.Destroy()
	
	def DoLoadFile(self, path):
		self.playButton.Disable()
		if not self.mc.Load(path):
			wx.MessageBox("Unable to load %s:Unsported file format?" % path,
						"ERROR",
						wx.ICON_ERROR | wx.OK)
		else:
			self.musicName.SetLabel(self.GetName(path))
			self.SetInitialSize()
			self.GetSizer().Layout()
			self.slider.SetRange(0, self.mc.Length())
	
	def GetName(self, path):
		tt = os.path.splitext(path)[0]
		name = os.path.basename(tt)
		return name

	def OnPlayClicked(self, evt):
		if not self.mc.Play():
			wx.MessageBox("Unable to Play media: Unsupported format?",
						"ERROR",
						wx.ICON_ERROR | wx.OK)
		else:
			if self.isPlaying == 0:
				self.isPlaying = 1
				self.mc.Play()
			else:
				self.mc.Pause()
				self.isPlaying = 0
	
	#def MainCtrl(self):
	#	self.Play()

	def Play(self):
		self.mc.SetInitialSize()
		self.GetSizer().Layout()
		self.slider.SetRange(0, self.mc.Length())

	def OnStopClicked(self, evt):
		self.mc.Stop()
		self.isPlaying = 0
		
	def OnSeek(self, evt):
		offset = self.slider.GetValue()
		self.mc.Seek(offset)

	def OnMediaLOaded(self, evt):
		self.playButton.Enable()

if __name__ == "__main__":
	app = wx.App(False)
	frame = wx.Frame(None)
	panel = PlayPanel(frame)
	frame.Show()
	app.MainLoop()

