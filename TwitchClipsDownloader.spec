# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
    ('','ChromeDrivers/')
]

a = Analysis(['TwitchClipsDownloader.py'],
             pathex=['D:\\Projects\\Python\\TwitchVideoDownloader'],
             binaries=[],
             datas=[],
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
a.datas += [('ChromeDrivers\\chromedriver.exe', 'ChromeDrivers\\chromedriver.exe', 'DATA')]
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Twitch Clips Downloader',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='Resources\\app.ico')
