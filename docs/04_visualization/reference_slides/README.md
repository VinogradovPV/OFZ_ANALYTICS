# Reference slides

Эта папка хранит ручные reference artifacts для визуального стандарта проекта.

## OFZ-PD yield + CBR key rate

Файл:

```text
docs/04_visualization/reference_slides/ofz_pd_yield_key_rate_reference.pptx
```

Назначение:

- design/reference input, а не generated output;
- источник style contract для графиков типа `lines + markers`;
- reference target для нового графика `ofz_pd_yield_key_rate`;
- пользовательский reference slide / стиль СП РФ.

Зафиксированный стиль:

- line chart с круглыми маркерами;
- линия примерно `2.25 pt`;
- маркер размером `7`;
- заливка маркера белая;
- обводка маркера цветом серии, примерно `1.5 pt`;
- легенда снизу;
- X-axis labels в формате `Jan-24` с поворотом около `-45` градусов;
- title color `#001648`, font family `Golos Text, Arial, sans-serif`;
- max OFZ-PD yield color `#FF5D50`;
- min OFZ-PD yield color `#00CE7E`;
- CBR key rate color `#BB88EF`.

PPTX не является pipeline output и не должен попадать в `outputs/`, `releases/` или runtime directories.
