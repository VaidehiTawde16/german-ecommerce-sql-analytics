-- Q3: RFM (Recency, Frequency, Monetary) customer segmentation.
-- Demonstrates: NTILE() quartile scoring, CASE segment logic, CTE chaining.
with bounds as (
    select max(order_date) as as_of from orders
),
rfm_base as (
    select
        o.customer_id,
        date_diff('day', max(o.order_date), b.as_of) as recency_days,
        count(*)                                     as frequency,
        sum(o.amount_eur * o.quantity)               as monetary
    from orders o cross join bounds b
    group by o.customer_id, b.as_of
),
scored as (
    select *,
        ntile(4) over (order by recency_days desc) as r_score,  -- lower recency = better
        ntile(4) over (order by frequency)         as f_score,
        ntile(4) over (order by monetary)          as m_score
    from rfm_base
)
select
    case
        when r_score >= 3 and f_score >= 3 and m_score >= 3 then 'Champions'
        when r_score >= 3 and f_score >= 2                  then 'Loyal'
        when r_score >= 3                                   then 'Recent / Promising'
        when r_score <= 2 and f_score >= 3                  then 'At Risk (was active)'
        else 'Hibernating'
    end                                            as segment,
    count(*)                                       as customers,
    round(avg(monetary), 0)                        as avg_lifetime_eur,
    round(avg(frequency), 1)                       as avg_orders
from scored
group by 1
order by customers desc;
