from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def has_value(cls, value: str):
        return value in set(item.value for item in cls)

    @classmethod
    def get_item(cls, value: str):
        return next((item for item in cls if item.value == value), None)


class Font(BaseEnum):
    LATO = 'lato'
    MERRIWEATHER = 'merriweather'
    NOTO_SANS = 'noto-sans'
    NOTO_SERIF = 'noto-serif'
    OPEN_SANS = 'open-sans'
    PLAYFAIR = 'playfair'
    PT_SERIF = 'pt-serif'
    ROBOTO = 'roboto'
    ROBOTO_MONO = 'roboto-mono'
    HELVETICA = 'helvetica'
    SOURCE_SANS_PRO = 'source-sans-pro'


class PaginationPosition(BaseEnum):
    NONE = 'NONE'  # Disabled
    LEFT = 'LEFT'
    CENTER = 'CENTER'
    RIGHT = 'RIGHT'


class ElementType(BaseEnum):
    TEXT = 'TEXT'
    IMAGE = 'IMAGE'
    BACKGROUND = 'BACKGROUND'
    TABLE = 'TABLE'


class PageBehavior(BaseEnum):
    FIRST_PAGE = 'FIRST_PAGE'
    LAST_PAGE = 'LAST_PAGE'
    ALL_PAGES = 'ALL_PAGES'


class ElementAlignment(BaseEnum):
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    TOP = 'TOP'
    BOTTOM = 'BOTTOM'
    CENTER = 'CENTER'


class AlignSetting(BaseEnum):
    CENTER = 'center'
    END = 'end'
    LEFT = 'left'
    RIGHT = 'right'
    START = 'start'


class TableStyleName(BaseEnum):
    LEADING = 'LEADING'
    FONTNAME = 'FONTNAME'
    FONTSIZE = 'FONTSIZE'
    LINEABOVE = 'LINEABOVE'
    LINEBELOW = 'LINEBELOW'
    ALIGNMENT = 'ALIGNMENT'
    VALIGN = 'VALIGN'
    TEXTCOLOR = 'TEXTCOLOR'
    NOSPLIT = 'NOSPLIT'
    BACKGROUND = 'BACKGROUND'
    BOX = 'BOX'
