Title: 从jellky迁移至pelican
Date: 2022-05-15
Category: 兴趣爱好
Tags: 兴趣爱好
Slug: jellky-to-pelican
Author: spk xu
Status: published
Summary: 因为新Mac上一直出现ruby和jellky之间的兼容性问题,导致基于jellky的blog一直无法运行.对于ruby,确实也不熟悉,所以问题也基本无从下手.这几天被隔离在家,清理github上的项目时,看到很久之前就fork的基于python的pelican,抱着试试看的态度想把blog从jekyll迁移至pelican.为了以后方便换机器等使用,记录下了整个迁移过程.没想到的是,整个过程波澜不惊,不管是大众需求还是个人喜好,通过一些配置和规则,pelican竟然都能很快找到答案,并且能很好的支持.


将blog从jekyll迁移至pelican,从开始行动,到本地成功,再到pages服务替换,整个过程没想到是如此的顺利.这个无心拆柳柳成荫的行为相比之前的ruby和jekyll的组合不知道省心了不少.jekyll和ruby最大的问题还是两者之间兼容性太差.对于我这种"程序老手"来说,每一次的环境部署都不会是一蹴而就的,总归中间会出现这样或者那样的妖孽做崇.有时候通过努力或者一遍一遍的重新安装,g各种问题的解决方案能莫名其妙的好了,但是很多时候只能选择从"努力到放弃".所以间接的,也导致了写blog兴趣不高了(终于找到一个长期不更新blog的理由,狗头奇怪!)..一想到要去搞烦人的环境,真的是无言以对.

这几天因为一直被封在家,在清理github的过程中,无意中看见很久之前fork的pelican,当初为什么fork已经无从考证了,而且是基fork以后就放在那里不管的态度.这回仔细看了一下,pelican是基于python的blog的生成工具.python,相比ruby我还是相对比较熟悉的.一想到ruby和jekyll的环境问题,就抱着试试看的态度把jekyll换成pelican.咱说干就干......

从pelican被fork开始到现在,就没理睬过它,所以第一件事先把pelican程序给更新到最新版本.然后clone下来进行了安装.对于python程序,virtualenvs是必须先给安排上的.使用virtualenvs对任何需要安装的程序进行环境隔离,能做到python环境/安装lib/安装程序3者之间一对一的服务,并且对于不同venv下面的程序,也不会出现冲突的问题.所以对于python程序,使用venv还是必须非常推荐的.对于我们第一次部署和使用pelican,在venv加持下,可以让你实现搞不定pelican的万一不幸下,删库跑路,不留下一丁点痕迹.所以对于python程序来说,venv基本就是居家旅行,杀人越货的必备良药.

    :::bash
    安装  Pelican
    sudo port selfupdate  #更新macprot
    sudo port install py39-virtualenv   #安装py39对应的venv,因为机器上的py是py39版本
    sudo port select --set virtualenv virtualenv39 #设置默认的venv版本
    virtualenv ~/virtualenvs/pelican  #创建一个pelican专属环境,你可以把它理解为py虚拟机
    cd ~/virtualenvs/pelican  #进入目录
    source bin/activate #这里是进入虚拟机,其实看了一下脚本,你可以简单的理解为加载PATH即可
    python -m pip install pelican  #安装pelican
    python -m pip install "pelican[markdown]" #安装markdown插件

在bash下运行上面的代码,将会在机器上新建一个py39的venv环境,也可以简单的认为建立了一个`py39`版本的虚拟机,并且在这个虚拟机里面安装了pelican和pelican的mardown支持. 如果你有兴趣,可以查看一下你新建虚拟机的目录,在我们的机器上是~/virtualenvs/pelican这个目录.在这个目录下,存在两个子目录:bin和lib.

- bin目录下为所有`py39`的可执行命令,另外如果你在这个venv环境中执行pip命令,那么安装的可执行文件也会出现在这个bin目录下;

- lib目录即为`py39`的所有库文件,同bin,如果同在venv环境下pip安装,那么库部分会放在此lib目录下;
  
  上面的命令中,需要说明一下的是下面这个命令:
  
    :::bash
    source bin/activate

