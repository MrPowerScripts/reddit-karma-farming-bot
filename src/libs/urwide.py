#!/usr/bin/env python
# encoding: utf8
# -----------------------------------------------------------------------------
# Project   : URWIDE - Extended URWID
# -----------------------------------------------------------------------------
# Author    : Sébastien Pierre                     <sebastien.pierre@gmail.com>
# License   : Lesser GNU Public License  http://www.gnu.org/licenses/lgpl.html>
# -----------------------------------------------------------------------------
# Creation  : 14-07-2006
# Last mod  : 15-12-2016
# -----------------------------------------------------------------------------

import sys, string, re, curses
import urwid, urwid.raw_display, urwid.curses_display
from   urwid.widget import FLOW, FIXED, PACK, BOX, GIVEN, WEIGHT, LEFT, RIGHT, RELATIVE, TOP, BOTTOM, CLIP, RELATIVE_100

__version__ = "0.2.1"
__doc__ = """\
URWIDE provides a nice wrapper around the awesome URWID Python library. It
enables the creation of complex console user-interfaces, using an easy to use
API .

URWIDE provides a simple notation to describe text-based UIs, and also provides
extensions to support events, tooltips, dialogs as well as other goodies for
every URWID widget.

URWID can be downloaded at <http://www.excess.org/urwid>.
"""

COLORS =  {
	# Colors
	"WH": "white",
	"BL": "black",
	"YL": "yellow",
	"BR": "brown",
	"LR": "light red",
	"LG": "light green",
	"LB": "light blue",
	"LC": "light cyan",
	"LM": "light magenta",
	"Lg": "light gray",
	"DR": "dark red",
	"DG": "dark green",
	"DB": "dark blue",
	"DC": "dark cyan",
	"DM": "dark magenta",
	"Dg": "dark gray",
	# Font attributes
	"BO": "bold",
	"SO": "standout",
	"UL": "underline",
	"_" : "default"
}
RIGHT  = "right"
LEFT   = "left"
CENTER = "center"


IS_PYTHON3 = sys.version_info[0] > 2

if IS_PYTHON3:
	# Python3 only defines str
	unicode = str
	long    = int
else:
	unicode = unicode

def isString( t ):
	return isinstance(t, (unicode, str))

def ensureString( t, encoding="utf8" ):
	if IS_PYTHON3:
		return t if isinstance(t, str) else str(t, encoding)
	else:
		return t.encode("utf8") if isinstance (t, unicode) else str(t)

def safeEnsureString( t,  encoding="utf8" ):
	if IS_PYTHON3:
		return ensureString(t, encoding)
	else:
		return t.encode("utf8", "ignore") if isinstance (t, unicode) else str(t)

def ensureUnicode( t, encoding="utf8" ):
	if IS_PYTHON3:
		return t if isinstance(t, str) else str(t, encoding)
	else:
		return t if isinstance(t, unicode) else str(t).decode(encoding)

def ensureBytes( t, encoding="utf8" ):
	if IS_PYTHON3:
		return t if isinstance(t, bytes) else bytes(t, encoding)
	else:
		return t

def add_widget( container, widget, options=None  ):
	w = widget
	if isinstance(container, urwid.Pile):
		# See: urwid.container.py Pile.__init__
		w = widget
		if not isinstance(w, tuple):
			container.contents.append((w, (WEIGHT, 1)))
		elif w[0] in (FLOW, PACK):
			f, w = w
			containe.contents.append((w, (PACK, None)))
		elif len(w) == 2:
			height, w = w
			container.contents.append((w, (GIVEN, height)))
		elif w[0] == FIXED: # backwards compatibility
			_ignore, height, w = w
			container.contents.append((w, (GIVEN, height)))
		elif w[0] == WEIGHT:
			f, height, w = w
			container.contents.append((w, (f, height)))
		else:
			raise ValueError("Widget not as expected: {0}".format(widet))
	else:
		container.contents.append(widget)


def remove_widgets( container ):
	w = [_ for _ in container.contents]
	for _ in w:
		container.contents.remove(_)

def original_widgets( widget ):
	if not widget:
		return []
	stack = [widget]
	if stack:
		while hasattr(stack[0], "original_widget"):
			original = stack[0].original_widget
			if original not in stack:
				stack.insert(0,original)
			else:
				break
	return stack

def original_widget(widget):
	r = original_widgets(widget)
	return r[0] if r else widget

def original_focus(widget):
	w = original_widgets(widget)
	for _ in w:
		if hasattr(_, "focus"):
			return _.focus
	return w[0]

# ------------------------------------------------------------------------------
#
# URWID Patching
#
# ------------------------------------------------------------------------------

class PatchedListBox(urwid.ListBox):

	_parent = None

	def __init__( self, *args, **kwargs ):
		PatchedListBox._parent.__init__(self, *args, **kwargs)

	def remove_widgets( self ):
		"""Remove all widgets from the body."""
		if isinstance(self.body, SimpleListWalker):
			self.body = SimpleListWalker([])
		else:
			raise Exception("Method only supported for SimpleListWalker")

	def add_widget( self, widget ):
		"""Adds a widget to the body of this list box."""
		if isinstance(self.body, SimpleListWalker):
			self.body.contents.append(widget)
		else:
			raise Exception("Method only supported for SimpleListWalker")

