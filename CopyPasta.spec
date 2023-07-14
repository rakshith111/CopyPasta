# tz_app.spec

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['src/main.py'],
             pathex=['src'],
             binaries=[],
             datas=[('src//ui_files//icons//icon.png', 'src//ui_files//icons//'),('src//ui_files//icons//title.png', 'src//ui_files//icons//')  ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)

exe = EXE(  pyz,
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,
            [],
            name='CopyPasta',
            debug=False,
            bootloader_ignore_signals=False,
            strip=False,
            upx=True,
            upx_exclude=[],
            icon='src/ui_files/icons/icon.ico',
            runtime_tmpdir=None,
            console=False)

