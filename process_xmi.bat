@SET ECHO OFF
REM Get file name w/o extesion
SET FFN=%1
SET FN=%FFN:~0,-4%

SET OUTPUT_DIR=output
IF NOT EXIST %OUTPUT_DIR% MKDIR %OUTPUT_DIR%

SET DB=%OUTPUT_DIR%\model.sqlite

REM Execute trasformations:
REM - Generate an HTML report:
cscript transform.js %1 xmi-html-summary.xslt %OUTPUT_DIR%\%FFN:~0,-4%.html
cscript transform.js %1 xmi-html-summary2.xslt %OUTPUT_DIR%\%FFN:~0,-4%_2.html

REM - Generat DML for model update
cscript transform.js %1 xmi-sql.xslt %OUTPUT_DIR%\create_model.sql

REM Load model data into DB model.sqlite:
sqlite3 %DB% < %OUTPUT_DIR%\create_model.sql

REM Extract table and column list in CSV format:
sqlite3 -header -csv %DB% "SELECT * FROM meta$table;" > %OUTPUT_DIR%\%FN%_tables.csv
sqlite3 -header -csv %DB% "SELECT c.*, t.schema, t.name AS table_name FROM meta$table AS t JOIN meta$column AS c ON c.table_id = t.id;"  > %OUTPUT_DIR%\%FN%_columns.csv


