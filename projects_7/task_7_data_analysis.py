import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch

# -----------------------------------------------------------------------------
# БЛОК 1: ПОДКЛЮЧЕНИЕ И ИЗВЛЕЧЕНИЕ ДАННЫХ
# -----------------------------------------------------------------------------

try:
    connection = psycopg2.connect(
        host="localhost",
        port="5435",
        user="postgres",
        password="student",
        database="student_task"
    )
    print("✓ Подключение установлено")

    # Средняя цена по категориям
    df_category_prices = pd.read_sql("""
        SELECT
            p.category AS category,
            ROUND(AVG(pr.price)::numeric, 2) AS avg_price,
            COUNT(pr.id) AS price_records
        FROM products p
        JOIN prices pr ON p.id = pr.product_id
        GROUP BY p.category
        ORDER BY avg_price DESC
    """, connection)

    # Все цены для распределения
    df_all_prices = pd.read_sql("""
        SELECT price
        FROM prices
        WHERE price IS NOT NULL
    """, connection)

    # Аномалии:
    # 1) у товара не 2 цены
    df_bad_price_count = pd.read_sql("""
        SELECT
            p.id,
            p.name,
            p.category,
            COUNT(pr.id) AS price_count
        FROM products p
        LEFT JOIN prices pr ON p.id = pr.product_id
        GROUP BY p.id, p.name, p.category
        HAVING COUNT(pr.id) <> 2
        ORDER BY price_count, p.name
    """, connection)

    # 2) у товара не 2 поставщика
    df_bad_supplier_count = pd.read_sql("""
        SELECT
            p.id,
            p.name,
            p.category,
            COUNT(s.id) AS supplier_count
        FROM products p
        LEFT JOIN suppliers s ON p.id = s.product_id
        GROUP BY p.id, p.name, p.category
        HAVING COUNT(s.id) <> 2
        ORDER BY supplier_count, p.name
    """, connection)

    # 3) некорректные цены
    df_invalid_prices = pd.read_sql("""
        SELECT id, product_id, price
        FROM prices
        WHERE price <= 0
    """, connection)

    # 4) цены без товара
    df_orphan_prices = pd.read_sql("""
        SELECT pr.id, pr.product_id, pr.price
        FROM prices pr
        LEFT JOIN products p ON pr.product_id = p.id
        WHERE p.id IS NULL
    """, connection)

    # 5) поставщики без товара
    df_orphan_suppliers = pd.read_sql("""
        SELECT s.id, s.product_id, s.name
        FROM suppliers s
        LEFT JOIN products p ON s.product_id = p.id
        WHERE p.id IS NULL
    """, connection)

    print(f"Категорий в выборке:           {len(df_category_prices)}")
    print(f"Всего цен в таблице prices:    {len(df_all_prices)}")
    print(f"Товаров с неверным числом цен:  {len(df_bad_price_count)}")
    print(f"Товаров с неверным числом поставщиков: {len(df_bad_supplier_count)}")
    print(f"Некорректных цен (<= 0):       {len(df_invalid_prices)}")
    print(f"Цен без товара:                {len(df_orphan_prices)}")
    print(f"Поставщиков без товара:        {len(df_orphan_suppliers)}")

except Exception as error:
    print(f"Ошибка подключения: {error}")
    raise SystemExit

finally:
    connection.close()
    print("✓ Соединение закрыто\n")

# -----------------------------------------------------------------------------
# БЛОК 2: ПОДГОТОВКА ДАННЫХ
# -----------------------------------------------------------------------------

overall_avg_price = df_all_prices["price"].mean()
overall_median_price = df_all_prices["price"].median()
overall_std_price = df_all_prices["price"].std()

bar_colors = [
    "#d9534f" if price < overall_avg_price else "#4a90d9"
    for price in df_category_prices["avg_price"]
]

# -----------------------------------------------------------------------------
# БЛОК 3: ПОСТРОЕНИЕ ГРАФИКОВ
# -----------------------------------------------------------------------------

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--",
    "figure.dpi": 130,
})

fig = plt.figure(figsize=(15, 8))
fig.suptitle("Анализ товаров и цен", fontsize=15, fontweight="bold", y=1.02)

gs = gridspec.GridSpec(
    2, 1, figure=fig,
    height_ratios=[1, 1],
    hspace=0.35
)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[1, 0])

# ── ГРАФИК 1: Средняя цена по категориям ─────────────────────────────────────

bars1 = ax1.barh(
    df_category_prices["category"],
    df_category_prices["avg_price"],
    color=bar_colors,
    edgecolor="white",
    height=0.6
)

