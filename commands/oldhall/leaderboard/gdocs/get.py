from .auth import get_credentials
from json import dumps
from os.path import join, dirname

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

dir = dirname(__file__)

def read_paragraph_element(element):
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')

def read_structural_elements(elements):
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
        elif 'table' in value:
            # The text in table cells are in nested Structural Elements and tables may be
            # nested.
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += read_structural_elements(cell.get('content'))
        elif 'tableOfContents' in value:
            # The text in the TOC is also in a Structural Element.
            toc = value.get('tableOfContents')
            text += read_structural_elements(toc.get('content'))
    return text


def teacher_list(doc: str) -> list[str]:
    with open (join(dir, 'dailypost.txt'), 'w') as f:
        f.write(doc)
    start = 'Absent Teachers:'
    startidx = doc.index(start) + len(start)
    end = 'Freshmen are reminded'
    endidx = doc.index(end)

    teachers_str = doc[startidx:endidx]
    return teachers_str.strip().split('\n')


def get_text(id: str):
    creds = get_credentials()

    service = build('docs', 'v1', credentials=creds)
    document = service.documents().get(documentId=id).execute()

    return read_structural_elements(document['body']['content'])

def get_teachers () -> list[str]:
    dailypost = '1jkuu7WO4JWWTWKcSAGUhIdb5IRkNjBcbutZcLPehtq8'
    doc_str = get_text(dailypost)
    return teacher_list(doc_str)