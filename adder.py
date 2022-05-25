import os
import sys
import shutil

if not os.path.exists('img'):
    os.mkdir('img')

if len(sys.argv) < 3:
    raise '参数不完整'
path_dest = os.path.join('img', sys.argv[1])
path_src = sys.argv[2]
copyMode = True
if len(sys.argv) > 3 and '0' == sys.argv[3]:
    copyMode = False

if not os.path.exists(path_src):
    raise '源路径不存在'

if not os.path.exists(path_dest):
    os.mkdir(path_dest)

filesIndexes = [int(os.path.splitext(x)[0]) for x in os.listdir(path_dest)]
beginIndex = (max(filesIndexes) if len(filesIndexes) else 0)+1
successCount = 0


def move(file):
    global beginIndex, successCount
    suffix = os.path.splitext(file)[1]
    dest = os.path.join(path_dest, '%04d%s' % (beginIndex, suffix))
    shutil.copyfile(file, dest)
    if not copyMode:
        os.remove(file)
    beginIndex += 1
    successCount += 1


if not os.path.isdir(path_src):
    move(path_src)
else:
    for root, dirs, files in os.walk(path_src):
        for file in files:
            move(os.path.join(root, file))

print('成功%s了%d张图片' % (['剪贴', '复制'][copyMode], successCount))
