SELECT
    window_start,
    window_end,
    symbol,
    avg_price,
    min_price,
    max_price,
    max_price - min_price AS price_range,
    total_volume,
    tick_count,
    total_volume::DOUBLE PRECISION / NULLIF(tick_count, 0)
        AS avg_volume_per_tick
FROM public.market_summary
