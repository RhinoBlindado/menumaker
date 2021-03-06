-- DDL

CREATE TABLE ingredient
(
    idIngr VARCHAR2(64) PRIMARY KEY,
    nanemIngr VARCHAR2(32),
    priceIngr FLOAT
);

CREATE TABLE food
(
    idFood      VARCHAR2(64) PRIMARY KEY,
    nameFood    VARCHAR2(32),
    
    isUniquePlate BOOLEAN NOT NULL CHECK (isUniquePlate IN (0,1)),

    breakfast   BOOLEAN CHECK (breakfast IN (0,1)),
    lunch       BOOLEAN CHECK (lunch IN (0,1)),
    dinner      BOOLEAN CHECK (dinner IN (0,1)),

    priceFood   FLOAT
);

CREATE TABLE twoTimes
(
    idTwoTimes VARCHAR2(64) PRIMARY KEY,
    nameTwoTimes VARCHAR2(32)
);

CREATE TABLE madeUp
(
    idFood VARCHAR2(64) REFERENCES food(idFood),
    idIngr VARCHAR2(64) REFERENCES ingredient(idIngr),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit VARCHAR2(10),
    PRIMARY KEY(idFood, idIngr)
);

CREATE TABLE composite
(
    idTwoTimes VARCHAR2(64) REFERENCES twoTimes(idTwoTimes),
    idFood VARCHAR2(64) REFERENCES food(idFood),
    PRIMARY KEY(idTwoTimes, idFood)
);