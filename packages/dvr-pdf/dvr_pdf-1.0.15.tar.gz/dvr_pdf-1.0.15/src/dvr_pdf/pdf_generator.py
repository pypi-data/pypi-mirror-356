import os
from tempfile import TemporaryDirectory
from typing import Callable, Union, Any, cast, IO, Literal

from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, StyleSheet1, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import BaseDocTemplate, Flowable, TableStyle, Table, Frame, PageTemplate, \
    NextPageTemplate

from dvr_pdf.util.custom_paragraph import CustomParagraph
from dvr_pdf.util.enums import ElementType, Font, PageBehavior, PaginationPosition, TableStyleName, AlignSetting
from dvr_pdf.util.typing import PDFTemplate, PDFElement, PDFTableElement, PDFTextElement, PDFImageElement, \
    TableStyleProp, PDFCellElement, ConfigurableTableElement, PDFRowElement, PDFBackgroundElement
from dvr_pdf.util.util import px_to_pt, replace_merge_tags, find_in_list

_show_boundaries = 0

_width, _height = A4
_page_padding = px_to_pt(72)
_inner_width, _inner_height = _width - _page_padding * 2, _height - _page_padding * 2

_TABLE_ROW_HEIGHT = 14


class NumberedPageCanvas(Canvas):
    """
    https://code.activestate.com/recipes/546511-page-x-of-y-with-reportlab/
    https://code.activestate.com/recipes/576832/
    https://www.blog.pythonlibrary.org/2013/08/12/reportlab-how-to-add-page-numbers/
    """

    def __init__(self, *args, render_total_pages: bool, font_name: str, render_text: Callable,
                 first_page_elements: list[PDFElement], last_page_elements: list[PDFElement], font_size: int,
                 table_element: PDFTableElement, document: BaseDocTemplate, page_position: PaginationPosition,
                 template: PDFTemplate, resources: dict[str, str], **kwargs):
        super().__init__(*args, **kwargs)
        self._font_name = font_name
        self.pages = []
        self._font_size = font_size
        self._page_position = page_position
        self._render_total_pages = render_total_pages
        self._first_page_elements = first_page_elements
        self._last_page_elements = last_page_elements
        self._table_element = table_element
        self._render_text = render_text
        self._document = document
        self._template = template
        self._resources = resources

    def showPage(self):
        """
        On a page break, add information to the list
        """
        self.pages.append(dict(self.__dict__))
        # noinspection PyUnresolvedReferences
        self._startPage()

    def save(self):
        """
        Add the page number to each page (page x of y)
        """
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self._render_page_elements(page_count=page_count)
            if page_count > 1 and self._template.pagination.position != PaginationPosition.NONE:
                self.draw_page_number(page_count)
            super().showPage()
        super().save()

    def _render_page_elements(self, page_count: int):
        # noinspection PyUnresolvedReferences
        current_page = self._pageNumber
        is_first_page = current_page == 1
        is_last_page = current_page == page_count
        render_elements: list[PDFElement] = list()
        if is_first_page:
            render_elements += self._first_page_elements
        if is_last_page:
            render_elements += self._last_page_elements
        _render_background_elements(render_elements=render_elements, canvas=self)
        for element in render_elements:
            if element.element_type == ElementType.TEXT:
                self._render_text(element=element, canvas=self)
            elif element.element_type == ElementType.IMAGE:
                _render_image_element(element=cast(PDFImageElement, element), canvas=self, resources=self._resources)

    def _render_background_elements(self, *, render_elements: list[PDFElement]):
        for element in render_elements:
            if element.element_type != ElementType.BACKGROUND:
                continue
            _render_background_element(element=cast(PDFBackgroundElement, element), canvas=self)

    def draw_page_number(self, page_count: int):
        """
        Add the page number
        """
        self.saveState()
        # noinspection PyUnresolvedReferences
        content = f'Pagina {self._pageNumber}'
        if self._render_total_pages:
            content += f' van {page_count}'
        self.setFont(self._font_name, self._font_size)
        if self._page_position == PaginationPosition.LEFT:
            self.drawString(x=1 * cm, y=1 * cm, text=content)
        elif self._page_position == PaginationPosition.RIGHT:
            self.drawRightString(_width - 1 * cm, 1 * cm, text=content)
        else:
            self.drawCentredString(x=_width / 2, y=1 * cm, text=content)
        self.restoreState()


