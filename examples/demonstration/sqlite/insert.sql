DELETE FROM B;

DELETE FROM C;

INSERT INTO B (c, d) VALUES (:id, :c); INSERT INTO C (e, f) VALUES (:id, :d);