class PatchedPile(urwid.Pile):

	_parent = None

	def __init__(self, widget_list, focus_item=None):
		# No need to call the constructor
		#super(PatchedPile, self).__init__(widget_list, focus_item)
		self.__super.__init__(widget_list, focus_item)
		self.widget_list = []
		self.item_types  = []
		for _ in widget_list: add_widget(self, _)
		if focus_item: self.set_focus(focus_item)
		self.pref_col = None

	def add_widget( self, widget ):
		"""Adds a widget to this pile"""
		w = widget
		self.widget_list.append(widget)
		if type(w) != type(()):
			self.item_types.append(('weight',1))
		elif w[0] == 'flow':
			f, widget = w
			self.widget_list[i] = widget
			self.item_types.append((f,None))
		elif w[0] in ('fixed', 'weight'):
			f, height, widget = w
			self.widget_list[i] = widget
			self.item_types.append((f,height))
		else:
			raise PileError("widget list item invalid %s" % (w))

	def remove_widget( self, widget ):
		"""Removes a widget from this pile"""
		if type(widget) != type(()): widget = widget[1]
		i = self.widget_list.index(widget)
		del self.widget_list[i]
		del self.item_types[i]

	def remove_widgets( self ):
		"""Removes all widgets from this pile"""
		self.widget_list = []
		self.item_types  = []

class PatchedColumns(urwid.Columns):
	_parent = None
	def set_focus(self, widget):
		"""Set the column in focus with a widget in self.widget_list."""
		position = self.widget_list.index(widget) if type(widget) != int else widget
		self.focus_col = position

PatchedPile._parent    = urwid.Pile
PatchedListBox._parent = urwid.ListBox
PatchedColumns._parent = urwid.Columns
# urwid.Pile    = PatchedPile
# urwid.ListBox = PatchedListBox
# urwid.Columns = PatchedColumns

# ------------------------------------------------------------------------------
#
# UI CLASS
#
# ------------------------------------------------------------------------------