class PDFGenerator:
    def __init__(self, *, file_path: str | IO[bytes], template: PDFTemplate, merge_tag_map: dict[str, str],
                 entities: dict[str, Any]):
        self._template = template
        self._entities = entities
        self._document = BaseDocTemplate(filename=file_path)
        self._first_page_elements: list[PDFElement] = list()
        self._last_page_elements: list[PDFElement] = list()
        self._all_pages_elements: list[PDFElement] = list()
        self._table_element: PDFTableElement | None = None
        self._page_template = PageTemplate(id='first_page', onPage=self._render_fixed_elements)
        self._story: list[Flowable] = list()
        self._styles: StyleSheet1 = _initialize_styles()
        self._merge_tag_map = merge_tag_map
        self._resources: dict[str, str] = dict()

    def generate_pdf(self):
        with TemporaryDirectory() as temp_dir:
            _initialize_fonts()
            self._prepare_resources(temp_dir=temp_dir)
            self._split_elements()
            self._render_table_element()
            self._document.build(self._story, canvasmaker=self._make_canvas)

    def _prepare_resources(self, *, temp_dir: str):
        for element in self._template.elements:
            if PDFElement.model_validate(element).element_type == ElementType.IMAGE:
                image = PDFImageElement.model_validate(element).image
                is_image_path = isinstance(image, str)
                if is_image_path:
                    image = open(image, 'rb')
                image_name = os.path.basename(image.name)
                temp_resource = os.path.join(temp_dir, image_name)
                with open(temp_resource, 'wb') as resource:
                    resource.write(image.read())
                if is_image_path:
                    image.close()
                self._resources[image_name] = temp_resource

    def _split_elements(self):
        elements = self._template.elements
        all_pages_elements: list[PDFElement] = list()
        first_page_elements: list[PDFElement] = list()
        last_page_elements: list[PDFElement] = list()
        for element in elements:
            if element.element_type == ElementType.TABLE:
                self._table_element = PDFTableElement.model_validate(element)
                continue
            if (page_behavior := element.page_behavior) == PageBehavior.FIRST_PAGE:
                first_page_elements.append(element)
            elif page_behavior == PageBehavior.LAST_PAGE:
                last_page_elements.append(element)
            else:
                all_pages_elements.append(element)
        self._all_pages_elements = all_pages_elements
        self._first_page_elements = first_page_elements
        self._last_page_elements = last_page_elements

    def _make_canvas(self, *args, **kwargs) -> Canvas:
        font_name = _get_font_name(font=self._template.font)
        canvas = NumberedPageCanvas(*args, font_name=font_name, render_text=self._render_text_element,
                                    font_size=px_to_pt(self._template.font_size),
                                    render_total_pages=self._template.pagination.render_total_pages,
                                    page_position=self._template.pagination.position,
                                    first_page_elements=self._first_page_elements,
                                    last_page_elements=self._last_page_elements,
                                    table_element=self._table_element, resources=self._resources,
                                    document=self._document, template=self._template, **kwargs)
        return canvas

    def _render_fixed_elements(self, canvas: Canvas, _document: BaseDocTemplate):
        if self._template.background_color:
            canvas.saveState()
            canvas.setFillColor(self._template.background_color)
            canvas.rect(0, 0, _width, _height, fill=1, stroke=0)
            canvas.restoreState()
        render_elements: list[PDFElement] = self._all_pages_elements
        _render_background_elements(render_elements=render_elements, canvas=canvas)
        for element in render_elements:
            element_type = element.element_type
            if element_type == ElementType.TEXT:
                self._render_text_element(element=cast(PDFTextElement, element), canvas=canvas)
            elif element_type == ElementType.IMAGE:
                _render_image_element(element=cast(PDFImageElement, element), canvas=canvas, resources=self._resources)

    def _render_text_element(self, *, element: PDFTextElement, canvas: Canvas):
        font_name = _get_font_name(font=element.font)
        font_size = px_to_pt(element.font_size or self._template.font_size)
        text = replace_merge_tags(text=element.text, merge_tag_map=self._merge_tag_map, entities=self._entities)
        if not text:
            return
        text_style = self._styles['TextStyle']
        text_style = text_style.clone(name=text_style.name, parent=text_style.parent)
        text_style.fontName = font_name
        if color := element.color:
            text_style.textColor = color
        text_style.fontSize = font_size
        paragraph = CustomParagraph(text=text, style=text_style)
        text_width = _get_required_string_width(text=text, font_name=font_name, font_size=font_size)
        width, height = paragraph.wrapOn(canvas, _inner_width, _inner_height)
        top = _get_top(y=element.y_pt, element_height=height)
        left = _get_left(x=element.x_pt)
        left = min(_width - text_width, left)
        paragraph.drawOn(canvas, left, top)

    def _render_table_element(self):
        if not (table := self._table_element):
            return
        element_width = table.width_pt if table.width_pt > 0 else _width
        column_widths = table.column_widths
        column_widths = _calculate_column_widths(table_width=element_width, column_widths=column_widths)
        styles: list[TableStyleProp] = [
            (TableStyleName.VALIGN.value, (0, 0), (-1, -1), 'MIDDLE'),
        ]
        if font := table.font:
            font_name = _get_font_name(font=font)
            styles.append((TableStyleName.FONTNAME.value, (0, 0), (-1, -1), font_name))
        else:
            font_name = _get_font_name(font=self._template.font)
            styles.append((TableStyleName.FONTNAME.value, (0, 0), (-1, -1), font_name))
        font_size = px_to_pt(table.font_size or self._template.font_size)
        styles.append((TableStyleName.FONTSIZE.value, (0, 0), (-1, -1), px_to_pt(font_size)))
        if background_color := table.background_color:
            styles.append((TableStyleName.BACKGROUND.value, (0, 0), (-1, -1), background_color))
        if color := table.color:
            styles.append((TableStyleName.TEXTCOLOR.value, (0, 0), (-1, -1), color))
        if border_color := table.border_color:
            styles.append((TableStyleName.BOX.value, (0, 0), (-1, -1), 1, border_color))
        rows: list[list[CustomParagraph]] = list()
        table_rows = table.rows

        # Head row
        if head_row_config := find_in_list(table_rows, condition=lambda row: row.key == 'head_row'):
            head_row, head_styles = self._render_table_head(config=head_row_config, font_size=font_size)
            rows.append(head_row)
            styles.extend(head_styles)

        # Content rows
        _rows, _styles = self._render_table_rows(rows=table_rows, font_size=font_size)
        rows.extend(_rows)
        styles.extend(_styles)

        y_modifier = 0
        content_y_assigned = False
        for idx, row in enumerate(table_rows):
            row = table_rows[idx]
            if row.key == 'head_row':
                continue
            elif row.key in ['even_rows', 'odd_rows']:
                if not content_y_assigned:
                    y_modifier = len(_rows) - 2
                    content_y_assigned = True
                continue
            if row.key == 'vat_rows':
                vat_rows, _styles = self._render_vat_rows(row=row, start_y=len(rows), font_size=font_size)
                rows.extend(vat_rows)
                styles.extend(_styles)
                y_modifier += len(vat_rows) - 1
                continue
            row_content, _styles = self._render_table_row(row=row, y=idx + y_modifier, row_data=None,
                                                          font_size=font_size)
            rows.append(row_content)
            styles.extend(_styles)

        row_height = _TABLE_ROW_HEIGHT + font_size
        total_height = row_height * len(rows)
        row_heights: list[int] = [row_height] * len(rows)
        table_style = TableStyle(styles)
        table = Table(rows, colWidths=column_widths, minRowHeights=row_heights, style=table_style, repeatRows=1)

        predicted_page_count = self._predict_page_count(table_height=total_height)
        self._generate_next_page_templates(page_count=predicted_page_count)
        self._story.append(table)

    def _render_table_head(self, *, config: PDFRowElement, font_size: int) -> \
            tuple[list[CustomParagraph], list[TableStyleProp]]:
        return self._render_table_row(row_data=config.model_dump(), row=config, y=0, font_size=font_size)

    def _render_table_rows(self, *, rows: list[PDFRowElement], font_size: int) -> \
            tuple[list[list[CustomParagraph]], list[TableStyleProp]]:
        table_rows: list[dict] = self._entities.get('table_rows')
        if not table_rows:
            return list(), list()
        even_row_config = find_in_list(rows, condition=lambda row: row.key == 'even_rows')
        odd_row_config = find_in_list(rows, condition=lambda row: row.key == 'odd_rows')
        if not even_row_config and not odd_row_config:
            return list(), list()
        fallback_config = even_row_config or odd_row_config
        styles: list[TableStyleProp] = list()
        cell_rows: list[list[CustomParagraph]] = list()
        for idx, row_data in enumerate(table_rows):
            if idx % 2:
                # Zero indexed, so odd idx is even row
                config = even_row_config or fallback_config
            else:
                config = odd_row_config or fallback_config
            cells, _styles = self._render_table_row(row_data=row_data, row=config, y=idx + 1, font_size=font_size)
            styles.extend(_styles)
            cell_rows.append(cells)
        return cell_rows, styles

    def _render_vat_rows(self, *, row: PDFRowElement, start_y: int, font_size: int) -> \
            tuple[list[list[CustomParagraph]], list[TableStyleProp]]:
        if not (vat_rows := self._entities.get('vat_rows')):
            return list(), list()
        rows: list[list[CustomParagraph]] = list()
        styles: list[TableStyleProp] = list()
        for idx, vat_row in enumerate(vat_rows):
            _row, _styles = self._render_table_row(row_data=vat_row, row=row, y=start_y + idx, ignore_tags=False,
                                                   font_size=font_size)
            rows.append(_row)
            styles.extend(_styles)
        return rows, styles

    def _render_table_row(self, *, row_data: Union[dict, tuple] | None, row: PDFRowElement, y: int,
                          ignore_tags: bool = False, font_size: int) -> \
            tuple[list[CustomParagraph], list[TableStyleProp]]:
        styles: list[TableStyleProp] = list()
        cells: list[CustomParagraph] = list()
        for column, cell in enumerate(row.columns):
            par, cell_style = self._render_table_cell(cell=cell, x=column, y=y, row=row, row_data=row_data,
                                                      ignore_tags=ignore_tags, font_size=font_size)
            cells.append(par)
            styles.extend(cell_style)
        styles.extend(self._get_configurable_table_element_styles(element=row, x_start=0, y_start=y,
                                                                  x_end=-1, y_end=y))
        return cells, styles

    def _render_table_cell(self, *, row_data: Union[dict, tuple] | None, cell: PDFCellElement, x: int, y: int,
                           row: PDFRowElement, ignore_tags: bool = False, font_size: int) -> \
            tuple[CustomParagraph, list[TableStyleProp]]:
        row_bold = row.bold
        row_italic = row.italic
        styles: list[TableStyleProp] = self._get_configurable_table_element_styles(element=cell, x_start=x, y_start=y,
                                                                                   x_end=x, y_end=y, bold=row_bold,
                                                                                   italic=row_italic)
        if ignore_tags and row_data:
            cell_value = row_data[x]
        else:
            cell_value = replace_merge_tags(text=cell.text, entities=self._entities, merge_tag_map=self._merge_tag_map,
                                            entity=row_data)
        par_style = self._styles['TableText']
        par_style = par_style.clone(name=par_style.name, parent=par_style.parent)
        par_style.valign = 'MIDDLE'
        par_style.fontSize = font_size
        if color := cell.color:
            par_style.textColor = color
        if background := cell.background_color:
            par_style.backColor = background
        par_style.alignment = TA_LEFT
        if alignment := cell.text_alignment:
            if alignment == AlignSetting.RIGHT:
                par_style.alignment = TA_RIGHT
            elif alignment == AlignSetting.CENTER:
                par_style.alignment = TA_CENTER
        font_name = _get_font_name(font=self._template.font, bold=cell.bold or row_bold,
                                   italic=cell.italic or row_italic)
        par_style.fontName = font_name
        cell_content = CustomParagraph(cell_value, style=par_style)
        return cell_content, styles

    def _get_configurable_table_element_styles(self, *, element: ConfigurableTableElement, x_start: int, y_start: int,
                                               x_end: int, y_end: int, bold: bool | None = None,
                                               italic: bool | None = None) -> list[TableStyleProp]:
        if bold is None:
            bold = element.bold
        if italic is None:
            italic = element.italic
        font_name = _get_font_name(font=self._template.font, bold=bold, italic=italic)
        font_size = px_to_pt(self._template.font_size)
        styles: list[TableStyleProp] = [
            (TableStyleName.FONTNAME.value, (x_start, y_start), (x_end, y_end), font_name),
            (TableStyleName.FONTSIZE.value, (x_start, y_start), (x_end, y_end), font_size)
        ]
        if background_color := element.background_color:
            styles.append((TableStyleName.BACKGROUND.value, (x_start, y_start), (x_end, y_end), background_color))
        if color := element.color:
            styles.append((TableStyleName.TEXTCOLOR.value, (x_start, y_start), (x_end, y_end), color))
        if border_bottom := element.border_bottom_color:
            styles.extend([
                (TableStyleName.LINEBELOW.value, (x_start, y_start), (x_end, y_end), 1, border_bottom),
                # No line after table split
                # (TableStyleName.LINEBELOW.value, (x_start, 'splitlast'), (x_end, 'splitlast'), 0, BLACK)
            ])
        if border_top := element.border_top_color:
            styles.append((TableStyleName.LINEABOVE.value, (x_start, y_start), (x_end, y_end), 1, border_top))
        return styles

    def _predict_page_count(self, *, table_height: int, page_count: int = 1) -> int:
        render_elements: list[PDFElement] = self._all_pages_elements
        if page_count == 1:
            if table_height > self._table_element.height_pt:
                return self._predict_page_count(table_height=table_height - self._table_element.height_pt,
                                                page_count=page_count + 1)
            else:
                return page_count
        if self._is_last_page(elements=render_elements, table_height=table_height):
            return page_count
        x, y, width, height = self._get_table_frame_coordinates(elements=render_elements,
                                                                table_element=self._table_element)
        table_height -= height
        return self._predict_page_count(table_height=table_height, page_count=page_count + 1)

    def _is_last_page(self, *, elements: list[PDFElement], table_height: int) -> bool:
        all_elements = elements + self._last_page_elements
        x, y, width, height = self._get_table_frame_coordinates(elements=all_elements,
                                                                table_element=self._table_element)
        return height >= table_height

    def _get_table_frame_coordinates(self, *, elements: list[PDFElement], table_element: PDFTableElement) -> \
            tuple[int, int, int, int]:
        used_tops: set[int] = set()
        used_bottoms: set[int] = set()
        for element in elements:
            if element.element_type == ElementType.BACKGROUND or not self._element_has_content(element=element):
                continue
            used_bottoms.add(element.y_pt + element.height_pt)
            used_tops.add(element.y_pt)
        table_top = int(table_element.y_pt)
        table_bottom = table_top
        while table_bottom not in used_tops and table_bottom < (_height - table_top):
            table_bottom = min(_height, table_bottom + 1)
        table_height = table_bottom - table_top
        y = _get_top(y=table_top, element_height=table_height)
        return table_element.x_pt + _page_padding, y - _page_padding, table_element.width_pt, table_height

    def _element_has_content(self, *, element: PDFElement) -> bool:
        if element.element_type != ElementType.TEXT:
            return True
        if not replace_merge_tags(text=element.text, entities=self._entities, merge_tag_map=self._merge_tag_map):
            return False
        return True

    def _generate_next_page_templates(self, page_count: int):
        if not self._table_element:
            return
        one_page_template = self._generate_one_page_template()
        first_page_template = self._generate_first_page_template()
        in_between_template = self._generate_in_between_page_template()
        last_page_template = self._generate_last_page_template()
        if page_count == 1:
            page_templates = [one_page_template]
        else:
            page_templates = [first_page_template, in_between_template, last_page_template]
        self._document.addPageTemplates(page_templates)
        if page_count == 1:
            templates = ['one_page_template']
        elif page_count > 2:
            templates = ['in_between_page_template'] * (page_count - 2) + ['last_page_template']
        else:
            templates = ['last_page_template']
        self._story.append(NextPageTemplate(templates))

    def _generate_one_page_template(self) -> PageTemplate:
        x, y, width, height = self._get_table_frame_coordinates(
            elements=self._all_pages_elements + self._last_page_elements + self._first_page_elements,
            table_element=self._table_element)
        frame = Frame(x1=x, y1=y + _page_padding, width=width, height=height, id='one_page_table_frame',
                      showBoundary=_show_boundaries)
        return PageTemplate(id='one_page_template', onPage=self._render_fixed_elements, frames=[frame])

    def _generate_first_page_template(self) -> PageTemplate:
        x, y, width, height = self._get_table_frame_coordinates(
            elements=self._all_pages_elements + self._first_page_elements, table_element=self._table_element)
        y = _get_top(y=self._table_element.y_pt, element_height=self._table_element.height_pt)
        frame = Frame(x1=self._table_element.x_pt + _page_padding, y1=y, width=width,
                      height=self._table_element.height_pt,
                      id='first_page_table_frame', showBoundary=_show_boundaries)
        return PageTemplate(id='first_page_template', onPage=self._render_fixed_elements, frames=[frame])

    def _generate_in_between_page_template(self) -> PageTemplate:
        x, y, width, height = self._get_table_frame_coordinates(elements=self._all_pages_elements,
                                                                table_element=self._table_element)
        frame = Frame(x1=x, y1=y + _page_padding, width=width, height=height, id='in_between_page_table_frame',
                      showBoundary=_show_boundaries)
        return PageTemplate(id='in_between_page_template', onPage=self._render_fixed_elements, frames=[frame])

    def _generate_last_page_template(self) -> PageTemplate:
        x, y, width, height = self._get_table_frame_coordinates(
            elements=self._all_pages_elements + self._last_page_elements, table_element=self._table_element)
        frame = Frame(x1=x, y1=y + _page_padding, width=width, height=height, id='last_page_table_frame',
                      showBoundary=_show_boundaries)
        return PageTemplate(id='last_page_template', onPage=self._render_fixed_elements, frames=[frame])


