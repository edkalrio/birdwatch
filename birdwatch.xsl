<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:atom="http://www.w3.org/2005/Atom">

	<xsl:template match="/">
		<html>
			<head>
				<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
				<meta name="theme-color" content="black"/>
				<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"/>
				<title><xsl:value-of select="/atom:feed/atom:title"/></title>
				<style>
					html {
						font-size: 16px;
						font-family: sans-serif;
					}

					body {
						max-width: 500px;
						margin: auto;
						line-height: 1.5;
					}
						
					img {
						max-width: 100%;
						height: auto;
					}

					h1 {
						margin: 0 0 0.5rem;
						text-align: center;
						font-size: 2.5rem;
						line-height: 1.2;
					}
					
					h3 {
						font-size: 1rem;
						font-weight: normal;
					}

					p, h3 {
						margin: 0 1rem;					
					}
					
					div {
						margin: 0;
						padding: 0.5rem 0;			
						font-size: 1rem;
						border-bottom: 1px solid gainsboro;
					}
					
					a {
						text-decoration: none;
						color: royalblue;
					}

					p a:first-child, b a, h1 a {
						color: black;
					}

					date, span a {
						color: gray;
					}

					date:before {
						content: " · "
					}

					b:after {
						content: " "
					}
				</style>
			</head>
			<body>
				<xsl:apply-templates select="/atom:feed"/>
			</body>
		</html>
	</xsl:template>

	<xsl:template match="/atom:feed">
		<h1>
			<xsl:element name="a">
				<xsl:attribute name="href">
					<xsl:value-of select="atom:link/@href"/>
				</xsl:attribute>
				<xsl:value-of select="atom:author/atom:name"/>
			</xsl:element>
		</h1>
	
		<xsl:apply-templates select="atom:entry"/>
	</xsl:template>

	<xsl:template match="atom:entry">
		<xsl:for-each select=".">
			<div>
				<h3>
					<b>
						<xsl:element name="a">
							<xsl:attribute name="href">
								<xsl:value-of select="atom:author/atom:uri"/>
							</xsl:attribute>
							<!-- <xsl:value-of select="atom:title" disable-output-escaping="yes"/> -->
							<xsl:value-of select="atom:author/atom:name"/>
						</xsl:element>
					</b>

					<span>
						<xsl:element name="a">
							<xsl:attribute name="href">
								<xsl:value-of select="atom:author/atom:uri"/>
							</xsl:attribute>
							<!-- <xsl:value-of select="atom:author/atom:name"/> -->
							<xsl:value-of select="atom:title" disable-output-escaping="yes"/>
						</xsl:element>
					</span>
					
					<date>
						<xsl:value-of select="atom:updated"/>
					</date>
				</h3>

				<p>
					<xsl:element name="a">
						<xsl:attribute name="href">
							<xsl:value-of select="atom:link/@href"/>
						</xsl:attribute>
						<xsl:value-of select="atom:content" disable-output-escaping="yes"/>
					</xsl:element>
				</p>
			</div>
		</xsl:for-each>
	</xsl:template>

</xsl:stylesheet>