class UISyntaxError(Exception): pass
class UIRuntimeError(Exception): pass
class UI:
	"""The UI class allows to build an URWID user-interface from a simple set of
	string definitions.

	Instanciation of this class, may raise syntax error if the given text data
	is not formatted as expected, but you can easily get detailed information on
	what the problem was."""

	BLANK = urwid.Text("")
	EMPTY = urwid.Text("")
	NOP   = lambda self:self

	class Collection(object):
		"""Keys of the given collection are recognized as attributes."""

		def __init__( self, collection=None ):
			object.__init__(self)
			if collection is None: collection = {}
			self.w_w_content = collection

		def __getattr__( self, name ):
			if name.startswith("w_w_"):
				return super(UI.Collection, self).__getattribute__(name)
			w = self.w_w_content
			if name not in w: raise UIRuntimeError("No widget with name: " + name )
			return w[name]

		def __setattr__( self, name, value):
			if name.startswith("w_w_"):
				return super(UI.Collection, self).__setattr__(name, value)
			if name in self.w_w_content:
				raise SyntaxError("Item name already used: " + name)
			self.w_w_content[name] = value

	def __init__( self ):
		"""Creates a new user interface object from the given text
		description."""
		self._content     = None
		self._stack       = None
		self._currentLine = None
		self._ui          = None
		self._palette     = None
		self._header      = None
		self._currentSize = None
		self._widgets     = {}
		self._groups      = {}
		self._strings     = {}
		self._data        = {}
		self._handlers    = []
		self.widgets      = UI.Collection(self._widgets)
		self.groups       = UI.Collection(self._groups)
		self.strings      = UI.Collection(self._strings)
		self.data         = UI.Collection(self._data)

	def id( self, widget ):
		"""Returns the id for the given widget."""
		if hasattr(widget, "_urwideId"):
			return widget._urwideId
		else:
			return None

	def new( self, widgetClass, *args, **kwargs ):
		"""Creates the given widget by instanciating @widgetClass with the given
		args and kwargs. Basically, this is equivalent to

		>	return widgetClass(*kwargs['args'], **kwargs['kwargs'])

		Excepted that the widget is wrapped in an `urwid.AttrWrap` object, with the
		proper attributes. Also, the given @kwargs are preprocessed before being
		forwarded to the widget:

		 - `data` is the text data describing ui attributes, constructor args
		   and kwargs (in the same format as the text UI description)

		 - `ui`, `args` and `kwargs` allow to pass preprocessed data to the
		   constructor.

		In all cases, if you want to pass args and kwargs, you should
		explicitely use the `args` and `kwargs` arguments. I know that this is a
		bit confusing..."""
		return self._createWidget( widgetClass, *args, **kwargs )

	def wrap( self, widget, properties ):
		"""Wraps the given in the given properties."""
		_ui, _, _ = self._parseAttributes(properties)
		return self._wrapWidget( widget, _ui )

	def unwrap( self, widget ):
		"""Unwraps the widget (see `new` method)."""
		if isinstance(widget, urwid.AttrWrap) and widget.w: widget = widget.w
		return widget

	# EVENT HANDLERS
	# -------------------------------------------------------------------------

	def handler( self, handler = None ):
		"""Sets/Gets the current event handler.

		This modifies the 'handler.ui' and sets it to this ui."""
		if handler is None:
			if not  self._handlers: raise UIRuntimeError("No handler defined for: %s" % (self))
			return self._handlers[-1][0]
		else:
			old_ui     = handler.ui
			handler.ui = self
			if not self._handlers:
				self._handlers.append((handler, old_ui))
			else:
				self._handlers[-1] = (handler, old_ui)

	def responder( self, event ):
		"""Returns the function that responds to the given event."""
		return self.handler().responder(event)

	def pushHandler( self, handler ):
		"""Push a new handler on the list of handlers. This handler will handle
		events until it is popped out or replaced."""
		self._handlers.append((handler, handler.ui))
		handler.ui = self

	def popHandler( self ):
		"""Pops the current handler of the list of handlers. The handler will
		not handle events anymore, while the previous handler will start to
		handle events."""
		handler, ui = self._handlers.pop()
		handler.ui = ui

	def _handle( self, event_name, widget, *args, **kwargs ):
		"""Handle the given given event name."""
		# If the event is an event name, we use the handler mechanism
		if type(event_name) in (str, unicode):
			handler = self.handler()
			if handler.responds(event_name):
				return handler.respond(event_name, widget, *args, **kwargs)
			elif hasattr(widget, event_name):
				getattr(widget, event_name, *args, **kwargs)
			else:
				raise UIRuntimeError("No handler for event: %s in %s" % (event_name, widget))
		# Otherwise we assume it is a callback
		else:
			return event_name(widget,  *args, **kwargs)

	def setTooltip( self, widget, tooltip ):
		widget._urwideTooltip = tooltip

	def setInfo( self, widget, info ):
		widget._urwideInfo = info

	def onKey( self, widget, callback ):
		"""Sets a callback to the given widget for the 'key' event"""
		widget = self.unwrap(widget)
		widget._urwideOnKey = callback

	def onFocus( self, widget, callback ):
		"""Sets a callback to the given widget for the 'focus' event"""
		widget = self.unwrap(widget)
		widget._urwideOnFocus = callback

	def onEdit( self, widget, callback ):
		"""Sets a callback to the given widget for the 'edit' event"""
		widget = self.unwrap(widget)
		widget._urwideOnEdit = callback

	def onPress( self, widget, callback ):
		"""Sets a callback to the given widget for the 'edit' event"""
		widget = self.unwrap(widget)
		widget._urwideOnPress = callback

	def _doPress( self, button, *args ):
		if hasattr(button, "_urwideOnPress"):
			event_name = button._urwideOnPress
			self._handle(event_name, button, *args)
		elif isinstance(button, urwid.RadioButton):
			return False
		else:
			raise UIRuntimeError("Widget does not respond to press event: %s" % (button))

	def _doFocus( self, widget, ensure=True ):
		if hasattr(widget, "_urwideOnFocus"):
			event_name = widget._urwideOnFocus
			self._handle(event_name, widget)
		elif ensure:
			raise UIRuntimeError("Widget does not respond to focus event: %s" % (widget))

	def _doEdit( self, widget, before, after, ensure=True ):
		if hasattr(widget, "_urwideOnEdit"):
			event_name = widget._urwideOnEdit
			self._handle(event_name, widget, before, after)
		elif ensure:
			raise UIRuntimeError("Widget does not respond to focus edit: %s" % (widget))

	def _doKeyPress( self, widget, key ):
		# THE RULES
		# ---------
		#
		# 1) Widget defines an onKey event handler, it is triggered
		# 2) If the handler returned False, or was not existent, we
		#    forward to the top widget
		# 3) The onKeyPress event is handled by the keyPress handler if the
		#    focused widget is not editable
		# 4) If no keyPresss handler is defined, the default key_press event is
		#    handled
		topwidget = self.getToplevel()
		current_widget = widget
		# We traverse the `original_widget` in case the widgets are nested.
		# This allows to get the deepest widget.
		stack = original_widgets(widget)
		# FIXME: Dialogs should prevent processing of events at a lower level
		if stack:
			for widget in stack:
				if hasattr(widget, "_urwideOnKey"):
					event_name = widget._urwideOnKey
					if self._handle(event_name, widget, key):
						return
			if current_widget != topwidget and current_widget not in stack:
				self._doKeyPress(topwidget, key)
			else:
				self._doKeyPress(None, key)
		elif widget and widget != topwidget:
			self._doKeyPress(topwidget, key)
		else:
			if key == "tab":
				self.focusNext()
			elif key == "shift tab":
				self.focusPrevious()
			if self.isEditable(self.getFocused()):
				res = False
			else:
				try:
					res = self._handle("keyPress", topwidget, key)
				except UIRuntimeError:
					res = False
			if not res:
				topwidget.keypress(self._currentSize, key)

	def getFocused( self ):
		raise Exception("Must be implemented by subclasses")

	def focusNext( self ):
		raise Exception("Must be implemented by subclasses")

	def focusPrevious( self ):
		raise Exception("Must be implemented by subclasses")

	def getToplevel( self ):
		raise Exception("Must be implemented by subclasses")

	def isEditable( self, widget ):
		return isinstance(widget, (urwid.Edit, urwid.IntEdit))

	def isFocusable( self, widget ):
		if   isinstance(widget, urwid.Edit):        return True
		elif isinstance(widget, urwid.IntEdit):     return True
		elif isinstance(widget, urwid.Button):      return True
		elif isinstance(widget, urwid.CheckBox):    return True
		elif isinstance(widget, urwid.RadioButton): return True
		else:                                       return False

	# PARSING WIDGETS STACK MANAGEMENT
	# -------------------------------------------------------------------------

	def _add( self, widget ):
		"""Adds the given widget to the @_content list. This list will be
		added to the current parent widget when the UI is finished or when an
		`End` block is encountered (see @_push and @_pop)"""
		# Piles cannot be created with [] as content, so we fill them with the
		# EMPTY widget, which is replaced whenever we add something
		if self._content == [self.EMPTY]: self._content[0] = widget
		self._content.append(widget)

	def _push( self, endCallback, ui=None, args=(), kwargs={} ):
		"""Pushes the given arguments (@ui, @args, @kwargs) on the stack,
		together with the @endCallback which will be invoked with the given
		arguments when an `End` block will be encountered (and that a @_pop is
		triggered)."""
		self._stack.append((self._content, endCallback, ui, args, kwargs))
		self._content = []
		return self._content

	def _pop( self ):
		"""Pops out the widget on the top of the stack and invokes the
		_callback_ previously associated with it (using @_push)."""
		previous_content = self._content
		self._content, end_callback, end_ui, end_args, end_kwargs = self._stack.pop()
		return previous_content, end_callback, end_ui, end_args, end_kwargs

	# GENERIC PARSING METHODS
	# -------------------------------------------------------------------------

	def create( self, style, ui, handler=None ):
		self.parseStyle(style)
		self.parseUI(ui)
		if handler: self.handler(handler)
		return self

	def parseUI( self, text ):
		"""Parses the given text and initializes this user interface object."""
		text = string.Template(text).substitute(self._strings)
		self._content = []
		self._stack   = []
		self._currentLine = 0
		for line in text.split("\n"):
			line = line.strip()
			if not line.startswith("#"): self._parseLine(line)
			self._currentLine += 1
		self._listbox     = self._createWidget(urwid.ListBox,self._content)
		return self._content

	def parseStyle( self, data ):
		"""Parses the given style."""
		res = []
		for line in data.split("\n"):
			if not line.strip(): continue
			line = line.replace("\t", " ").replace("  ", " ")
			name, attributes = [_.strip() for _ in line.split(":")]
			res_line = [name]
			for attribute in attributes.split(","):
				attribute = attribute.strip()
				color     = COLORS.get(attribute)
				if not color: raise UISyntaxError("Unsupported color: " + attribute)
				res_line.append(color)
			if len(res_line) != 4:
				raise UISyntaxError("Expected NAME: FOREGROUND BACKGROUND FONT")
			res.append(tuple(res_line))
		self._palette = res
		return res

	RE_LINE = re.compile("^\s*(...)\s?")
	def _parseLine( self, line ):
		"""Parses a line of the UI definition file. This automatically invokes
		the specialized parsers."""
		if not line:
			self._add( self.BLANK )
			return
		match = self.RE_LINE.match(line)
		if not match: raise UISyntaxError("Unrecognized line: " + line)
		name  = match.group(1)
		data  = line[match.end():]
		if hasattr(self, "_parse" + name ):
			getattr(self, "_parse" + name)(data)
		elif name[0] == name[1] == name[2]:
			self._parseDvd(name + data)
		else:
			raise UISyntaxError("Unrecognized widget: `" + name + "`")

	def _parseAttributes( self, data ):
		assert type(data) in (str, unicode)
		ui_attrs, data = self._parseUIAttributes(data)
		args, kwargs   = self._parseArguments(data)
		return ui_attrs, args, kwargs

	RE_UI_ATTRIBUTE = re.compile("\s*([#@\?\:]|\&[\w]+\=)([\w\d_\-]+)\s*")
	def _parseUIAttributes( self, data ):
		"""Parses the given UI attributes from the data and returns the rest of
		the data (which corresponds to something else thatn the UI
		attributes."""
		assert type(data) in (str, unicode)
		ui = {"events":{}}
		while True:
			match = self.RE_UI_ATTRIBUTE.match(data)
			if not match: break
			ui_type, ui_value = match.groups()
			assert type(ui_value) in (str, unicode)
			if   ui_type    == "#": ui["id"]      = ui_value
			elif ui_type    == "@": ui["style"]   = ui_value
			elif ui_type    == "?": ui["info"]    = ui_value
			elif ui_type    == "!": ui["tooltip"] = ui_value
			elif ui_type[0] == "&": ui["events"][ui_type[1:-1]]=ui_value
			data = data[match.end():]
		return ui, data

	def _parseArguments( self, data ):
		"""Parses the given text data which should be a list of attributes. This
		returns a dict with the attributes."""
		assert type(data) in (str, unicode)
		def as_dict(*args, **kwargs): return args, kwargs
		res = eval("as_dict(%s)" % (data))
		try:
			res = eval("as_dict(%s)" % (data))
		except:
			raise SyntaxError("Malformed arguments: " + repr(data))
		return res

	def hasStyle( self, *styles ):
		for s in styles:
			for r in self._palette:
				if r[0] == s: return s
		return False

	def _styleWidget( self, widget, ui ):
		"""Wraps the given widget so that it belongs to the given style."""
		styles = []
		if "id" in ui: styles.append("#" + ui["id"])
		if "style" in ui:
			s = ui["style"]
			if type(s) in (tuple, list): styles.extend(s)
			else: styles.append(s)
		styles.append( widget.__class__.__name__ )
		unf_styles = [_ for _ in styles if self.hasStyle(_)]
		foc_styles = [_ + "*" for _ in styles if self.hasStyle(_ + "*")]
		if unf_styles:
			if foc_styles:
				return urwid.AttrWrap(widget, unf_styles[0], foc_styles[0])
			else:
				return urwid.AttrWrap(widget, unf_styles[0])
		else:
			return widget

	def _createWidget( self, widgetClass, *args, **kwargs ):
		"""Creates the given widget by instanciating @widgetClass with the given
		args and kwargs. Basically, this is equivalent to

		>	return widgetClass(*kwargs['args'], **kwargs['kwargs'])

		Excepted that the widget is wrapped in an `urwid.AttrWrap` object, with the
		proper attributes. Also, the given @kwargs are preprocessed before being
		forwarded to the widget:

		 - `data` is the text data describing ui attributes, constructor args
		   and kwargs (in the same format as the text UI description)

		 - `ui`, `args` and `kwargs` allow to pass preprocessed data to the
		   constructor.

		In all cases, if you want to pass args and kwargs, you should
		explicitely use the `args` and `kwargs` arguments. I know that this is a
		bit confusing..."""
		_data = _ui = _args = _kwargs = None
		for arg, value in kwargs.items():
			if   arg == "data":   _data = value
			elif arg == "ui":     _ui = value
			elif arg == "args":   _args = value
			elif arg == "kwargs": _kwargs = value
			else: raise Exception("Unrecognized optional argument: " + arg)
		if _data:
			_ui, _args, _kwargs = self._parseAttributes(_data)
		args = list(args)
		if _args: args.extend(_args)
		kwargs = _kwargs or {}
		widget = widgetClass(*args, **kwargs)
		return self._wrapWidget(widget, _ui)

	def _wrapWidget( self, widget, _ui ):
		"""Wraps the given widget into anotger widget, and applies the various
		properties listed in the '_ui' (internal structure)."""
		# And now we process the ui information
		if not _ui: _ui = {}
		if "id" in _ui:
			setattr(self.widgets, _ui["id"], widget)
			widget._urwideId = _ui["id"]
		if _ui.get("events"):
			for event, handler in _ui["events"].items():
				if   event == "press":
					if not isinstance(widget, urwid.Button)\
					and not isinstance(widget, urwid.RadioButton):
						raise UISyntaxError("Press event only applicable to Button: " + repr(widget))
					widget._urwideOnPress = handler
				elif event == "edit":
					if not isinstance(widget, urwid.Edit):
						raise UISyntaxError("Edit event only applicable to Edit: " + repr(widget))
					widget._urwideOnEdit = handler
				elif event == "focus":
					widget._urwideOnFocus = handler
				elif event == "key":
					widget._urwideOnKey = handler
				else:
					raise UISyntaxError("Unknown event type: " + event)
		if _ui.get("info"):
			widget._urwideInfo = _ui["info"]
		if _ui.get("tooltip"):
			widget._urwideTooltip = _ui["tooltip"]
		return self._styleWidget( widget, _ui )

	# WIDGET-SPECIFIC METHODS
	# -------------------------------------------------------------------------

	def _argsFind( self, data ):
		args = data.find("args:")
		if args == -1:
			attr = ""
		else:
			attr = data[args+5:]
			data = data[:args]
		return attr, data

	def _parseTxt( self, data ):
		attr, data = self._argsFind(data)
		ui, args, kwargs = self._parseAttributes(attr)
		self._add(self._createWidget(urwid.Text,data, ui=ui, args=args, kwargs=kwargs))

	def _parseHdr( self, data ):
		if self._header is not None:
			raise UISyntaxError("Header can occur only once")
		attr, data = self._argsFind(data)
		ui, args, kwargs = self._parseAttributes(attr)
		ui.setdefault("style", "header")
		self._header = self._createWidget(urwid.Text, data, ui=ui, args=args, kwargs=kwargs)

	RE_BTN = re.compile("\s*\[([^\]]+)\]")
	def _parseBtn( self, data ):
		match = self.RE_BTN.match(data)
		if not match: raise SyntaxError("Malformed button: " + repr(data))
		data  = data[match.end():]
		self._add(self._createWidget(urwid.Button, match.group(1), self._doPress, data=data))

	RE_CHC = re.compile("\s*\[([xX ])\:(\w+)\](.+)")
	def _parseChc( self, data ):
		attr, data = self._argsFind(data)
		# Parses the declaration
		match = self.RE_CHC.match(data)
		if not match: raise SyntaxError("Malformed choice: " + repr(data))
		state = match.group(1) != " "
		group = group_name = match.group(2).strip()
		group = self._groups.setdefault(group,[])
		assert self._groups[group_name] == group
		assert getattr(self.groups,group_name) == group
		label = match.group(3)
		# Parses the attributes
		ui, args, kwargs = self._parseAttributes(attr)
		# Creates the widget
		self._add(self._createWidget(urwid.RadioButton, group, label, state,
		self._doPress,  ui=ui, args=args, kwargs=kwargs))

	def _parseDvd( self, data ):
		ui, args, kwargs = self._parseAttributes(data[3:])
		self._add(self._createWidget(urwid.Divider, data, ui=ui, args=args, kwargs=kwargs))

	def _parseBox( self, data ):
		def end( content, ui=None, **kwargs ):
			if not content: content = [self.EMPTY]
			if len(content) == 1: w = content[0]
			else: w = self._createWidget(urwid.Pile, content)
			border = kwargs.get('border') or 1
			w = self._createWidget(urwid.Padding, w, ('fixed left', border), ('fixed right', border) )
			# TODO: Filler does not work
			# w = self._createWidget(urwid.Filler, w, ('fixed top', border), ('fixed bottom', border) )
			# w = urwid.Filler(w,  ('fixed top', 1),  ('fixed bottom',1))
			self._add(w)
		ui, args, kwargs = self._parseAttributes(data)
		self._push(end, ui=ui, args=args, kwargs=kwargs)

	RE_EDT = re.compile("([^\[]*)\[([^\]]*)\]")
	def _parseEdt( self, data ):
		match = self.RE_EDT.match(data)
		data  = data[match.end():]
		label, text = match.groups()
		ui, args, kwargs = self._parseAttributes(data)
		if label and self.hasStyle('label'): label = ('label', label)
		self._add(self._createWidget(urwid.Edit, label, text,
		ui=ui, args=args, kwargs=kwargs))

	def _parsePle( self, data ):
		def end( content, ui=None, **kwargs ):
			if not content: content = [self.EMPTY]
			self._add(self._createWidget(urwid.Pile, content, ui=ui, kwargs=kwargs))
		ui, args, kwargs = self._parseAttributes(data)
		self._push(end, ui=ui, args=args, kwargs=kwargs)

	def _parseCol( self, data ):
		def end( content, ui=None, **kwargs ):
			if not content: content = [self.EMPTY]
			self._add(self._createWidget(urwid.Columns, content, ui=ui, kwargs=kwargs))
		ui, args, kwargs = self._parseAttributes(data)
		self._push(end, ui=ui, args=args, kwargs=kwargs)

	def _parseGFl( self, data ):
		def end( content, ui=None, **kwargs ):
			max_width = 0
			# Gets the maximum width for the content
			for widget in content:
				if hasattr(widget, "get_text"):
					max_width = max(len(widget.get_text()), max_width)
				if hasattr(widget, "get_label"):
					max_width = max(len(widget.get_label()), max_width)
			kwargs.setdefault("cell_width", max_width + 4)
			kwargs.setdefault("h_sep", 1)
			kwargs.setdefault("v_sep", 1)
			kwargs.setdefault("align", "center")
			self._add(self._createWidget(urwid.GridFlow, content, ui=ui, kwargs=kwargs))
		ui, args, kwargs = self._parseAttributes(data)
		self._push(end, ui=ui, args=args, kwargs=kwargs)

	def _parseLBx( self, data ):
		def end( content, ui=None, **kwargs ):
			self._add(self._createWidget(urwid.ListBox, content, ui=ui, kwargs=kwargs))
		ui, args, kwargs = self._parseAttributes(data)
		self._push(end, ui=ui, args=args, kwargs=kwargs)

	def _parseEnd( self, data ):
		if data.strip(): raise UISyntaxError("End takes no argument: " + repr(data))
		# We get the end callback that will instanciate the widget and add it to
		# the content.
		if not self._stack: raise SyntaxError("End called without container widget")
		end_content, end_callback, end_ui, end_args, end_kwargs = self._pop()
		end_callback(end_content, end_ui, *end_args, **end_kwargs)