这个命令特别重要,你可以把这句命令看成是"启动"虚拟机,如果你不执行这个命令,直接就使用了,那么你调用的bin目录下的命令和pip安装的库等都会将使用系统环境的,而不是venv环境下的.有兴趣可以看一下`activate`这个脚本,它的功能就是设置当前环境的PATH,让你可以在命令行中优先调用当前venv环境下的命令.

PS:如果你不想要这个venv了,或者你把这个venv玩坏了,最直接最简单的办法就是一句`rm -rf`把这个目录删除就可以了.有没有"删库跑路"的快感?!

## pelican基础

搞好py虚拟机,安装好pelican的基本环境后,开始建立blog.

使用pelican的命令快速的搭建一个空的架子,在这个架子的基础上搭建我们的blog会更加的快速一些.使用如下命令:

    :::bash
    # 注意当前命令必须链接在上面的venvs环境下执行
    mkdir -p 94geek/source #因为blog的名字就是94geek,所以就创建一个同名字的
    cd 94geek/source  # 完整路径~/virtualenvs/pelican/94geek/source
    pelican-quickstart #新建一个blog的框架
    
    pelican --autoreload --listen  #启动blog  默认本机,端口8000

以上的命令让我们在原来的vens的目录下创建了一个以我们的blog为名字的目录,之所以再创建一个source目录是因为考虑到按照这种blog框架的尿性,后续肯定还会有pe各种组件/plugin/themes等需要拉取安装和自定义,这样创建目录能分门别类的管理清楚.

使用pelican的快速启动命令生成了一个框架,生成框架的过程很简单,照着提示问答一些诸如:blog的名字,作者的名字,url,时区...这些问题就可以了.这里最好是如实填写,但是如果你瞎写也没关系,后续可以在配置文件中更改.命令执行完后会在当前文件夹下生成一个以你blog名字为路径的/blog-name/source/的目录.,在我们的机器上如下图:

![pelican初始目录](./attach/pelican-floder.png  "pelican初始目录")

这么看,前面我们创建的/blog-name/source/的目录其实是多此一举了,不过也无所谓反正是同名.

在source目录中的几个文件和文件夹,它们的作用分别如下:

- Makefile: 一个可以通过make命令来运行pelican和生成html等操作的快速命令集合,它的原理是pelican通过定义makefile的某些目标从而执行相应的命令,以此让使用者可以通过统一的make target的方式控制pelican,熟悉makefile规则的同学可以打开看一下,非常的简单明了;
- content: 这个文件夹即为我们的整个blog的root目录,只不过是提供我们编辑的场所.你可以在里面新建一些文件夹,比如我的新建如下:
  - files: 放置静态文件,可以在files文件夹下面再新建images,js,css等等你需要的子目录;
  - posts: 这是我们blog重点所在,我们的blog文章的原始rst或者md文件全部在这个目录下,当然为了方便,你也可以在这个目录下新建子目录来控制原始文件的存放;
  - pages:这个文件夹是存放一些纯页面的地方,它不是html文件,也是markdown文件,但是这里的文件只是会简单的生成,不会产生某些站点的副作用(比如:sitemap之类的).一般这个文件我们会存放一些对于网站,或者是介绍性的文章;
- pelicanconf.py: 整个pelican环境的配置信息,在创建框架的时候输入的一些信息会以配置信息的方式存放在这个文件中,在不断完善pelican的过程中,我们将一直和这个文件打交道.
- publishconf.py: pelican发布信息的配置文件,如果是使用的快速搭建框架命令的话,这个文件不需要管.
- task.py: 发布时候的一个文件,目前暂未使用

至此,我们可以在source文件夹下执行命令:

    :::bash
    pelican --autoreload --listen

 启动pelican,只不过目前整个blog中没有任何的东西,在浏览器中使用`http://127.0.0.1:8000`查看的时候是一个空的blog,相当于目前我们的blog还是毛胚状态,虽然可以使用,但是一点美感和质量都没有,所以我们还是要适当的装修一下.

## themes

