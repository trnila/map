#!/usr/bin/env python3
import json
from xml import sax
from xml.sax import ContentHandler


class TramParser:
    def parse(self, node, tags):
        if 'public_transport' in tags and 'tram' in tags:
            return tags.get('name', 'unknown')
        return None

class BicycleParking:
    def parse(self, node, tags):
        if 'amenity' in tags and tags['amenity'] == 'bicycle_parking':
            return 'bicycle parking'

class AmenityParser:
    def __init__(self, name):
        self.name = name

    def parse(self, node, tags):
        if 'amenity' in tags and tags['amenity'] == self.name:
            return tags.get('name', 'unknown')

class BikeRentalParser:
    def parse(self, node, tags):
        if 'service:bicycle:rental' in tags:
            return '\n'.join([
                tags.get('service:bicycle:rental:operator', 'unknown'),
                tags.get('service:bicycle:rental:opening_hours', ''),
            ])


class XMLHandler(ContentHandler):
    def __init__(self):
        ContentHandler.__init__(self)

        self._buffer = ''
        self.node = None
        self.tags = {}
        self.parsers = {}

        self.locations = {}

    def add_parser(self, name, parser):
        self.parsers[name] = parser

    def startElement(self, name, attrs):
        if name == 'node':
            self.node = dict(attrs)
            self.tags = {}
        elif name == 'tag':
            self.tags[attrs['k']] = attrs['v']

    def endElement(self, name):
        self._buffer = ''

        if name == 'node' and self.tags:
            for name, parser in self.parsers.items():
                result = parser.parse(self.node, self.tags)
                if result:
                    self.locations.setdefault(name, []).append({
                        'name': result,
                        'lat': self.node['lat'],
                        'lon': self.node['lon'],
                    })

    def characters(self, c):
        self._buffer += c

    def dump(self):
        return json.dumps(self.locations, indent=4)



p = sax.make_parser()
h = XMLHandler()
h.add_parser("tram", TramParser())
h.add_parser("bicycle_parking", BicycleParking())
h.add_parser("libraries", AmenityParser('library'))
h.add_parser("bike rent", BikeRentalParser())
p.setContentHandler(h)
p.parse(open('/home/daniel//Downloads/ostrava.osm'))

print("export default ", end='')
print(h.dump())
