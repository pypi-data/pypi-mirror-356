from io import BufferedReader
from typing import BinaryIO, Any, Annotated

from pydantic import BaseModel, Field, BeforeValidator, ConfigDict

from dvr_pdf.util.enums import PaginationPosition, ElementType, PageBehavior, ElementAlignment, Font, AlignSetting
from dvr_pdf.util.util import px_to_pt


class PydanticModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True
    )


class PDFElement(PydanticModel):
    x: int
    y: int
    id: str
    width: int
    height: int
    element_type: ElementType = Field(alias='elementType')
    page_behavior: PageBehavior = Field(alias='pageBehavior')
    alignment: ElementAlignment | None = None

    @property
    def x_pt(self):
        return px_to_pt(self.x)

    @property
    def y_pt(self):
        return px_to_pt(self.y)

    @property
    def width_pt(self):
        return px_to_pt(self.width)

    @property
    def height_pt(self):
        return px_to_pt(self.height)


class PDFTextElement(PDFElement):
    text: str
    font_size: int | None = Field(alias='fontSize', default=None)
    font: Font | None = None
    color: str | None = None


class PDFImageElement(PDFElement):
    model_config = {
        'arbitrary_types_allowed': True
    }
    image: BinaryIO | BufferedReader | str


class PDFBackgroundElement(PDFElement):
    color: str


class ConfigurableTableElement(PydanticModel):
    id: str
    bold: bool | None = False
    italic: bool | None = False
    background_color: str | None = Field(alias='backgroundColor', default=None)
    color: str | None = None
    border_bottom_color: str | None = Field(alias='borderBottomColor', default=None)
    border_top_color: str | None = Field(alias='borderTopColor', default=None)


class PDFCellElement(ConfigurableTableElement):
    text: str | float | int
    text_alignment: AlignSetting | None = Field(alias='textAlignment', default=None)


class PDFRowElement(ConfigurableTableElement):
    columns: list[PDFCellElement]
    key: str


class PDFTableElement(PDFElement):
    rows: list[PDFRowElement]
    column_widths: list[int] = Field(alias='columnWidths')
    font: Font | None = None
    font_size: int | None = Field(alias='fontSize', default=None)
    background_color: str | None = Field(alias='backgroundColor', default=None)
    color: str | None = None
    border_color: str | None = Field(alias='borderColor', default=None)


class Pagination(PydanticModel):
    position: PaginationPosition
    render_total_pages: bool = Field(alias='renderTotalPages')


def _pdf_elements_initializer(data: list[dict | PDFElement]) -> list[PDFElement]:
    return [_pdf_element_initializer(element) for element in data]


def _pdf_element_initializer(data: dict | PDFElement) -> PDFElement:
    if isinstance(data, PDFElement):
        return data
    element_type = ElementType.get_item(data.get('elementType') or data.get('element_type'))
    if not element_type:
        raise ValueError('elementType not found')
    if element_type == ElementType.TEXT:
        return PDFTextElement(**data)
    elif element_type == ElementType.IMAGE:
        return PDFImageElement(**data)
    elif element_type == ElementType.BACKGROUND:
        return PDFBackgroundElement(**data)
    elif element_type == ElementType.TABLE:
        return PDFTableElement(**data)
    raise ValueError(f'Unknown element_type {element_type}')


class PDFTemplate(PydanticModel):
    font: Font
    font_size: int = Field(alias='fontSize')
    pagination: Pagination
    elements: Annotated[list[PDFElement], BeforeValidator(_pdf_elements_initializer)]
    background_color: str | None = Field(alias='backgroundColor', default=None)


type TableStyleProp = tuple[str, tuple[int, int], tuple[int, int], Any] | tuple[
    str, tuple[int, int], tuple[int, int], int, Any]
