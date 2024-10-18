class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def search(node, key):
    if node is None:
        return False
    if node.key == key:
        return True
    if key < node.key:
        return search(node.left, key)
    return search(node.right, key)