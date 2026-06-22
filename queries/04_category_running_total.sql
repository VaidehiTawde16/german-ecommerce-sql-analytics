-- Q4: Revenue by category with running cumulative total and share of grand total.
-- Demonstrates: window SUM() OVER for running totals, ratio-to-report.
with cat as (
    select
        category,
        sum(amount_eur * quantity) as revenue
    from orders
    group by category
)
select
    category,
    round(revenue, 0)                                                   as revenue_eur,
    round(100.0 * revenue / sum(revenue) over (), 1)                    as pct_of_total,
    round(sum(revenue) over (order by revenue desc
          rows between unbounded preceding and current row), 0)         as running_total_eur
from cat
order by revenue desc;
