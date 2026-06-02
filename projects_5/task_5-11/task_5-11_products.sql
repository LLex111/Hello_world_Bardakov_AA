SELECT *
FROM products
WHERE category = 'электроника';

SELECT *
FROM products
WHERE category = 'одежда'
  AND name LIKE '%Ж%';

SELECT *
FROM products
WHERE category IN ('продукты', 'книги');

SELECT *
FROM products
WHERE category <> 'бытовая техника';

SELECT *
FROM products
WHERE category IN ('электроника', 'одежда', 'книги');

SELECT *
FROM products
WHERE (category = 'электроника' AND name LIKE '%Samsung%')
   OR category = 'бытовая техника';

SELECT *
FROM products
WHERE (
        category IN ('электроника', 'одежда', 'бытовая техника')
        AND id BETWEEN 1 AND 15
        AND name NOT LIKE '%Samsung%'
      )
   OR category = 'книги';