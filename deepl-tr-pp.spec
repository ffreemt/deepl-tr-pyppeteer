# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['deepl_tr_pp\\__main__.py'],
             pathex=['C:\\dl\\Dropbox\\mat-dir\\myapps\\pypi-projects\\deepl-tr-pyppeteer'],
             binaries=[],
             datas=[],
             hiddenimports=["dataclasses"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='deepl-tr-pp',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='deepl-tr-pp')
