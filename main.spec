# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = collect_submodules('sqlalchemy')
hiddenimports += collect_submodules('pandas')
hiddenimports += collect_submodules('xlsxwriter')
hiddenimports += collect_submodules('pyodbc')
hiddenimports += collect_submodules('smtplib')
hiddenimports += collect_submodules('email')
hiddenimports += collect_submodules('xlrd')
hiddenimports += collect_submodules('openpyxl')
hiddenimports += collect_submodules('yaml')

added_files = [
    ('./modules', 'modules'),
]

# Add python313.dll to the binaries list
added_binaries = [
    ('C:\\Program Files\\Python313', '.'),  # Adjust the path to where python<version>.dll is located
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=added_binaries,  # Add binaries here
    datas=added_files,
    hiddenimports=hiddenimports,
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
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=r'images\first_investors_financial_services_logo_IJY_icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
