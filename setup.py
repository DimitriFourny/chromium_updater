from cx_Freeze import setup, Executable

executables = [
  Executable(
    'run.py',
    base = None,
    targetName = 'chromium_updater'
  )
]

setup(
  name='Chromium Updater',
  version = '0.1',
  description = 'Chromium Updater',
  executables = executables
)