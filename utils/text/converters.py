import pypandoc

def html2markdown(html):
    markdown = pypandoc.convert(html, 'md', format='html')
    return markdown
