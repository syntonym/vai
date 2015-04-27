from vaitk import gui
from .Editor import Editor
from . import models
import random
import os


class EditorApp(gui.VApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # We keep them at the App level because the app will be responsible
        # for coordinating the async system in the future.
        self._global_model = models.GlobalState()
        self._buffer_list = models.BufferList()

        self._editor = Editor(self, self._global_model, self._buffer_list)

        self._editor.show()

    def openFile(self, path):
        """Make the file at 'path' ready to edit.

        Args:
            path (str) : as expected by `open(path, 'r')`

        If the file is already opened in a buffer, focus that buffer. Else create
        a new buffer and focuse that one.
        """
        self._editor.controller.openFile(path)

    def dumpBuffers(self, destination_dir=None):
        """
        Dumps the content of the buffers to destionation_dir.

        Args:
            destionation_dir (str) : directory to dump buffers into

        Returns:
            (list): list of files dumped

        Default destination is the home directory of the user.
        """

        if destination_dir is None:
            destination_dir = os.path.expanduser("~")

        file_list = []

        for buffer in self._buffer_list.buffers:
            document_text = buffer.document.documentText()
            document_name = buffer.document.documentMetaInfo("Filename").data() or "noname"
            random_number = random.randint(1, 100000)
            path = os.path.join(destination_dir, "vaidump-%s-%d.txt" % (os.path.basename(document_name), random_number))

            with open(path, "w") as f:
                f.write(document_text)

            file_list.append(path)

        return file_list

    @property
    def editor(self):
        return self._editor

