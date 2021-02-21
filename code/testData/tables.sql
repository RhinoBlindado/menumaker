-- DDL

CREATE TABLE ingredient
(
    idIngr VARCHAR2(64) PRIMARY KEY,
    nanemIngr VARCHAR2(32),
    priceIngr FLOAT
);

CREATE TABLE food
(
    idFood VARCHAR2(64) PRIMARY KEY,
    nameFood VARCHAR2(32),
    isUniquePlate BOOLEAN NOT NULL CHECK(isUniquePlate IN (0,1)),
    /*
        timeOfDay has to be read as a binary value. It defines when a food is desired to be eaten. 
        The format is B L D. B is the breakfast bit, L the lunch bit and D the dinner bit.

        Example:
        B L D
        0 0 1 -> This food is only for dinner time
        1 0 1 -> This food can be had as breakfast or dinner.
    */
    timeOfDay INTEGER NOT NULL CHECK(timeOfDay BETWEEN 1 AND 7),
    priceFood FLOAT
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