# ------------------------------------------------------------------------------
#
# CONSOLE CLASS
#
# ------------------------------------------------------------------------------

class Console(UI):
	"""The console class allows to create console applications that work 'full
	screen' within a terminal."""

	def __init__( self ):
		UI.__init__(self)
		self._ui          = None
		self._frame       = None
		self._header      = None
		self._footer      = None
		self._listbox     = None
		self._dialog      = None
		self._tooltiptext = ""
		self._infotext    = ""
		self._footertext  = ""
		self.isRunning    = False
		self.endMessage   = ""
		self.endStatus    = 1

	# USER INTERACTION API
	# -------------------------------------------------------------------------

	def tooltip( self, text=-1 ):
		"""Sets/Gets the current tooltip text."""
		if text == -1:
			return self._tooltiptext
		else:
			self._tooltiptext = ensureUnicode(text)

	def info( self, text=-1 ):
		"""Sets/Gets the current info text."""
		if text == -1:
			return self._infotext
		else:
			self._infotext = ensureUnicode(text)

	def footer( self, text=-1 ):
		"""Sets/Gets the current footer text."""
		if text == -1:
			return self._footertext
		else:
			self._footertext = ensureUnicode(text)

	def dialog( self, dialog ):
		"""Sets the dialog as this UI dialog. All events will be forwarded to
		the dialog until exit."""
		self._dialog = dialog

	# WIDGET INFORMATION
	# -------------------------------------------------------------------------

	def getFocused( self ):
		"""Gets the focused widget"""
		# We get the original widget to focus on
		focused     = original_widget(self._listbox.get_focus()[0])
		old_focused = None
		while focused != old_focused:
			old_focused = focused
			# There are some types that are not focuable
			if isinstance(focused, urwid.AttrWrap):
				if focused.w: focused = focused.w
			elif isinstance(focused, urwid.Padding):
				if focused.min_width: focused = focused.min_width
			elif isinstance(focused, urwid.Filler):
				if focused.w: focused = focused.w
			elif hasattr(focused, "get_focus"):
				if focused.get_focus(): focused = focused.get_focus()
		return focused

	def focusNext( self ):
		focused = self._listbox.get_focus()[1] + 1
		self._listbox.set_focus(focused)
		while True:
			if not self.isFocusable(self.getFocused()) \
			and self._listbox.body.get_next(focused)[0] is not None:
				focused += 1
				self._listbox.set_focus(focused)
			else:
				break

	def focusPrevious( self ):
		focused = max(self._listbox.get_focus()[1] - 1, 0)
		self._listbox.set_focus(focused)
		while True:
			if not self.isFocusable(self.getFocused()) \
			and focused > 0:
				focused -= 1
				self._listbox.set_focus(focused)
			else:
				break

	def getToplevel( self ):
		"""Returns the toplevel widget, which may be a dialog's view, if there
		was a dialog."""
		if self._dialog:
			return self._dialog.view()
		else:
			return self._frame

	def getCurrentSize( self ):
		"""Returns the current size for this UI as a couple."""
		return self._currentSize

	# URWID EVENT-LOOP
	# -------------------------------------------------------------------------

	def main( self ):
		"""This is the main event-loop. That is what you should invoke to start
		your application."""
		#self._ui = urwid.curses_display.Screen()
		self._ui  = urwid.raw_display.Screen()
		self._ui.clear()
		if self._palette: self._ui.register_palette(self._palette)
		self._ui.run_wrapper( self.run )
		# We clear the screen (I know, I should use URWID, but that was the
		# quickest way I found)
		curses.setupterm()
		sys.stdout.write(curses.tigetstr('clear').decode())
		if self.endMessage:
			print (self.endMessage)
		return self.endStatus

	def run( self ):
		"""Run function to be used by URWID. You should not call it directly,
		use the 'main' function instead."""
		#self._ui.set_mouse_tracking()
		self._currentSize = self._ui.get_cols_rows()
		self.isRunning    = True
		while self.isRunning:
			self._currentSize = self._ui.get_cols_rows()
			self.loop()

	def end( self, msg=None, status=1 ):
		"""Ends the application, registering the given 'msg' as end message, and
		returning the given 'status' ('1' by default)."""
		self.isRunning = False
		self.endMessage = msg
		self.endStatus  = status

	def loop( self ):
		"""This is the main URWID loop, where the event processing and
		dispatching is done."""
		# We get the focused element, and update the info and and tooltip
		if self._dialog:
			focused = self._dialog.view()
		else:
			focused = self.getFocused() or self._frame
		# We trigger the on focus event
		self._doFocus(focused, ensure=False)
		# We update the tooltip and info in the footer
		if hasattr(focused, "_urwideInfo"):
			self.info(self._strings.get(focused._urwideInfo) or focused._urwideInfo)
		if hasattr(focused, "_urwideTooltip"):
			self.tooltip(self._strings.get(focused._urwideTooltip) or focused._urwideTooltip)
		# We draw the screen
		self._updateFooter()
		self.draw()
		self.tooltip("")
		self.info("")
		# And process keys
		if not self.isRunning: return
		keys    = self._ui.get_input()
		if isinstance(focused, urwid.Edit): old_text = focused.get_edit_text()
		# We handle keys
		for key in keys:
			#if urwid.is_mouse_event(key):
				# event, button, col, row = key
				# self.view.mouse_event( self._currentSize, event, button, col, row, focus=True )
				#pass
			# NOTE: The key press might actually be send not to the focused
			# widget but to its original_widget
			if key == "window resize":
				self._currentSize = self._ui.get_cols_rows()
			elif self._dialog:
				self._doKeyPress(self._dialog.view(), key)
			else:
				self._doKeyPress(focused, key)
		# We check if there was a change in the edit, and we fire and event
		if isinstance(focused, urwid.Edit):
			self._doEdit( focused, old_text, focused.get_edit_text(), ensure=False)

	def draw( self ):
		"""Main loop to draw the console. This takes into account the fact that
		there may be a dialog to display."""
		if self._dialog is not None:
			o = urwid.Overlay( self._dialog.view(), self._frame,
				"center",
				self._dialog.width(),
				"middle",
				self._dialog.height()
			)
			canvas = o.render( self._currentSize, focus=True )
		else:
			canvas = self._frame.render( self._currentSize, focus=True )
		self._ui.draw_screen( self._currentSize, canvas )

	def _updateFooter(self):
		"""Updates the frame footer according to info and tooltip"""
		remove_widgets(self._footer)
		footer = []
		if self.tooltip():
			footer.append(self._styleWidget(urwid.Text(self.tooltip()), {'style':'tooltip'}))
		if self.info():
			footer.append(self._styleWidget(urwid.Text(self.info()), {'style':'info'}))
		if self.footer():
			footer.append(self._styleWidget(urwid.Text(self.footer()), {'style':'footer'}))
		if footer:
			for _ in footer:
				add_widget(self._footer, _)
			self._footer.set_focus(0)

	def parseUI( self, text ):
		"""Parses the given text and initializes this user interface object."""
		UI.parseUI(self, text)
		self._listbox     = self._createWidget(urwid.ListBox,self._content)
		self._footer      = urwid.Pile([self.EMPTY])
		self._frame       = self._createWidget(urwid.Frame,
			self._listbox,
			self._header,
			self._footer
		)
		return self._content

	def _parseFtr( self, data ):
		self.footer(data)

