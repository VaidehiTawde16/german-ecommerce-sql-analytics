-- Q5: Top-3 customers by spend within each city.
-- Demonstrates: RANK() with PARTITION BY, qualifying window results.
select city, customer_id, total_spend_eur, orders, city_rank
from (
    select
        city,
        customer_id,
        round(sum(amount_eur * quantity), 0)                        as total_spend_eur,
        count(*)                                                    as orders,
        rank() over (partition by city
                     order by sum(amount_eur * quantity) desc)      as city_rank
    from orders
    group by city, customer_id
) ranked
where city_rank <= 3
order by city, city_rank;
