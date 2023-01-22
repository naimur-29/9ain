import src.shell as shell

def main():    
    while True:
        text = input("9Shell -> ")
        res, error = shell.run("<stdin>", text)

        if error: print(error.as_string())
        else: print(res)

main()