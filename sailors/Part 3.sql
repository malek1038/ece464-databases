-- Biweekly payment query
SELECT 
    e.employee_id,
    e.ename,
    SUM(w.hours_worked) AS total_hours,
    SUM(w.hours_worked) * e.hourly_rate AS total_pay
FROM 
    employees e
JOIN 
    work_logs w ON e.employee_id = w.employee_id
WHERE 
    w.work_date BETWEEN ? AND ? -- replace with the desired date range
GROUP BY 
    e.employee_id;

-- Results for '2023-10-01' to '2023-10-14':
-- +-------------+----------+-------------+------------------+
-- | employee_id |     ename      | total_hours | total_pay  |
-- +-------------+----------+-------------+------------------+
-- |      1      |    John Doe    |     16.5    |   330.0    |
-- |      2      |   Jane Smith   |     7.5     |   112.5    |
-- |      3      |   Emily Jones  |      8      |    144     |
-- +-------------+----------+-------------+------------------+

-- Available boats query
SELECT * FROM boats
WHERE bid NOT IN (
    SELECT bid FROM reserves
    WHERE day = 'YYYY-MM-DD' -- replace with the desired date
);

-- Results for '1998-10-10':
-- +------+------------+-------+------+
-- | bid  |   bname    | color |  len |
-- +------+------------+-------+------+
-- | 103  |  Clipper   | green |  40  |
-- | 105  |   Marine   |  red  |  35  |
-- | 106  |   Marine   | green |  35  |
-- | 107  |   Marine   | blue  |  35  |
-- | 110  |  Klapser   |  red  |  30  |
-- | 111  |   Sooney   | green |  28  |
-- | 112  |   Sooney   |  red  |  28  |
-- +------+------------+-------+------+

-- Returns a sailors preference in color and length (based on past history)
-- Used to suggest a boat to a sailor

WITH ColorPreference AS (
  SELECT b.color, COUNT(*) AS color_count
  FROM reserves r
  JOIN boats b ON r.bid = b.bid
  WHERE r.sid = ? -- (sailor ID)
  GROUP BY b.color
  ORDER BY color_count DESC
  LIMIT 1
),
LengthPreference AS (
  SELECT b.length, COUNT(*) AS length_count
  FROM reserves r
  JOIN boats b ON r.bid = b.bid
  WHERE r.sid = ? -- (sailor ID)
  GROUP BY b.length
  ORDER BY length_count DESC
  LIMIT 1
)
SELECT color AS most_common_color, length AS most_common_length
FROM ColorPreference, LengthPreference;

-- Suggest boats based on the sailor's past preferences

SELECT b.*
FROM boats b
WHERE b.bid NOT IN (
    SELECT r.bid
    FROM reserves r
    WHERE r.sid = ? -- Sailor's ID
)
AND (
    b.color = (SELECT most_common_color FROM ColorPreference)
    OR b.length = (SELECT most_common_length FROM LengthPreference)
)
ORDER BY
    (b.color = (SELECT most_common_color FROM ColorPreference)) DESC,
    (b.length = (SELECT most_common_length FROM LengthPreference)) DESC
LIMIT 5;

