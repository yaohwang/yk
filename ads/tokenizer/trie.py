# encoding: utf-8

import re

from collections import namedtuple
from typing import Union, List, Tuple
from pathlib import Path

Record = namedtuple('Record', ('value', 'alias', 'special', 'norm'), defaults=(None, None, None, None))
Node = namedtuple('Node', ('value', 'alias', 'special', 'norm', 'children', 'leaf'), defaults=(None, None, None, None, None, False))

# TODO: check special when trie create


def parse_dicts(path_dicts: str) -> List[Record]:
    path = Path(path_dicts)
    if path.is_dir():
        for path_dict in path.iterdir():
            for record in parse_dict(path_dict):
                yield record
    else:
        yield parse_dict(path)


def parse_dict(path_dict: Union[str, Path]) -> List[Record]:
    path = Path(path_dict) if str == type(path_dict) else path_dict
    with path.open() as f:
        for line in f.readlines():
            if line.startswith('#'): continue
            yield parse_line(line)


def parse_line(line: str) -> Record:
    """
    word, alias
    军团, [SPECIAL-TOKEN], (0, (均,君))
    """
    record = line.split(',', 1)

    if 1 == len(record):
        return Record(record[0].strip())
    
    alias = {}
    for (i, _alias) in re.findall(r'(?:\(([0-9]{1,}),\s*\((.*?)\)\))', record[1].strip()):
        alias[int(i)] = _alias.split(',')

    special = re.findall(r'(\[.*\])', record[1].strip())
    special = special[0] if special else None

    norm = re.findall(r'<(.*)>', record[1].strip())
    norm = norm[0] if norm else None
    
    return Record(record[0].strip(), alias, special, norm)


def trie(path_dicts: str) -> Node:
    root = Node(None, None, None, None, [])

    for record in parse_dicts(path_dicts):
        current_node = root

        for i, char in enumerate(record.value):
            node = find_in_children(current_node, char)
            alias = record.alias.get(i,[]) if record.alias is not None else []
            leaf = i == len(record.value)-1
            special = record.special if leaf else None
            norm = record.norm if leaf else None

            if node is not None:
                # update new info
                if (not node.alias and alias) or (not node.special and special) or (not node.leaf and leaf):
                    old_node = node
                    alias = alias if alias else old_node.alias
                    special = special if special else old_node.special
                    norm = norm if norm else old_node.norm
                    leaf = leaf if leaf else node.leaf
                    node = Node(old_node.value, alias, special, norm, old_node.children, leaf)
                    current_node.children.remove(old_node)
                    del old_node
                    current_node.children.append(node)
            else:
                node = Node(char, alias, special, norm, [], leaf)
                current_node.children.append(node)

            current_node = node

    return root


def has(root: Node, text: Union[str, List[str]]) -> bool:
    current_node = root
    for char in text:
        current_node = find_in_children(current_node, char)
        if current_node is None:
            return False
    if current_node.leaf:
        return True
    return False


def find(root: Node, text: Union[str, List[str]]) -> Tuple[str, int]:
    token = None
    idx = -1

    match_nodes = []
    current_node = root
    i = 0
    for i, char in enumerate(text):
        node = find_in_children(current_node, char)
        # print(i, char, node.value if node is not None else repr(node))
        if node is None:
            i -= 1
            break
        match_nodes.append(node)
        current_node = node
        if not current_node.children:
            break

    if match_nodes and current_node.leaf:
        if match_nodes[-1].special is not None:
            token = match_nodes[-1].special
        elif match_nodes[-1].norm is not None:
            token = match_nodes[-1].norm
        else:
            token = ''.join([n.value for n in match_nodes])
        # print([_.value for _ in match_nodes])

    return token, i


def find_in_children(node: Node, char: str) -> bool:
    for c in node.children:
        if char == c.value or char in c.alias:
            return c


def fprint(node: Node):
    return f'value:{node.value}, alias:{repr(node.alias)}, special:{repr(node.special)}, leaf:{node.leaf}'# \
           # f' ---- id:{id(node)} ---- children:{[id(c) for c in node.children]}'


def tree(node, depth=0):
    if depth == 0:
        print(fprint(node))

    if not node.children:
        print('|' if 0 != depth else '')
        return
 
    for c in node.children:
        print(('|' if 0 != depth else '') + '    ' * depth + '|____' + fprint(c))
        tree(c, depth+1)
 

if __name__ == '__main__':
    # print(list(parse_dicts('./dict')))
    root = trie('./dict')
    # print()
    # print(root)
    # print()
    tree(root)
