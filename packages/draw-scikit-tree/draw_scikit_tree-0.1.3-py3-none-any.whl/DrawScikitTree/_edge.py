class Edge:
    '''
    Class to represent a tree edge.

    Parameters
    ----------
    line : str
     - Line from DOT script

    Attributes
    ----------
    Set : str
     - Node ID the edge starts/sets out from

    End : str
     - Node ID the edge ends at
    '''
    def __init__(self, line):
        self.line = line

        linesplit = self.line.split(" -> ")

        self.Set = linesplit[0]
        self.End = linesplit[1]

    def __str__(self):
        _printOut = f"Edge :: {self.line}"

        return _printOut