# ------------------------------------------------------------------------------
#
# DIALOG CLASSES
#
# ------------------------------------------------------------------------------

class Dialog(UI):
	"""Utility class to create dialogs that will fit within a console
	application.

	See the constructor documentation for more information."""

	PALETTE = """
	dialog        : BL, Lg, SO
	dialog.shadow : DB, BL, SO
	dialog.border : Lg, DB, SO
	"""

	def __init__( self, parent, ui, width=40, height=-1, style="dialog",
	header="", palette=""):
		"""Creates a new dialog that will be attached to the given 'parent'. The
		user interface is described by the 'ui' string. The dialog 'width' and
		'height' will indicate the dialog size, when 'height' is '-1', it will
		be automatically computed from the given 'ui'."""
		UI.__init__(self)
		if height == -1: height = ui.count("\n") + 1
		self._width         = width
		self._height        = height
		self._style         = style
		self._view          = None
		self._headertext    = header
		self._parent        = parent
		self._startCallback = lambda x:x
		self._endCallback   = lambda x:x
		self._palette       = None
		self.make(ui, palette)

	def width( self ):
		"""Returns the dialog width"""
		return self._width

	def height( self ):
		"""Returns the dialog height"""
		return self._height

	def view( self ):
		"""Returns the view attached to this 'Dialog'. The _view_ is created by
		the 'make' method, and is an 'urwid.Frame' instance."""
		assert self._view
		return self._view

	def make( self, uitext, palui=None ):
		"""Makes the dialog using a UI description ('uitext') and a style
		definition for the palette ('palui'), which can be 'None', in which case
		the value will be 'Dialog.PALETTE'."""
		if not palui: palui = self.PALETTE
		self.parseStyle(palui)
		style = self._styleWidget
		assert self._view is None
		content = []
		if self._headertext:
			content.append(style(urwid.Text(self._headertext), {'style':(self._style +'.header', "dialog.header", 'header')}))
			content.append(urwid.Text(""))
			content.append(urwid.Divider("_"))
		content.extend(self.parseUI(uitext))
		w = style(urwid.ListBox(content), {'style':(self._style +'.content', "dialog.content", self._style)})
		# We wrap the dialog into a box
		w = urwid.Padding(w, ('fixed left', 1), ('fixed right', 1))
		#w = urwid.Filler(w,  ('fixed top', 1),  ('fixed bottom',1))
		w = style(w,  {'style':(self._style+".body", "dialog.body", self._style)} )
		w = style( w, {'style':(self._style, "dialog")} )
		# Shadow
		shadow = self.hasStyle( self._style + ".shadow", "dialog.shadow", "shadow")
		border = self.hasStyle( self._style + ".border", "dialog.border", "border")
		if shadow:
			border = (border, '  ') if border else '  '
			w = urwid.Columns([w,('fixed', 2, urwid.AttrWrap(urwid.Filler(urwid.Text(border), "top") ,shadow))])
			w = urwid.Frame( w, footer = urwid.AttrWrap(urwid.Text(border),shadow))
		self._view = w
		self._startCallback(self)
		w._urwideOnKey = self.doKeyPress

	def onStart( self, callback ):
		"""Registers the callback that will be triggered on dialog start."""
		self._startCallback = callback

	def onEnd( self, callback ):
		"""Registers the callback that will be triggered on dialog end."""
		self._endCallback = callback

	def doKeyPress( self, widget, key ):
		self._handle("keyPress", widget, key)

	def end( self ):
		"""Call this to close the dialog."""
		self._endCallback(self)
		self._parent._dialog = None

	def _parseHdr( self, data ):
		if self._header is not None:
			raise UISyntaxError("Header can occur only once")
		attr, data = self._argsFind(data)
		ui, args, kwargs = self._parseAttributes(attr)
		ui.setdefault("style", ("dialog.header", "header") )
		self._content.append( self._createWidget(urwid.Text, data, ui=ui, args=args, kwargs=kwargs))

