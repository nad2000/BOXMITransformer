var oArgs = WScript.Arguments;

if (oArgs.length == 0)
{
    WScript.Echo ("Usage : cscript xslt.js xml xsl outputfile");
    WScript.Quit();
}
xmlFile = oArgs(0);
xslFile = oArgs(1);
htmlFile = oArgs(2);

var xsl = new ActiveXObject("MSXML2.DOMDocument.3.0");
var xml = new ActiveXObject("MSXML2.DOMDocument.3.0");

xml.async = false
xml.resolveExternals = true

xsl.async = false
xsl.resolveExternals = true
xsl.setProperty("AllowDocumentFunction", true)
xsl.setProperty("AllowXsltScript", true)
xsl.setProperty("ProhibitDTD", false);


xml.validateOnParse = false;
xml.async = false;
xml.load(xmlFile);

if (xml.parseError.errorCode != 0)
    WScript.Echo ("XML Parse Error : " + xml.parseError.reason);

xsl.async = false;
xsl.load(xslFile);

if (xsl.parseError.errorCode != 0)
    WScript.Echo ("XSL Parse Error : " + xsl.parseError.reason);

try
{
    var result = xml.transformNode(xsl.documentElement)
    var fso = new ActiveXObject("Scripting.FileSystemObject");    
    var a = fso.CreateTextFile(htmlFile, true);
    a.WriteLine(result);
    a.Close();

}
catch(err)
{
    WScript.Echo("Transformation Error : " + err.number + "*" + err.description);
}