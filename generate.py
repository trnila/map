#!/usr/bin/env python3
import json
from xml import sax
from xml.sax import ContentHandler


class XMLHandler(ContentHandler):
    def __init__(self):
        ContentHandler.__init__(self)

        self._buffer = ''
        self.node = None
        self.tags = {}

        self.locations = []

    def startElement(self, name, attrs):
        if name == 'node':
            self.node = dict(attrs)
            self.tags = {}
        elif name == 'tag':
            self.tags[attrs['k']] = attrs['v']

    def endElement(self, name):
        self._buffer = ''

        if name == 'node' and self.tags:
            if 'public_transport' in self.tags and 'tram' in self.tags:
                self.locations.append({
                    'name': self.tags.get('name', 'NOP'),
                    'lat': self.node['lat'],
                    'lon': self.node['lon'],
                })
#                print(self.node)
#                print(self.tags)

    def characters(self, c):
        self._buffer += c



p = sax.make_parser()
h = XMLHandler()
p.setContentHandler(h)
p.parse(open('/home/daniel//Downloads/ostrava.osm'))

print("export default ", end='')
print(json.dumps(h.locations, indent=4))
