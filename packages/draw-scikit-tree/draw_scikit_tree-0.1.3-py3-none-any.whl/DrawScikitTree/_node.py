class Node:
    '''
    Class to represent a tree node.

    Parameters
    ----------
    line : str
     - Line from DOT script.

    shape : str
     - Default shape for the node.

    Attributes
    ----------
    line : str
     - The entire string representation of the node.

    shape : str
     - Shape of the node.

    ID : str
     - ID of the node.

    Feature : str
     - Feature used in this node to split the tree.

    FeatureThreshold : str
     - Threshold of feature used, to split the feature space.

    color : str
     - Color of node edge in RGBA value as hexadecimal strings.
    '''
    def __init__(self, line, shape):
        self.line = line
        self.shape = shape
        
        self.ID = self.get_id(self.line)

        self.Feature, self.FeatureThreshold = self.get_feature_threshold(
            self.line
        )

    def get_id(self, line):
        '''Get node's ID.'''
        return line.split(" [")[0]

    def __str__(self):
        _printOut = f"Node :: {self.line}"

        return _printOut

    def get_feature_threshold(self, line):
        '''Returns the feature name and threshold.'''
        linesplits = line.split('\\n')

        f = linesplits[0].split("<=")[0].split("=")[1][1:]
        
        featureSplit = f.split('_')
        f_threshold = linesplits[0].split("<= ")[-1]
        
        return f, f_threshold

    def get_label(self):
        '''Get label.'''
        return self.line.split("label=\"")[1].split(
            "\"] ;"
        )[0]

    def set_label(self, _input):
        '''Set label.'''
        self.line = self.line.replace(self.get_label(), _input)

    def get_shape(self):
        '''Get shape.'''
        return self.shape

    def set_shape(self, _shape):
        '''
        Set shape.

        Parameters
        ----------
        _shape : str
         - Desired shape of node. Get available shapes for nodes from:
           https://graphviz.org/doc/info/shapes.html
        '''
        self.shape = _shape
        self.line = self.line.replace(
            "] ;", f" shape=\"{_shape}\"] ;"
        )

    def set_color(self, red, green, blue, alpha):
        '''
        Set RGBA colors.

        Parameters
        ----------
        red : int [0, 255]
         - Value for red.

        green : int [0, 255]
         - Value for green.

        blue : int [0, 255]
         - Value for blue.

        alpha : float [0.0, 1.0]
         - Value for alpha.
        '''
        # Convert numerical values to hexadecimal strings
        R = self.convert_int_to_hexstring(red)
        G = self.convert_int_to_hexstring(green)
        B = self.convert_int_to_hexstring(blue)
        alpha = self.convert_int_to_hexstring(int(alpha*255))

        self.color = f"#{R}{G}{B}{alpha}"
        self.line = self.line.replace(
            "] ;", f" color=\"{self.color}\"] ;"
        )

    def convert_int_to_hexstring(self, _value):
        '''
        Function to convert values ([0, 255] for RGB or [0.0, 1.0] for alpha)
        to hexadecimal string.

        Parameters
        ----------
        _values : int [0, 255] or float [0.0, 1.0]
        '''
        _hexStr = hex(_value).split('x')[1]
        if len(_hexStr) == 1:
            _hexStr = f"0{_hexStr}"
        
        return _hexStr

    def set_penwidth(self, width):
        '''
        Function to set the width (thickness) of the node outline.

        Parameters
        ----------
        width : float
        '''
        self.line = self.line.replace("] ;", f" penwidth={width}] ;")
        
