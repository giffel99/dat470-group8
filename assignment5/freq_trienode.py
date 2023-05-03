#!/usr/bin/env python3

import sys
import argparse
'''
För root trie:
	1. Räkna storleken på children = 8(första pekaren till arrayn) + 8 * num_children
	2. räkna storlek på child_chars = 8 + num_children * 2
	3. räkna storlek på num_children = 1
	4. räkna storlek på count = 4
	Iterera igenom alla children:
		0. Ifall children är null så är totala storlek på sista noden = 8 + 8 + 1 + 4
		1. Räkna storleken på children = 8(första pekaren till arrayn) + 8 * num_children
		2. räkna storlek på child_chars = 8 + num_children * 2
		3. räkna storlek på num_children = 1
		4. räkna storlek på count = 4
		5. Iterera igenom alla children:
			....

'''

def get_total_storage(trie):
    children_size = 8 + 8 * trie._num_children
    child_chars_size = 8 + trie._num_children * 2
    num_children_size = 1
    count_size = 4
    current_total = children_size + child_chars_size + num_children_size + count_size

    for child in trie._children:
        current_total += get_total_storage(child)
    return current_total
    

class TrieNode:
    def __init__(self, word = '', count = None):
        self._children = list()
        self._child_chars = list()
        self._num_children = 0
        if len(word) == 0:
            self._count = 1 if count is None else count
        else:
            self._count = 0
            try:
                i = self._child_chars.index(word[0])
                self._children[i] = TrieNode(word[1:],count)
            except ValueError:
                self._child_chars.append(word[0])
                self._num_children += 1
                self._children.append(TrieNode(word[1:],count))

    def add(self, word, count=None):
        if len(word) == 0:
            self._count += 1 if count is None else count
        else:
            if word[0] not in self._child_chars:
                self._child_chars.append(word[0])
                self._children.append(TrieNode(word[1:], count))
                self._num_children += 1
            else:
                i = self._child_chars.index(word[0])
                self._children[i].add(word[1:], count)

    def __iter__(self):
        for i in range(self._num_children):
            for k,v in self._children[i]:
                if v > 0: yield (self._child_chars[i]+k, v)
        if self._count > 0: yield ('', self._count)

    def __getitem__(self, key):
        if len(key) == 0 and self._count > 0:
            return self._count
        if len(key) == 0: raise KeyError('key not found')
        try:
            i = self._child_chars.index(key[0])
        except ValueError:
            raise KeyError('key not found')
        return self._children[i][key[1:]]

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="freq for trie")
    parser.add_argument('--file_path', type=str)
    args = parser.parse_args()


    trie = TrieNode('',0)
    if(args.file_path):
        with open(args.file_path) as file:
            for line in file:
                 for word in line.strip().split():
                    trie.add(word)
    else:
        for line in sys.stdin:
            if 'q' == line.rstrip():
             break
            for word in line.strip().split():
                trie.add(word)
    for k,v in trie:
        print(k,v)
    
    total_storage = get_total_storage(trie)
    print("Approximate memory storage is:",total_storage," bytes.")
