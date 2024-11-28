import base64
from dataclasses import dataclass
from bson.objectid import ObjectId


@dataclass
class Image:
    mongo_db_image: dict

    @property
    def id(self) -> ObjectId:
        return self.mongo_db_image["_id"]

    @property
    def file(self) -> bytes:
        return self.mongo_db_image["data"]

    @property
    def base64(self) -> bytes:
        return base64.b64encode(self.file)

    @property
    def utf8(self) -> str:
        return self.base64.decode('utf-8')

    @property
    def mime(self) -> str:
        return self.mongo_db_image["mime"]


@dataclass
class NewsItem:
    """

    {
      _id: ObjectId('66a930051e920cdd7576f318'),
      link: 'https://campus.uni-freiburg.de/',
      _public: true,
      showlastday: true,
      archiv: true,
      image: [
        {
          _id: ObjectId('66c0e7df4c00c184fbc55762'),
          stylehome: 'height: 20vw; object-fit: cover',
          stylemonitor: 'height: 20vw; object-fit: cover',
          widthmonitor: 5
        }
      ],
      home: {
        fuerhome: true,
        title_de: 'Bewerbung für die Master-Studiengänge',
        title_en: '',
        text_de: 'Die Bewerbungsphase für die M.Sc.-Studiengänge Mathematik und Mathematics in Data and Technology endet am 15.9.',
        text_en: 'Applications for M.Sc.-Mathematics and Mathematics in Data and Technology must be sent in by September 15.',
        popover_title_de: '',
        popover_title_en: '',
        popover_text_de: '',
        popover_text_en: '',
        start: ISODate('2024-07-10T00:00:00.000Z'),
        end: ISODate('2024-09-15T13:00:00.000Z')
      },
      monitor: {
        start: ISODate('2024-07-10T00:00:00.000Z'),
        end: ISODate('2024-07-15T13:00:00.000Z'),
        title: 'Bewerbung für die Master-Studiengänge',
        text: '<ul><li>Die Bewerbungsfrist für den M.Ed. endet am 15.7.</li><li>Die erste Bewerbungsphase für die M.Sc.-Studiengänge Mathematik und Mathematics in Data and Technology endet am 15.7. Bewerbungen, die danach eingehen, bekommen erst im September eine Zu- oder Absage.</li></ul>',
        fuermonitor: true
      },
      rang: 4,
      bearbeitet: 'Zuletzt bearbeitet von Peter Pfaffelhuber am 17.08.2024 um 20:14:27.',
      kommentar: ''
    }

    """
    mongo_db_newsItem: dict
    image: Image

    @property
    def id(self) -> ObjectId:
        return self.mongo_db_newsItem["_id"]

    @property
    def link(self) -> str:
        return self.mongo_db_newsItem["link"]

    @property
    def public(self) -> bool:
        return self.mongo_db_newsItem["_public"]

    @property
    def show_last_day(self) -> bool:
        return self.mongo_db_newsItem["showlastday"]

    @property
    def is_archived(self) -> bool:
        return self.mongo_db_newsItem["archiv"]

    @property
    def start(self):
        return self.mongo_db_newsItem["home"]["start"]

    @property
    def end(self):
        return self.mongo_db_newsItem["home"]["end"]

    @property
    def intended_for_homepage(self) -> bool:
        return self.mongo_db_newsItem["home"]["fuerhome"]

    @property
    def title_de(self) -> str:
        return self.mongo_db_newsItem["home"]["title_de"]

    @property
    def text_de(self) -> str:
        return self.mongo_db_newsItem["home"]["text_de"]

    @property
    def title_en(self) -> str:
        return self.mongo_db_newsItem["home"]["title_en"]

    @property
    def text_en(self) -> str:
        return self.mongo_db_newsItem["home"]["text_en"]

