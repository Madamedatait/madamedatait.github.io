# 📊 Analyse de Performance Commerciale — SQL

**Stack :** SQL (SQLite) — JOIN, GROUP BY, CTE, Window Functions
**Objectif :** Analyser les performances de vente d'une entreprise à partir de 3 tables relationnelles (employés, ventes, produits) afin d'identifier les meilleurs vendeurs, les tendances mensuelles et la répartition du catalogue produit.

---

## 📋 Contexte

Ce projet s'appuie sur une base de données relationnelle composée de **3 tables liées** :

- **employees** — informations sur les employés (identifiant, nom, date d'embauche, département)
- **sales** — transactions de vente (employé, produit, quantité, date)
- **products** — catalogue produit (nom, catégorie, prix)

L'objectif est de répondre à des questions métier concrètes : qui sont les meilleurs vendeurs ? Quelle est la tendance des ventes mois par mois ? Comment se répartit le catalogue produit par gamme de prix ?

Ce projet illustre la maîtrise de requêtes SQL avancées : jointures multiples, agrégations, fonctions de fenêtrage (window functions) et CTE (Common Table Expressions).

---

## 1. 🏷️ Segmentation du catalogue produit

**Objectif :** classer les produits en deux gammes selon leur prix, pour faciliter l'analyse commerciale.

```sql
SELECT
    product_name,
    price,
    CASE
        WHEN price > 700 THEN 'Premium'
        ELSE 'Standard'
    END AS product_category
FROM products;
```

**Résultat (extrait) :**

| product_name | price | product_category |
|---|---|---|
| Laptop | 1755 | Premium |
| TV | 1623 | Premium |
| Gaming Console | 731 | Premium |
| Recliner Chair | 648 | Standard |
| Watch | 237 | Standard |

➡️ La majorité du catalogue se positionne sur la gamme **Standard** (prix ≤ 700€), avec quelques produits Premium à forte valeur unitaire (Laptop, TV).

---

## 2. 📅 Chiffre d'affaires mensuel par employé

**Objectif :** calculer le total des ventes réalisées par chaque employé, mois par mois, pour suivre la performance dans le temps.

```sql
SELECT
    e.first_name,
    e.last_name,
    strftime('%Y-%m', s.sale_date) AS sale_month,
    SUM(s.product_quantity * p.price) AS total_sales
FROM sales s
JOIN employees e ON s.employee_id = e.employee_id
JOIN products p ON s.product_id = p.product_id
GROUP BY e.employee_id, e.first_name, e.last_name, sale_month
ORDER BY e.employee_id, sale_month;
```

**Résultat (extrait — Alexis Bartlett) :**

| sale_month | total_sales |
|---|---|
| 2024-03 | 146 467 |
| 2024-11 | 57 618 |
| 2024-12 | 76 058 |

➡️ Ce type de requête permet de repérer les pics et creux d'activité par employé, utile pour le pilotage commercial et les primes de performance.

---

## 3. 🏆 Classement des employés (Window Function)

**Objectif :** classer tous les employés selon leur chiffre d'affaires total, du meilleur au moins performant.

```sql
SELECT
    first_name,
    last_name,
    total_sales,
    RANK() OVER (ORDER BY total_sales DESC) AS sales_rank
FROM (
    SELECT
        e.employee_id,
        e.first_name,
        e.last_name,
        SUM(s.product_quantity * p.price) AS total_sales
    FROM employees e
    JOIN sales s ON e.employee_id = s.employee_id
    JOIN products p ON s.product_id = p.product_id
    GROUP BY e.employee_id, e.first_name, e.last_name
) t;
```

**Résultat (Top 5) :**

| Rang | Employé | Total ventes |
|---|---|---|
| 1 | Donald Fisher | 526 403 |
| 2 | Whitney Mason | 475 518 |
| 3 | Jack Cook | 472 665 |
| 4 | Jenna Bass | 460 438 |
| 5 | Jasmin Gonzales | 454 219 |

➡️ La fonction `RANK()` permet d'obtenir un classement précis, y compris en cas d'égalité de chiffre d'affaires entre plusieurs employés.

---

## 4. 🥇 Segmentation des vendeurs (Top Seller vs Regular Seller)

**Objectif :** identifier rapidement les employés performants pour orienter les actions commerciales (formation, primes, reconnaissance).

```sql
SELECT
    e.first_name,
    e.last_name,
    SUM(s.product_quantity * p.price) AS total_sales,
    CASE
        WHEN SUM(s.product_quantity * p.price) > 300000 THEN 'Top Seller'
        ELSE 'Regular Seller'
    END AS sales_classification
FROM employees e
JOIN sales s ON e.employee_id = s.employee_id
JOIN products p ON s.product_id = p.product_id
GROUP BY e.employee_id, e.first_name, e.last_name;
```

➡️ Sur 300 employés analysés, une minorité dépasse le seuil des 300 000€ de ventes cumulées et se distingue comme "Top Seller".

---

## 5. 📈 Cumul progressif des ventes (Running Total)

**Objectif :** suivre l'évolution cumulée des ventes d'un employé au fil du temps — un indicateur clé pour visualiser la progression vers un objectif annuel.

```sql
SELECT
    e.first_name,
    e.last_name,
    s.sale_date,
    s.product_quantity * p.price AS sale_amount,
    SUM(s.product_quantity * p.price)
        OVER (PARTITION BY e.employee_id ORDER BY s.sale_date) AS running_total
FROM sales s
JOIN employees e ON s.employee_id = e.employee_id
JOIN products p ON s.product_id = p.product_id
ORDER BY e.employee_id, s.sale_date;
```

**Résultat (extrait — Alexis Bartlett) :**

| sale_date | sale_amount | running_total |
|---|---|---|
| 2024-03-12 | 86 427 | 86 427 |
| 2024-03-16 | 51 740 | 138 167 |
| 2024-03-25 | 8 300 | 146 467 |
| 2024-11-28 | 57 618 | 246 904 |

➡️ Cette vue cumulative est particulièrement utile pour des tableaux de bord de suivi d'objectifs commerciaux en temps réel.

---

## 6. 🔁 Requête avec CTE — Filtrage des meilleurs vendeurs

**Objectif :** utiliser une CTE (Common Table Expression) pour structurer une requête en deux étapes lisibles : calcul du chiffre d'affaires, puis filtrage.

```sql
WITH employee_sales AS (
    SELECT
        e.employee_id,
        e.first_name,
        e.last_name,
        SUM(s.product_quantity * p.price) AS total_sales
    FROM employees e
    JOIN sales s ON e.employee_id = s.employee_id
    JOIN products p ON s.product_id = p.product_id
    GROUP BY e.employee_id, e.first_name, e.last_name
)
SELECT first_name, last_name, total_sales
FROM employee_sales
ORDER BY total_sales DESC;
```

➡️ L'usage d'une CTE rend la requête plus lisible et facilement réutilisable pour d'autres filtres (ex : ventes > seuil, par période, etc.).

---

## 📝 Conclusions

Ce projet illustre un éventail de compétences SQL essentielles pour l'analyse de données métier :

- **Jointures multiples** entre tables relationnelles pour reconstituer une vue complète des transactions
- **Agrégations (GROUP BY, SUM)** pour calculer des indicateurs de performance par employé et par mois
- **CASE WHEN** pour créer des segmentations métier (gammes de produits, classification des vendeurs)
- **Window functions (RANK, SUM OVER PARTITION BY)** pour des classements et des cumuls progressifs
- **CTE (WITH)** pour structurer des requêtes complexes de façon lisible et maintenable

Ces techniques sont directement applicables à des problématiques réelles de pilotage commercial : identification des top performers, suivi d'objectifs, segmentation produit.

---
