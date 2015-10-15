import pypandoc
import re

def html2markdown(html):
    """Converts `html` to Markdown-formatted text
    """
    markdown_text = pypandoc.convert(html, 'markdown_strict', format='html')
    return markdown_text

def markdown_to_slack(markdown_text):
    """Converts Markdown-formatted text to Slack-formatted text
    """
    markdown_lines = markdown_text.split('\n')
    slack_lines = []
    for line in markdown_lines:
        line = line.strip()
        # MD headings to Slack bold
        line = re.sub(r'^#+(.*)$', r'*\1*', line)
        # MD bold to Slack bold
        line = re.sub(r'\*\*(.*)\*\*', r'*\1*', line)
        slack_lines.append(line)
    slack_text = '\n'.join(slack_lines)
    return slack_text
