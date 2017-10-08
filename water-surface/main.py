
from Canvas import Canvas
from vispy import app
from surface.Surface import Surface

if __name__ == '__main__':
    c = Canvas(Surface(nwave=5, max_height=0.3))
    app.run()
