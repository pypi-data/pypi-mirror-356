from newick import loads

def getPath(langCode, trees):
    found = None
    for tree in trees:
        if found != None:
            break
        for item in tree.walk():
            if '[' + langCode + ']' in item.name:
                found = item
    if found == None:
        return None
    curNode = found
    path = [curNode.name]
    while hasattr(curNode, 'ancestor') and curNode != None:
        curNode = curNode.ancestor
        if curNode == None:
            break
        path.append(curNode.name)
    return path

def collect(all_data, data_folder, langname_utils):
    # Add language family information from glottolog
    print('Getting lang family trees')
    trees = []
    for line in open(data_folder + 'tree_glottolog_newick.txt'):
        tree = loads(line.strip())
        trees.append(tree[0])

    for lang_code in all_data:
        all_data[lang_code]['glot_tree'] = getPath(lang_code, trees)
    return all_data

def distance_metric(path1, path2, key):
    # The average percentage of trees of distance. This means that if you are in two
    # different trees, it will always be 1.0. If both languages are in the same
    # tree it is #overlapping edges/the total edges of the deepest language of
    # the two. 
    if path1 == None or path2 == None:
        return None
        
    overlap_counter = 0
    found = False
    for item in path1:
        if item in path2:
            overlap_counter += 1
    if overlap_counter == 0:
        return 1.0
    overlap_tree1 = 1- overlap_counter/len(path1)
    overlap_tree2 = 1- overlap_counter/len(path2)
    return (overlap_tree1 + overlap_tree2) /2


