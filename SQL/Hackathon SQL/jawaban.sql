DROP TEMPORARY TABLE IF EXISTS temp_order_level2;
DROP TEMPORARY TABLE IF EXISTS temp_stats;
DROP TEMPORARY TABLE IF EXISTS temp_outliers_detail;
DROP TEMPORARY TABLE IF EXISTS temp_outliers_detail_2;
DROP TEMPORARY TABLE IF EXISTS temp_final_output;

CREATE TEMPORARY TABLE temp_order_level2 AS
SELECT
    o.no_urut,
    o.node_id,
    o.nilai_order,
    CASE
        WHEN n0.parent_id = 'ROOT' THEN n0.id
        WHEN n1.parent_id = 'ROOT' THEN n1.id
        WHEN n2.parent_id = 'ROOT' THEN n2.id
        WHEN n3.parent_id = 'ROOT' THEN n3.id
        WHEN n4.parent_id = 'ROOT' THEN n4.id
        WHEN n5.parent_id = 'ROOT' THEN n5.id
        ELSE NULL
    END AS level2_mgr
FROM orders o
LEFT JOIN nodes n0 ON n0.id = o.node_id
LEFT JOIN nodes n1 ON n1.id = n0.parent_id
LEFT JOIN nodes n2 ON n2.id = n1.parent_id
LEFT JOIN nodes n3 ON n3.id = n2.parent_id
LEFT JOIN nodes n4 ON n4.id = n3.parent_id
LEFT JOIN nodes n5 ON n5.id = n4.parent_id;

CREATE TEMPORARY TABLE temp_stats AS
SELECT
    level2_mgr,
    AVG(nilai_order)  AS average,
    STDDEV_POP(nilai_order)  AS stdev
FROM temp_order_level2
WHERE level2_mgr IS NOT NULL
GROUP BY level2_mgr;

CREATE TEMPORARY TABLE temp_outliers_detail AS
SELECT
    t.level2_mgr,
    t.node_id AS sales_id,
    t.nilai_order,
    s.average,
    s.stdev,
    (t.nilai_order - s.average) AS jarak_average,
    (t.nilai_order - s.average) / NULLIF(s.stdev, 0) AS z_score
FROM temp_order_level2 t
JOIN temp_stats s ON s.level2_mgr = t.level2_mgr
WHERE s.stdev > 0
  AND ABS((t.nilai_order - s.average) / s.stdev) > 3;

CREATE TEMPORARY TABLE temp_outliers_detail_2 AS 
SELECT * FROM temp_outliers_detail;

    SELECT 
        level2_mgr AS level2,
        COUNT(*) AS jumlah_anomali,
        NULL AS id,
        NULL AS nilai_order,
        NULL AS average,
        NULL AS stdev,
        NULL AS jarak_average,
        NULL AS z_score
    FROM temp_outliers_detail
    GROUP BY level2_mgr
UNION ALL
    SELECT 
        level2_mgr AS level2,
        NULL AS jumlah_anomali,
        sales_id AS id,
        nilai_order,
        average,
        stdev,
        jarak_average,
        z_score
    FROM temp_outliers_detail_2