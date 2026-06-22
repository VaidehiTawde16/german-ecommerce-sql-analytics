-- Q2: Monthly acquisition cohorts and their retention over the following months.
-- Demonstrates: first-touch cohorting, self-join on customer activity, pivot-style retention.
with first_order as (
    select
        customer_id,
        date_trunc('month', min(order_date)) as cohort_month
    from orders
    group by customer_id
),
activity as (
    select distinct
        o.customer_id,
        fo.cohort_month,
        date_trunc('month', o.order_date) as active_month
    from orders o
    join first_order fo using (customer_id)
),
retention as (
    select
        cohort_month,
        date_diff('month', cohort_month, active_month) as month_offset,
        count(distinct customer_id)                    as active_customers
    from activity
    group by 1, 2
),
cohort_size as (
    select cohort_month, count(distinct customer_id) as cohort_customers
    from first_order group by 1
)
select
    r.cohort_month,
    cs.cohort_customers,
    r.month_offset,
    r.active_customers,
    round(100.0 * r.active_customers / cs.cohort_customers, 1) as retention_pct
from retention r
join cohort_size cs using (cohort_month)
where r.month_offset between 0 and 6
order by r.cohort_month, r.month_offset;
