# jupyter-notebook-html-tools

The project is a stub and has born for 2 reason, getting an easy and cheap way to generate, display and manipulate HTML in Python jupiter notebooks to be able to do fancy thing like updating charts and images on the fly. But also have been for me a nice way to familiarize with the jupyter notebook enviroment and play more with python. 
Because of this, you may find bugs and things not written it pythonic way.

As always the software is provided "as-is", feel free to use it, change it, fork it and distribute it as peases you. Feel free to drop me a line or a pull request.


- Example 1   
Insert a div and append some content later using jQuery
```python

htk = HtmlToolkit()
js = htk.js
jQuery = htk.jQuery

elemId = 'my-div-is-better'
elemHtml = htk.buildTag('div',{'id':elemId},'This is the first message')

htk.printHTML(elemHtml)
hr = htk.buildTag('hr')
jQuery('#'+elemId).append(hr)
jQuery('#'+elemId).append('This is the second message')
js.alert('Eureka!')

```

- Example 2   
Embed (base64) an image via html
```python

htk = HtmlToolkit()
js = htk.js
jQuery = htk.jQuery

img = np.random.random((100, 100, 3)) #perhaps use a real image
  
elemId = 'embed-img'
elemHtml = htk.embedImageArray(img,{'id':elemId})

htk.printHTML(elemHtml)

```




