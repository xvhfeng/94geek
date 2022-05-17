AUTHOR = 'spk xu'
SITENAME = '大嘴的嘴bu大'
SITETITLE= '94geek.com'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'zh'

OUTPUT_PATH = 'doc/'
# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'https://getpelican.com/'),
       ('Python.org', 'https://www.python.org/'),
       ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
      # ('You can modify those links in your config file', '#'),
       )



DEFAULT_PAGINATION = 10
THEME = "pelican-clean-blog"

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# Social widget
#SOCIAL_PROFILE_LABEL = u'Contact me'
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)#
SOCIAL = (('github', 'https://github.com/xvhfeng$_blank'),
          #  ('facebook','https://facebook.com/myprofile'),
          #('flickr','https://www.flickr.com/myprofile/'),
         # ('wechat','/pages/follow.html'),
          ('envelope','mailto:xvhfeng@126.com'),
          )

MENUITEMS = (("About","/pages/about.html"),
             ("Sharing","/pages/sharing.html"),
             ("Follow","/pages/follow.html"),
             ("Linux C函数","/files/linuxc/main.htm$_blank"),
             )

COLOR_SCHEME_CSS = 'github.css'

# Page相关设置，主要是为了About页面
PAGE_PATHS = ['pages']
PAGE_URL = 'pages/{slug}.html'
PAGE_SAVE_AS = 'pages/{slug}.html'
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False

# 文章生成
ARTICLE_SAVE_AS = 'posts/{slug}/{slug}-{date:%Y}{date:%m}{date:%d}.html'
ARTICLE_URL = 'posts/{slug}/{slug}-{date:%Y}{date:%m}{date:%d}.html'
ARTICLE_LANG_SAVE_AS = 'posts/{slug}/{slug}-{date:%Y}{date:%m}{date:%d}.html'
ARTICLE_LANG_URL = 'posts/{slug}/{slug}-{date:%Y}{date:%m}{date:%d}.html'

STATIC_PATHS = ['files','linuxc','posts','extra/CNAME']  # 静态文件目录
ARTICLE_EXCLUDES = ['files','linuxc'] # 生成忽略的目录
EXTRA_PATH_METADATA = { #按照目录的鸳鸯输出
    'files/*': {'path': 'files/*'},
    'linuxc/*': {'path': 'linuxc/*'},
    'posts/*': {'path': 'posts/*'},
    'files/images/favicon.ico': {'path': 'favicon.ico'},
    'extra/CNAME': {'path': 'CNAME'},
}

TAG_URL            = "tag/{slug}.html"
TAG_SAVE_AS        = TAG_URL
TAGS_URL           = "tag/tags.html"
TAGS_SAVE_AS       = TAGS_URL
CATEGORY_URL       = "category/{slug}.html"
CATEGORY_SAVE_AS   = CATEGORY_URL
CATEGORIES_URL     = "category/categories.html"
CATEGORIES_SAVE_AS = CATEGORIES_URL
