from django import template
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.lexers import BashLexer
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

register = template.Library()

# @register.filter
def syn(code, lang="python", linenos=True):
    lexer = get_lexer_by_name(lang)
    formatter = HtmlFormatter(linenos=linenos, cssclass="syntax")
    return highlight(code, lexer, formatter)

@register.filter
def error_msg(ex):
    
    error_type = ex.__class__.__name__
    try:
        msg = ex.args[0]
    except:
        msg = ""
    extra = ""
    try: # for syntax errors
        msg = ex.msg
        extra = """
Failed at line {}, col {}
{}
{}^
""".format(ex.lineno, ex.offset, ex.text.strip(), " " * max(ex.offset - 1, 0))
    except:
        pass

    if error_type == "AssertionError":
        msg = "returned unexpected result"
        extra = ex.args[0]

    report = """{}: {}
{}
"""

    # formatter = HtmlFormatter(linenos=False, cssclass="source")
    # result = highlight(, BashLexer(), formatter)

    return report.format(error_type, msg, extra)