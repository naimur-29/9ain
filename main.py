import src.shell as shell

while True:
    text = input("9ain-shell -> ")
    res, error = shell.run("<stdin>", text)

    if error: print(error.as_string())
    else: print(res)