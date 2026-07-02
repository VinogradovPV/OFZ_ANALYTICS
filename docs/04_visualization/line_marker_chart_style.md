# Line+marker chart style

Дата актуализации: 2026-07-02.

Этот документ является текстовой политикой стиля для графиков типа `lines + markers`. Reference PPTX/PNG больше не является source artifact проекта и не должен использоваться как входной файл pipeline.

## Style tokens

Кодовый helper:

```text
scripts/charts/line_marker_style.py
```

Основные параметры:

- `ofz_pd_yield_max`: `#FF5D50`;
- `ofz_pd_yield_min`: `#00CE7E`;
- `key_rate`: `#BB88EF`;
- line width: `2.25`;
- marker size: `7`;
- marker fill: `white`;
- marker outline width: `1.5`;
- title color: `#001648`;
- font family: `Golos Text, Arial, sans-serif`;
- legend: bottom horizontal;
- X-axis tick angle: `-45`;
- для production-графиков с русской аудиторией подписи месяцев выводятся в формате `Янв-24`.

## Когда применять

Применять к графикам, где основной тип визуализации:

- `px.line(..., markers=True)`;
- `go.Scatter(... mode="lines+markers")`;
- `go.Scatter(... mode="lines+markers+text")`.

## Когда не применять

Не применять к:

- scatter charts;
- boxplot;
- Sankey;
- stacked bar charts;
- heatmap;
- density/facet charts, где marker style не является смысловым элементом.

## Label density

Подписи на каждой точке безопасны только для короткого горизонта.

Политика:

- до 24 точек включительно можно показывать подписи всех точек;
- свыше 24 точек показывать endpoints и экстремумы;
- CSV всегда сохраняет все значения;
- исключения должны быть описаны в chart-specific QA contract.

Для графика `ofz_pd_yield_key_rate` подписи значений вынесены в annotations:

- максимальная доходность ОФЗ-ПД и ключевая ставка Банка России подписываются сверху маркера;
- минимальная доходность ОФЗ-ПД подписывается снизу маркера;
- у подписей используется белый фон `rgba(255,255,255,0.90)`, чтобы линия не проходила через текст;
- если значения нескольких серий в одном месяце близки, сдвиг подписи увеличивается от линии;
- collision-aware helper использует порог `max(0.25 п.п., 2.5% диапазона Y)` и разводит близкие верхние подписи по разным lanes;
- ключевая ставка всегда форматируется с двумя знаками после запятой, например `15.00`.

## Artifact policy

Reference PPTX/PNG не коммитятся и не хранятся в `docs/`, `data/raw/`, `outputs/`, `releases/` или runtime directories. В Git остается только текстовая политика стиля и кодовый helper.
