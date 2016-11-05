# -*- encoding: utf8 -*-

import re
import io

FLAG = True
    
class Reader(object):
    def __init__(self, input, flag=False):
        """Takes as argument an object to feed lines to the Reader."""
        try:            
            self.lineFeeder = open(input)
        except Exception:
            self.lineFeeder = io.StringIO(unicode(input))
        global FLAG
        FLAG = flag
    
    @staticmethod
    def _cleverSplit(line):
        # Split tokens (keeping quoted strings intact).
        PATTERN = re.compile(r"""(
                ^\[.*?\] |                        # Match Braces
                ".*?[^\\]?" | '.*?[^\\]?' |       # Match Single/double-quotes
                \# |                              # hash
                \s | \] | \[ | \, | \s= |         # Whitespace, braces, comma, =
            )""", re.X)
        # Line stripping is essential for keygroup matching to work.
        if FLAG:
            print("token:", [p for p in PATTERN.split(line.strip()) if p.strip()])
        return [p for p in PATTERN.split(line.strip()) if p.strip()]
        
    def _readNextLine(self):
        # Get next line from input.
        try: # Turn next line into a list of tokens.
            tline = self._cleverSplit(next(self.lineFeeder))
            if not tline or tline[0] == "#":
                self.line = self._readNextLine()
            else:
                self.line = tline
        except StopIteration:
            self.line = None
        return self.line

    def __next__(self):
        # Returns next token in the current LINE.
        # Ignores comments.
        if not self.line or self.line[0] == "#":
            return None
        return self.line[0]

    def assertEOL(self):
        if self.line and self.line[0] != '#':
            raise Exception("EOF expected but not found.",self.line)
    def pop(self,expect=None):
        if not self.line:
            return False
        val = self.line.pop(0)
        if expect and val != expect:
            raise Exception("Poped token '%s' was not expected '%s'." % (val,expect))
        return val
    def top(self):
        rem = self.__next__()
        if not rem:
            self._readNextLine()
            return self.top()
        return rem
    def skip(self,*expect):
        val = self.pop()
        if expect and val not in expect:
            raise Exception("failed to skip token '%s':expected one in '%s,'." % (val,', '.join(expect)))
    def allownl(self):
        if not self.__next__():
            self._readNextLine()
    def custom_next(self):
        return self.__next__()
