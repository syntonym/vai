import vaitk
from vaitk import core, gui, utils
from . import controllers
from .models.TextDocument import CharMeta
from . import models
from . import Search


class EditArea(gui.VWidget):
    """
    Args:
        global_state      (models.global_state)          : global state of the app
        editor_controller (controllers.EditorController) : TODO
        parent            (vaitk.gui.VWidget)            : parent in widget tree
    """
    def __init__(self, global_state, editor_controller, parent):
        super().__init__(parent)
        self._buffer = None

        self._controller = controllers.EditAreaController(self, global_state, editor_controller)
        self._color_schema = models.SyntaxColors(
                                    models.Configuration.get("colors.syntax_schema"),
                                    gui.VApplication.vApp.screen().numColors()
                             ).colorMap()

        self._visual_cursor_pos = (0,0)
        self._highlight_current_identifier = False
        self._current_identifier_highlight_timer = core.VTimer()
        self._current_identifier_highlight_timer.setSingleShot(True)
        self._current_identifier_highlight_timer.setInterval(500)
        self._current_identifier_highlight_timer.timeout.connect(self.identifierHighlightTimeout)

        self.setFocusPolicy(vaitk.FocusPolicy.StrongFocus)

        self._icons = models.Icons.getCollection(
                                models.Configuration.get("icons.collection")
                                )

    # properties
    @property
    def buffer(self):
        return self._buffer

    @buffer.setter
    def buffer(self, buffer):
        if buffer is None:
            raise Exception("Cannot set buffer to None")

        self._buffer = buffer
        self._controller.buffer = buffer
        self.update()

    @property
    def visual_cursor_pos(self):
        return self._visual_cursor_pos

    @visual_cursor_pos.setter
    def visual_cursor_pos(self, cursor_pos):
        pos_x = utils.clamp(cursor_pos[0], 0, self.width()-1)
        pos_y = utils.clamp(cursor_pos[1], 0, self.height()-1)
        self._visual_cursor_pos = (pos_x, pos_y)
        self._highlight_current_identifier = False
        if self._current_identifier_highlight_timer.isRunning():
            self._current_identifier_highlight_timer.stop()
        self._current_identifier_highlight_timer.start()
        gui.VCursor.setPos(self.mapToGlobal((pos_x, pos_y)))

    def identifierHighlightTimeout(self):
        self._current_identifier_highlight_timer.stop()
        self._highlight_current_identifier = True
        self.update()

    def paintEvent(self, event):
        painter = gui.VPainter(self)
        painter.erase()

        buffer = self._buffer
        if buffer is None:
            return

        w, h = self.size()
        pos_at_top = buffer.edit_area_model.document_pos_at_top
        visible_line_interval = (pos_at_top[0], pos_at_top[0]+h)
        cursor_pos = buffer.cursor.pos
        document = buffer.document

        # Find the current hovered word to set highlighting
        current_word, current_word_pos = document.wordAt(cursor_pos)
        word_entries = []
        if current_word_pos is not None:
            # find all the words only in the visible area
            word_entries = Search.findAll(document,
                                          current_word,
                                          line_interval=visible_line_interval,
                                          word=True)


        for visual_line_num, doc_line_num in enumerate(range(*visible_line_interval)):
            if doc_line_num > document.numLines():
                continue

            # Get the relevant text
            line_text = document.lineText(doc_line_num)[pos_at_top[1]-1:]
            line_text.replace('\n', ' ')

            # Apply colors. First through the Lexer designation
            colors = [(None, None, None)]*len(line_text)

            # Add markers for the indentation
            indent_spaces = len(line_text)-len(line_text.lstrip())
            for i in range(5, indent_spaces, 4):
                line_text = line_text[:i-1]+self._icons["tabulator"]+line_text[i:]

            char_meta = document.charMeta( (doc_line_num,1))
            if CharMeta.LexerToken in char_meta:
                colors = [self._color_schema[tok] for tok in char_meta.get(CharMeta.LexerToken)]

            for i in range(5, indent_spaces, 4):
                colors[i-1] = (gui.VGlobalColor.term_303030, None, None)

            selection = buffer.selection
            if selection.isValid() and \
                (selection.low_line <= doc_line_num <= selection.high_line):
                colors = [ (c[0], c[1], gui.VGlobalColor.yellow) for c in colors]

            # Then, if there's a word, replace (None, None) entries with the highlight color
            word_entries_for_line = [x[1] for x in word_entries if x[0] == doc_line_num]
            for word_start in word_entries_for_line:
                for pos in range(word_start-1, word_start-1+len(current_word)):
                    if colors[pos] == (None, None, None) and self._highlight_current_identifier:
                        colors[pos] = (gui.VGlobalColor.lightred, None, None)

            painter.drawText( (0, visual_line_num), line_text.replace('\n', ' '))
            painter.recolor((0, visual_line_num), colors[pos_at_top[1]-1:])

        #self.visual_cursor_pos = (cursor_pos[1]-pos_at_top[1], cursor_pos[0]-pos_at_top[0])

    def keyEvent(self, event):
        self._controller.handleKeyEvent(event)

    def focusInEvent(self, event):
        gui.VCursor.setPos(self.mapToGlobal((self._visual_cursor_pos[0], self._visual_cursor_pos[1])))