空的blog没啥意义,加了文章也有点难看,所以根据这种blog的当前的特征,我们需要对blog装修一下.这种类型的blog一般是使用themes来完成它的美化工作.theme也不是什么很高深的东西,其实就是一堆模版,使用tag的方式来把你定义和配置的信息通过模版的方式展现成规定的那个样子.本质上,你可以把theme看上是`一堆html文件和js css image`等组合成的一个站点.pelican也给我们准备了很多的themes,找到themes的仓库:[Pelican的themes](http://www.pelicanthemes.com/ "Pelican的themes"),选取一个你自己喜欢的theme,然后先fork到自己的github,再clone到本地.为什么要先fork然后再clone而不是直接clone,主要有2个原因:

1. 为了避免后续仓库被删除或者仓库不存在之类的问题,还是先fork了安心;
2. 对于既有theme,肯定有一些是不对你胃口的,所以你肯定是要自定义一些东西的;那么你还不如直接在你自己的仓库上去修改;

我个人因为不需要花里胡哨,也不喜欢那种很多栏目的blog,所以就选了一个相对比较简单但又不是那么"毛胚"的theme:pelican-clean-blog.把这个theme的代码拉到本地,在source同级的目录中,建立一个名为themes的文件夹,把pelican-clean-blog的代码拉取到themes目录下,这样做的好处是:当你对其它themes见异思迁的时候,你可以方便的在themes目录下拉取多个themes,然后每个都可以试试,反正试试也不要钱.

    :::bash
    pelican-themes -lv  #查看当前已经安装的themes
    pelican-themes --install ./pelican-clean-blog/ --verbose #安装theme
    pelican-themes -lv #查看一下themes是否已经被安装

使用上面的命令安装本地的themes到pelican的环境下,使用-v参数可以看到themes安装存放的地址.在我的机器上,themes被安装到了venvs下lib目录下:

  virtualenvs/pelican/lib/python3.9/site-packages/pelican/themes/pelican-clean-blog
记住这个路径,后面有用.

要启用这个theme,我们还得在pelicancong.py文件上增加一行:

    :::python
    THEME = "pelican-clean-blog" # 说明使用theme,theme必须安装到当前环境下

然后我们再启动pelican,就能看到带有theme的blog,但是因为我们还是么有放内容,所以当前的blog还是空的.但至少已经美观了很多.

## 配置与自定义
### 自定义
在选择的pelican-clean-blog上,带有Social widget和menuitems的功能.前者一般被配置为SNS等账号,比如wechat,facebook等等;后者为blog上一些除正文内容外的内链和外链,比如内链有"关于",等等,外链有github地址等等.这里的配置根据自己的情况自己决定,我的配置为:

    :::pytohn
        SOCIAL = (('github', 'https://github.com/xvhfeng$_blank'), #打开_blank方式
                        ('wechat','/pages/follow.html'),
                        ('envelope','mailto:xvhfeng@126.com'),
                        )
    
        MENUITEMS = (("About","/pages/about.html"),
                                ("Sharing","/pages/sharing.html"),
                                ("Follow","/pages/follow.html"),
                                ("Linux C函数","/files/linuxc/main.htm$_blank"),
                        )

在配置Social widget和menuitems的时候碰到了一个问题:即默认的情况下,链接的打开方式都是"_self"方式,但是这种模式对于像About,Sharing,Follow这种页面是没有问题,因为这些页面本身就是站内链接,是根据当前的模版生成的,并且点击了也还是在本站内,不会跨站;对于github,是一个标准的外链地址,点击这个链接跳转到站外,所以属于是跨站行为;另外特殊的linux c函数栏虽然是一个站内链接,但是它只是简单的html文件,并不是根据当前站点的模版生成的,没有当前站点的主题.对于跨站和非同theme下的替换当前页面操作会显得非常突兀,所以对于这种方式,更想要的是使用"_blank"打开方式,而不是"_self"打开方式.找了一圈都没找到支持"_blank"打开方式的配置支持.如果非要使用"_blank",也只能自己去解决了.

找到主题的代码,注意这里我们不应该去themes目录下找,因为pelican使用的是你安装后的主题,所以我们要去venvs的lib下的主题文件夹找,根据链接输出的样式,我们找到在base.html文件中,存在有这两个板块的链接输出.代码如下(仅以menuitems为例):

    :::html
    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
        <ul class="nav navbar-nav navbar-right">
        {% for title, link in MENUITEMS %}
                <li><a href="{{ link }}">{{ title }}</a></li>
        {% endfor %}
        {% if DISPLAY_PAGES_ON_MENU %}
            .......
        {% endif %}
        </ul>
    </div>
    <!-- /.navbar-collapse -->

在上面的代码中,模版对于MENUITEMS这个变量进行foreach,拿到这个变量的中的element来进行输出.我第一想到的是,在配置文件中在后面再增加一个元素,打开方式的元素,将需要配置的文件都配置成以下的形式:

    :::python
    ('github', 'https://github.com/xvhfeng','_blank')

这种方式简单明了,并且各个部分都不会受影响.但是无奈这种配置收到enumitem定义的影响,pelican并不支持,所以我们只能另想办法.在enumitems元素只有2个(text和link)被限定的情况下,我们只能在text或者是link上选其一做一点手脚.在配置的时候,在选中的部分中加上某些特殊的标签,然后在上面的foreach中处理一下,把特殊的标签识别出来,并且对其进行处理.在我们的现实情况中,我们在link这部分上坐了手脚,主要是因为打开的方式毕竟是和link更近一些,也是属于link的某种行为,所以放在link上更合适.我们的定义如下所示:

    :::python
    ('github', 'https://github.com/xvhfeng$_blank')

我们在link上增加了"$_target"的标志,这样不会对pelican解析emunitems产生影响,也能把pelican跑起来.但是就这么改了配置还不能实现我们的功能,我们必要在展现的地方进行相应的更改,来完成最后的link绑定工作.找到`base.html`中的相关代码,在foreach的时候对每一个element的link部分进行处理一下,因为我们只有_blank这一种打开方式,所以我们只要判断配置项是不是具有2个配置信息,如果是的话,直接给与_blank打开方式即可.修改后的代码如下所示:

    :::html
    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
        <ul class="nav navbar-nav navbar-right">
        {% for title, link in MENUITEMS %}
            {% if link.split('$')[0] == link %}
                <li><a href="{{ link }}">{{ title }}</a></li>
            {% else %}
                <li><a href="{{ link.split('$')[0] }}" target="_blank">{{ title }}</a></li>
            {% endif %}
        {% endfor %}
        {% if DISPLAY_PAGES_ON_MENU %}
            .......
        {% endif %}
        </ul>
    </div>
    <!-- /.navbar-collapse -->

对于Social widget,我们也使用同样的方式更改即可.

之所以我们是直接去更改lib目录下的文件,而不是通过更改github上拉下来的文件,是有原因的:

1. 实际上,当你安装完theme后,pelican引用的是lib下面的theme,和github上clone下来的theme已经没有关系了;
2. 在修改的过程中,可能需要不停的修改和调试,如果直接修改从github上clone下来的themes中的文件,不安装或者更新的话,对于pelican是不起任何作用的;所以如果这样做的话,那么每次修改完成后还要去卸载已经安装的和安装更改过的,或者是直接更新,然而我们并不知道这个繁琐的过程需要多少次;
3. 我们目前仅仅只是debug,所以直接修改就可以,修改完成达到效果后,我们用修改后的文件去更新github上clone下来的theme,虽然流程反过来了,但是一样能达到目的;

但是不管怎么样,主要还是为了方便和快速的解决问题.

另外提一嘴:我个人就是把pelican-clean-blog这个主题给fork到了我自己的github上,然后自己给自己开了一个myself的分支,我的所有更改都是在myself这个分支上进行,这样既能保证主题的master可以升级又能保证myself供给我自己使用,一举两得.

### MENUITEMS显示设置
在pelican的配置中,关于pages的配置也说一下,我个人比较在乎ControlInAll,秉着这个原则,我对于pages也采取了这种原则.我的配置如下:

	:::python
	# Page相关设置，主要是为了About页面
	PAGE_PATHS = ['pages'] #配置content下,作为pages输出的文件夹
	PAGE_URL = 'pages/{slug}.html' 
	PAGE_SAVE_AS = 'pages/{slug}.html'
	DISPLAY_PAGES_ON_MENU = False
	DISPLAY_CATEGORIES_ON_MENU = False
	
这里的配置把所有pages的内容全部归纳到站点root下的pages文件夹内,并且通过DISPLAY_PAGES_ON_MENU和DISPLAY_CATEGORIES_ON_MENU选项设置为Flase将禁止这些页面与链接自动的在menu区域内显示.这样做的好处是:我们可以通过MENUITEMS配置项来做到需要显示多少就显示多少.

### 内容与静态文件
作为一个技术blog,我们对于blog最主要的内容有几个要求:

1. markdown或者rst文件作为源文件,blog可以解析并且生成html输出
2. blog内的代码可以格式化高亮显示
3. 支持自定义静态文件,特别是图片等

在pelican中,可以在pelicanconf.py文件中,通过ARTICLE相关的配置项来配置由markdown/rst文件生成文件的行为,由STATIC_PATHS来配置静态文件的支持.

开始,我对于文章的生成和静态文件是打算把公用的静态文件放在files文件夹下,把文件生成通过日期的方式来分割,这样能既能做到文件分门别类,又能比较清晰的展现blog内容.但是对于markdown文件中引用的图片等,我是想在posts下面每篇blog建立一个文件夹,在这个文件夹内即为一篇blog的全部内容,包括markdown文件,blog可能引用的图片等等.之所以采取这种一篇blog一个文件夹且包括静态文件的方式完全是因为2点:

1. 好管理,如果该篇文章不想要了,直接删除整个文件夹即可
2. 兼容offline编辑器,因为图片的引用问题,online的图片和offline的图片地址总归有一点不一样,除非放在同样的目录下,这样即可通过当前文件夹引用即可完美的解决
3. 不把markdown文件和图片分离是因为想在写blog的时候更多的专注于写,而不是图片放在哪里?我要怎么引用?等等这一序列繁琐的问题.从而造成写作的思路别打断;

结合这些需求,开始我的pelicanconf.py中,但对于静态文件夹和内容文件夹的配置如下:

	:::python
	# 文章生成
	ARTICLE_SAVE_AS = 'posts/{date:%Y}-{date:%m}-{date:%d}/{slug}.html'
	ARTICLE_URL = 'posts/{date:%Y}-{date:%m}-{date:%d}/{slug}.html'
	ARTICLE_LANG_SAVE_AS = 'posts/{date:%Y}-{date:%m}-{date:%d}/{slug}.html'
	ARTICLE_LANG_URL = 'posts/{date:%Y}-{date:%m}-{date:%d}/{slug}.html'
	
	STATIC_PATHS = ['files','linuxc'] # 静态文件目录
	ARTICLE_EXCLUDES = ['files','linuxc'] # 生成忽略的目录
	EXTRA_PATH_METADATA = { #按照目录的原样输出
		'files/*': {'path': 'files/*'},
		'linuxc/*': {'path': 'linuxc/*'},
	}

这种模式确实能很好的解决生成文件的问题,但是却无法解决静态文件和markdown的引用问题.
因为posts文件夹中存放的静态图片无法被pelican无差别的复制到markdown相应的html文件的文件夹中.主要的原因是,根据上面的配置信息,markdown在转换成html的过程中,pelican会根据markdown中的date信息来去生成html所存放的目录.而且因为posts被指定为markdown的文件夹,所以默认pelican不会对其进行静态文件的赋值操作,所以我们必须首先把posts文件夹也要静态文件夹化,所以在STATIC_PATHS中先增加一个试试看,将STATIC_PATHS配置成如下:

	:::python
	STATIC_PATHS = ['files','linuxc','posts']
	EXTRA_PATH_METADATA = { #按照目录的原样输出
		'files/*': {'path': 'files/*'},
		'linuxc/*': {'path': 'linuxc/*'},
		'posts/*': {'path': 'posts/*'},
	}
这样配置后,我们删除output文件夹,重新生成一下blog发现:我们的静态文件也被copy过去了,而且markdown文件被自动识别出来,并没有作为静态文件被copy,而是生成了对应的html文件,但html文件和静态文件不在一个文件夹下.html文件根据配置信息,存放到了在`{date:%Y}-{date:%m}-{date:%d}`对应的文件夹下,而静态文件根据配置信息保持了和在content的posts下面一样目录路径.那么显然这种方式还是无法满足要求.

要想把markdown生成的html和静态文件放在一个文件夹下,就还得再想想办法.分析一下:

1. 对于静态文件,我们能做的事情很少,因为静态文件没办法写入blog mate header信息,所以基本上唯一能控制的生成路径就是要么保持原样路径输出,要么输出到一个指定的目录.如果输出到一个指定的目录,和我们html和静态文件在一个文件夹的初衷相违背.所以只有保持原样这一条路;
2. 对于markdown文件,相对来说自由度高一些,因为可以通过配置blog mate header信息来自定义某些信息.既然我们生成的文件名上带有slug信息,那么我们是不是可以把slug信息也指定为生成html的目录,这样不就是可以把这个html生成到与slug同名的目录中去了吗?因为静态文件无法控制`{date:%Y}-{date:%m}-{date:%d}` 这段配置信息,所以还不如直接把这段日期信息拿掉,直接改成:posts/{slug}/{slug}.html这样的.

更改后,配置信息如下:

	:::python
	# 文章生成
	ARTICLE_SAVE_AS = 'posts/{slug}/{slug}.html'
	ARTICLE_URL = 'posts/{slug}/{slug}.html'
	ARTICLE_LANG_SAVE_AS = 'posts/{slug}/{slug}.html'
	ARTICLE_LANG_URL = 'posts/{slug}/{slug}.html'

这种方式生成的html文件最后被保存到以slug为名的文件夹,但是静态文件还是一样,所以如果要保证静态文件也要被放入slug的文件夹,那么当前blog在posts下新建的文件夹就应该和slug同样,这样生成的html文件会被通过配置存入到slug这个文件夹,而静态文件也会因为pelican的配置执行"按照content下同路径复制",所以也会在slug文件夹下,这样就能做到静态文件和生成的tml文件同目录,不会出现编辑的时候和访问的时候,静态文件相对于markdown文件和html文件不一样的情况.

到这里为止,在本机offline生成静态站点完成了.可以通过命令:

    :::bash
    pelican --autoreload --listen

来看一下具有主题,能实现文件管理的blog了.

## 与github page服务结合
与github page的结合相对简单.只要在github上开一个pages的服务,然后把我们整个94geek文件下的文件全部签入就可以.这里要说一下,以前的pages服务也不知道是我没注意呢?还是没有相对的功能.原来的pages服务只能是从gh-pages这个分支下去支持服务,所以就搞的很麻烦.要先在本地通过blog的source生成一遍html,然后再把生成的html签入github,但是因为分支的原因,你的source和生成的html文件还得分开处理.所以像我怕麻烦的就是直接索性开了两个仓库,一个存放blog的source一个用来做pages服务.但是这次去看了一下设置,发现pages可以通过gh-pages(也有可以选择master分支的,没试,不知道是不是真的可行)分支的docs目录来提供服务.这样就方便多了,可以把source放在仓库的根目录下,本机生成的html定位到docs目录,这样只要一次提交就可以把所有的东西全部提交到github,方便多了!

## 总结
至此,我们的blog迁移完成了,总体来说不难,中间碰到的问题也不多.就算是碰到了,也能很方便快速的解决.pelican用了几次发现比jekyll方便多了,并且得益于python具有的venv功能,环境也干净,目前在迁移和使用的过程中并没有发生像jekyll这样需要花很长时间去处理环境的问题.所以这一点还是比较满意的.

虽然整个blog的写作和处理的方式和以前差不多,但pelican提供了还是比jekyll更符合我的某些特殊爱好的功能,所以也更适合我一些吧!以后blog应该会一直使用pelican管理下去了,jekyll应该是不会再用了!

** Bye Bye,Jekyll! **
** Hello, Pelican! **