def _render_image_element(*, element: PDFImageElement, canvas: Canvas, resources: dict[str, str]):
    image_width = element.width_pt
    image_height = element.height_pt
    left = _get_left(x=element.x_pt)
    top = _get_top(y=element.y_pt, element_height=image_height)
    if isinstance(element.image, str):
        element.image = open(element.image, 'rb')
    image_name = os.path.basename(element.image.name)
    image_path = resources[image_name]
    canvas.drawImage(image_path, left, top, width=image_width, height=image_height, preserveAspectRatio=True,
                     mask='auto')


def _render_background_elements(*, render_elements: list[PDFElement], canvas: Canvas):
    for element in render_elements:
        if element.element_type != ElementType.BACKGROUND:
            continue
        _render_background_element(element=cast(PDFBackgroundElement, element), canvas=canvas)


def _render_background_element(*, element: PDFBackgroundElement, canvas: Canvas):
    width = element.width_pt
    height = element.height_pt
    left = _get_left(x=element.x_pt)
    top = _get_top(y=element.y_pt, element_height=height)
    canvas.saveState()
    canvas.setFillColor(element.color)
    canvas.rect(x=left, y=top, width=width, height=height, stroke=0, fill=1)
    canvas.restoreState()


def _initialize_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(leading=16, alignment=cast(Literal[0], TA_LEFT), parent=styles['BodyText'], name='TextStyle'))
    styles.add(ParagraphStyle(valign='MIDDLE', parent=styles['BodyText'], name='TableText'))
    styles.add(ParagraphStyle(alignment=cast(Literal[2], TA_RIGHT), parent=styles['TableText'], name='TableTextRight'))
    styles.add(ParagraphStyle(parent=styles['TableText'], name='TableHeaderText'))
    styles.add(ParagraphStyle(fontName='Helvetica-Bold', parent=styles['BodyText'], name='Bold'))
    styles.add(
        ParagraphStyle(fontName='Helvetica-BoldOblique', parent=styles['BodyText'], name='BoldItalic'))
    return styles


