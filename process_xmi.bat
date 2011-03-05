@SET ECHO OFF
REM Get file name w/o extesion
SET FFN=%1
SET FN=%FFN:~0,-4%

REM Execute trasformations:
REM - Generate an HTML report:
cscript transform.js %1 xmi-html-summary.xslt %FFN:~0,-4%.html
cscript transform.js %1 xmi-html-summary2.xslt %FFN:~0,-4%_2.html

REM - Generat DML for model update
cscript transform.js %1 xmi-sql.xslt create_model.sql

REM Load model data into DB model.sqlite:
sqlite3 model.sqlite < create_model.sql

REM Extract table and column list in CSV format:
sqlite3 -header -csv model.sqlite "SELECT * FROM meta$table;" > %FN%_tables.csv
sqlite3 -header -csv model.sqlite "SELECT c.*, t.schema, t.name AS table_name FROM meta$table AS t JOIN meta$column AS c ON c.table_id = t.id;"  > %FN%_columns.csv


