import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="BlackJack",
    options={"build_exe":{"packages":["pygame"],
                          "included_file":["img/icon.png"]}},
    executables = executables
)