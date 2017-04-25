import cx_Freeze
import os

os.environ['TCL_LIBRARY'] = "C:\\Users\\huang\\AppData\\Local\\Programs\\Python\\Python35\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\huang\\AppData\\Local\\Programs\\Python\\Python35\\tcl\\tk8.6"

executables = [cx_Freeze.Executable("simulator.py")]

cx_Freeze.setup(
    name="A bit Racey",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["car_toEast.gif","car_toNorth.gif",
                           "car_toSouth.gif","car_toSouth.gif",
                           "greenLight.gif","redLight.gif","intersection2.gif"]}},
    executables = executables

    )