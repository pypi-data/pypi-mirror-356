from typing import Any, Callable, TypeVar
import re


def px_to_pt(px: int):
    return round(px * .75)


def pt_to_px(pt: int):
    return round(pt / .75)


def replace_merge_tags(*, text: str, entities: dict[str, Any], merge_tag_map: dict[str, str], entity: dict = None,
                       replace_line_breaks: bool = True) -> str:
    regex = r'(\{[a-z]+(_[a-z]+)?\})'
    merge_tags = re.findall(regex, text)
    for merge_tag in merge_tags:
        if isinstance(merge_tag, (list, tuple)):
            merge_tag = merge_tag[0]
        entity_prop = merge_tag.replace('{', '').replace('}', '')
        if entity is not None:
            _entity = entity
        else:
            if not (mapped_value := merge_tag_map.get(merge_tag.replace('{', '').replace('}', ''))):
                continue
            entity_name, entity_prop = _split_entity_name_prop(mapped_value=mapped_value)
            if not entity_name or not entity_prop:
                continue
            if not (_entity := entities.get(entity_name)):
                continue
        try:
            if isinstance(_entity, dict):
                value = _entity.get(entity_prop)
            else:
                value = getattr(_entity, entity_prop)
        except AttributeError:
            value = None
        if callable(value):
            value = value()
        if value:
            text = text.replace(merge_tag, str(value))
    lines: list[str] = text.split('\n')
    final_lines: list[str] = list()
    for line in lines:
        line = line.strip()
        break_split = re.split(r'<br ?/?>', line)
        final_break_lines: list[str] = list()
        for break_line in break_split:
            break_line = break_line.strip()
            if len(break_line) and not re.search(regex, break_line):
                final_break_lines.append(break_line)
        line = '<br/>'.join(final_break_lines)
        if len(line):
            final_lines.append(line)
    text = '<br/>'.join(final_lines) if replace_line_breaks else '\n'.join(final_lines)
    return re.sub(r'<p></p>|<p><br/?></p>', '<br/>', re.sub(regex, '', text))


def _split_entity_name_prop(*, mapped_value: str) -> tuple[str | None, str | None]:
    if not re.match(r'^([a-z]+)\.', mapped_value):
        return None, None
    parts = mapped_value.split('.')
    return parts[0], parts[1]


T = TypeVar('T')


def find_in_list(lst: list[T], *, condition: Callable[[Any], bool]) -> T | None:
    for item in lst:
        if condition(item):
            return item
    return None