def _get_font_name(*, font: Font, bold: bool = None, italic: bool = None):
    font_name = 'Helvetica'
    if font == Font.LATO:
        font_name = 'Lato'
    elif font == Font.MERRIWEATHER:
        font_name = 'Merriweather'
    elif font == Font.NOTO_SANS:
        font_name = 'NotoSans'
    elif font == Font.NOTO_SERIF:
        font_name = 'NotoSerif'
    elif font == Font.OPEN_SANS:
        font_name = 'OpenSans'
    elif font == Font.PLAYFAIR:
        font_name = 'Playfair'
    elif font == Font.PT_SERIF:
        font_name = 'PTSerif'
    elif font == Font.ROBOTO:
        font_name = 'Roboto'
    elif font == Font.ROBOTO_MONO:
        font_name = 'RobotoMono'
    elif font == Font.SOURCE_SANS_PRO:
        font_name = 'SourceSansPro'

    if bold:
        font_name += _get_bold_name(font_name=font_name)
    if italic:
        font_name += _get_italic_name(font_name=font_name, bold=bold)
    return font_name


def _get_top(*, y: int, element_height: Union[float, int] = 0) -> int:
    top = _height - y - (element_height if element_height > 0 else 0) - _page_padding
    return max(0, top)


def _get_left(*, x: int) -> int:
    return max(0, x + _page_padding)


