#!./bin/python
from proxyweb.startup.create_app import create_app
from proxyweb.startup.manager import manager

app = create_app()

if __name__ == "__main__":
    manager.run()
