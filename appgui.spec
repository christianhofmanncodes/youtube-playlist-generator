# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['src/gui/app_gui.py'],
             pathex=[],
             binaries=[],
             datas=[('src/gui/forms/form.ui', 'forms'), ('src/gui/forms/info_dialog.ui', 'forms'), ('src/gui/forms/settings_dialog.ui', 'forms'), ('src/gui/config/settings.config', 'config'), ('src/icon/youtube-play.icns', 'icon'), ('src/icon/youtube-play.ico', 'icon')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          name='YouTube Playlist Generator',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          icon='src/icon/youtube-play.ico',
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='YouTube Playlist Generator')
app = BUNDLE(coll,
             name='YouTube Playlist Generator.app',
             icon='src/icon/youtube-play.icns',
             bundle_identifier=None)