# ------------------------------------------------------------------------------
#
# HANDLER CLASS
#
# ------------------------------------------------------------------------------

FORWARD = False

class Handler(object):
	"""A handler can be subclassed an can be plugged into a UI to react to a
	specific set of events. The interest of handlers is that they can be
	dynamically switched, then making "modal UI" implementation easier.

	For instance, you could have a handler for your UI in "normal mode", and
	have another handler when a dialog box is displayed."""

	def __init__( self ):
		self.ui = None

	def respond( self, event, *args, **kwargs ):
		"""Responds to the given event name. An exception must be raised if the
		event cannot be responded to. False is returned if the handler does not
		want to handle the event, True if the event was handled."""
		responder = self.responder(event)
		return responder(*args, **kwargs) != FORWARD

	def responds( self, event ):
		"""Tells if the handler responds to the given event."""
		_event_name = "on" + event[0].upper() + event[1:]
		if hasattr(self, _event_name): return _event_name
		else: return None

	def responder( self, event ):
		"""Returns the function that responds to the given event."""
		_event_name = "on" + event[0].upper() + event[1:]
		if not hasattr(self, _event_name):
			raise UIRuntimeError("Event not implemented: " + event)

		res = getattr(self, _event_name)
		assert res
		return res

# EOF - vim: tw=80 ts=4 sw=4 noet
