# setup.py
import PyInstaller.__main__

PyInstaller.__main__.run([
    '--onefile',
    '--windowed',
    '--name', 'PesaDeDescarte',
    '--add-data', 'Descarte.xlsx;.',
    'main.py'  # Substitua pelo nome real do seu script
])
