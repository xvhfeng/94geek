---
layout: default
title: "94geek.com - by Seapeak.Xu"
---
<ul id="cate" class="list-unstyled">
</ul>
<script src="/js/purl.js">
</script>
<script type="text/javascript">
var dataStr = '{ {% for cat in site.categories %}{% if cat[0] != site.categories.first[0] %},{% endif %}"{{ cat[0] }}":[{% for post in cat[1] %}{% if post != cat[1].first %},{% endif %}{"url":"{{post.url}}", "title":"{{post.title}}", "date":"{{post.date | date:"%d/%m/%Y"}}"}{% endfor %}]{% endfor %} }',
    data = JSON.parse(dataStr);
    curTag = purl().param('show');
    as = data[curTag];
    var t = "";
    for( i = 0; i < as.length; i ++){
        a = as[i];
       t +=  "<li><h4><span>" 
           + a.date + '</span>   <a href="' + a.url + '" style="color:black">'+ a.title
           + '</a></h4></li>';
    }
    $("#cate").html(t);
</script>

