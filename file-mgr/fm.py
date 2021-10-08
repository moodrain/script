import os

cd = os.getcwd()
sep = os.sep
lsep = os.linesep

print('文件管理，请输入操作：')
print('1 重命名后缀')
print('2 按名称删除')
print('3 数字文件名')
print('4 合并文件夹')
print('5 文件名去词' + lsep)
operType = input()

def errIf(judge, msg):
    if judge:
        print(msg)
        quit()

def inputr(text):
    return input(text +lsep).lower()

def handMsg(msg):
    print('已处理：' + msg.replace(cd + sep, ''))

def fileNameExt(name):
    piece = name.split('.')
    ext = piece.pop()
    base = '.'.join(piece)
    return {'base': base, 'ext': ext}

def base(name):
    return fileNameExt(name)['base']

def ext(name):
    return fileNameExt(name)['ext']

def renameExtension(dir, oldExt, newExt):
    files = os.listdir(dir)
    for f in files:
        if os.path.isdir(dir + sep + f):
            renameExtension(dir + sep + f, oldExt, newExt)
        elif not oldExt or f.endswith('.' + oldExt):
                oldFile = dir + sep + f
                newFile = dir + sep + base(f) + '.' + newExt
                os.rename(oldFile, newFile)
                handMsg(oldFile)

def delByName(dir, name):
    files = os.listdir(dir)
    for f in files:
        path = dir + sep + f
        if os.path.isdir(path):
            delByName(path, name)
        elif f == name:
            os.remove(path)
            handMsg(path)

def escapeWord(dir, word):
    files = os.listdir(dir)
    for f in files:
        path = dir + sep + f
        if os.path.isfile(path):
            if f.find(word) != -1:
                os.rename(path, dir + sep + base(f).replace(word, '', 1) + '.' + ext(f))
                handMsg(path)
        elif os.path.isdir(path):
            escapeWord(path, word)
            piece = path.split(sep)
            baseDir = piece[len(piece)-1]
            newDir = baseDir.replace(word, '', 1)
            os.rename(path, newDir)
            handMsg(path)

def numberFile(dir):
    tmpPrefix = 'number_file_tmp_prefix_2021'
    files = os.listdir(dir)
    toSort = []
    for f in files:
        if os.path.isdir(dir + sep + f):
            numberFile(dir + sep + f)
        else:
            toSort.append(f)
    toSort.sort()
    no = 1
    for s in toSort:
        os.rename(dir + sep + s, dir + sep + tmpPrefix + str(no) + '.' + ext(s))
        handMsg(dir + sep + s)
        no += 1
    tmpFiles = os.listdir(dir)
    for f in tmpFiles:
        path = dir + sep + f
        if os.path.isfile(path):
            if f.find(tmpPrefix) != -1:
                os.rename(path, dir + sep + base(f).replace(tmpPrefix, '', 1) + '.' + ext(f))

def mergeDir(target, parent, numberName, no):
    parentPath = cd + parent
    files = os.listdir(parentPath)
    toMoveFiles = []
    toHandleDirs = []
    for f in files:
        fPath = parentPath + f
        if os.path.isdir(fPath):
            toHandleDirs.append(f)
        else:
            toMoveFiles.append(f)
    if numberName:
        toMoveFiles.sort()
    for tmf in toMoveFiles:
        oldFile = parentPath + tmf
        if numberName:
            newFile = target + sep + no.get() + '.' + ext(tmf)
            no.add()
        else:
            rawPiece = parent.split(sep)
            piece = []
            for p in rawPiece:
                if p:
                    piece.append(p)
            piece.append(tmf)
            newFile = target + sep + ' - '.join(piece)
        os.rename(oldFile, newFile)
        handMsg(oldFile)
    for thd in toHandleDirs:
        if parentPath + thd == target:
            continue
        mergeDir(target, parent + thd + sep, numberName, no)
        try:
            os.removedirs(parentPath + thd)
        except:
            pass



if operType == '1':
    newExt = inputr('输入更改之后的后缀')
    errIf(not newExt, '后缀不能为空')
    oldExt = inputr('输入需要更改的后缀，默认全部')
    renameExtension(cd, oldExt, newExt)
elif operType == '2':
    name = inputr('请输入要删除的名称')
    errIf(not name, '名称不能为空')
    delByName(cd, name)
elif operType == '3':
    numberFile(cd)
elif operType == '4':
    targetName = inputr('请输入汇总后的文件夹名')
    errIf(not targetName, '文件夹名不能为空')
    target = cd + sep + targetName
    errIf(os.path.exists(target), '该目录已存在相同名称的文件')
    numberName = inputr('是否按数字重命名文件，默认是，否输 n') != 'n'
    os.mkdir(target)
    class No:
        def __init__(self):
            self.no = 1
        def add(self):
            self.no += 1
        def get(self):
            return str(self.no)
    mergeDir(target, sep, numberName, No())
elif operType == '5':
    word = inputr('请输入需要去掉的关键词')
    errIf(not word, '关键词不能为空')
    escapeWord(cd, word)
