"""Единая цветовая палитра проекта OFZ_ANALITICS.

Модуль хранит только визуальные константы и небольшие helper-функции. Расчетная
логика графиков должна оставаться в профильных скриптах.
"""

from __future__ import annotations

from collections.abc import Sequence


# Контрастная качественная палитра для категорий, периодов и серий.
QUALITATIVE_PALETTE: list[str] = [
    "#001542",
    "#09C886",
    "#FF5A50",
    "#3A3377",
    "#822B93",
    "#2EA3D8",
    "#7D8AFA",
    "#166A75",
    "#B48DE9",
    "#60AEA1",
    "#E6D957",
    "#D8D8D8",
]

# Последовательная палитра: светлые значения ниже, темные/насыщенные выше.
SEQUENTIAL_PALETTE: list[str] = [
    "#D2ECF9",
    "#BFD5E9",
    "#ACBED9",
    "#90A7C8",
    "#737BAA",
    "#606998",
    "#4D4A87",
    "#3A3377",
]

# Более контрастная последовательная шкала для colorbar.
CONTRAST_SEQUENTIAL_PALETTE: list[str] = [
    "#D2ECF9",
    "#BFD5E9",
    "#ACBED9",
    "#90A7C8",
    "#737BAA",
    "#606998",
    "#4D4A87",
    "#3A3377",
]

# Статусы и предупреждения.
STATUS_PALETTE: dict[str, str] = {
    "норма": "#09C886",
    "предупреждение": "#E6D957",
    "риск": "#FF5A50",
    "требует проверки": "#FF5A50",
    "нет данных": "#D8D8D8",
}
WARNING_STATUS_PALETTE = STATUS_PALETTE

# Форматы размещения. Ключи русские, потому что они используются в легендах.
FORMAT_COLOR_MAP: dict[str, str] = {
    "Аукцион": "#001542",
    "Аукционы": "#001542",
    "ДРПА": "#2EA3D8",
    "Требует проверки": "#FF5A50",
}

# Сроковая структура.
MATURITY_COLOR_MAP: dict[str, str] = {
    "Долгосрочные": "#822B93",
    "Среднесрочные": "#166A75",
    "Краткосрочные": "#D76B55",
    "Требует проверки": "#8F969E",
    "requires_review": "#8F969E",
}

MATURITY_CATEGORY_ORDER: list[str] = [
    "Долгосрочные",
    "Среднесрочные",
    "Краткосрочные",
    "Требует проверки",
    "requires_review",
]

STRUCTURE_PALETTE: list[str] = [
    "#822B93",
    "#166A75",
    "#D76B55",
    "#3A3377",
    "#60AEA1",
    "#8F969E",
]

# Узлы Sankey и другие измерения.
DIMENSION_COLOR_MAP: dict[str, str] = {
    "Период": "#001542",
    "Вид бумаги": "#166A75",
    "Срок": "#3A3377",
    "Формат": "#822B93",
}

BINARY_PALETTE: list[str] = [FORMAT_COLOR_MAP["Аукцион"], FORMAT_COLOR_MAP["ДРПА"]]


def build_period_color_map(periods: Sequence[object]) -> dict[str, str]:
    """Вернуть стабильную карту цветов для периодов в порядке их отображения."""
    return {
        str(period): QUALITATIVE_PALETTE[index % len(QUALITATIVE_PALETTE)]
        for index, period in enumerate(periods)
    }


def color_for_period(period: object, periods: Sequence[object]) -> str:
    """Вернуть цвет периода из качественной палитры."""
    return build_period_color_map(periods).get(str(period), QUALITATIVE_PALETTE[0])
