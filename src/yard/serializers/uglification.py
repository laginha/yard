ALPHABET = [chr(i) for i in range(97, 123)]
ALPHABET_SIZE = len(ALPHABET)


class Mapping(dict):
    def __init__(self):
        self.inverted = {}
        self.length = 0
    
    def to_char(self, number):
        index = number / ALPHABET_SIZE
        first_char = ALPHABET[ index-1 ] if index else ''
        last_char = ALPHABET[ (number % ALPHABET_SIZE)-1 ]
        return first_char + last_char
    
    def add(self, key):
        mapped_to = self.inverted.get( key )
        if mapped_to:
            return mapped_to
        self.length += 1
        char = self.to_char(self.length)
        self[ char ] = key
        self.inverted[key] = char
        return char


def uglify_json(json):
    def uglify(value):
        if isinstance(value, list):
            uglify_list( value )
        elif isinstance(value, dict):
            uglify_dict( value )
    
    def uglify_list(list_):
        for item in list_:
            uglify( item )
    
    def uglify_dict(dict_):
        for key,value in dict_.items():
            dict_[ mapping.add(key) ] = dict_.pop( key )
            uglify( value )
     
    mapping = Mapping()
    uglify( json )
    return {
        "Mapping": mapping,
        "Objects": json
    }
