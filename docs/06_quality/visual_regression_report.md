# Отчет visual regression

Метка: `вторая модернизация`.

## Режим

- Screenshot/backend mode: `auto_fallback_static_html`
- Screenshot backend: `auto_fallback_static_html`
- Комментарий: visual_regression_mode=auto; screenshot backend unavailable, fallback used: browser screenshot backend skipped in Codex managed sandbox; run the same command from project PowerShell to use Playwright
- HTML-файлов в проверке: `50`
- `report_date`: `2026-05-01`
- `period_type`: `month`
- `aggregation_mode`: `cumulative`
- `retrospective_years`: `4`

## Сводка

- OK: `1054`
- Warnings: `1`
- Failures: `0`

## Проверки

| Файл | Проверка | Статус | Сообщение |
| --- | --- | --- | --- |
| `-` | `visual_regression_mode` | `ok` | visual_regression_mode=auto; screenshot backend unavailable, fallback used: browser screenshot backend skipped in Codex managed sandbox; run the same command from project PowerShell to use Playwright |
| `-` | `screenshot_backend` | `warning` | Playwright unavailable; fallback used: browser screenshot backend skipped in Codex managed sandbox; run the same command from project PowerShell to use Playwright |
| `-` | `screenshot_backend` | `ok` | visual_regression_mode=auto; screenshot backend unavailable, fallback used: browser screenshot backend skipped in Codex managed sandbox; run the same command from project PowerShell to use Playwright |
| `-` | `html_files_exist` | `ok` | Найдено HTML-файлов: 50. |
| `-` | `yield_vs_discount_exists` | `ok` | Найдено yield_vs_discount HTML: 3. |
| `monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | scatter |
| `monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Помесячное покрытие предложения спросом |
| `monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 10. |
| `monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `monthly_demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | bar |
| `monthly_demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Помесячный спрос и предложение |
| `monthly_demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `monthly_demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 27. |
| `monthly_demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Легенда отключена явно; статический fallback считает это допустимым. |
| `monthly_demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `monthly_demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `monthly_demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `monthly_demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `monthly_demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Подписи спроса/предложения найдены. |
| `monthly_demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `monthly_demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `monthly_demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `monthly_demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Повторяющиеся Y-title не найдены. |
| `monthly_demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `monthly_demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `monthly_demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `monthly_demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `monthly_demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `monthly_demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `monthly_demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `monthly_heatmap_placement_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | heatmap |
| `monthly_heatmap_placement_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Год |
| `monthly_heatmap_placement_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `monthly_heatmap_placement_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 7. |
| `monthly_heatmap_placement_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `monthly_heatmap_placement_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `monthly_heatmap_placement_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Volume policy подтверждена. |
| `monthly_heatmap_placement_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `monthly_heatmap_placement_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `monthly_heatmap_placement_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `monthly_heatmap_placement_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `monthly_heatmap_placement_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `monthly_heatmap_placement_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Итого вынесено в нейтральный overlay вне основной шкалы. |
| `monthly_heatmap_placement_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `monthly_heatmap_placement_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `monthly_heatmap_placement_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `monthly_heatmap_placement_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `monthly_heatmap_placement_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `monthly_heatmap_placement_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `monthly_heatmap_placement_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `monthly_heatmap_placement_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `monthly_heatmap_revenue_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | heatmap |
| `monthly_heatmap_revenue_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Год |
| `monthly_heatmap_revenue_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `monthly_heatmap_revenue_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 7. |
| `monthly_heatmap_revenue_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `monthly_heatmap_revenue_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `monthly_heatmap_revenue_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Revenue volume policy подтверждена. |
| `monthly_heatmap_revenue_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `monthly_heatmap_revenue_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `monthly_heatmap_revenue_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `monthly_heatmap_revenue_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `monthly_heatmap_revenue_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `monthly_heatmap_revenue_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Итого вынесено в нейтральный overlay вне основной шкалы. |
| `monthly_heatmap_revenue_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `monthly_heatmap_revenue_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `monthly_heatmap_revenue_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `monthly_heatmap_revenue_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `monthly_heatmap_revenue_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `monthly_heatmap_revenue_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `monthly_heatmap_revenue_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `monthly_heatmap_revenue_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `monthly_cumulative_placement_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | scatter |
| `monthly_cumulative_placement_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Накопленный объем размещения ОФЗ по номиналу |
| `monthly_cumulative_placement_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `monthly_cumulative_placement_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 9. |
| `monthly_cumulative_placement_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `monthly_cumulative_placement_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `monthly_cumulative_placement_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Volume policy подтверждена. |
| `monthly_cumulative_placement_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `monthly_cumulative_placement_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `monthly_cumulative_placement_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `monthly_cumulative_placement_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `monthly_cumulative_placement_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Подписи ключевых точек найдены. |
| `monthly_cumulative_placement_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `monthly_cumulative_placement_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `monthly_cumulative_placement_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `monthly_cumulative_placement_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `monthly_cumulative_placement_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `monthly_cumulative_placement_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `monthly_cumulative_placement_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `monthly_cumulative_placement_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `monthly_cumulative_placement_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `monthly_placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | bar |
| `monthly_placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Помесячный объем размещения ОФЗ по номиналу |
| `monthly_placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `monthly_placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 10. |
| `monthly_placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `monthly_placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `monthly_placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Volume policy подтверждена. |
| `monthly_placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `monthly_placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `monthly_placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `monthly_placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Подписи monthly_placement_volume найдены. |
| `monthly_placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `monthly_placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `monthly_placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `monthly_placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `monthly_placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `monthly_placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `monthly_placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `monthly_placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `monthly_placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `monthly_placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `monthly_placement_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | bar, scatter |
| `monthly_placement_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Помесячная структура объема размещения по номиналу по форматам |
| `monthly_placement_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `monthly_placement_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 30. |
| `monthly_placement_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Легенда отключена явно; статический fallback считает это допустимым. |
| `monthly_placement_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `monthly_placement_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Volume policy подтверждена. |
| `monthly_placement_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Total labels найдены. |
| `monthly_placement_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `monthly_placement_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `monthly_placement_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `monthly_placement_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `monthly_placement_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `monthly_placement_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Повторяющиеся Y-title не найдены. |
| `monthly_placement_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `monthly_placement_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `monthly_placement_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `monthly_placement_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `monthly_placement_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `monthly_placement_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `monthly_placement_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `monthly_placement_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | bar, scatter |
| `monthly_placement_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Помесячная структура объема размещения по номиналу по срокам обращения |
| `monthly_placement_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `monthly_placement_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 37. |
| `monthly_placement_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Легенда отключена явно; статический fallback считает это допустимым. |
| `monthly_placement_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `monthly_placement_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Volume policy подтверждена. |
| `monthly_placement_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Total labels найдены. |
| `monthly_placement_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `monthly_placement_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `monthly_placement_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `monthly_placement_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `monthly_placement_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `monthly_placement_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Повторяющиеся Y-title не найдены. |
| `monthly_placement_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `monthly_placement_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `monthly_placement_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `monthly_placement_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `monthly_placement_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `monthly_placement_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `monthly_placement_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `monthly_weighted_avg_yield_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | scatter |
| `monthly_weighted_avg_yield_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Помесячная средневзвешенная доходность ОФЗ |
| `monthly_weighted_avg_yield_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `monthly_weighted_avg_yield_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 9. |
| `monthly_weighted_avg_yield_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `monthly_weighted_avg_yield_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `monthly_weighted_avg_yield_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `monthly_weighted_avg_yield_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `monthly_weighted_avg_yield_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `monthly_weighted_avg_yield_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `monthly_weighted_avg_yield_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `monthly_weighted_avg_yield_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `monthly_weighted_avg_yield_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `monthly_weighted_avg_yield_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `monthly_weighted_avg_yield_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `monthly_weighted_avg_yield_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `monthly_weighted_avg_yield_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `monthly_weighted_avg_yield_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `monthly_weighted_avg_yield_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `monthly_weighted_avg_yield_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `monthly_weighted_avg_yield_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `revenue_gap_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | bar |
| `revenue_gap_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Разница номинал - выручка по срокам обращения |
| `revenue_gap_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `revenue_gap_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 7. |
| `revenue_gap_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `revenue_gap_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `revenue_gap_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `revenue_gap_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `revenue_gap_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `revenue_gap_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `revenue_gap_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `revenue_gap_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `revenue_gap_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `revenue_gap_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `revenue_gap_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `revenue_gap_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `revenue_gap_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `revenue_gap_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `revenue_gap_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `revenue_gap_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `revenue_gap_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `revenue_gap_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | bar |
| `revenue_gap_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Разница номинал - выручка по видам ОФЗ |
| `revenue_gap_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `revenue_gap_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 6. |
| `revenue_gap_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `revenue_gap_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `revenue_gap_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `revenue_gap_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `revenue_gap_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `revenue_gap_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `revenue_gap_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `revenue_gap_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `revenue_gap_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `revenue_gap_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `revenue_gap_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `revenue_gap_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `revenue_gap_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `revenue_gap_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `revenue_gap_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `revenue_gap_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `revenue_gap_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `format_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | bar |
| `format_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Разница между номинальным размещением и выручкой по форматам |
| `format_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `format_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 6. |
| `format_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `format_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `format_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `format_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `format_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `format_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `format_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `format_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `format_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `format_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `format_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `format_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `format_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `format_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `format_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `format_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `format_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `nominal_revenue_gap_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | bar |
| `nominal_revenue_gap_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Разница между номиналом и выручкой от реализации |
| `nominal_revenue_gap_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `nominal_revenue_gap_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 4. |
| `nominal_revenue_gap_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Один trace; легенда не обязательна. |
| `nominal_revenue_gap_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `nominal_revenue_gap_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `nominal_revenue_gap_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `nominal_revenue_gap_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `nominal_revenue_gap_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `nominal_revenue_gap_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `nominal_revenue_gap_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `nominal_revenue_gap_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `nominal_revenue_gap_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `nominal_revenue_gap_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `nominal_revenue_gap_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `nominal_revenue_gap_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `nominal_revenue_gap_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `nominal_revenue_gap_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `nominal_revenue_gap_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `nominal_revenue_gap_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `monthly_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | bar |
| `monthly_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Помесячная разница между номиналом и выручкой |
| `monthly_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `monthly_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 9. |
| `monthly_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `monthly_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `monthly_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `monthly_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `monthly_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `monthly_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `monthly_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `monthly_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `monthly_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `monthly_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `monthly_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `monthly_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `monthly_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `monthly_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `monthly_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `monthly_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `monthly_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `monthly_revenue_vs_nominal_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | bar |
| `monthly_revenue_vs_nominal_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Помесячное размещение и выручка от реализации ОФЗ |
| `monthly_revenue_vs_nominal_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `monthly_revenue_vs_nominal_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 27. |
| `monthly_revenue_vs_nominal_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Легенда отключена явно; статический fallback считает это допустимым. |
| `monthly_revenue_vs_nominal_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `monthly_revenue_vs_nominal_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `monthly_revenue_vs_nominal_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `monthly_revenue_vs_nominal_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `monthly_revenue_vs_nominal_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `monthly_revenue_vs_nominal_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `monthly_revenue_vs_nominal_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `monthly_revenue_vs_nominal_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `monthly_revenue_vs_nominal_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Повторяющиеся Y-title не найдены. |
| `monthly_revenue_vs_nominal_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `monthly_revenue_vs_nominal_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `monthly_revenue_vs_nominal_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `monthly_revenue_vs_nominal_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `monthly_revenue_vs_nominal_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `monthly_revenue_vs_nominal_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `monthly_revenue_vs_nominal_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `revenue_vs_nominal_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | bar |
| `revenue_vs_nominal_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Номинальное размещение и выручка от реализации ОФЗ |
| `revenue_vs_nominal_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `revenue_vs_nominal_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 6. |
| `revenue_vs_nominal_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `revenue_vs_nominal_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `revenue_vs_nominal_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `revenue_vs_nominal_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `revenue_vs_nominal_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `revenue_vs_nominal_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `revenue_vs_nominal_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `revenue_vs_nominal_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `revenue_vs_nominal_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `revenue_vs_nominal_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `revenue_vs_nominal_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `revenue_vs_nominal_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `revenue_vs_nominal_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `revenue_vs_nominal_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `revenue_vs_nominal_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `revenue_vs_nominal_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `revenue_vs_nominal_by_period_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `revenue_to_nominal_ratio_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | scatter |
| `revenue_to_nominal_ratio_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Выручка от реализации к номинальному объему размещения |
| `revenue_to_nominal_ratio_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `revenue_to_nominal_ratio_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 4. |
| `revenue_to_nominal_ratio_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Один trace; легенда не обязательна. |
| `revenue_to_nominal_ratio_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `revenue_to_nominal_ratio_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `revenue_to_nominal_ratio_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `revenue_to_nominal_ratio_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `revenue_to_nominal_ratio_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `revenue_to_nominal_ratio_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `revenue_to_nominal_ratio_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `revenue_to_nominal_ratio_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `revenue_to_nominal_ratio_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `revenue_to_nominal_ratio_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `revenue_to_nominal_ratio_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `revenue_to_nominal_ratio_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `revenue_to_nominal_ratio_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `revenue_to_nominal_ratio_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `revenue_to_nominal_ratio_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `revenue_to_nominal_ratio_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `risk_quadrant_retrospective_facet_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | scatter |
| `risk_quadrant_retrospective_facet_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Ретроспективный квадрант риска: small multiples (кратность спроса к размещению) |
| `risk_quadrant_retrospective_facet_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `risk_quadrant_retrospective_facet_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 26. |
| `risk_quadrant_retrospective_facet_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `risk_quadrant_retrospective_facet_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `risk_quadrant_retrospective_facet_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `risk_quadrant_retrospective_facet_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `risk_quadrant_retrospective_facet_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `risk_quadrant_retrospective_facet_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `risk_quadrant_retrospective_facet_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `risk_quadrant_retrospective_facet_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `risk_quadrant_retrospective_facet_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `risk_quadrant_retrospective_facet_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `risk_quadrant_retrospective_facet_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `risk_quadrant_retrospective_facet_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `risk_quadrant_retrospective_facet_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `risk_quadrant_retrospective_facet_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `risk_quadrant_retrospective_facet_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `risk_quadrant_retrospective_facet_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `risk_quadrant_retrospective_facet_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `risk_quadrant_retrospective_logx_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | scatter |
| `risk_quadrant_retrospective_logx_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Ретроспективный квадрант риска: log-X (кратность спроса к размещению) |
| `risk_quadrant_retrospective_logx_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `risk_quadrant_retrospective_logx_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 11. |
| `risk_quadrant_retrospective_logx_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `risk_quadrant_retrospective_logx_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `risk_quadrant_retrospective_logx_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `risk_quadrant_retrospective_logx_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `risk_quadrant_retrospective_logx_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `risk_quadrant_retrospective_logx_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `risk_quadrant_retrospective_logx_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `risk_quadrant_retrospective_logx_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `risk_quadrant_retrospective_logx_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `risk_quadrant_retrospective_logx_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `risk_quadrant_retrospective_logx_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `risk_quadrant_retrospective_logx_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `risk_quadrant_retrospective_logx_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `risk_quadrant_retrospective_logx_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `risk_quadrant_retrospective_logx_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `risk_quadrant_retrospective_logx_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `risk_quadrant_retrospective_logx_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `risk_quadrant_retrospective_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | scatter |
| `risk_quadrant_retrospective_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Ретроспективный квадрант риска: выбросы (кратность спроса к размещению) |
| `risk_quadrant_retrospective_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `risk_quadrant_retrospective_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 11. |
| `risk_quadrant_retrospective_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `risk_quadrant_retrospective_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `risk_quadrant_retrospective_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `risk_quadrant_retrospective_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `risk_quadrant_retrospective_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `risk_quadrant_retrospective_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `risk_quadrant_retrospective_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `risk_quadrant_retrospective_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `risk_quadrant_retrospective_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `risk_quadrant_retrospective_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `risk_quadrant_retrospective_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `risk_quadrant_retrospective_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `risk_quadrant_retrospective_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `risk_quadrant_retrospective_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `risk_quadrant_retrospective_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `risk_quadrant_retrospective_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `risk_quadrant_retrospective_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `risk_quadrant_retrospective_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | scatter |
| `risk_quadrant_retrospective_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Ретроспективный квадрант риска: кратность спроса к размещению и доходность |
| `risk_quadrant_retrospective_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `risk_quadrant_retrospective_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 12. |
| `risk_quadrant_retrospective_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `risk_quadrant_retrospective_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `risk_quadrant_retrospective_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `risk_quadrant_retrospective_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `risk_quadrant_retrospective_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `risk_quadrant_retrospective_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `risk_quadrant_retrospective_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `risk_quadrant_retrospective_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `risk_quadrant_retrospective_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `risk_quadrant_retrospective_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `risk_quadrant_retrospective_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `risk_quadrant_retrospective_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `risk_quadrant_retrospective_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `risk_quadrant_retrospective_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `risk_quadrant_retrospective_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `risk_quadrant_retrospective_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `risk_quadrant_retrospective_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | scatter |
| `bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Покрытие предложения спросом |
| `bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 6. |
| `bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Один trace; легенда не обязательна. |
| `bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | bar |
| `demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Спрос и предложение |
| `demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 6. |
| `demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `risk_quadrant_demand_to_placement_by_quarter_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | scatter |
| `risk_quadrant_demand_to_placement_by_quarter_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Квадрант риска: спрос к размещению и доходность, отчетный год |
| `risk_quadrant_demand_to_placement_by_quarter_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `risk_quadrant_demand_to_placement_by_quarter_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 11. |
| `risk_quadrant_demand_to_placement_by_quarter_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `risk_quadrant_demand_to_placement_by_quarter_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `risk_quadrant_demand_to_placement_by_quarter_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `risk_quadrant_demand_to_placement_by_quarter_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `risk_quadrant_demand_to_placement_by_quarter_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `risk_quadrant_demand_to_placement_by_quarter_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `risk_quadrant_demand_to_placement_by_quarter_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `risk_quadrant_demand_to_placement_by_quarter_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `risk_quadrant_demand_to_placement_by_quarter_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `risk_quadrant_demand_to_placement_by_quarter_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `risk_quadrant_demand_to_placement_by_quarter_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `risk_quadrant_demand_to_placement_by_quarter_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `risk_quadrant_demand_to_placement_by_quarter_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `risk_quadrant_demand_to_placement_by_quarter_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `risk_quadrant_demand_to_placement_by_quarter_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `risk_quadrant_demand_to_placement_by_quarter_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `risk_quadrant_demand_to_placement_by_quarter_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `risk_quadrant_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | scatter |
| `risk_quadrant_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Квадрант риска: кратность спроса к размещению и доходность |
| `risk_quadrant_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `risk_quadrant_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 8. |
| `risk_quadrant_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `risk_quadrant_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `risk_quadrant_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `risk_quadrant_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `risk_quadrant_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `risk_quadrant_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `risk_quadrant_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `risk_quadrant_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `risk_quadrant_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `risk_quadrant_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `risk_quadrant_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `risk_quadrant_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `risk_quadrant_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `risk_quadrant_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `risk_quadrant_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `risk_quadrant_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `risk_quadrant_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `sankey_period_format_maturity_type_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | sankey |
| `sankey_period_format_maturity_type_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Структура размещений ОФЗ: период → формат → срок → вид бумаги |
| `sankey_period_format_maturity_type_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `sankey_period_format_maturity_type_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 2. |
| `sankey_period_format_maturity_type_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Один trace; легенда не обязательна. |
| `sankey_period_format_maturity_type_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `sankey_period_format_maturity_type_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Volume policy подтверждена. |
| `sankey_period_format_maturity_type_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `sankey_period_format_maturity_type_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `sankey_period_format_maturity_type_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `sankey_period_format_maturity_type_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `sankey_period_format_maturity_type_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `sankey_period_format_maturity_type_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `sankey_period_format_maturity_type_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `sankey_period_format_maturity_type_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `sankey_period_format_maturity_type_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `sankey_period_format_maturity_type_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `sankey_period_format_maturity_type_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `sankey_period_format_maturity_type_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `sankey_period_format_maturity_type_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `sankey_period_format_maturity_type_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `sankey_period_format_type_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | sankey |
| `sankey_period_format_type_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Структура размещений ОФЗ: период → формат → вид бумаги → срок |
| `sankey_period_format_type_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `sankey_period_format_type_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 2. |
| `sankey_period_format_type_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Один trace; легенда не обязательна. |
| `sankey_period_format_type_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `sankey_period_format_type_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Volume policy подтверждена. |
| `sankey_period_format_type_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `sankey_period_format_type_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `sankey_period_format_type_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `sankey_period_format_type_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `sankey_period_format_type_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `sankey_period_format_type_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `sankey_period_format_type_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `sankey_period_format_type_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `sankey_period_format_type_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `sankey_period_format_type_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `sankey_period_format_type_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `sankey_period_format_type_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `sankey_period_format_type_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `sankey_period_format_type_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `sankey_period_maturity_type_format_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | sankey |
| `sankey_period_maturity_type_format_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Структура размещений ОФЗ: период → срок → вид бумаги → формат |
| `sankey_period_maturity_type_format_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `sankey_period_maturity_type_format_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 2. |
| `sankey_period_maturity_type_format_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Один trace; легенда не обязательна. |
| `sankey_period_maturity_type_format_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `sankey_period_maturity_type_format_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Volume policy подтверждена. |
| `sankey_period_maturity_type_format_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `sankey_period_maturity_type_format_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `sankey_period_maturity_type_format_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `sankey_period_maturity_type_format_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `sankey_period_maturity_type_format_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `sankey_period_maturity_type_format_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `sankey_period_maturity_type_format_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `sankey_period_maturity_type_format_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `sankey_period_maturity_type_format_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `sankey_period_maturity_type_format_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `sankey_period_maturity_type_format_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `sankey_period_maturity_type_format_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `sankey_period_maturity_type_format_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `sankey_period_maturity_type_format_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `sankey_structure_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | sankey |
| `sankey_structure_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Структура объема размещения ОФЗ: период → вид бумаги → срок → формат |
| `sankey_structure_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `sankey_structure_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 2. |
| `sankey_structure_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Один trace; легенда не обязательна. |
| `sankey_structure_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `sankey_structure_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Volume policy подтверждена. |
| `sankey_structure_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `sankey_structure_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `sankey_structure_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `sankey_structure_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `sankey_structure_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `sankey_structure_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `sankey_structure_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `sankey_structure_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `sankey_structure_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `sankey_structure_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `sankey_structure_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `sankey_structure_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `sankey_structure_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `sankey_structure_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `sankey_target_period_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | sankey |
| `sankey_target_period_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Структура размещений ОФЗ в отчетном периоде: 2026-M01-M04 |
| `sankey_target_period_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `sankey_target_period_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 2. |
| `sankey_target_period_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Один trace; легенда не обязательна. |
| `sankey_target_period_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `sankey_target_period_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Volume policy подтверждена. |
| `sankey_target_period_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `sankey_target_period_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `sankey_target_period_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `sankey_target_period_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `sankey_target_period_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `sankey_target_period_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `sankey_target_period_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `sankey_target_period_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `sankey_target_period_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `sankey_target_period_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `sankey_target_period_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `sankey_target_period_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `sankey_target_period_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `sankey_target_period_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `demand_cutoff_explanation_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | scatter |
| `demand_cutoff_explanation_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Отсечение спроса: кратность спроса, дисконт и доходность |
| `demand_cutoff_explanation_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `demand_cutoff_explanation_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 13. |
| `demand_cutoff_explanation_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Один trace; легенда не обязательна. |
| `demand_cutoff_explanation_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `demand_cutoff_explanation_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `demand_cutoff_explanation_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `demand_cutoff_explanation_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `demand_cutoff_explanation_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `demand_cutoff_explanation_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `demand_cutoff_explanation_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `demand_cutoff_explanation_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `demand_cutoff_explanation_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `demand_cutoff_explanation_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Bubble-size policy и лимит подписей подтверждены. |
| `demand_cutoff_explanation_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `demand_cutoff_explanation_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `demand_cutoff_explanation_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `demand_cutoff_explanation_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `demand_cutoff_explanation_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `demand_cutoff_explanation_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `discount_vs_demand_logx_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | scatter |
| `discount_vs_demand_logx_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Дисконт к номиналу и спрос: log-X |
| `discount_vs_demand_logx_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `discount_vs_demand_logx_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 12. |
| `discount_vs_demand_logx_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `discount_vs_demand_logx_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `discount_vs_demand_logx_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `discount_vs_demand_logx_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `discount_vs_demand_logx_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `discount_vs_demand_logx_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `discount_vs_demand_logx_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `discount_vs_demand_logx_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `discount_vs_demand_logx_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `discount_vs_demand_logx_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `discount_vs_demand_logx_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `discount_vs_demand_logx_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `discount_vs_demand_logx_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `discount_vs_demand_logx_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `discount_vs_demand_logx_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `discount_vs_demand_logx_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `discount_vs_demand_logx_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `discount_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | scatter |
| `discount_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Дисконт к номиналу и спрос |
| `discount_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `discount_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 12. |
| `discount_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `discount_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `discount_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `discount_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `discount_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `discount_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `discount_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `discount_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `discount_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `discount_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `discount_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `discount_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `discount_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `discount_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `discount_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `discount_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `discount_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `discount_vs_demand_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | scatter |
| `discount_vs_demand_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Дисконт к номиналу и спрос: выбросы |
| `discount_vs_demand_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `discount_vs_demand_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 11. |
| `discount_vs_demand_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `discount_vs_demand_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `discount_vs_demand_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `discount_vs_demand_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `discount_vs_demand_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `discount_vs_demand_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `discount_vs_demand_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `discount_vs_demand_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `discount_vs_demand_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `discount_vs_demand_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `discount_vs_demand_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `discount_vs_demand_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `discount_vs_demand_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `discount_vs_demand_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `discount_vs_demand_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `discount_vs_demand_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `discount_vs_demand_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `discount_vs_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | scatter |
| `discount_vs_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Дисконт выручки и разница между номиналом и выручкой |
| `discount_vs_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `discount_vs_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 5. |
| `discount_vs_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `discount_vs_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `discount_vs_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `discount_vs_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `discount_vs_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `discount_vs_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `discount_vs_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `discount_vs_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `discount_vs_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `discount_vs_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `discount_vs_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `discount_vs_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `discount_vs_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `discount_vs_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `discount_vs_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `discount_vs_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `discount_vs_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `format_terms_aggregate_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | scatter |
| `format_terms_aggregate_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Средние условия размещения по форматам<br><sup>Одна точка — формат размещения в периоде; размер точки — объем размещения по номиналу</sup> |
| `format_terms_aggregate_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `format_terms_aggregate_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 9. |
| `format_terms_aggregate_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `format_terms_aggregate_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `format_terms_aggregate_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `format_terms_aggregate_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `format_terms_aggregate_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `format_terms_aggregate_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `format_terms_aggregate_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `format_terms_aggregate_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `format_terms_aggregate_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `format_terms_aggregate_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `format_terms_aggregate_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `format_terms_aggregate_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `format_terms_aggregate_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `format_terms_aggregate_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `format_terms_aggregate_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Aggregate scatter contract подтвержден. |
| `format_terms_aggregate_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `format_terms_aggregate_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `format_terms_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | scatter |
| `format_terms_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Условия размещения ОФЗ по форматам<br><sup>Цвет — формат; форма — вид ОФЗ; размер — объем размещения по номиналу</sup> |
| `format_terms_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `format_terms_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 8. |
| `format_terms_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `format_terms_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `format_terms_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `format_terms_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `format_terms_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `format_terms_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `format_terms_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `format_terms_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `format_terms_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `format_terms_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `format_terms_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `format_terms_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `format_terms_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `format_terms_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `format_terms_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `format_terms_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Detailed scatter contract подтвержден. |
| `format_terms_scatter_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `yield_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | scatter |
| `yield_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Доходность и спрос |
| `yield_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `yield_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 11. |
| `yield_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `yield_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `yield_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `yield_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `yield_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `yield_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `yield_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `yield_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `yield_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `yield_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `yield_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `yield_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `yield_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `yield_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `yield_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `yield_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `yield_vs_demand_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `yield_vs_discount_facet_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | scatter |
| `yield_vs_discount_facet_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Квадрант риска: дисконт к номиналу и доходность — по периодам |
| `yield_vs_discount_facet_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `yield_vs_discount_facet_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 28. |
| `yield_vs_discount_facet_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `yield_vs_discount_facet_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `yield_vs_discount_facet_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `yield_vs_discount_facet_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `yield_vs_discount_facet_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `yield_vs_discount_facet_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `yield_vs_discount_facet_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `yield_vs_discount_facet_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `yield_vs_discount_facet_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `yield_vs_discount_facet_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Повторяющиеся Y-title не найдены. |
| `yield_vs_discount_facet_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `yield_vs_discount_facet_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Контракт yield_vs_discount подтвержден. |
| `yield_vs_discount_facet_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `yield_vs_discount_facet_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `yield_vs_discount_facet_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `yield_vs_discount_facet_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `yield_vs_discount_facet_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `yield_vs_discount_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | scatter |
| `yield_vs_discount_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Квадрант риска: дисконт к номиналу и доходность |
| `yield_vs_discount_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `yield_vs_discount_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 17. |
| `yield_vs_discount_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `yield_vs_discount_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `yield_vs_discount_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `yield_vs_discount_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `yield_vs_discount_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `yield_vs_discount_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `yield_vs_discount_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `yield_vs_discount_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `yield_vs_discount_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `yield_vs_discount_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `yield_vs_discount_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `yield_vs_discount_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Контракт yield_vs_discount подтвержден. |
| `yield_vs_discount_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `yield_vs_discount_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `yield_vs_discount_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `yield_vs_discount_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `yield_vs_discount_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `yield_vs_discount_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | scatter |
| `yield_vs_discount_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Квадрант риска: дисконт к номиналу и доходность — выбросы |
| `yield_vs_discount_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `yield_vs_discount_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 17. |
| `yield_vs_discount_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `yield_vs_discount_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `yield_vs_discount_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `yield_vs_discount_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `yield_vs_discount_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `yield_vs_discount_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `yield_vs_discount_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `yield_vs_discount_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `yield_vs_discount_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `yield_vs_discount_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `yield_vs_discount_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `yield_vs_discount_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Контракт yield_vs_discount подтвержден. |
| `yield_vs_discount_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `yield_vs_discount_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `yield_vs_discount_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `yield_vs_discount_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `yield_vs_discount_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `format_discount_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | bar |
| `format_discount_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Средневзвешенный дисконт к номиналу по форматам<br><sup>Y = средневзвешенный дисконт к номиналу, п.п.; размер размещения доступен в hover и CSV</sup> |
| `format_discount_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `format_discount_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 6. |
| `format_discount_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `format_discount_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `format_discount_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `format_discount_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `format_discount_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `format_discount_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `format_discount_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `format_discount_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `format_discount_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `format_discount_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `format_discount_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `format_discount_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `format_discount_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Discount-axis contract format_discount подтвержден. |
| `format_discount_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `format_discount_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `format_discount_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `format_discount_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `format_structure_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | bar, scatter |
| `format_structure_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Форматы размещения ОФЗ |
| `format_structure_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `format_structure_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 8. |
| `format_structure_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Легенда отключена явно; статический fallback считает это допустимым. |
| `format_structure_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `format_structure_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Volume policy подтверждена. |
| `format_structure_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Total labels найдены. |
| `format_structure_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Подписи сегментов и total labels format_structure подтверждены. |
| `format_structure_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `format_structure_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `format_structure_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `format_structure_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `format_structure_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `format_structure_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `format_structure_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `format_structure_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `format_structure_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `format_structure_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `format_structure_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `format_structure_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `format_terms_comparison_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | bar |
| `format_terms_comparison_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Сравнение условий размещения по форматам<br><sup>Доходность и дисконт рассчитаны средневзвешенно по объему размещения по номиналу; n — количество размещений формата в периоде</sup> |
| `format_terms_comparison_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `format_terms_comparison_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 22. |
| `format_terms_comparison_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Легенда отключена явно; статический fallback считает это допустимым. |
| `format_terms_comparison_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `format_terms_comparison_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `format_terms_comparison_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `format_terms_comparison_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `format_terms_comparison_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `format_terms_comparison_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `format_terms_comparison_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `format_terms_comparison_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `format_terms_comparison_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `format_terms_comparison_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `format_terms_comparison_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `format_terms_comparison_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `format_terms_comparison_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | n labels и CSV contract подтверждены. |
| `format_terms_comparison_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `format_terms_comparison_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `format_terms_comparison_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `format_terms_delta_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | bar |
| `format_terms_delta_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Разница условий размещения: ДРПА минус Аукцион<br><sup>Δ = ДРПА − Аукцион; цвет показывает аналитическую оценку различия с учетом направления метрики</sup> |
| `format_terms_delta_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `format_terms_delta_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 21. |
| `format_terms_delta_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Легенда отключена явно; статический fallback считает это допустимым. |
| `format_terms_delta_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `format_terms_delta_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `format_terms_delta_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `format_terms_delta_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `format_terms_delta_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `format_terms_delta_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `format_terms_delta_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `format_terms_delta_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `format_terms_delta_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `format_terms_delta_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `format_terms_delta_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `format_terms_delta_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `format_terms_delta_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `format_terms_delta_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `format_terms_delta_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `format_terms_delta_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Смысловая легенда и facet-title подтверждены. |
| `maturity_structure_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | bar, scatter |
| `maturity_structure_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Структура размещения ОФЗ по срокам |
| `maturity_structure_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `maturity_structure_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 8. |
| `maturity_structure_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Легенда отключена явно; статический fallback считает это допустимым. |
| `maturity_structure_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `maturity_structure_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Volume policy подтверждена. |
| `maturity_structure_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Total labels найдены. |
| `maturity_structure_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `maturity_structure_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `maturity_structure_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `maturity_structure_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `maturity_structure_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `maturity_structure_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `maturity_structure_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `maturity_structure_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `maturity_structure_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `maturity_structure_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `maturity_structure_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `maturity_structure_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `maturity_structure_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | bar |
| `placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Объем размещения ОФЗ по номиналу |
| `placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 5. |
| `placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Один trace; легенда не обязательна. |
| `placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Volume policy подтверждена. |
| `placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `yield_boxplot_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | box, scatter |
| `yield_boxplot_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Распределение доходности ОФЗ по видам бумаг |
| `yield_boxplot_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `yield_boxplot_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 15. |
| `yield_boxplot_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Легенда отключена явно; статический fallback считает это допустимым. |
| `yield_boxplot_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `yield_boxplot_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `yield_boxplot_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `yield_boxplot_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `yield_boxplot_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `yield_boxplot_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `yield_boxplot_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `yield_boxplot_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `yield_boxplot_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `yield_boxplot_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `yield_boxplot_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `yield_boxplot_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `yield_boxplot_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `yield_boxplot_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `yield_boxplot_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `yield_boxplot_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `yield_boxplot_ofz_pd_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | box, scatter |
| `yield_boxplot_ofz_pd_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Период |
| `yield_boxplot_ofz_pd_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `yield_boxplot_ofz_pd_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 20. |
| `yield_boxplot_ofz_pd_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Легенда отключена явно; статический fallback считает это допустимым. |
| `yield_boxplot_ofz_pd_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `yield_boxplot_ofz_pd_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `yield_boxplot_ofz_pd_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `yield_boxplot_ofz_pd_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `yield_boxplot_ofz_pd_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `yield_boxplot_ofz_pd_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `yield_boxplot_ofz_pd_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `yield_boxplot_ofz_pd_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `yield_boxplot_ofz_pd_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `yield_boxplot_ofz_pd_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `yield_boxplot_ofz_pd_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `yield_boxplot_ofz_pd_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `yield_boxplot_ofz_pd_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `yield_boxplot_ofz_pd_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `yield_boxplot_ofz_pd_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `yield_boxplot_ofz_pd_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |
| `yield_by_type_month_cumulative_2026-05-01_retrospective_4.html` | `trace_types` | `ok` | scatter |
| `yield_by_type_month_cumulative_2026-05-01_retrospective_4.html` | `title` | `ok` | Средневзвешенная доходность по видам ОФЗ |
| `yield_by_type_month_cumulative_2026-05-01_retrospective_4.html` | `axis_titles` | `ok` | Русские подписи осей/измерений найдены. |
| `yield_by_type_month_cumulative_2026-05-01_retrospective_4.html` | `annotations` | `ok` | Найдены annotation/text entries: 6. |
| `yield_by_type_month_cumulative_2026-05-01_retrospective_4.html` | `legend` | `ok` | Legend/name metadata найдено. |
| `yield_by_type_month_cumulative_2026-05-01_retrospective_4.html` | `hovertemplate` | `ok` | hovertemplate найден. |
| `yield_by_type_month_cumulative_2026-05-01_retrospective_4.html` | `volume_scale` | `ok` | Не volume-график. |
| `yield_by_type_month_cumulative_2026-05-01_retrospective_4.html` | `stacked_total_labels` | `ok` | Не stacked structure chart. |
| `yield_by_type_month_cumulative_2026-05-01_retrospective_4.html` | `format_structure_contract` | `ok` | Не format_structure. |
| `yield_by_type_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_demand_supply_labels` | `ok` | Не monthly_demand_supply. |
| `yield_by_type_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_placement_volume_labels` | `ok` | Не monthly_placement_volume. |
| `yield_by_type_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_cumulative_placement_labels` | `ok` | Не monthly_cumulative_placement. |
| `yield_by_type_month_cumulative_2026-05-01_retrospective_4.html` | `monthly_heatmap_total_contract` | `ok` | Не monthly heatmap. |
| `yield_by_type_month_cumulative_2026-05-01_retrospective_4.html` | `facet_yaxis_titles` | `ok` | Не facet-график. |
| `yield_by_type_month_cumulative_2026-05-01_retrospective_4.html` | `demand_cutoff_contract` | `ok` | Не demand_cutoff_explanation. |
| `yield_by_type_month_cumulative_2026-05-01_retrospective_4.html` | `yield_vs_discount_contract` | `ok` | Не yield_vs_discount. |
| `yield_by_type_month_cumulative_2026-05-01_retrospective_4.html` | `format_discount_contract` | `ok` | Не format_discount. |
| `yield_by_type_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_comparison_contract` | `ok` | Не format_terms_comparison. |
| `yield_by_type_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_aggregate_scatter_contract` | `ok` | Не format_terms_aggregate_scatter. |
| `yield_by_type_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_scatter_contract` | `ok` | Не format_terms_scatter. |
| `yield_by_type_month_cumulative_2026-05-01_retrospective_4.html` | `format_terms_delta_by_format_contract` | `ok` | Не format_terms_delta_by_format. |

## Скриншоты

Папка для скриншотов: `outputs/reports/visual_regression/screenshots`.
Если screenshot backend недоступен, папка создается, но изображения не формируются.

## Ограничения

- Fallback static HTML inspection проверяет структуру Plotly/HTML, но не заменяет визуальный просмотр графика.
- Проверка наложения подписей без screenshot backend является эвристической.
- Полноценное сравнение контрольных зон будет доступно после подключения screenshot backend.

## Screenshot-артефакты

- Screenshot artifacts count: `0`
- Screenshot manifest directory: `outputs/reports/visual_regression`
- Diff report directory: `outputs/reports/visual_regression/diffs`

| HTML | Screenshot | Baseline status | SHA256 |
| --- | --- | --- | --- |

Screenshot PNG, manifest and diff report files are generated outputs and must not be committed.
If baseline screenshots are absent, the diff report records `missing_baseline` instead of failing the run.
