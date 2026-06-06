import re
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont


class AIHighlighter(QSyntaxHighlighter):

    def __init__(self, parent):
        super().__init__(parent)
        self._rules = []

        # Comments  ── green
        self._add_rule(r'//[^\n]*', '#6A9955')

        # Block type keywords  ── blue, bold
        keywords = (
            r'\b(attributes|spawn|trigger|death|pain|enemysight|bulletimpact'
            r'|inspectsoundstart|inspectbodystart|inspectfriendlycombatstart'
            r'|playerstart|blocked)\b'
        )
        self._add_rule(keywords, '#569CD6', bold=True)

        # Known attribute keys  ── light blue
        attr_keys = (
            r'\b(starting_health|aggression|aim_accuracy|fov|camper'
            r'|tactical|attack_skill|alertness)\b'
        )
        self._add_rule(attr_keys, '#9CDCFE')

        # Numbers  ── light green
        self._add_rule(r'\b\d+(\.\d+)?\b', '#B5CEA8')

        # Weapon / ammo / sound identifiers  ── orange
        self._add_rule(r'\b(weapon_\w+|ammo_\w+|sound/\S+)\b', '#CE9178')

    def _add_rule(self, pattern, colour, bold=False):
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(colour))
        if bold:
            fmt.setFontWeight(QFont.Bold)
        self._rules.append((re.compile(pattern), fmt))

    def highlightBlock(self, text):
        for pattern, fmt in self._rules:
            for match in pattern.finditer(text):
                self.setFormat(match.start(), match.end() - match.start(), fmt)
