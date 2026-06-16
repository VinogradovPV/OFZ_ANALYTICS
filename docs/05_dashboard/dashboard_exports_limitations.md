# Dashboard exports limitations

Дата формирования: `2026-06-16 11:32:33`.

Параметры: `month`, `cumulative`, `2026-05-01`, ретроспектива `4`.

## Ограничения

- В demand/supply export есть ДРПА без спроса; demand-based ratios по ним требуют ограничения.
- Объем выручки отсутствует или полностью пуст; соответствующие поля экспортируются пустыми.
- Строки ДРПА: 35; они не должны смешиваться с demand-based ratios без проверки валидности спроса.
- Строки с нулевым или отрицательным размещением: 9; demand_to_placement_ratio по ним пустой.

## Методологические правила

- `bid_to_cover_ratio = demand_volume / supply_volume`.
- `demand_to_placement_ratio = demand_volume / placement_volume`.
- `demand_satisfaction_ratio = placement_volume / demand_volume`.
- ДРПА не смешиваются с demand-based ratios без проверки валидности спроса.
- Сроки классифицируются как: краткосрочные до 5 лет включительно; среднесрочные свыше 5 и до 10 лет включительно; долгосрочные более 10 лет.
