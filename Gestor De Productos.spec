# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\iplup\\Desktop\\Python\\Tokio\\Entregas\\M6_Aplicacion_De_Escritorio\\Gestor_De_Productos\\models.py', '.'), ('C:\\Users\\iplup\\Desktop\\Python\\Tokio\\Entregas\\M6_Aplicacion_De_Escritorio\\Gestor_De_Productos\\app.py', '.'), ('C:\\Users\\iplup\\Desktop\\Python\\Tokio\\Entregas\\M6_Aplicacion_De_Escritorio\\Gestor_De_Productos\\db.py', '.'), ('C:\\Users\\iplup\\Desktop\\Python\\Tokio\\Entregas\\M6_Aplicacion_De_Escritorio\\Gestor_De_Productos\\resources', 'resources'), ('C:\\Users\\iplup\\Desktop\\Python\\Tokio\\Entregas\\M6_Aplicacion_De_Escritorio\\Gestor_De_Productos\\database', 'database'), ('C:\\Users\\iplup\\Desktop\\Python\\Tokio\\Entregas\\M6_Aplicacion_De_Escritorio\\Gestor_De_Productos\\windows', 'windows')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Gestor De Productos',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\iplup\\Desktop\\Python\\Tokio\\Entregas\\M6_Aplicacion_De_Escritorio\\Gestor_De_Productos\\resources\\icon.ico'],
)
