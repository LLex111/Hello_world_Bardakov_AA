SELECT *
FROM prices
WHERE price BETWEEN 100 AND 150;

SELECT *
FROM prices
WHERE price BETWEEN 50 AND 60
  AND product_id <= 5;

SELECT *
FROM prices
WHERE price < 100
   OR price BETWEEN 150 AND 200;