def _calculate_column_widths(*, table_width: int, column_widths: list[int]) -> list[int]:
    return [round(table_width / 100 * percentage) for percentage in column_widths]


def _get_required_string_width(*, text: str, font_name: str, font_size: int) -> int:
    lines = text.split('<br/>')
    return stringWidth(text=max(lines), fontName=font_name, fontSize=font_size)


def _get_bold_name(*, font_name: str):
    return '-Bold' if font_name == 'Helvetica' else 'Bold'


def _get_italic_name(*, font_name, bold: bool) -> str:
    if font_name == 'Helvetica':
        prefix = '' if bold else '-'
        return f'{prefix}Oblique'
    return 'Italic'


def _initialize_fonts():
    pdfmetrics.registerFont(TTFont('Lato', 'Lato-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('LatoItalic', 'Lato-Italic.ttf'))
    pdfmetrics.registerFont(TTFont('LatoBold', 'Lato-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('LatoBoldItalic', 'Lato-BoldItalic.ttf'))
    pdfmetrics.registerFont(TTFont('Merriweather', 'Merriweather-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('MerriweatherItalic', 'Merriweather-Italic.ttf'))
    pdfmetrics.registerFont(TTFont('MerriweatherBold', 'Merriweather-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('MerriweatherBoldItalic', 'Merriweather-BoldItalic.ttf'))
    pdfmetrics.registerFont(TTFont('NotoSans', 'NotoSans-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('NotoSansItalic', 'NotoSans-Italic.ttf'))
    pdfmetrics.registerFont(TTFont('NotoSansBold', 'NotoSans-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('NotoSansBoldItalic', 'NotoSans-BoldItalic.ttf'))
    pdfmetrics.registerFont(TTFont('NotoSerif', 'NotoSerif-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('NotoSerifItalic', 'NotoSerif-Italic.ttf'))
    pdfmetrics.registerFont(TTFont('NotoSerifBold', 'NotoSerif-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('NotoSerifBoldItalic', 'NotoSerif-BoldItalic.ttf'))
    pdfmetrics.registerFont(TTFont('OpenSans', 'OpenSans-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('OpenSansItalic', 'OpenSans-Italic.ttf'))
    pdfmetrics.registerFont(TTFont('OpenSansBold', 'OpenSans-SemiBold.ttf'))
    pdfmetrics.registerFont(TTFont('OpenSansBoldItalic', 'OpenSans-SemiBoldItalic.ttf'))
    pdfmetrics.registerFont(TTFont('Playfair', 'PlayfairDisplay-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('PlayfairItalic', 'PlayfairDisplay-Italic.ttf'))
    pdfmetrics.registerFont(TTFont('PlayfairBold', 'PlayfairDisplay-Medium.ttf'))
    pdfmetrics.registerFont(TTFont('PlayfairBoldItalic', 'PlayfairDisplay-MediumItalic.ttf'))
    pdfmetrics.registerFont(TTFont('PTSerif', 'PTSerif-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('PTSerifItalic', 'PTSerif-Italic.ttf'))
    pdfmetrics.registerFont(TTFont('PTSerifBold', 'PTSerif-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('PTSerifBoldItalic', 'PTSerif-BoldItalic.ttf'))
    pdfmetrics.registerFont(TTFont('Roboto', 'Roboto-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('RobotoItalic', 'Roboto-Italic.ttf'))
    pdfmetrics.registerFont(TTFont('RobotoBold', 'Roboto-Medium.ttf'))
    pdfmetrics.registerFont(TTFont('RobotoBoldItalic', 'Roboto-MediumItalic.ttf'))
    pdfmetrics.registerFont(TTFont('RobotoMono', 'RobotoMono-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('RobotoMonoItalic', 'RobotoMono-Italic.ttf'))
    pdfmetrics.registerFont(TTFont('RobotoMonoBold', 'RobotoMono-Medium.ttf'))
    pdfmetrics.registerFont(TTFont('RobotoMonoBoldItalic', 'RobotoMono-MediumItalic.ttf'))
    pdfmetrics.registerFont(TTFont('SourceSansPro', 'SourceSansPro-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('SourceSansProItalic', 'SourceSansPro-Italic.ttf'))
    pdfmetrics.registerFont(TTFont('SourceSansProBold', 'SourceSansPro-SemiBold.ttf'))
    pdfmetrics.registerFont(TTFont('SourceSansProBoldItalic', 'SourceSansPro-SemiBoldItalic.ttf'))
