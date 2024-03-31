# WeaponPaintsTranslator
自动翻译cs2-WeaponPaints插件前端的物品名称脚本，从VPK内的游戏翻译文件读取

## 使用方法
先执行:
```
pip install -r requirements.txt
```

然后执行:
```
python translate.py
```

根据命令行提示，输入路径，即可开始翻译

翻译后的文件生成在这个脚本所在目录下的output文件夹

## Credits
`keyvalues.py` 来自 [valve-keyvalues-python](https://github.com/gorgitko/valve-keyvalues-python)

`vpk` 包 [vpk](https://github.com/ValvePython/vpk)
