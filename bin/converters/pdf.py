from natsort import natsorted
import pprint
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

from converters.base import AbstractConverter


class PdfConverter(AbstractConverter):
    def __init__(self, args):
        super().__init__()
        self._from_dir = args.from_dir
        self._out_path = args.to
        self._songs = []

    @staticmethod
    def create_argparser(subparsers):
        parser_html = subparsers.add_parser("pdf", help="Converts to a PDF document for offline use.")
        parser_html.add_argument("--to", required=True, help="path to the output file; will be overwritten if exists")
        return parser_html

    def convert(self, song_yaml, filepath):
        self._preprocessor.preprocess(song_yaml, soft_line_break_strategy='ignore', hard_break_strategy='convert')

        hu_book = self._get_book_from_yaml(song_yaml, 'emm_hu')
        if hu_book is None:
            return
        song_yaml['_pdfconv_hu_book'] = hu_book

        self._songs.append(song_yaml)

    def finish(self):
        self._songs = natsorted(self._songs, key=lambda s: s['_pdfconv_hu_book']['number'])

        books_yaml = self.read_books(self._from_dir)
        chapters = next((b for b in books_yaml if b['id'] == 'emm_hu'))['chapters']
        songs_by_chapters = {c['id']: {'chapter': c, 'songs': []} for c in chapters}
        songs_by_chapters_seq = [songs_by_chapters[c['id']] for c in chapters]
        for song in self._songs:
            songs_by_chapters[self._get_book_from_yaml(song, 'emm_hu')['chapter']]['songs'].append(song)

        html_header = [
            '<!DOCTYPE html>',
            '<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Emmet Offline</title><style>',
            _CSS_SECTION,
            '</style></head><body>',
            '<h1>Jézus él!</h1>',
        ]

        html_toc = ['<h2 id="toc">Tartalomjegyzék</h2><section class="emmet-toc">']
        html_songs = []
        # for song in self._songs:
        for chapter in songs_by_chapters_seq:
            html_toc.append('<h3><span class="badge badge-primary">{badge}</span> {name}</h3><ul>'
                            .format(badge=chapter['chapter']['badge'], name=chapter['chapter']['name']))
            for song in chapter['songs']:
                book = song['_pdfconv_hu_book']
                lyrics = self._get_lyrics_from_yaml(song, book['lang'])

                html_toc.append('<li><span class="badge badge-info">{songNo}</span> <a name="toc-song-{songNo}" href="#song-{songNo}">{songTitle}</a></li>'
                                .format(songNo=book['number'], songTitle=lyrics['title']))
                html_songs.append('<h2 id="song-{songNo}" class="emmet-song-header"><span class="badge badge-info">{songNo}</span> {songTitle}</h2>'
                                  .format(songNo=book['number'], songTitle=lyrics['title']))
                html_songs.append('<div class="emmet-song">')
                for verse in lyrics['verses']:
                    disp_verse_number = self._get_displayed_verse_name(verse['name'])
                    additional_class = ''
                    if verse['name'].startswith('c'):
                        additional_class = ' emmet-chorus'
                    if verse['name'].startswith('b'):
                        additional_class = ' emmet-bridge'
                    html_songs.extend((
                        '<div class="emmet-song-verse">',
                        '<div class="emmet-header{additional_class}">{disp_verse_number}</div>'
                            .format(additional_class=additional_class, disp_verse_number=disp_verse_number),
                        '<div class="emmet-body{additional_class}">'
                            .format(additional_class=additional_class),
                        '\n'.join('<p>'+l+'</p>' for l in verse['lines']),
                        '</div></div>'
                    ))
                html_songs.append('</div>')
                html_songs.append('<p class="emmet-toplink"><a href="#toc-song-{songNo}">↑ Vissza a tartalomjegyzékre</a></p>'
                                  .format(songNo=book['number']))
            html_toc.append('</ul>')
        html_toc.append('</section>')
        html_end = '</body></html>'

        html_doc = '\n'.join(html_header + html_toc + html_songs + [html_end])

        pdf_fontconfig = FontConfiguration()
        pdf_html = HTML(string=html_doc)
        pdf_css = CSS(string="""
            @font-face {
                font-family: 'lato';
                src: url(file:/usr/share/fonts/truetype/lato/Lato-Regular.ttf);
                font-weight: normal;
                font-style: normal;
            }
            @font-face {
                font-family: 'lato';
                src: url(file:/usr/share/fonts/truetype/lato/Lato-Bold.ttf);
                font-weight: 700;
                font-style: normal;
            }
            @font-face {
                font-family: 'lato';
                src: url(file:/usr/share/fonts/truetype/lato/Lato-Italic.ttf);
                font-weight: normal;
                font-style: italic;
            }
            @font-face {
                font-family: 'lato';
                src: url(file:/usr/share/fonts/truetype/lato/Lato-BoldItalic.ttf);
                font-weight: 700;
                font-style: italic;
            }
            @page {
                size: 105mm 149mm;
                margin: 0;
            }
        """ + _CSS_SECTION, font_config=pdf_fontconfig)
        pdf_html.write_pdf(self._out_path, stylesheets=[pdf_css], font_config=pdf_fontconfig)

    @staticmethod
    def _get_displayed_verse_name(verse_code):
        # This is copied as is from loader.js:getDisplayedVerseCode.
        verse_type = verse_code[0]
        verse_number = verse_code[1:]

        disp_code = ""
        if verse_type == "c":
            disp_code = "R"
        elif verse_type == "b":
            disp_code = "Á"
        elif verse_type == "p":
            disp_code = "E"

        disp_code += verse_number
        return disp_code


