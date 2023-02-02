import sys
import re
import os
# import glob
import shutil
import hashlib
import random


def printHelpCmd():
    with open('README.md', encoding='utf8') as f:
        raw = f.read()
        helpText = re.findall('支持的指令：(.*)当执行帮助指令时，会输出该文档这一段话。', raw, re.S)[0]
        helpText = helpText.strip()
        helpText = helpText.replace('\n\n', '\n')
        print(helpText)


if len(sys.argv) < 2:
    print('参数不正确，输入 python manager.py help 查看帮助')
    # printHelpCmd()
    exit()

cmd = sys.argv[1]
args = sys.argv[2:]
datapath = 'data.txt'
cachepath = 'cache'


def getCachePath(name):
    return os.path.join(cachepath, name+'.txt')


def createCmd():
    if not os.path.exists(datapath):
        with open(datapath, 'w') as f:
            f.write('{}')
    name = args[0]
    with open(datapath, encoding='utf8') as f:
        data = eval(f.read())
    if name in data:
        print('已存在%s图片库:%s' % (name, data[name]))
        return
    data[name] = {'top': 1, 'ranCmd': name}
    with open(datapath, 'w', encoding='utf8') as f:
        f.write(str(data))
    if not os.path.exists(name):
        os.mkdir(name)
    if not os.path.exists(cachepath):
        os.mkdir(cachepath)
    with open(getCachePath(name), 'w') as f:
        f.write('{}')
    print('创建%s图片库成功' % name)


def allFiles(path):
    # return glob.glob(os.path.join(path, '**'), recursive=True)
    res = []
    for root, dirs, files in os.walk(path):
        for file in files:
            res.append(os.path.join(root, file))
    return res


def initCmd():
    try:
        with open(datapath, encoding='utf8') as f:
            data = eval(f.read())
        for name in data:
            # for file in allFiles(name):
            #     os.remove(file)
            # for dirname in glob.glob(os.path.join(name, '**'), recursive=True):
            #     os.rmdir(dirname)
            shutil.rmtree(name)
    except:
        pass
    try:
        os.remove(datapath)
    except:
        pass
    try:
        shutil.rmtree(cachepath)
    except:
        pass
    print('系统初始化完毕')


def md5(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def updateCmd():
    name = args[0]
    cache = {}
    top = 0
    for file in allFiles(name):
        key = md5(file)
        val = os.path.split(file)[-1]
        cache[key] = val
        try:
            intval = int(os.path.splitext(val)[0])
            top = max(top, intval + 1)
        except:
            print('检查出不合规文件名%s,请手动处理' % val)
    with open(getCachePath(name), 'w', encoding='utf8') as f:
        f.write(str(cache))
    with open(datapath, encoding='utf8') as f:
        data = eval(f.read())
    data[name]['top'] = top
    with open(datapath, 'w', encoding='utf8') as f:
        f.write(str(data))
    print('更新图片库MD5等缓存信息完毕')


def getFiles(path):
    if not os.path.isdir(path):
        return [path]
    else:
        return allFiles(path)


def insertCmd():
    name = args[0]
    ncachepath = getCachePath(name)
    with open(ncachepath, encoding='utf8') as f:
        cache = eval(f.read())
    srcpath = args[1]
    srcs = getFiles(srcpath)
    with open(datapath, encoding='utf8') as f:
        data = eval(f.read())
    top = data[name]['top']
    cnt = 0
    for src in srcs:
        srcmd5 = md5(src)
        if srcmd5 in cache:
            print('%s已存在,路径为%s,MD5为%s' % (src, cache[srcmd5], srcmd5))
            continue
        suf = os.path.splitext(src)[-1]
        rawdest = '%06d%s' % (top, suf)
        dest = os.path.join(name, rawdest)
        shutil.copyfile(src, dest)
        top += 1
        cnt += 1
        cache[srcmd5] = rawdest
        # print('%s添加成功,重命名为%s' % (src, rawdest))
    data[name]['top'] = top
    with open(datapath, 'w', encoding='utf8') as f:
        f.write(str(data))
    with open(ncachepath, 'w', encoding='utf8') as f:
        f.write(str(cache))
    print('共添加%d张图片' % cnt)


def deleteCmd():
    name = args[0]
    with open(getCachePath(name), encoding='utf8') as f:
        cache = eval(f.read())
    srcs = getFiles(args[1])
    cnt = 0
    for src in srcs:
        srcmd5 = md5(src)
        if srcmd5 not in cache:
            print('%s不在图片库中' % src)
            continue
        dest = os.path.join(name, cache[srcmd5])
        os.remove(dest)
        cnt += 1
        del cache[srcmd5]
        # print('%s删除成功,在图库中名为' % (src, dest))
    with open(getCachePath(name), 'w', encoding='utf8') as f:
        f.write(str(cache))
    print('共删除%d张图片' % cnt)


def selectCmd():
    name = args[0]
    with open(getCachePath(name), encoding='utf8') as f:
        cache = eval(f.read())
    return random.choice(tuple(cache.values()))



if cmd == 'help':
    printHelpCmd()
elif cmd == 'create':
    createCmd()
elif cmd == 'insert' or cmd == 'add':
    insertCmd()
elif cmd == 'init':
    initCmd()
elif cmd == 'update':
    updateCmd()
elif cmd == 'delete':
    deleteCmd()
elif cmd == 'select':
    selectCmd()