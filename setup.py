from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine-tuning.
# Removed "excludes": ["tkinter"] as tkinter is needed.
# Ensure that "packages" includes all the necessary packages.
build_exe_options = {
    "packages": ["os", "tkinter", "matplotlib", "PIL", "sys", "colorsys"],
    "include_files": ["icon.png", "copy.png", "picker.png", "logo.ico"]
}

# If the application is a GUI application, uncomment the line below:
# base = "Win32GUI"

setup(
    name="ColorConverter",
    version="0.1",
    description="Your application description",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base="Win32GUI", icon='logo.ico')]  # Include the icon for the executable if needed
)
