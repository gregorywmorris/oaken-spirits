# SQL Style Guide

1. Table names are plural
1. Column names are lowercase and underscore word separators
1. Date/time columns end with _@
1. Table Alias fully qualified names
1. Analytics table named for intended use
1. SQL action all upper case
1. Indent all code related to first SQL action
1. New line after SQL action
1. Single indentation for SQL actions
1. Double indention for all others
1. Trailing commas
1. Alternative action
    * IF ELSE for single alternative
    * CASE WHEN for multiple alternatives
1. Boolean values True and False
1. Alias aggregate date with descriptive name
1. Semicolon at the end of the last line

**Example:**

```SQL
SELECT
        domesticated_pets.date_@,
        domesticated_pets.cats
    FROM
        domesticated_pets
    LEFT JOIN
        zoo on zoo.cats = domesticated_pets.cats;
```
