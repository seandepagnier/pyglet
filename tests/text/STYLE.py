#!/usr/bin/env python

'''Test that character and paragraph-level style is adhered to correctly in
incremental layout.

Examine and type over the text in the window that appears.  The window
contents can be scrolled with the mouse wheel.  There are no formatting
commands, however formatting should be preserved as expected when entering or
replacing text and resizing the window.

Press ESC to exit the test.
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id$'

import unittest

from pyglet import app
from pyglet import gl
from pyglet import graphics
from pyglet import text
from pyglet.text import caret
from pyglet.text import layout
from pyglet import window
from pyglet.window import key, mouse

doctext = '''STYLE.py test document.

{font_size 24}This is 24pt text.{font_size 12}

This is 12pt text (as is everything that follows).

This text has some {bold True}bold character style{bold False}, some
{italic True}italic character style{italic False}, a {color [255, 0, 0,
255]}change {color [0, 255, 0, 255]}in 
{color [0, 0, 255, 255]}color{color None}, and in 
{background_color [255, 255, 0, 255]}background 
{background_color [0, 255, 255, 255]}color{background_color None}.

This paragraph uses {font_name 'Courier New'}Courier New{font_name None} and
{font_name 'Times New Roman'}Times New Roman{font_name None} fonts.

{.align 'left'}This paragraph is left aligned. Lorem ipsum dolor
sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut
labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud
exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis
aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
culpa qui officia deserunt mollit anim id est laborum.

{.align 'right'}This paragraph is right aligned. Lorem ipsum dolor sit amet,
consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et
dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation
ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor
in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui
officia deserunt mollit anim id est laborum.

{.align 'center'}This paragraph is centered. Lorem ipsum dolor sit amet,
consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et
dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation
ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor
in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui
officia deserunt mollit anim id est laborum.

{.align 'left'}{.margin_left 50}This paragraph has a 50 pixel left margin.
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

{.margin_left 0}{.margin_right 50}This paragraph has a 50 pixel right margin.
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

{.margin_left 200}{.margin_right 200}This paragraph has 200 pixel left and
right margins. Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed
do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex
ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate
velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat
cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id
est laborum.

{.align 'right'}{.margin_left 100}{.margin_right 100}This paragraph is
right-aligned, and has 100 pixel left and right margins. Lorem ipsum dolor sit
amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore
et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation
ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor
in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui
officia deserunt mollit anim id est laborum.

{.align 'center'}{.margin_left 100}{.margin_right 100}This paragraph is
centered, and has 100 pixel left and right margins. Lorem ipsum dolor sit
amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore
et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation
ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor
in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui
officia deserunt mollit anim id est laborum.

{.align 'left'}{.margin_left 0}{.margin_right 0}{.wrap False}This paragraph
does not word-wrap. Lorem ipsum dolor sit amet, consectetur adipisicing elit,
sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit
esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

{.wrap True}{.margin_bottom 15}This and the following two paragraphs have a 15
pixel vertical margin separating them. Lorem ipsum dolor sit amet, consectetur
adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna
aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
nisi ut aliquip ex ea commodo consequat.{}
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore
eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt
in culpa qui officia deserunt mollit anim id est laborum.{}
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore
eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt
in culpa qui officia deserunt mollit anim id est laborum.{}
{.margin_bottom 0}{.margin_top 30}This and the following two paragraphs have
a 30 pixel vertical margin (this time, the top margin is used instead of the
bottom margin).  There is a 45 pixel margin between this paragraph and the
previous one.{}
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore
eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt
in culpa qui officia deserunt mollit anim id est laborum.{}
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore
eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt
in culpa qui officia deserunt mollit anim id est laborum.{}
'''

class TestWindow(window.Window):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)

        self.batch = graphics.Batch()
        self.document = text.attributed(doctext)
        self.margin = 2
        self.layout = layout.IncrementalTextLayout(self.document,
            10, 10, # on_resize resolves this before layout happens
            multiline=True,
            batch=self.batch)
        self.caret = caret.Caret(self.layout)
        self.push_handlers(self.caret)

        self.set_mouse_cursor(self.get_system_mouse_cursor('text'))

    def on_resize(self, width, height):
        super(TestWindow, self).on_resize(width, height)
        self.layout.x = self.margin
        self.layout.y = self.height - self.margin
        self.layout.width = width - self.margin * 2
        self.layout.height = height - self.margin * 2
        self.caret._update() # XXX

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.layout.view_x -= scroll_x
        self.layout.view_y += scroll_y * 16

    def on_draw(self):
        gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.batch.draw()

class TestCase(unittest.TestCase):
    def test(self):
        self.window = TestWindow(resizable=True)
        app.run()

if __name__ == '__main__':
    unittest.main()