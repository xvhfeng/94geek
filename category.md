---
layout: default
---
<ul id="cate" class="list-unstyled">
</ul>
<script src="/js/purl.js">
</script>
<script type="text/javascript">
var dataStr = '{ {% for cat in site.categories %}{% if cat[0] != site.categories.first[0] %},{% endif %}"{{ cat[0] }}":[{% for post in cat[1] %}{% if post != cat[1].first %},{% endif %}{"url":"{{post.url}}", "title":"{{post.title}}", "date":"{{post.date | date:"%d/%m/%Y"}}"}{% endfor %}]{% endfor %} }',
    data = JSON.parse(dataStr);
    curTag = purl().param('show');
    archieves = data[curTag];
    var t = "";
    for a in archieves {
       t +=  "<li><h4><span>" 
           + a.date + '</span> &raquo; <a href="' + a.url + '">'+ a.title
           + '</a></h4></li>';
    }
    $(#cate).html(t);
</script>

