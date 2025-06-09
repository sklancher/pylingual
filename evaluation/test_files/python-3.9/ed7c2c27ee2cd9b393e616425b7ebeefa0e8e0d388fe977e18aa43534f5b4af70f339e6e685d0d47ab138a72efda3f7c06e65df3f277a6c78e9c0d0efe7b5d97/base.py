import socket
import geoip2.database
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address
from django.utils._os import to_path
from .resources import City, Country
GEOIP_SETTINGS = {'GEOIP_PATH': getattr(settings, 'GEOIP_PATH', None), 'GEOIP_CITY': getattr(settings, 'GEOIP_CITY', 'GeoLite2-City.mmdb'), 'GEOIP_COUNTRY': getattr(settings, 'GEOIP_COUNTRY', 'GeoLite2-Country.mmdb')}

class GeoIP2Exception(Exception):
    pass

class GeoIP2:
    MODE_AUTO = 0
    MODE_MMAP_EXT = 1
    MODE_MMAP = 2
    MODE_FILE = 4
    MODE_MEMORY = 8
    cache_options = frozenset((MODE_AUTO, MODE_MMAP_EXT, MODE_MMAP, MODE_FILE, MODE_MEMORY))
    _city_file = ''
    _country_file = ''
    _city = None
    _country = None

    def __init__(self, path=None, cache=0, country=None, city=None):
        """
        Initialize the GeoIP object. No parameters are required to use default
        settings. Keyword arguments may be passed in to customize the locations
        of the GeoIP datasets.

        * path: Base directory to where GeoIP data is located or the full path
            to where the city or country data files (*.mmdb) are located.
            Assumes that both the city and country data sets are located in
            this directory; overrides the GEOIP_PATH setting.

        * cache: The cache settings when opening up the GeoIP datasets. May be
            an integer in (0, 1, 2, 4, 8) corresponding to the MODE_AUTO,
            MODE_MMAP_EXT, MODE_MMAP, MODE_FILE, and MODE_MEMORY,
            `GeoIPOptions` C API settings,  respectively. Defaults to 0,
            meaning MODE_AUTO.

        * country: The name of the GeoIP country data file. Defaults to
            'GeoLite2-Country.mmdb'; overrides the GEOIP_COUNTRY setting.

        * city: The name of the GeoIP city data file. Defaults to
            'GeoLite2-City.mmdb'; overrides the GEOIP_CITY setting.
        """
        if cache not in self.cache_options:
            raise GeoIP2Exception('Invalid GeoIP caching option: %s' % cache)
        path = path or GEOIP_SETTINGS['GEOIP_PATH']
        if not path:
            raise GeoIP2Exception('GeoIP path must be provided via parameter or the GEOIP_PATH setting.')
        path = to_path(path)
        if path.is_dir():
            country_db = path / (country or GEOIP_SETTINGS['GEOIP_COUNTRY'])
            if country_db.is_file():
                self._country = geoip2.database.Reader(str(country_db), mode=cache)
                self._country_file = country_db
            city_db = path / (city or GEOIP_SETTINGS['GEOIP_CITY'])
            if city_db.is_file():
                self._city = geoip2.database.Reader(str(city_db), mode=cache)
                self._city_file = city_db
            if not self._reader:
                raise GeoIP2Exception('Could not load a database from %s.' % path)
        elif path.is_file():
            reader = geoip2.database.Reader(str(path), mode=cache)
            db_type = reader.metadata().database_type
            if 'City' in db_type:
                self._city = reader
                self._city_file = path
            elif 'Country' in db_type:
                self._country = reader
                self._country_file = path
            else:
                raise GeoIP2Exception('Unable to recognize database edition: %s' % db_type)
        else:
            raise GeoIP2Exception('GeoIP path must be a valid file or directory.')

    @property
    def _reader(self):
        return self._country or self._city

    @property
    def _country_or_city(self):
        if self._country:
            return self._country.country
        else:
            return self._city.city

    def __del__(self):
        if self._reader:
            self._reader.close()

    def __repr__(self):
        meta = self._reader.metadata()
        version = '[v%s.%s]' % (meta.binary_format_major_version, meta.binary_format_minor_version)
        return '<%(cls)s %(version)s _country_file="%(country)s", _city_file="%(city)s">' % {'cls': self.__class__.__name__, 'version': version, 'country': self._country_file, 'city': self._city_file}

    def _check_query(self, query, city=False, city_or_country=False):
        """Check the query and database availability."""
        if not isinstance(query, str):
            raise TypeError('GeoIP query must be a string, not type %s' % type(query).__name__)
        if city_or_country and (not (self._country or self._city)):
            raise GeoIP2Exception('Invalid GeoIP country and city data files.')
        elif city and (not self._city):
            raise GeoIP2Exception('Invalid GeoIP city data file: %s' % self._city_file)
        try:
            validate_ipv46_address(query)
        except ValidationError:
            query = socket.gethostbyname(query)
        return query

    def city(self, query):
        """
        Return a dictionary of city information for the given IP address or
        Fully Qualified Domain Name (FQDN). Some information in the dictionary
        may be undefined (None).
        """
        enc_query = self._check_query(query, city=True)
        return City(self._city.city(enc_query))

    def country_code(self, query):
        """Return the country code for the given IP Address or FQDN."""
        return self.country(query)['country_code']

    def country_name(self, query):
        """Return the country name for the given IP Address or FQDN."""
        return self.country(query)['country_name']

    def country(self, query):
        """
        Return a dictionary with the country code and name when given an
        IP address or a Fully Qualified Domain Name (FQDN). For example, both
        '24.124.1.80' and 'djangoproject.com' are valid parameters.
        """
        enc_query = self._check_query(query, city_or_country=True)
        return Country(self._country_or_city(enc_query))

    def coords(self, query, ordering=('longitude', 'latitude')):
        cdict = self.city(query)
        if cdict is None:
            return None
        else:
            return tuple((cdict[o] for o in ordering))

    def lon_lat(self, query):
        """Return a tuple of the (longitude, latitude) for the given query."""
        return self.coords(query)

    def lat_lon(self, query):
        """Return a tuple of the (latitude, longitude) for the given query."""
        return self.coords(query, ('latitude', 'longitude'))

    def geos(self, query):
        """Return a GEOS Point object for the given query."""
        ll = self.lon_lat(query)
        if ll:
            from django.contrib.gis.geos import Point
            return Point(ll, srid=4326)
        else:
            return None

    @property
    def info(self):
        """Return information about the GeoIP library and databases in use."""
        meta = self._reader.metadata()
        return 'GeoIP Library:\n\t%s.%s\n' % (meta.binary_format_major_version, meta.binary_format_minor_version)

    @classmethod
    def open(cls, full_path, cache):
        return GeoIP2(full_path, cache)