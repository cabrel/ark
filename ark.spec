# -*- mode: python -*-
a = Analysis(['ark.py'],
             pathex=['C:\\Users\\robin.harper.RED4\\workspace\\mine\\python\\projects\\ark'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='ark.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
