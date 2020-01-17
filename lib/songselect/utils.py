# Python Standard Library Imports
import re

# Third Party (PyPI) Imports
from bs4 import BeautifulSoup


class SongSelectSong(object):
    def __init__(self, content):
        soup = BeautifulSoup(content, 'html.parser')

        title = soup.select('.cproTitle')
        if title:
            title = title[0].string
            self.title = title
        else:
            self.title = ''

        key = soup.select('.cproSongKey')
        if key:
            self.key = key[0].string
        else:
            self.key = None

        authors = soup.select('.cproAuthors')
        if len(authors):
            self.author = authors[0].string
        else:
            self.author = ''

        self.tempo = None
        self.time = None
        tempo_time = soup.select('.cproTempoTimeWrapper')
        if tempo_time:
            tempo_time = tempo_time[0].string
            parts = [s.strip() for s in tempo_time.split(' ')]
            parts = filter(lambda x: x not in ('|', '-'), parts)
            mode = None
            for i in range(len(parts)):
                value = parts[i]
                if value in ('Tempo', 'Time',):
                    mode = value
                else:
                    if mode == 'Tempo':
                        self.tempo = value
                    else:
                        self.time = value
        else:
            pass

        copyright_info = soup.select('.copyright-info')
        if copyright_info:
            copyright_info = copyright_info[0]
            song_number = copyright_info.select('.songnumber')
            if song_number:
                song_number_str = '%s' % song_number[0].string
                song_number = re.match(r'.*?(\d+).*?', song_number_str).group(1)
                self.song_number = song_number
            else:
                self.song_number = None

            try:
                self.copyright = copyright_info.ul.li.string
            except:
                self.copyright = None

        song_body = soup.select('.cproSongBody')[0]
        song_sections = song_body.select('.cproSongSection')
        if len(song_sections) == 0:
            # treat entire body as one section, if there are no sections
            song_sections = [song_body]
        self.song_sections = []
        for song_section in song_sections:
            self.song_sections.append(self.song_section_html2chopro(song_section))

        self.song_body = '\n\n'.join(self.song_sections)

    def song_section_html2chopro(self, song_section_html):
        comments = song_section_html.select('span.cproComment')
        for comment in comments:
            comment.string = '{c: %s}' % comment.string
            comment.unwrap()

        chords = song_section_html.select('code.chord')
        for chord in chords:
            chord.string = '[%s]' % chord.text
            chord.unwrap()

        lyrics = song_section_html.select('span.chordLyrics')
        for lyric in lyrics:
            lyric.unwrap()

        chord_wrappers = song_section_html.select('span.chordWrapper')
        for chord_wrapper in chord_wrappers:
            chord_wrapper.unwrap()

        song_lines = song_section_html.select('.cproSongLine')
        for song_line in song_lines:
            s = '%s' % ''.join([s for s in song_line.strings])
            song_line.string = re.sub(r'[\t\n]', '', s)
            song_line.unwrap()

        song_section_html.string = ''.join([s for s in song_section_html.strings])
        return '%s' % song_section_html.string

    def chordpro(self):
        chordpro_text = """{title: %(title)s}
{author: %(author)s}
{tempo: %(tempo)s}
{time: %(time)s}

%(song_body)s
        """ % {
            'title' : self.title,
            'author' : self.author,
            'key' : self.key,
            'tempo' : self.tempo,
            'time' : self.time,
            'song_body' : self.song_body,
        }
        return chordpro_text
