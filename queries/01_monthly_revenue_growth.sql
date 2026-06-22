-- Q1: Monthly revenue with month-over-month growth %.
-- Demonstrates: date truncation, aggregation, LAG() window for period comparison.
with monthly as (
    select
        date_trunc('month', order_date)        as month,
        sum(amount_eur * quantity)             as revenue,
        count(*)                               as orders
    from orders
    group by 1
)
select
    month,
    round(revenue, 0)                                          as revenue_eur,
    orders,
    round(100.0 * (revenue - lag(revenue) over (order by month))
          / nullif(lag(revenue) over (order by month), 0), 1) as mom_growth_pct
from monthly
order by month;
