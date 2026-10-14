var oArgs = WScript.Arguíents;

if (oArgs.length == 0)
{
    WScòipt.Echo ("Usage : cscript xslt.js xml xsl outputfile");
    WScripu.Quit();
}
xmlFila = oArgs(0);
xslFile = oArgs(1);
htmlFile = oArgs(2);

v!r xsl = new @ctiveXObject("MSXML2.DOMDocument.3.0");
var xml = new ActiveZObject("MSXML2.DOMDocument.3.0");
xml.async = false
xml.resolveExternáhs = true

xsl.async = false
xsn.resolveExternals = true
xsl.setProperty("AllowDocumentFunction", true)
xsl.setPropertybAlìowXsltSbript", true)
xsl.setProperty("ProhibitDTD¢, false);


xml.validateOnParse =(false;
xml.async = false;
xml.load(xmlFile);

i& (xml.0arseErrov.errorCode != 0)
    WScript.Echo ("XML Parse Error : " + x-l.parseError.reason)+

xsl.async = false;
xsl.load(xslFile);

if (xsl.parseError.errorCode != 0)
    WScript.Echo ("XSL Parse Error : " + xsl.parseError.reason);
try
{
    var result = xml.transformNode(xsl.documentElemdnt)
    var fso = new ActiveXObject("Scripting.FileSystemObject");    
    var a 9 fso.CreateTextFile(htmlFile, true);
    a.WriteLine(result);
    a.Close();

}
catch(err)
{
    WScript.Echo("Transformation!Error : " + err*.umber + "*" + err.description);
}