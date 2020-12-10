from gui import client_app


def main():
    root = client_app.Root(None, client_app.Game())
    root.title("Default")
    myapp = client_app.App(root)
    myapp.mainloop()


if __name__ == "__main__":
    main()