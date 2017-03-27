# html output helper

from IPython.core.display import display, HTML
import base64, cv2, uuid
import numpy as np
from io import StringIO


class JsRunner():
    def __init__(self, htk):
        self.htk = htk

    def __getattr__(self, name):
        def wrapper(*args, **kw):
            # print(self.htk.functionJS(name,(args)))
            # print('called with %r and %r' % (args, kw))
            return self.htk.runFunctionJS(name, (args))

        return wrapper


class jQueryRunner():
    def __init__(self, element):
        self.htk = HtmlToolkit()
        self.element = element

    def __getattr__(self, name):
        def wrapper(*args, **kw):
            element = self.htk.functionJS('$', [self.element])
            funct = self.htk.functionJS(name, args)
            contrap = element + "." + funct + ";"
            self.htk.runJS(contrap)

        return wrapper
        pass


class HtmlToolkit():
    def __init__(self):
        self.js = JsRunner(self)

    def jQuery(self, element):
        return jQueryRunner(element)

    def printHTML(self, string):
        display(HTML(str(string)))

    def buildTag(self, tag, attr={}, content=None):
        attr_str = ""
        for key in attr:
            value = attr[key]
            if str(value) == value:
                value = str(value).replace('"', '\\"')
            attr_str += key + "=\"" + str(value) + "\" "
        tag_str = ""
        if content is not None:
            tag_str = "<" + tag + " " + attr_str + ">" + content + "</" + tag + ">"
        else:
            tag_str = "<" + tag + " " + attr_str + "/>"
        # print('buildTag!',tag_str)
        return tag_str

    def runJS(self, js):
        elementId = 'script-' + str(uuid.uuid1())
        js = "$('#" + elementId + "').parentsUntil('.output_area').hide();\n" + js
        # display(Javascript(js))
        html = self.buildTag('script', {'id': elementId}, js)
        # print(html)
        self.printHTML(html)

    def runFunctionJS(self, name, params, milliseconds=None):
        functionCall = self.functionJS(name, params) + ";"
        if milliseconds is None:
            self.runJS(functionCall)
        else:
            self.runDelayJS(functionCall, milliseconds)

    def _(self, name, params, milliseconds=None):
        return self.runFunctionJS(name, params, milliseconds)

    def functionJS(self, name, params):
        cleanParams = []
        for param in params:
            if str(param) == param:
                param = str(param).replace("'", "\\'")
                param = "'" + param + "'"
            cleanParams.append(str(param))
        paramsStr = ', '.join(cleanParams)
        functionCall = name + '(' + paramsStr + ')'
        return functionCall

    def quirkQuotes(param, quote='"'):
        if str(param) == param:
            param = str(param).replace(quote, "\\" + quote)
            param = "'" + param + "'"
        return param

    def runDelayJS(self, js, milliseconds):
        milliseconds = str(int(milliseconds))
        js = "setTimeout(function(){" + js + "}, " + milliseconds + ");"
        self.runJS(js)

    def htmlTableRow(self, row, attr=[]):
        content = ''
        for cell in row:
            if not isinstance(cell, dict):
                cell = {'content': cell}
            if 'attr' not in cell:
                cell['attr'] = {}
            content += self.htmlTableCell(cell['content'], cell['attr'])
        return self.buildTag('tr', attr, content)

    def htmlTableCell(self, content, attr=[]):
        return self.buildTag('td', attr, content)

    def htmlTable(self, rows, attr=[]):
        content = ''
        for row in rows:
            if not isinstance(row, dict) or 'content' not in row:
                row = {'content': row}
            if 'attr' not in row:
                row['attr'] = {}
            content += self.htmlTableRow(row['content'], row['attr'])
        return self.buildTag('table', attr, content)

    def htmlImage(self, src, attr={}):
        attr['src'] = src
        html = self.buildTag('img', attr)
        # print(html)
        return html

    def embedImage(self, image_png, attr={}):
        image_b64 = base64.encodebytes(image_png).decode("utf-8").replace('\n', '')
        image_b64 = "data:image/png;base64, " + image_b64
        return self.htmlImage(image_b64, attr)

    def embedImageArray(self, image, attr={}):
        # denormalize
        image = np.array(image)

        if np.amax(image) <= 1:
            image = image * 255

        # image=np.array(image,np.int32)
        # print(image)
        # convert to RGB if needed
        s = image.shape
        if len(s) == 2 or (len(s) == 3 and s[2] == 1):
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        # print(image[:,:,0][15,15])
        image_png = cv2.imencode('.png', image)[1]
        image_png = np.reshape(image_png, (-1))
        return self.embedImage(image_png, attr)

    def embedFigure(self, fig, attr={}):  # pyplot figure
        imgPointer = StringIO()
        fig.savefig(imgPointer, format='png')
        imgPointer.reset()
        data = imgPointer.read()
        return self.embedImage(data, attr)
