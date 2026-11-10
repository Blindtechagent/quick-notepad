import os
import winsound

import wx

class Menu:
	def __init__(self, frame):
		self.frame = frame
		self.menuBar = wx.MenuBar()
		self.frame.SetMenuBar(self.menuBar)

	def add_menu(self, name):
		menu = wx.Menu()
		self.menuBar.Append(menu, f"&{name}")
		return menu

class NewFrame(wx.Frame):
	def __init__(self):
		super().__init__(None, title="Quick Notepad", size=(900, 700))
		self.isModified = False
		self.file_path = None
		self.CreateStatusBar()
		self.update_title()
		panel = wx.Panel(self)

		self.editField = wx.TextCtrl(
			panel,
			style=wx.TE_MULTILINE | wx.TE_RICH2 | wx.TE_WORDWRAP
		)
		font = wx.Font(14, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName="Consolas")
		self.editField.SetFont(font)
		self.editField.SetMargins(wx.Point(10, 10))
		self.editField.Bind(wx.EVT_TEXT, self.on_text_changed)
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.editField, 1, wx.EXPAND | wx.ALL, 8)
		panel.SetSizer(sizer)

		menu = Menu(self)
		fileMenu = menu.add_menu("File")
		self.newBtn = fileMenu.Append(wx.ID_NEW, "&New\tCtrl+N")
		self.openBtn = fileMenu.Append(wx.ID_OPEN, "&Open...\tCtrl+O")
		fileMenu.AppendSeparator()
		self.saveBtn = fileMenu.Append(wx.ID_SAVE, "&Save\tCtrl+S")
		self.saveAsBtn = fileMenu.Append(wx.ID_ANY, "&Save as\tCtrl+Shift+S")
		fileMenu.AppendSeparator()
		self.closeBtn = fileMenu.Append(wx.ID_EXIT, "&Close\tCtrl+W")
		self.Bind(wx.EVT_MENU, self.new_file, self.newBtn)
		self.Bind(wx.EVT_MENU, self.open_file, self.openBtn)
		self.Bind(wx.EVT_MENU, self.try_save, self.saveBtn)
		self.Bind(wx.EVT_MENU, self.save_as, self.saveAsBtn)
		self.Bind(wx.EVT_MENU, lambda e: self.Close(), self.closeBtn)
		self.Bind(wx.EVT_CLOSE, self.close)
		editMenu = menu.add_menu("Edit")
		self.undoBtn = editMenu.Append(wx.ID_UNDO, "&Undo\tCtrl+Z")
		self.redoBtn = editMenu.Append(wx.ID_REDO, "&Redo\tCtrl+Y")
		editMenu.AppendSeparator()
		self.cutBtn = editMenu.Append(wx.ID_CUT, "Cu&t\tCtrl+X")
		self.copyBtn = editMenu.Append(wx.ID_COPY, "&Copy\tCtrl+C")
		self.pasteBtn = editMenu.Append(wx.ID_PASTE, "&Paste\tCtrl+V")
		self.deleteBtn = editMenu.Append(wx.ID_DELETE, "&Delete\tDel")
		editMenu.AppendSeparator()
		self.selectAllBtn = editMenu.Append(wx.ID_SELECTALL, "Select &All\tCtrl+A")
		self.Bind(wx.EVT_MENU, lambda e: self.editField.Undo(), self.undoBtn)
		self.Bind(wx.EVT_MENU, lambda e: self.editField.Redo(), self.redoBtn)
		self.Bind(wx.EVT_MENU, lambda e: self.editField.Cut(), self.cutBtn)
		self.Bind(wx.EVT_MENU, lambda e: self.editField.Copy(), self.copyBtn)
		self.Bind(wx.EVT_MENU, lambda e: self.editField.Paste(), self.pasteBtn)
		self.Bind(wx.EVT_MENU, lambda e: self.editField.Remove(*self.editField.GetSelection()), self.deleteBtn)
		self.Bind(wx.EVT_MENU, lambda e: self.editField.SelectAll(), self.selectAllBtn)
		toolsMenu = menu.add_menu("Tools")
		textAnalysisBtn = toolsMenu.Append(wx.ID_ANY, "Analyse Text")
		self.Bind(wx.EVT_MENU, self.analyse_text, textAnalysisBtn)
		settingsMenu = menu.add_menu("Settings")
		themeBtn = settingsMenu.Append(wx.ID_ANY, "Theme")
		fontBtn = settingsMenu.Append(wx.ID_ANY, "Font\tCtrl+D")
		self.Bind(wx.EVT_MENU, self.theme_selection, themeBtn)
		self.Bind(wx.EVT_MENU, self.change_font, fontBtn)
		helpMenu = menu.add_menu("Help")
		helpBtn = helpMenu.Append(wx.ID_HELP, "Show &Help")
		aboutBtn = helpMenu.Append(wx.ID_ABOUT, "About")
		self.Bind(wx.EVT_MENU, self.show_help, helpBtn)
		self.Bind(wx.EVT_MENU, self.show_about, aboutBtn)


	def on_text_changed(self, event):
		if not self.isModified:
			self.isModified = True
			self.update_title()
		event.Skip()

	def new_file(self, event):
		if not self.confirm_discard_changes():
			return
		self.editField.Clear()
		self.file_path = None
		self.isModified = False
		self.update_title()

	def open_file(self, event):
		with wx.FileDialog(
			self,
			"Open Text File",
			wildcard="Text files (*.txt)|*.txt|All files (*.*)|*.*",
			style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
		) as dialog:

			if dialog.ShowModal() == wx.ID_CANCEL:
				return

			file_path = dialog.GetPath()

			with open(file_path, "r", encoding="utf-8") as file:
				content = file.read()
		if not self.confirm_discard_changes():
			return
		self.file_path = file_path
		self.editField.SetValue(content)
		self.isModified = False
		self.update_title()
		self.SetStatusText("Opened")

	def try_save(self, event):
		if self.file_path is None:
			self.save_as()
		else:
			self.save()

	def save(self):
		with open(self.file_path, "w", encoding="utf-8") as file:
			file.write(self.editField.GetValue())
		self.isModified = False
		self.update_title()
		self.SetStatusText("Saved!")
		winsound.Beep(1000, 150)
		wx.CallLater(1500, lambda: self.SetStatusText(""))

	def save_as(self, event=None):
		with wx.FileDialog(
			self,
			"Save Text File",
			wildcard="Text files (*.txt)|*.txt",
			style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
		) as dialog:
			if dialog.ShowModal() == wx.ID_CANCEL:
				return
			self.file_path = dialog.GetPath()
			self.update_title()
		self.save()

	def close(self, event):
		if self.confirm_discard_changes():
			event.Skip()

	def confirm_discard_changes(self):
		if not self.isModified:
			return True
		result = wx.MessageBox(
			"The changes are not saved. Discard them?",
			"Confirmation",
			wx.YES_NO | wx.ICON_QUESTION
		)
		return result == wx.YES

	def update_title(self):
		if self.file_path is None:
			self.SetTitle("Untitled - Quick Notepad")
		else:
			filename = os.path.basename(self.file_path)
			prefix = "*" if self.isModified else ""
			self.SetTitle(f"{prefix}{filename} - Quick Notepad")

	def theme_selection(self, event):
		themeDlg = wx.SingleChoiceDialog(
			self,
			"Select Theme",
			"Theme Selection",
			["light", "dark"]
		)
		if themeDlg.ShowModal() == wx.ID_OK:
			if themeDlg.GetStringSelection() == 'light':
				self.editField.SetBackgroundColour("white")
				self.editField.SetForegroundColour("black")
			else:
				self.editField.SetBackgroundColour("black")
				self.editField.SetForegroundColour("white")
			self.editField.Refresh()
		themeDlg.Destroy()

	def change_font(self, event):
		data = wx.FontData()
		data.SetInitialFont(self.editField.GetFont())
		dlg = wx.FontDialog(self, data)
		if dlg.ShowModal() == wx.ID_OK:
			font = dlg.GetFontData().GetChosenFont()
			colour = dlg.GetFontData().GetColour()
			self.editField.SetFont(font)
			self.editField.SetForegroundColour(colour)
		dlg.Destroy()

	def show_help(self, event):
		dlg = wx.Dialog(self, title="Help - Quick Notepad", size=(800, 600))
		text = wx.TextCtrl(dlg,
			value="""Quick Notepad

Quick Notepad is a simple, fast, and lightweight text editor built with wxPython.

It allows you to create, open, edit, and save plain text documents while providing the essential editing tools expected from a basic notepad application. The editor includes undo and redo support, clipboard operations, selectable light and dark themes, automatic word wrapping, and an indicator for unsaved changes.

Quick Notepad is designed to provide a clean and distraction-free environment for writing and editing text.""",
			style=wx.TE_MULTILINE | wx.TE_READONLY | wx.BORDER_NONE
		)
		ok = wx.Button(dlg, wx.ID_OK)
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(text, 0, wx.EXPAND | wx.ALL, 8)
		sizer.Add(ok, 0, wx.ALIGN_CENTER | wx.ALL, 8)
		dlg.SetSizer(sizer)
		dlg.Centre()
		dlg.ShowModal()
		dlg.Destroy()

	def show_about(self, event):
		dlg = wx.Dialog(self, title="About Quick Notepad", size=(800, 600))
		text = wx.TextCtrl(
			dlg,
			value="""Quick Notepad

Version: 1.0

Developed by: Pawan Kumar

Developed using Python.""",
			style=wx.TE_MULTILINE | wx.TE_READONLY
		)
		ok = wx.Button(dlg, wx.ID_OK)
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(text, 0, wx.ALL | wx.ALIGN_CENTER, 8)
		sizer.Add(ok, 0, wx.ALL | wx.ALIGN_CENTER, 8)
		dlg.SetSizer(sizer)
		dlg.Centre()
		dlg.ShowModal()
		dlg.Destroy()

	def analyse_text(self, event):
		text = self.editField.GetValue()
		chars = len("".join(text.split()))
		words = len(text.split())
		lines = len(text.splitlines())
		dlg = wx.Dialog(self, title="Text Analysis", size=(800, 600))
		box = wx.TextCtrl(
			dlg,
			value=f"""Text Analysis:

Characters: {chars}

Words: {words}

Lines: {lines}""",
			style=wx.TE_MULTILINE | wx.TE_READONLY
		)
		ok = wx.Button(dlg, wx.ID_OK)
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(box, 0, wx.ALL | wx.ALIGN_CENTER, 8)
		sizer.Add(ok, 0, wx.ALL | wx.ALIGN_CENTER, 8)
		dlg.SetSizer(sizer)
		dlg.Centre()
		dlg.ShowModal()
		dlg.Destroy()





app = wx.App()
frame = NewFrame()
frame.Show()
frame.Centre()
frame.Maximize(True)
app.MainLoop()