class EditorMode:
    """
    Modes in which the editor can be.

    Args:
        id          (int): unique identification number
        name        (str): name of the mode
        description (str): Description of the mode
        text        (str): Displayed in the statusbar to indicate in which state the editor is.
    """

    def __init__(self, id, name, description="", text=""):
        self.id = id
        self.name = name
        if name and not status_prompt:
            self.status_prompt = "-- {} --".format(name.replace("_", " "))
        else:
            self.status_prompt = status_prompt
        self.description = description

COMMAND = EditorMode(0, "COMMAND", "Normal command mode, waiting for something to happen", "")
COMMAND_INPUT = EditorMode(1, "COMMAND_INPUT", "When : has been pressed", "Command: ")
INSERT = EditorMode(2, "INSERT", "When in insert mode and you can type in the document")
REPLACE = EditorMode(3, "REPLACE", "single place replacement for r<char>")
VISUAL_BLOCK = EditorMode(4, "VISUAL_BLOCK", "For visual block mode (selection). Not yet used.")
VISUAL_LINE = EditorMode(5, "VISUAL_LINE", "For visual line mode (selection). Not yet used.")
VISUAL = EditorMode(6, "VISUAL", "For visual char mode (selection). Not yet used.")
DELETE = EditorMode(7, "DELETE", "When d has been pressed and waiting for specification on what to delete", "Delete ...")
SEARCH_FORWARD = EditorMode(8, "SEARCH_FORWARD", "When / has been pressed", "Search: ")
SEARCH_BACKWARD = EditorMode(9,"SEARCH_BACKWARD", "When ? has been pressed", "Search backward: ")
GO = EditorMode(10, "GO", "When g is pressed and it's waiting for the second g to go at BOF", "Go to ...")
YANK = EditorMode(11, "YANK", "When y has been pressed and waiting for the second y.", "")
ZETA = EditorMode(12, "ZETA", "When capital Z has been pressed and waiting for the second Z", "")
BOOKMARK = EditorMode(13, "BOOKMARK", "", "Set bookmark ...")
GOTOBOOKMARK = EditorMode(14, "GOTOBOOKMARK", "", "Go to bookmark ...")

