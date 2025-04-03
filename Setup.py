# setup.py
import PyInstaller.__main__
import os
import sys

# Define o separador correto para diferentes sistemas operacionais
sep = ";" if sys.platform == "win32" else ":"

PyInstaller.__main__.run([
    '--onefile',               # Gera um único arquivo executável
    '--windowed',              # Oculta o terminal (troque por --console se quiser ver os logs)
    '--name', 'PesaDeDescarte',  # Nome do executável
    '--add-data', f'Descarte.xlsx{sep}.',  # Adiciona o arquivo Excel
    '--hidden-import=openpyxl',  # Importa openpyxl explicitamente
    '--hidden-import=openpyxl.cell', 
    '--hidden-import=openpyxl.cell._writer',
    '--hidden-import=openpyxl.utils',  
    '--hidden-import=openpyxl.styles',  
    '--hidden-import=openpyxl.workbook',  
    '--hidden-import=openpyxl.worksheet',  
    'Main.py'  # Substitua pelo nome real do seu script
])
