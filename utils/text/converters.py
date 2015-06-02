import pypandoc

def html2markdown(html):
    markdown = pypandoc.convert(html, 'markdown_strict', format='html')
    return markdown
