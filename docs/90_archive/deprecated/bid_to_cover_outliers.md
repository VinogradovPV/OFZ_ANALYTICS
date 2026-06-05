# Выбросы bid-to-cover

Дата формирования: `2026-06-04 19:08:33`.

Отчет содержит строки, где `bid_to_cover_ratio = demand_volume / supply_volume` больше 5.
Порог `> 10` является критическим подмножеством этого отчета.

- Строк `bid_to_cover_ratio > 5`: `1`
- Строк `bid_to_cover_ratio > 10`: `1`

| auction_date | report_period_label | issue_code | format | demand_volume | supply_volume | placement_volume | bid_to_cover_ratio | source_file | data_quality_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024-03-13 | 2024 | 26243RMFS | Аукцион | 86075.1 | 3 | 48969.1 | 28691.7 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | ok |
