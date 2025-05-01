CREATE TABLE Product (
    product_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255)
);
CREATE TABLE Location (
    location_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255)
);
CREATE TABLE ProductMovement (
    movement_id VARCHAR(255) PRIMARY KEY,
    timestamp DATETIME,
    from_location VARCHAR(255),
    to_location VARCHAR(255),
    product_id VARCHAR(255),
    qty INT,
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);

SELECT p.name AS Product, l.name AS Warehouse,
       COALESCE(SUM(CASE WHEN pm.to_location = l.location_id THEN pm.qty ELSE 0 END), 0) -
       COALESCE(SUM(CASE WHEN pm.from_location = l.location_id THEN pm.qty ELSE 0 END), 0) AS Qty
FROM Location l
CROSS JOIN Product p
LEFT JOIN ProductMovement pm ON pm.to_location = l.location_id OR pm.from_location = l.location_id
GROUP BY p.name, l.name;