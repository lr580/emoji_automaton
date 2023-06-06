**图片资源大部分源自网络，如果侵犯了您的版权，请联系我删掉相关图片**



已收录表情列表：(在 `img/` 下)

- `capoo` (bugcat capoo，猫猫虫)

  预览： <img src='img/capoo/0004.gif'></img>

- `dolo` (一套猫猫头表情包，未发现官名自己起的名字，暂未收录完整，待更新)

  含自己原创的部分表情。预览：<img src='img/dolo/0001.jpg'></img>

  目前暂未开始收录 `dolo` 表情包。
  
- `oni` 别当欧尼酱了 番剧表情包和截图



参考管理工具：

- `manager.py`

  支持的指令：

  - `python manager.py help` 查看帮助

  - `python manager.py create 图片库名`

    添加一个图片库(命名不要包含特殊字符等，程序不主动检查命名规范)

    图片库信息会以 python dict 格式存储在根目录 `data.txt` 中，key 为图片库名 value 包含：
  
    - `ranCmd` 随机输出指令(若空默认与图片库名一致)*(暂未实体化)*
    - `top` 下次添加图片的编号(为了避免遍历而作缓存处理)，注意 top 不一定等于图片数+1，因为可能会发生对图片库图片的删除，而删除不改变编号
  
    图片库名是后续存储图片所用的目录名，该目录存在根路径上。
  
    此外，还会在 `cache\` 里添加图片库的图片 MD5 计算结果缓存文件(文件名是图片库名+`.txt`)，格式是 python dict，key 是 MD5 值，value 是相对文件名。
  
    如：`python manager.py create capoo`，存储配置同时创建 `capoo/` 路径。
  
  - `python manager.py insert 图片库名 要添加的目录/文件路径`
  
    遍历要添加的路径，读取所有有效图片，检查 MD5 是否与图片库一致，如果不一致则添加新图片到图片库。
  
    添加的图片默认命名格式是 `%06d`。
  
    程序会缓存所有图片 MD5，但这样无法追踪任何手动修改图片库图片的操作。除非使用 `update` 强制刷新。
  
  - `python manager.py update 图片库名`
  
    重新计算并缓存所有图片的 MD5，重新计算 top。
  
  - `python manager.py delete 图片库名 要删除的目录/文件路径`
  
    查询图片库里是否有
  
  - `python manager.py init`
  
    清空所有图片库。不会发出警告，请谨慎执行本指令。
  
  当执行帮助指令时，会输出该文档这一段话。
  
  注意本程序不鉴权，如果需要配合其他项目使用(如聊天 bot，请自行在被调处鉴权)。
  
- `adder.py` (旧版管理工具)

  使用方法：`adder.py 表情包目录名 要添加的目录/文件 是否复制` 

  举例： `python adder.py capoo abc.gif 0` , `python adder.py capoo mylist/` 

  是否复制可以不填，默认为复制，填了 0 的话为剪贴

  将会在对应目录下新增对应表清包，名字格式为整数编号 `%04d` 

  为了避免命名混乱，建议 pull\_request 更新使用本格式处理好文件名；如果您有其他命名和文件管理方案也可以。本方案仅供参考。
  
- `repeatChecker.py`

  检查一个文件夹里重复的文件有多少个(用于去重) (懒，以后再做)



后续可能添加更多功能，比如随机输出一个表情(到剪贴板)等。看看有什么需求再更。

