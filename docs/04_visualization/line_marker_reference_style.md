# Line+marker reference style

Дата: 2026-07-02

## Источник

Reference artifact:

```text
docs/04_visualization/reference_slides/ofz_pd_yield_key_rate_reference.pptx
```

Он задает единый стиль для графиков типа `lines + markers`.

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
- X-axis tick angle: `-45`.

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

Reference slide показывает подписи на каждой точке, но это безопасно только для короткого горизонта.

Политика:

- до 24 точек включительно можно показывать подписи всех точек;
- свыше 24 точек показывать endpoints и экстремумы;
- CSV всегда сохраняет все значения;
- исключения должны быть описаны в chart-specific QA contract.

## NEXT.16 integration

В NEXT.16 helper применен к:

- новому графику `ofz_pd_yield_key_rate`;
- существующим line+marker графикам в `scripts/06_build_charts.py`;
- monthly line+marker графикам в `scripts/10_build_monthly_charts.py`.

Семантика, output filenames и методология существующих графиков не менялись.
