-- Initialize the database.
-- Drop any existing data and create empty tables.
--DROP TABLE IF EXISTS users;
--DROP TABLE IF EXISTS posts;


-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- Table user
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CREATE TABLE users IF NOT EXISTS(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);


-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- Table user
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CREATE TABLE actions IF NOT EXISTS(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    volume REAL DEFAULT 0.00,
    FOREIGN KEY (sound_id) REFERENCES sounds(id),
    light_control BOOLEAN DEFAULT TRUE,
    light_command BOOLEAN DEFAULT TRUE -- True == on
);

--DELIMITER $$
--CREATE TRIGGER actions_volume_range
--    AFTER INSERT ON actions
--    FOR EACH ROW BEGIN
--    INSERT INTO tableB
--    SET sku_copy = OLD.sku,
--         order_id = OLD.order_id,
--        order = OLD.order;
--END $$
--DELIMITER ;


-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- Table user
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CREATE TABLE alarms IF NOT EXISTS(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title LONGTEXT NOT NULL,
    repeats BOOLEAN NOT NULL,
    FOREIGN KEY (action_id) REFERENCES actions(id)
);
