"""
parser.py
Parses RTCW .ai script files into a list of entity dicts, and rebuilds
them back to text after edits.

Entity dict structure:
    {
        'name':       str,
        'raw':        str,          # original full text of this entity
        'blocks':     [block, ...],
        'start_line': int,
        'end_line':   int,
    }

Block dict structure:
    {
        'type':        str,         # e.g. 'attributes', 'spawn', 'trigger'
        'arg':         str,         # optional argument after the type keyword
        'header':      str,         # full header text before the brace
        'inner_lines': [str, ...],  # lines between the braces
        'kvs':         [kv, ...],   # parsed key-value pairs (attributes block)
        'raw':         str,         # original text of this block
    }

KV dict structure:
    { 'key': str, 'value': str, 'comment': str }
"""

import re


# ── Public API ─────────────────────────────────────────────────────────────────

def parse_ai_file(text):
    """Parse a full .ai file and return a list of entity dicts."""
    entities = []
    lines = text.split('\n')
    n = len(lines)
    i = 0

    while i < n:
        stripped = lines[i].strip()

        # Skip blank lines and comment-only lines at the top level
        if not stripped or stripped.startswith('//'):
            i += 1
            continue

        # Entity name: a bare word (letters/digits/underscores), optional inline comment
        if re.match(r'^[\w]+\s*(//.*)?\s*$', stripped) and not stripped.startswith('//'):
            entity_name = stripped.split()[0]

            brace_line = _skip_to_open_brace(lines, n, i + 1)
            if brace_line >= n:
                i += 1
                continue

            outer_lines, end_idx = _read_block(lines, n, brace_line)
            raw_entity = '\n'.join(lines[i:end_idx + 1])

            # Parse the contents between the outer braces
            blocks = _parse_subblocks(outer_lines[1:-1])

            entities.append({
                'name':       entity_name,
                'raw':        raw_entity,
                'blocks':     blocks,
                'start_line': i,
                'end_line':   end_idx,
            })
            i = end_idx + 1
        else:
            i += 1

    return entities


def reconstruct_entity(entity):
    """
    Rebuild the raw text of an entity from its parsed blocks.
    Only the attributes block is regenerated; all other blocks keep
    their original text so comments and formatting are preserved.
    """
    raw = entity['raw']
    for block in entity['blocks']:
        if block['type'] == 'attributes' and block['kvs']:
            new_raw = _build_attributes_block(block['kvs'])
            raw = raw.replace(block['raw'], new_raw, 1)
    return raw


# ── Internal helpers ───────────────────────────────────────────────────────────

def _skip_to_open_brace(lines, n, start):
    """Return the index of the first line containing '{', starting from start."""
    for j in range(start, n):
        if '{' in lines[j]:
            return j
    return start


def _read_block(lines, n, start):
    """
    Read from the opening '{' at lines[start] to the matching '}'.
    Returns (content_lines, end_index).
    """
    depth = 0
    content = []
    j = start
    while j < n:
        line = lines[j]
        depth += line.count('{')
        depth -= line.count('}')
        content.append(line)
        if depth == 0:
            return content, j
        j += 1
    return content, j


def _parse_kvs(inner_lines):
    """Extract key-value pairs from the inner lines of a block."""
    kvs = []
    for line in inner_lines:
        s = line.strip()
        if not s or s.startswith('//'):
            continue
        m = re.match(r'^(\w+)\s+(.+?)(\s*//.*)?$', s)
        if m:
            kvs.append({
                'key':     m.group(1),
                'value':   m.group(2).strip(),
                'comment': (m.group(3) or '').strip(),
            })
    return kvs


def _parse_subblocks(lines):
    """
    Parse sub-blocks (attributes, spawn, trigger X, death, etc.)
    from the inner lines of an entity.
    """
    blocks = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped or stripped.startswith('//'):
            i += 1
            continue

        # Header on its own line, brace on the next line
        header_match = re.match(r'^([\w][\w\s]*)(//.*)?\s*$', stripped)
        if header_match and i + 1 < n and '{' in lines[i + 1]:
            block_header = stripped.split('//')[0].strip()
            parts = block_header.split(None, 1)
            block_type = parts[0]
            block_arg  = parts[1] if len(parts) > 1 else ''

            # Find the opening brace
            j = i + 1
            while j < n and '{' not in lines[j]:
                j += 1
            if j >= n:
                i += 1
                continue

            block_lines, k = _read_block(lines, n, j)
            inner_lines = block_lines[1:-1]
            raw_block   = '\n'.join(lines[i:k + 1])

            blocks.append({
                'type':        block_type,
                'arg':         block_arg,
                'header':      block_header,
                'inner_lines': inner_lines,
                'kvs':         _parse_kvs(inner_lines),
                'raw':         raw_block,
            })
            i = k + 1

        # Header and opening brace on the same line
        elif stripped and '{' in stripped:
            header_part = stripped[:stripped.index('{')].strip()
            parts = header_part.split(None, 1)
            block_type = parts[0] if parts else 'unknown'
            block_arg  = parts[1] if len(parts) > 1 else ''

            block_lines, k = _read_block(lines, n, i)
            inner_lines = block_lines[1:-1] if len(block_lines) > 1 else []
            raw_block   = '\n'.join(block_lines)

            blocks.append({
                'type':        block_type,
                'arg':         block_arg,
                'header':      header_part,
                'inner_lines': inner_lines,
                'kvs':         _parse_kvs(inner_lines),
                'raw':         raw_block,
            })
            i = k + 1

        else:
            i += 1

    return blocks


def _build_attributes_block(kvs):
    """Serialise a list of KV dicts back to an attributes block string."""
    lines = ['attributes', '\t{']
    for kv in kvs:
        comment = f'  {kv["comment"]}' if kv['comment'] else ''
        lines.append(f'\t\t{kv["key"]} {kv["value"]}{comment}')
    lines.append('\t}')
    return '\n'.join(lines)
