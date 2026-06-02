SELECT
    p.name AS "название товара",
    pr.price AS "цену"
FROM products AS p
JOIN prices AS pr ON p.id = pr.product_id;