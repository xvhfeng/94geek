---
layout: default
title: "分类：Categories"
---

    <script src="js/Jquery.Queryjs">
    </script>
<ul class="list-unstyled">
var dataStr = '{ {% for cat in site.categories %}{% if cat[0] != site.categories.first[0] %},{% endif %}"{{ cat[0] }}":[{% for post in cat[1] %}{% if post != cat[1].first %},{% endif %}{"url":"{{post.url}}", "title":"{{post.title}}", "date":"{{post.date | date:"%d/%m/%Y"}}"}{% endfor %}]{% endfor %} }',
    data = JSON.parse(dataStr),
    curTag = $.query.get("show"),
    archieves = data[curTag];
</ul>
