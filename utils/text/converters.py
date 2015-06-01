import pypandoc

def html_to_markdown(html):
    markdown = pypandoc.convert(html, 'md', format='html')
    return markdown
