<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version = "1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
    | X | Sin(X) |
    |---|--------|
    <xsl:for-each select="sin/value">
        |<xsl:value-of select="x_axis"/>|<xsl:value-of select="y_axis"/>|

    </xsl:for-each>
</xsl:template>
</xsl:stylesheet>
