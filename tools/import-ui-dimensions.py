"""Import dimension data from a catalog DOCX without resizing artwork.

Usage: python3 tools/import-ui-dimensions.py /path/to/catalog.docx
"""
import json
from pathlib import Path
import re
import sys
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]


def read_dimensions(source):
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    with ZipFile(source) as doc:
        root = ET.fromstring(doc.read('word/document.xml'))
    paragraphs = [''.join(n.text or '' for n in p.findall('.//w:t', ns))
                  for p in root.findall('.//w:p', ns)]
    result = {}
    current = None
    for value in paragraphs:
        match = re.match(r'^(UI-\d{3})\s+\S', value)
        if match:
            current = match[1]
            if current in result:
                raise ValueError(f'Duplicate element: {current}')
            result[current] = {}
        elif current and value.startswith('Размер и позиция · '):
            size, marker, position = value.removeprefix('Размер и позиция · ').partition(' Расположение: ')
            if not marker:
                raise ValueError(f'Missing position: {current}')
            result[current].update(screen=size, position=position,
                                   summary=size.split(';', 1)[0].rstrip('.'))
        elif current and value.startswith('Экспорт и размеры файлов · '):
            result[current]['export'] = value.removeprefix('Экспорт и размеры файлов · ')
    expected = {f'UI-{n:03}' for n in range(1, 36)}
    if set(result) != expected:
        raise ValueError('Expected all 35 UI IDs')
    for ui_id, values in result.items():
        if set(values) != {'screen', 'position', 'summary', 'export'} or not all(values.values()):
            raise ValueError(f'Incomplete dimensions: {ui_id}')
    return result


def main():
    source = Path(sys.argv[1])
    dimensions = read_dimensions(source)
    outputs = {}
    for filename in ['catalog.json', 'manifest.json']:
        target = ROOT / 'UI' / filename
        catalog = json.loads(target.read_text())
        for item in catalog['items']:
            item['dimensions'] = dimensions[item['id']]
        catalog['dimensionsSource'] = source.name
        catalog['dimensionsReference'] = {
            'width': 1920, 'height': 1080, 'unit': 'px', 'safeMargin': 48,
            'checkResolutions': [[1920, 1080], [1600, 900], [1280, 720]],
            'coordinateOrigin': 'top-left',
            'canvasScaler': 'Scale With Screen Size',
            'screenMatchMode': 'Match Width Or Height', 'match': 0.5,
            'guidance': 'Размеры на экране и координаты — рекомендации для первого макета. '
                        'В Unity используются anchors и адаптивные панели. '
                        'Размеры экспорта указаны отдельно; экранный размер 3D-предметов зависит от камеры.'
        }
        outputs[target] = json.dumps(catalog, ensure_ascii=False, indent=2) + '\n'
    for target, content in outputs.items():
        target.write_text(content)
    print('Imported screen dimensions, positions and export sizes for all 35 UI elements.')


if __name__ == '__main__':
    main()
