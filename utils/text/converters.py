# Python Standard Library Imports
import re

# Third Party / PIP Imports
import pypandoc


def html2markdown(html):
    """Converts `html` to Markdown-formatted text
    """
    markdown_text = pypandoc.convert_text(html, 'markdown_strict', format='html')
    return markdown_text


def markdown2slack(markdown_text):
    """Converts Markdown-formatted text to Slack-formatted text
    """
    markdown_lines = markdown_text.split('\n')
    slack_lines = []
    for line in markdown_lines:
        line = line.strip()
        # MD bold to intermediate bold markup (to prevent conflict with rewrite of MD italic)
        line = re.sub(r'\*\*(.+?)\*\*', r'<b>\1<b>', line)
        # MD italic to Slack italic
        line = re.sub(r'(\*(.+?)\*)', r'_\1_', line)
        # intermediate bold markup to Slack bold
        line = re.sub(r'<b>(.+?)<b>', r'*\1*', line)
        # MD headings to Slack bold
        line = re.sub(r'^#+(.*)$', r'*\1*', line)
        slack_lines.append(line)
    slack_text = '\n'.join(slack_lines)
    return slack_text


def html2slack(html):
    markdown_text = html2markdown(html)
    slack_text = markdown2slack(markdown_text)
    return slack_text
