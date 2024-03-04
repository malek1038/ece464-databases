// Prompt 1:

SELECT b.bid, b.bname, COUNT(r.sid) AS reservation_count
FROM boats b
JOIN reserves r ON b.bid = r.bid
GROUP BY b.bid, b.bname
HAVING COUNT(r.sid) > 0;

// Response:
// +------+------------+-------------------+
// | bid  |   bname    | reservation_count |
// +------+------------+-------------------+
// |  101 | Interlake  |         2         |
// |  102 | Interlake  |         3         |
// |  103 |  Clipper   |         3         |
// |  104 |  Clipper   |         5         |
// |  105 |  Marine    |         3         |
// |  106 |  Marine    |         3         |
// |  107 |  Marine    |         1         |  
// |  108 | Driftwood  |         1         |
// |  109 | Driftwood  |         4         |
// |  110 |  Klapser   |         3         |
// |  111 |  Sooney    |         1         |
// |  112 |  Sooney    |         1         |
// +------+------------+-------------------+

// Prompt 2:

SELECT s.sid, s.sname
FROM sailors s
WHERE NOT EXISTS (
    SELECT b.bid
    FROM boats b
    WHERE b.color = 'red'
    AND NOT EXISTS (
        SELECT r.bid
        FROM reserves r
        WHERE r.bid = b.bid
        AND r.sid = s.sid
    )
);

// Response:
// No response (no sailors meet the criteria)

// Prompt 3:

SELECT DISTINCT s.sid, s.sname
FROM sailors s
JOIN reserves r ON s.sid = r.sid
JOIN boats b ON r.bid = b.bid
WHERE b.color = 'red'
AND NOT EXISTS (
    SELECT 1
    FROM reserves r2
    JOIN boats b2 ON r2.bid = b2.bid
    WHERE b2.color <> 'red'
    AND r2.sid = s.sid
);

// Response:
// +------+----------+
// | sid  |   sname  |
// +------+----------+
// |  23  |  emilio  |
// |  24  | scruntus |
// |  35  |  figaro  |
// |  62  |  shaun   |
// |  61  |  ossola  |
// +------+----------+

// Prompt 4:

SELECT b.bid, b.bname, COUNT(*) AS reservation_count
FROM boats b
JOIN reserves r ON b.bid = r.bid
GROUP BY b.bid, b.bname
ORDER BY reservation_count DESC
LIMIT 1;

// Response:

// +------+-----------+-------------------+
// | bid  |   bname   | reservation_count |
// +------+-----------+-------------------+
// |  104 |  Clipper  |         5         |
// +------+-----------+-------------------+


// Prompt 5:

SELECT s.sid, s.sname
FROM sailors s
WHERE NOT EXISTS (
    SELECT 1
    FROM reserves r
    JOIN boats b ON r.bid = b.bid
    WHERE b.color = 'red'
    AND r.sid = s.sid
);

// Response:
// +------+----------+
// | sid  |  sname   |
// +------+----------+
// |  29  |  brutus  |
// |  32  |   andy   | 
// |  58  |  rusty   |
// |  60  |    jit   |
// |  71  |  zorba   |
// |  74  | horatio  |
// |  85  |    art   |
// |  90  |    vin   |
// |  95  |    bob   |
// +------+----------+

// Prompt 6:

SELECT AVG(age) AS average_age
FROM sailors
WHERE rating = 10;

// Response:
// +--------------+
// | average_age  |
// +--------------+
// |     35.00    |
// +--------------+

// Prompt 7:

WITH RankedSailors AS (
  SELECT s.sid, s.sname, s.rating, s.age,
         ROW_NUMBER() OVER (PARTITION BY s.rating ORDER BY s.age ASC) AS Rank
  FROM sailors s
)
SELECT sid, sname, rating, age
FROM RankedSailors
WHERE Rank = 1;

// Response:

// +------+----------+--------+------+
// | sid  |  sname   | rating | age  |
// +------+----------+--------+------+
// |  24  | scruntus |   1    | 33.0 |
// |  85  |   art    |   3    | 25.0 |
// |  61  |  ossola  |   7    | 16.0 |
// |  32  |   andy   |   8    | 25.0 |
// |  74  | horatio  |   9    | 25.0 |
// |  58  |   rusty  |   10   | 35.0 |
// +------+----------+--------+------+

// Prompt 8:

SELECT b.bid, b.bname, s.sid, s.sname, COUNT(*) as reservation_count
FROM reserves r
JOIN sailors s ON r.sid = s.sid
JOIN boats b ON r.bid = b.bid
GROUP BY b.bid, b.bname, s.sid, s.sname
HAVING COUNT(*) = (
  SELECT MAX(reservation_count) FROM (
    SELECT COUNT(*) as reservation_count
    FROM reserves r2
    WHERE r2.bid = b.bid
    GROUP BY r2.sid
  ) temp
)
ORDER BY b.bid, reservation_count DESC;

// Response:

// +------+-----------+------+----------+-------------------+
// | bid  |   bname   | sid  |  sname   | reservation_count |
// +------+-----------+------+----------+-------------------+
// | 101  | Interlake |  22  | dusting  |         1         |
// | 101  | Interlake |  64  | horatio  |         1         |
// | 102  | Interlake |  22  | dusting  |         1         |
// | 102  | Interlake |  31  |  lubber  |         1         |
// | 102  | Interlake |  64  | horatio  |         1         |
// | 103  |  Clipper  |  22  | dusting  |         1         |
// | 103  |  Clipper  |  31  |  lubber  |         1         |
// | 103  |  Clipper  |  74  | horatio  |         1         |
// | 104  |  Clipper  |  22  | dusting  |         1         |
// | 104  |  Clipper  |  23  |  emilio  |         1         |
// | 104  |  Clipper  |  24  | scruntus |         1         |
// | 104  |  Clipper  |  31  |  lubber  |         1         |
// | 104  |  Clipper  |  35  |  figaro  |         1         |
// | 105  |  Marine   |  23  |  emilio  |         1         |
// | 105  |  Marine   |  35  |  figaro  |         1         |
// | 105  |  Marine   |  59  |   stum   |         1         |
// | 106  |  Marine   |  60  |   jit    |         2         |
// | 107  |  Marine   |  88  |   dan    |         1         |
// | 108  | Driftwood |  89  |   dye    |         1         |
// | 109  | Driftwood |  59  |   stum   |         1         |
// | 109  | Driftwood |  60  |   jit    |         1         |
// | 109  | Driftwood |  89  |   dye    |         1         |
// | 109  | Driftwood |  90  |   vin    |         1         |
// | 110  |  Klapser  |  88  |   dan    |         2         |
// | 111  |  Sooney   |  88  |   dan    |         1         |
// | 112  |  Sooney   |  61  |  ossola  |         1         |
// +------+-----------+------+----------+-------------------+