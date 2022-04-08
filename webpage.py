from bs4 import BeautifulSoup

html = """<!DOCTYPE html>
<html lang="en">
<meta charset="UTF-8">
<title>Page Title</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="">
<style>
</style>
<script src=""></script>
<body>

<img src="img_la.jpg" alt="LA" style="width:100%">

<div class="">
 <h1>This is a Heading</h1>
 <p>This is a paragraph.</p>
 <p>This is another paragraph.</p>
</div>

</body>
</html>"""

with open('index.html', 'w') as f:
    f.write(html)

soup = BeautifulSoup(html, "lxml")
# print(soup.prettify())

print(soup.find_all("p")[1])
print(soup.find_all("p")[1].string)
soup.find_all("p")[1].string.replace_with("My name is Alec")
print(soup.find_all("p")[1].string)


print(soup.find_all("img")[0]["src"])

# del soup.find_all("img")[0]["src"]
# print(soup.find_all("img")[0])

# print(soup.find_all("img")[0].attrs)
