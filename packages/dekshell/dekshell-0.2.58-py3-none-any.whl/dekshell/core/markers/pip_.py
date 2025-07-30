from dektools.file import write_file, remove_path
from .base import MarkerWithEnd


class PipMarker(MarkerWithEnd):
    tag_head = "_pip"

    def execute(self, context, command, marker_node, marker_set):
        text = self.get_inner_content(context, marker_node, translate=None)
        fp = write_file(s=text)
        marker_set.shell_cmd(f'pip install -r {fp}')
        remove_path(fp)
        return []
