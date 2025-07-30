from reportlab.platypus import Paragraph, ParaParser


class CustomParser(ParaParser):
    def findSpanStyle(self, style: str):
        return None


class CustomParagraph(Paragraph):
    def __init__(self, text, style=None, bulletText=None, frags=None, caseSensitive=1, encoding='utf8'):
        super().__init__(text, style, bulletText, frags, caseSensitive, encoding)

    def _setup(self, text, style, bulletText, frags, cleaner):

        # This used to be a global parser to save overhead.
        # In the interests of thread safety it is being instantiated per paragraph.
        # On the next release, we'll replace with a cElementTree parser
        if frags is None:
            text = cleaner(text)
            _parser = CustomParser()
            _parser.caseSensitive = self.caseSensitive
            style, frags, bulletTextFrags = _parser.parse(text, style)
            if frags is None:
                raise ValueError("xml parser error (%s) in paragraph beginning\n'%s'" \
                                 % (_parser.errors[0], text[:min(30, len(text))]))
            textTransformFrags(frags, style)
            if bulletTextFrags: bulletText = bulletTextFrags

        # AR hack
        self.text = text
        self.frags = frags  # either the parse fragments or frag word list
        self.style = style
        self.bulletText = bulletText
        self.debug = 0  # turn this on to see a pretty one with all the margins etc.


def textTransformFrags(frags, style):
    tt = style.textTransform
    if tt:
        tt = tt.lower()
        if tt == 'lowercase':
            tt = str.lower
        elif tt == 'uppercase':
            tt = str.upper
        elif tt == 'capitalize':
            tt = str.title
        elif tt == 'none':
            return
        else:
            raise ValueError('ParaStyle.textTransform value %r is invalid' % style.textTransform)
        n = len(frags)
        if n == 1:
            # single fragment the easy case
            frags[0].text = tt(frags[0].text)
        elif tt is str.title:
            pb = True
            for f in frags:
                u = f.text
                if not u: continue
                if u.startswith(u' ') or pb:
                    u = tt(u)
                else:
                    i = u.find(u' ')
                    if i >= 0:
                        u = u[:i] + tt(u[i:])
                pb = u.endswith(u' ')
                f.text = u
        else:
            for f in frags:
                u = f.text
                if not u: continue
                f.text = tt(u)
