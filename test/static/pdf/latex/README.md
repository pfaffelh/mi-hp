#### How to convert a pdf from latex into some high quality jpg:
Important note: In /etc/ImageMagick-7/policy.xml, include
<policy domain="coder" rights="read | write" pattern="PDF" />
just before </policymap> 

Then, e.g., 

convert -density 300 in.pdf -quality 90 out.jpg
