# SQL Style Guide

1. Table names are plural
1. Table names are lowercase and underscore word separators
1. Column names are singular
1. Column names are lowercase and underscore word separators
1. Table Alias fully qualified names
1. Analytics table named for intended use
1. SQL statements all upper case
1. Indent all code related to first SQL statements
1. INSERT INTO statements are single line
1. New line after SQL statements, double indention
1. Trailing commas
1. Alternative statements
    * IF ELSE for single alternative
    * CASE WHEN for multiple alternatives
1. Boolean values 1 for True and 0 for False
1. Alias aggregate date with descriptive name
1. All exceptions must have documented reasoning
    * Prioritize readability for naming
    * SQL statement exceptions allowed for performance justification

**Example:**

```SQL
SELECT
        domesticated_pets.date,
        domesticated_pets.cats
    FROM
        domesticated_pets
    LEFT JOIN
        zoo on zoo.cats = domesticated_pets.cats;

INSERT INTO employees VALUES (10000,'first','last',100,10000,1);
```
