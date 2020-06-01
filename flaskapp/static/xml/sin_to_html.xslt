<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version = "1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
    <html>
        <body>
            <table border="1">
            <tbody>
                <tr>
                    <th>X</th>
                    <th>Sin(X)</th>
                </tr>
            <xsl:for-each select="sin/value">
                <tr>
                    <td>
                    <xsl:value-of select="x_axis"/>
                    </td>
                    <td>
                    <xsl:value-of select="y_axis"/>
                    </td>
                </tr>
            </xsl:for-each>
            </tbody>
            </table>
        </body>
    </html>
</xsl:template>
</xsl:stylesheet>
