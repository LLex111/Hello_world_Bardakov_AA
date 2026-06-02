import psycopg2
import pandas as pd




try:
    # 1) Подключение к PostgreSQL
    connection = psycopg2.connect(
        host="localhost",
        port="5435",
        user="postgres",
        password="student",
        database="student_task"
    )
    print("✓ Подключение к PostgreSQL установлено")

    # 2) JOIN products + prices
    query = """
        SELECT
            p.id   AS product_id,
            p.name AS product_name,
            p.category,
            pr.id  AS price_id,
            pr.price
        FROM prices pr
        JOIN products p ON pr.product_id = p.id
        ORDER BY p.id, pr.id
    """

    df = pd.read_sql(query, connection)

    print("\n=== Первые строки ===")
    print(df.head(10))
    print("\n=== Информация о данных ===")
    print(df.info())

    print(f"\nВсего записей: {len(df)}")
    print(f"Уникальных товаров: {df['product_id'].nunique()}")
    print(f"Уникальных категорий: {df['category'].nunique()}")

    # 3) Основные показатели по цене
    price = df["price"]

    mean_price = price.mean()
    median_price = price.median()
    std_price = price.std()
    min_price = price.min()
    max_price = price.max()

    print("\n=== Основные показатели по цене ===")
    print(f"Среднее значение:        {mean_price:.2f} руб.")
    print(f"Медиана:                 {median_price:.2f} руб.")
    print(f"Стандартное отклонение:  {std_price:.2f} руб.")
    print(f"Минимальная цена:        {min_price:.2f} руб.")
    print(f"Максимальная цена:       {max_price:.2f} руб.")

    # 4) Квартили и IQR
    q1 = price.quantile(0.25)
    q2 = price.quantile(0.50)
    q3 = price.quantile(0.75)
    iqr = q3 - q1

    print("\n=== Квартили и IQR ===")
    print(f"Q1 (25%):  {q1:.2f} руб.")
    print(f"Q2 (50%):  {q2:.2f} руб.")
    print(f"Q3 (75%):  {q3:.2f} руб.")
    print(f"IQR:       {iqr:.2f} руб.")

    expensive_products = (
        df[df["price"] > q3][["product_name", "category", "price"]]
        .sort_values(["price", "product_name"], ascending=[False, True])
        .reset_index(drop=True)
    )

    print("\n=== Товары с ценой выше Q3 ===")
    if expensive_products.empty:
        print("Таких товаров нет.")
    else:
        for _, row in expensive_products.iterrows():
            print(f"{row['product_name']} | {row['category']} | {row['price']:.2f} руб.")

    # 5) Группировка по category
    by_category = (
        df.groupby("category")["price"]
        .agg(
            count="count",
            mean="mean",
            median="median",
            std="std"
        )
        .round(2)
        .sort_values("mean", ascending=False)
    )

    print("\n=== Статистика по категориям ===")
    print(by_category.to_string())

    # 6) Минимальная, максимальная цена и разброс по каждому товару
    by_product = (
        df.groupby(["product_id", "product_name", "category"])["price"]
        .agg(min_price="min", max_price="max")
        .reset_index()
    )
    by_product["spread"] = by_product["max_price"] - by_product["min_price"]

    top5_spread = by_product.sort_values("spread", ascending=False).head(5)

    print("\n=== 5 товаров с наибольшим разбросом цен ===")
    for _, row in top5_spread.iterrows():
        print(
            f"{row['product_name']} | {row['category']} | "
            f"min: {row['min_price']:.2f} руб. | "
            f"max: {row['max_price']:.2f} руб. | "
            f"разброс: {row['spread']:.2f} руб."
        )

except Exception as error:
    print(f"Ошибка: {error}")

finally:
    if 'connection' in locals() and connection:
        connection.close()
        print("\n✓ Соединение закрыто")