for bar, val in zip(bars1, df_category_prices["avg_price"]):
    ax1.text(
        bar.get_width() + 0.02,
        bar.get_y() + bar.get_height() / 2,
        f"{val:.2f}",
        va="center",
        fontsize=9
    )

ax1.axvline(
    overall_avg_price,
    color="darkorange",
    linestyle="--",
    linewidth=1.3,
    label=f"Средняя цена: {overall_avg_price:.2f}"
)

ax1.set_xlabel("Средняя цена")
ax1.set_title("Средняя цена по категориям", fontweight="bold", pad=8)

legend_patches = [
    Patch(facecolor="#4a90d9", label="Не ниже среднего"),
    Patch(facecolor="#d9534f", label="Ниже среднего")
]
ax1.legend(handles=legend_patches, fontsize=8, loc="lower right")

# ── ГРАФИК 2: Распределение цен ──────────────────────────────────────────────
# Здесь нужен histogram, а не столбцы по каждому уникальному значению цены.

n, bins, patches = ax2.hist(
    df_all_prices["price"],
    bins=10,
    color="#f0ad4e",
    edgecolor="white"
)

ax2.axvline(
    overall_avg_price,
    color="royalblue",
    linestyle="--",
    linewidth=1.5,
    label=f"Среднее: {overall_avg_price:.2f}"
)

ax2.axvline(
    overall_median_price,
    color="crimson",
    linestyle="--",
    linewidth=1.5,
    label=f"Медиана: {overall_median_price:.2f}"
)

# Подписи над столбцами гистограммы
for count, patch in zip(n, patches):
    if count > 0:
        ax2.text(
            patch.get_x() + patch.get_width() / 2,
            patch.get_height() + max(n) * 0.02,
            str(int(count)),
            ha="center",
            va="bottom",
            fontsize=8
        )

stats_text = (
    f"Всего цен: {len(df_all_prices)}\n"
    f"Среднее: {overall_avg_price:.2f}\n"
    f"Медиана: {overall_median_price:.2f}\n"
    f"Ст. откл.: {overall_std_price:.2f}"
)

ax2.text(
    0.97, 0.95, stats_text,
    transform=ax2.transAxes,
    va="top", ha="right", fontsize=8,
    bbox={
        "boxstyle": "round,pad=0.4",
        "facecolor": "lightyellow",
        "edgecolor": "lightgray",
        "alpha": 0.85
    }
)

ax2.set_xlabel("Цена")
ax2.set_ylabel("Количество записей")
ax2.set_title("Распределение цен", fontweight="bold", pad=8)
ax2.legend(fontsize=8)

# -----------------------------------------------------------------------------
# БЛОК 4: АНОМАЛИИ
# -----------------------------------------------------------------------------

if (
    len(df_bad_price_count) == 0 and
    len(df_bad_supplier_count) == 0 and
    len(df_invalid_prices) == 0 and
    len(df_orphan_prices) == 0 and
    len(df_orphan_suppliers) == 0
):
    fig.text(
        0.5, -0.03,
        "Аномалии не обнаружены: у всех товаров по 2 цены и 2 поставщика, некорректных и осиротевших записей нет.",
        ha="center", fontsize=9, color="#1a7f37",
        bbox={
            "boxstyle": "round,pad=0.4",
            "facecolor": "#f0fff4",
            "edgecolor": "#7bc96f"
        }
    )
else:
    anomaly_text = (
        f"Аномалии: товаров с неверным числом цен — {len(df_bad_price_count)}; "
        f"товаров с неверным числом поставщиков — {len(df_bad_supplier_count)}; "
        f"цены <= 0 — {len(df_invalid_prices)}; "
        f"цен без товара — {len(df_orphan_prices)}; "
        f"поставщиков без товара — {len(df_orphan_suppliers)}."
    )
    fig.text(
        0.5, -0.03,
        anomaly_text,
        ha="center", fontsize=9, color="#8b0000",
        bbox={
            "boxstyle": "round,pad=0.4",
            "facecolor": "#fff3f3",
            "edgecolor": "#d9534f"
        }
    )

# -----------------------------------------------------------------------------
# БЛОК 5: СОХРАНЕНИЕ
# -----------------------------------------------------------------------------

OUTPUT_FILE = "products_analysis.png"
plt.savefig(OUTPUT_FILE, bbox_inches="tight", dpi=150)
print(f"✓ График сохранён: {OUTPUT_FILE}")

plt.show()