#-------------------------------------------------------------------------------
# Name:        process_xmi.py
# Purpose:	   Data collecttion from SAP BusinessObject DATA SERVICES XI
#			   DI CWM 1.0 XML/XMI 1.1 Metadata export file
#			   Sample that demonstrats Expat and sqlite3 application for real life
#              situation.
#
# Author:      Radomirs Cirskis
#
# Created:     26/02/2011
# Copyright:   (c) Radomirs Cirskis 2011
# Licence:     CC BY-SA 3.0 (http://creativecommons.org/licenses/by-sa/3.0/)
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from xml.parsers import expat
import sqlite3

# Module Constants
# Name spaces:
nsCWM = 'org.omg.CWM1.0/ObjectModel'
nsUML = 'org.omg.CWM1.0/Core'
nsCWMRDB = 'org.omg.CWM1.0/Relational'

# namespace and tag name separator:
xmlnsSeparator = '#'

# element/tag full names:
tagTable = nsCWMRDB+xmlnsSeparator+'Table'
tagSQLSimpleType = nsCWMRDB+xmlnsSeparator+'SQLSimpleType'
tagColumn = nsCWMRDB+xmlnsSeparator+'Column'
tagDescription = nsCWM+xmlnsSeparator+'Description'
tagCatalog = nsCWMRDB+xmlnsSeparator+'Catalog'
tagPrimaryKey = nsCWMRDB+xmlnsSeparator+'PrimaryKey'
tagStructuralFeature = nsCWMRDB+xmlnsSeparator+'StructuralFeature'

class XMIParser:
    def __init__(self):
        self._parser = expat.ParserCreate(
            namespace_separator = xmlnsSeparator )
        self._parser.StartElementHandler = self.start
        self._parser.EndElementHandler = self.end
        self._parser.CharacterDataHandler = self.data
        self._dataTypes = {}
        self._catalog = None
        self._initDb()
        self._mode = None

    def _initDb(self):
        self._cn = sqlite3.connect('output\\model.sqlite')
        self._cn.executescript("""
DROP TABLE IF EXISTS tmp$table;
CREATE TABLE IF NOT EXISTS tmp$table (
    xmi_id      TEXT    NOT NULL,
    schema      TEXT    NOT NULL,
    name        TEXT    NOT NULL
);

DROP TABLE IF EXISTS tmp$column;
CREATE TABLE IF NOT EXISTS tmp$column (
    xmi_id      TEXT    NOT NULL,
    table_xmi_id    TEXT NOT NULL,
    name        TEXT    NOT NULL,
    type        TEXT    NOT NULL,
    is_nullable BOOLEAN,
    is_pk       BOOLEAN,
    length      INTEGER,
    precision   INTEGER,
    scale       INTEGER
 );

DROP TABLE IF EXISTS tmp$desc;
CREATE TABLE IF NOT EXISTS tmp$desc (
    xmi_id      TEXT    NOT NULL,
    -- Model Element:
    el_xmi_id   TEXT    NOT NULL,
    body TEXT);
""")

    def feed(self, data):
        self._parser.Parse(data, 0)

    def feedFile(self, fileName):
        self._file= open( fileName, mode='rb')
        self._parser.ParseFile( self._file)
        self._file.close()

    def close(self):
        # self._parser.Parse("", 1) # end of data
        del self._parser # get rid of circular references
        if self._cn != None:
            self._cn.commit()
            self._cn.close()

    def start(self, tag, attrs):
        # last ID attribute value
        if 'xmi.id' in attrs: id = self._id = attrs['xmi.id']
        # last name attribute value
        if 'name' in attrs: name = self._name = attrs['name']
        if tag == tagTable:
            self._columns = {}
            self._tableId = self._id
            self._tableName = self._name
            self._tableIsSystem = ( attrs['isSystem'] == "true" )
            self._tableIsTemporary = ( attrs['isTemporary'] == "false" )
            self._tableVisibility = attrs['visibility']

        elif tag == tagColumn:
            typeId = attrs['type']
            tableId = attrs['owner']
            dataType = self._dataTypes[ typeId ] if typeId in self._dataTypes else typeId
            isNullable = ( attrs['isNullable']== 'columnNoNulls' )
            length = attrs['length'] if 'length' in attrs else None
            precision = attrs['precision'] if 'precision' in attrs else None
            scale = attrs['scale'] if 'scale' in attrs else None
            self._cn.execute("""INSERT INTO tmp$column
            ( xmi_id, table_xmi_id, name, type, is_nullable, length, precision, scale)
            VALUES (?,?,?,?,?,?,?,?)""",
            ( id, tableId, name, dataType, isNullable, length, precision, scale,) )

        elif tag == tagDescription:
            elementId = attrs['modelElement']
            body = attrs['body']
            self._cn.execute(
              "INSERT INTO tmp$desc (xmi_id,el_xmi_id,body) VALUES (?,?,?)",
              ( id, elementId, body) )

        elif tag == tagPrimaryKey or \
                (self._mode == 'pk' and tag == tagStructuralFeature):
            if tag == tagPrimaryKey: self._mode = 'pk'
            if 'xmi.idref' in attrs or 'feature' in attrs:
                colId = attrs['feature'] if 'feature' in attrs else attrs['xmi.idref']
                self._cn.execute( "UPDATE tmp$column SET is_pk=1 WHERE xmi_id=?", (colId,) )

        elif tag == tagSQLSimpleType:
            self._dataTypes[ self._id ] = attrs['name']
            pass

        elif tag == tagCatalog:
            self._catalog = attrs['name']
            pass

    def end(self, tag):
        if tag == tagTable:
            self._cn.execute(
                "INSERT INTO tmp$table (xmi_id,schema,name) VALUES (?,?,?)",
                ( self._tableId, self._catalog, self._tableName) )
        elif tag == tagPrimaryKey:
            self._mode = None
        pass

    def data(self, data):
		# Not used
        pass

def main():
    p = XMIParser()
    p.feedFile( "sample_xmi.xml")
    p.close()
    pass

if __name__ == '__main__':
    main()