_CSS_SECTION = """
/* Copied from Emmet, as is */
.emmet-song {
    display: table;
    border-spacing: 7px 10px;
    margin-left: -7px; margin-top: -10px;
}
.emmet-song-verse {
    display: table-row;
}
.emmet-song-verse > * {
    display: table-cell;
}
.emmet-song-verse .emmet-header {
    background-color: #444;
    padding: 5px;
    border-radius: 6px;
    text-align: center;
}
.emmet-song-verse .emmet-header.emmet-chorus {
    background-color: #981b27;
}
.emmet-song-verse .emmet-header.emmet-bridge {
    background-color: #003e80;
}
.emmet-song-verse .emmet-body {
    padding-bottom: 5px;
}
.emmet-song-verse .emmet-body.emmet-chorus {
    font-style: italic;
}
.emmet-song-verse .emmet-body p {
    margin-bottom: 0px;
}
.emmet-song-verse .emmet-body p::after {
    content: "";
    display: inline-block;
    width: 0px;
}
span.badge {
    padding-top: 0.4em;
    vertical-align: text-bottom;
}
.badge-info {
    color: #fff;
    background-color: #3498DB;
}
.badge-primary {
    color: #fff;
    background-color: #375a7f;
}
.badge {
    display: inline-block;
    padding: 0.25em 0.4em;
    font-size: 75%;
    /* font-weight: 700; -- removed */
    line-height: 1;
    text-align: center;
    white-space: nowrap;
    vertical-align: baseline;
    border-radius: 0.25rem;
}
/* Custom fixes */
body {
    font-family: Lato;
    /* Copied from the Bootstrap template */
    background-color: #222;
    color: #fff;
    font-size: 0.9375rem;
    font-weight: 400;
    line-height: 1.5;
}
p {margin-top: 0px;}
a, a:visited {color: #fff;}
section.emmet-toc ul {margin-top: 0px; margin-bottom: 25px;}
section.emmet-toc h3 {margin-bottom: 7px;}
p.emmet-toplink {font-size: 12px;}
.emmet-song-verse .emmet-body {width: 100%;}
.emmet-song-verse .emmet-body p {text-indent: -15px; padding-left: 15px;}
.emmet-song-header {
    page-break-before: always;
    padding-top: 9px;
    margin-top: 9px; /* margin-top: ~18px split to have a margin at the top of the pages */
}
"""