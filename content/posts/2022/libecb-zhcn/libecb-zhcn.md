Title: libecb中文翻译
Date: 2022-05-26
Category: 翻译
Tags: 翻译
Slug: libecb-zhcn
Author: spk xu
Status: published
Summary: libecb是一个不需要configurtion脚本就可以在c语言中直接使用的接近编译器分类的简单头文件.几年前偶然看到这个库,然后忘记名字了.直到去看libev源码才发现原来两者是一起的.它们应该出于同一家公司,可能还是同一个项目.本着这个比较实用的原则,我花了点时间把它原来的文档给翻译了.

# LIBECB - e-C-Builtins

## ABOUT LIBECB

Libecb目前是一个简单的头文件，可以在不需要任何配置的情况下加入到你自己的项目中。

它是整个套件的一部分，其他成员包括libev libeio。

[主页]( [http://software.schmorp.de/pkg/libecb](http://software.schmorp.de/pkg/libecb))可在此找到(但是这个网址已经失效了,可惜):

它主要为许多内置编译器提供了许多包装器，以及其他编译器的替换函数。 除此之外，它还提供了许多其他比较底层的C实用程序，如字节交换或位旋转。

或者换句话说，libecb可以被引入到任何标准C开发的系统中， 它可以保证不同编译器中的通用性.

**_译者注:_** libecb是一个不需要configurtion脚本就可以在c语言中直接使用的接近编译器分类的简单头文件.几年前偶然看到这个库,然后忘记名字了.直到去看libev源码才发现原来两者是一起的.它们应该出于同一家公司,可能还是同一个项目.本着这个比较实用的原则,我花了点时间把它原来的文档给翻译了.然后,因为经常做开发的原因,我也在libecb的基础上添加了一些宏定义,所以libceb的源文件和我添加的文件一直组成了我自己使用的基础头文件.

[libecb开源地址](https://github.com/xvhfeng/libecb)

## ABOUT THE HEADER

现在，你所要做的就是复制<ecb.h\>,放入你的项目.编译器可以找到它并包含它:

	#include <ecb.h>

头文件对于C和c++编译都可以很好地工作，并为您提供除了ECB符号外，所有的<inttypes.h\>。

目前没有.o文件需要被link,未来的版本可能会提供可选的.o文件, 以用来减少代码的大小和增加额外的功能.

它目前还包括从<inttypes.h\>开始的所有内容。

## ABOUT THIS MANUAL / CONVENTIONS

本手册主要描述了<ecb.h\>头文件内可用的每个(公共)函数. 头文件可以定义其他符号,但那些都不是公共API的一部分，也不会有任何的支持.

当手册提到一个“函数”时，它可以一个内联函数、一个宏定义或外部符号。

当函数使用具体的标准类型时，例如`int`或`uint32_t`，则相应的函数只适用于该类型。 如果只使用通用名称(`expr`， `cond`， `value`，等等)，那么对应的函数依赖于C语言来实现正确的类型，并且通常作为宏实现。 具体地说，是本手册中的“bool”指任何类型的布尔值，而不是特定类型。

## TYPES / TYPE SUPPORT

ecb.h确保以下类型被定义(以预期的方式):

```
int8_t       uint8_
int16_t      uint16_t
int32_t      uint32_
int64_t      uint64_t
int_fast8_t  uint_fast8_t
int_fast16_t uint_fast16_t
int_fast32_t uint_fast32_t
int_fast64_t uint_fast64_t
intptr_t     uintptr_t
```

宏`ECB_PTRSIZE`定义为目标平台上的指针的大小(目前`4`或`8`),可以用于预处理器表达式。

而`ptrdiff_t`和`size_t`使用的`stddef.h`/`cstddef`中的定义.

## LANGUAGE/ENVIRONMENT/COMPILER VERSIONS

下面的符号都可以在预处理器指令中被展开且可以被作为一个bool值而被测试(如果你需要的话,使用`!!`确保它是`0`或`1`).

### ECB_C

当该值为true,则表示当前实现定义了`__STDC__`宏定义.仅仅是c,不是cxx. PS:当前的版本好像去掉了这个宏,因为没找到.

### ECB_C99

当该值为True,这表示当前实现声称符合C99 (ISO/IEC9999:1999)或任何更新的版本，而不是声称是c++。

请注意，新版本(ECB_C11)会再次删除核心特性(例如可变长度数组)。

### ECB_C11, ECB_C17

当该值为True,这表示当前实现声称符合ECB_C11, ECB_C17 (ISO/IEC9899:2011, :20187)或任何更新的版本，而不是声称是c++。

### ECB_CPP

当该值为True,则表示定义的宏 `__cplusplus__`为True. 这是一个典型的对于c++编译器的真值.

### ECB_CPP11, ECB_CPP14, ECB_CPP17

当该值为True,则表示当前实现符合C++11/C++14/C++17(ISO/IEC 14882:2011, :2014, :2017)或任何更新的版本.

请注意，c++ 20的许多特性可能都有自己的特性测试(参见[c++ 20新特性](http://eel.is/c++draft/cpp.predefined#1.8))。

### ECB_OPTIMIZE_SIZE

当编译器优化大小时为`1`，否则为`0`。

这个符号也可以在包含_ecb.h_之前定义，那么该值将会是定义的值,而不会改变。

### ECB_GCC_VERSION (major, minor)

如果编译器使用的是指定版本或者更改版本的GNU C编译器,则该值为True.

当认为编译器为GCC但是它不是的时候,则返回False.

### ECB_EXTERN_C

该值在c++中扩展为`extern "C"`，在C中扩展为简单的`extern`。

这可以用来声明一个单独的外部C函数:

```
ECB_EXTERN_C int printf (const char *format，…);
```

### ECB_EXTERN_C_BEG / ECB_EXTERN_C_END

这两个宏可以用来包装多个 `extern "C"` 的定义-在C里面不会有任何的效果

它们在头文件中多数被这样使用:

```
ECB_EXTERN_C_BEG

int mycfun1 (int x);
int mycfun2 (int x);

ECB_EXTERN_C_END
```

### ECB_STDFP

如果此值计算为真(可用于预处理器做判断),那么`float`和`double` 使用IEEE 754 single/binary32和double/binary64表示. 内部两者的字节序和`uint32_t`与`uint64_t`的字节序相同.

这意味着您可以将`float`(或`double`)的位复制到`uint32_t`(或`uint64_t`)， 得到原始的IEEE 754位表示而无需考虑格式或字节序。

这对于所有现代的平台都是正确的，虽然_ecb.h_可能无法在任何地方正确地推导出这点，而且可能会在安全方面出错。

PS:也就是说int和float两者之间可以转换,但是没有办法证明一定正确,但现实就是很多都是这么使用的.如何转换,是一个C的hack,自己想一下??

### ECB_64BIT_NATIVE

如果计算结果为真(该值也可用于预处理器和C代码的测试),那么该体系结构对于64位的支持是内置的. 也就是说,速度上64位和32位整数是差不对哦的,虽然64位支持非常常见(实际上libecb也需要), 但32位的cpu必须模拟64位的操作,所以你可能希望避免它们. PS:libecb的年代64位还没那么普及??

### ECB_AMD64, ECB_AMD64_X32

这两个宏在x86_64/amd64 ABI和X32 ABI上分别定义为`1`，在其他地方未定义。

新的X32 ABI的设计者出于某种无法解释的原因，决定让它看起来像amd64的一模一样.

尽管它与那个ABI完全不兼容，这打破了假定`__x86_64`表示x86-64 ABI，所以使得这些宏是必要的。

## MACRO TRICKERY

### ECB_CONCAT (a, b)

展开`a`和`b`中的任何宏，然后将结果连接起来形成单个标记。这主要用于从组件中形成标识符，

e.g.:

```
#define S1 str
#define S2 cpy

ECB_CONCAT (S1, S2)(s1, s2); // == strcpy (s1, s2);
```

### ECB_STRINGIFY (arg)

展开`arg`中的任何宏并返回它的字符串化版本。这主要用于以字符串形式获取宏的内容，

e.g.:

```
#define SQL_LIMIT 100
sql_exec ("select * from table limit " ECB_STRINGIFY (SQL_LIMIT));
```

### ECB_STRINGIFY_EXPR (expr)

类似于`ECB_STRINGIFY`，但是会先计算一次`expr`以确保它是一个有效的表达式。 (PS:所以,这里会有一个宏定义常有的,expr被多次计算的问题) 这对于捕捉输入错误或宏不可用的情况很有用:

```
#include <errno.h>

ECB_STRINGIFY      (EDOM); // "33" (on my system at least)
ECB_STRINGIFY_EXPR (EDOM); // "33"

// now imagine we had a typo:
//现在假设我们有一个打印错误

ECB_STRINGIFY      (EDAM); // "EDAM" 这样的话直接就是输出
ECB_STRINGIFY_EXPR (EDAM); // error: EDAM undefined,第一次计算发现EDAM没有被定义,所以直接报错
```

## ATTRIBUTES

libecb的大部分的附加属性可以用于函数、变量的处理，有时甚至是一些类型的附加属性,像C中的`const`或`volatile`。 它们是使用GCC属性或其他编译器/语言特定特性实现的。属性声明必须放在整个声明之前:

```
ecb_const int mysqrt (int a);
ecb_unused int i;
```

### ecb_unused

将函数或变量标记为“未使用”，这只会在编译器检测到它未使用时，简单地抑制编译器的警告。 当你声明一个变量但不总是使用它时，这是很有用的:

```
{
  ecb_unused int var;

  #ifdef SOMECONDITION
     var = ...;
     return var;
  #else
     return 0;
  #endif
}
```

### ecb_deprecated

类似于`ecb_unused`，此标记讲函数、变量或类型标记为弃用。 这使得一些编译器在使用该类型时发出警告。

### ecb_deprecated_message (message)

与`ecb_deprecated`相同，但如果可能，在使用对象时使用指定的诊断信息，而不是通用的报错消息。

### ecb_inline

扩展为`static inline`,或者如果不支持内联，仅仅扩展为`static`(编译器特定的等效)。 由于代码大小或速度的原因，它应该仅仅用于声明应该内联的函数。

示例:内联这个函数，它肯定会减少代码。

```
ecb_inline int
negmul (int a, int b)
{
  return - (a * b);
}
```

### ecb_noinline

防止函数内联——它可能会被优化掉，但不会内联到其他函数中。 如果您知道您的函数很少被调用，并且足够大以至于内联不会有帮助，那么这个宏定义是很有用的。

### ecb_noreturn

将函数标记为“永远不返回”。 一些永不返回的典型函数像是`exit`或`abort`(这些函数确实很难做到不返回)， 现在你可以创建自己类似的函数:

```
ecb_noreturn void
my_abort (const char *errline)
{
  puts (errline);
  abort ();
}
```

在这种情况下，编译器足够聪明的话能够自行推导出它，所以这主要用于声明。

### ecb_restrict

在支持的编译器上扩展为`restrict`关键字或等效值，而在其他编译器上则没有扩展为任何值。 必须在指针类型或数组索引上指定，以指示内存没有与同一作用域中的任何其他受限制的指针别名。 PS: 参考restrict关键字:restrict是c99标准引入的，它只可以用于限定和约束指针， 并表明指针是访问一个数据对象的唯一且初始的方式. 即它告诉编译器，所有修改该指针所指向内存中内容的操作都必须通过该指针来修改, 而不能通过其它途径(其它变量或指针)来修改;这样做的好处是,能帮助编译器进行更好的优化代码,生成更有效率的汇编代码. 也就是说在restrict关键字形容的变量的相同的访问内,不允许出现restrict修饰指针或者数组的别名.

例如:将一个向量乘起来，并允许编译器并行化循环，因为编译器知道它不会覆盖输入的值。

```
void
multiply (ecb_restrict float *src,
          ecb_restrict float *dst,
          int len, float factor)
{
  int i;

  for (i = 0; i < len; ++i)
    dst [i] = src [i] * factor;
}
```

### ecb_const

声明函数只依赖于其实参的值，就像数学函数。它特殊之处在于不读取或写入任何参数可能指向的内存、全局变量或调用任何非const函数。它也也会有任何的副作用。

这样的函数可以由编译器更好地优化——例如，具有相同参数的多个调用可以优化为一个调用，如果编译器预设该调用具有任何副作用，那么这种优化是不可能的。

它最适合于数学函数意义上的函数，例如返回其输入参数平方根的函数。

不适合使用计算传入内存区域的哈希值、打印一些消息或查看全局变量来决定舍入的函数。

请参阅`ecb_pure`了解限制稍少的函数类。

PS: 用const属性修饰的函数与用pure属性修饰的十分类似，不过const属性比pure更严格. 它要求函数不能读全局对象。 此外，用const属性修饰的函数的参数不能是一个指针类型，而且在用const属性修饰的函数内往往不能调用一个非const属性的函数。

### ecb_pure

类似于`ecb_const`，声明一个没有副作用的函数。与`ecb_const`不同， 该函数允许检查全局变量和任何其他内存区域(比如通过指针传递给它的内存区域)。

虽然这些函数不能像`ecb_const`函数那样被更好地优化，但在很多情况下， 它们仍然可以被优化掉，而且编译器可以更自由地将调用转移到它们那里。

这类函数的典型例子是`strlen`或`memcmp`。函数计算输入的MD5并且作为参数传递更新MD5的状态, 这些函数不是pure的,因为这些函数将修改一些不是返回值的内存区域.

PS: 用pure属性修饰的函数用来说明该函数除了返回值之外没有其他任何效果， 并且该函数所返回的值仅仅依赖于函数的形参以及/或全局对象。 用 pure属性所修饰的函数可以用来辅助编译器做消除公共子表达式以及帮助做循环优化，使用这种函数就好比使用算术操作符一般。

用pure属性所修饰的函数体内不应该含有无限循环，不应该对volatile修饰的全局对象进行访问或是对多个线程所共享的全局对象进行访问， 也 不应该访问其他系统资源，比如对文件、套接字等进行操作。 简而言之， 对同一个使用pure属性修饰的函数连续做两次调用（如果该函数带有参 数，那么两次调用应该用同样的实参）， 那么这两次调用所返回的结果应 该始终是相同的。因此，用pure属性所修饰的函数也很容易让编译器做内 联处理。

### ecb_hot

这是声明函数对于缓存是“hot”函数,也就是说此函数使用频繁.如果可能的话,将它保持在缓存中是非常有用的.

编译器的做法是试图将热函数彼此靠近保存在内存里。

一个函数是否热通常取决于整个程序，函数本身的作用更小。实践中`ecb_cold`可能更有用。

PS:是不是就是说,将函数直接保存在内存中,减少加载的时间?

### ecb_cold

与`ecb_hot`相反的是，声明一个函数对于缓存来说是“冷的”. 或者换句话说，这个函数不经常被调用，或者不是在临界速度的时候调用，将它保存在缓存中可能是对缓存的浪费。

除了一起放置冷功能(或者至少远离热功能),这些知识可以用在其他方面. 例如,函数将优化函数大小,而不是速度.导致调用这些函数的代码路径可以自动标记为`ecb_expect_false`，就像已经使用`ecb_expect_false`访问它们一样。

这类函数的好例子是错误报告函数，或者仅在异常或罕见情况下调用的函数。

### ecb_artificial

声明函数是“artificial”的,在这种情况下,也就是说,这个函数并不意味着是一个函数, 更像一个访问器——许多方法在C++类中仅仅是访问器的功能,具有和崩溃报告同样的方法,或单步通过他们. 通常不是那么有用,特别是当它只内联到几个指令的时候。

将它们标记为artificial将指导调试器了解这一点，从而使调试工作更愉快，从而使生活更愉快。

例如:在某种智能指针类中，将指针访问器标记为人工的，这样整个类的行为就更像一个指针，而不像某个c++抽象怪物。

```
template<typename T>
struct my_smart_ptr
{
  T *value;

  ecb_artificial
  operator T *()
  {
    return value;
  }
};
```

## OPTIMISATION HINTS

### bool ecb_is_constant (expr)

如果表达式被推断为编译时常量，则返回true，否则返回false。

例如，当您有一个返回16位随机数的`rndm16`函数，并且您有一个函数将其映射到从0开始到N-1的范围，那么你可以在头文件中使用这个内联函数:

```
ecb_inline uint32_t
rndm (uint32_t n)
{
  return (n * (uint32_t)rndm16 ()) >> 16;
}
```

但是，对于2的幂，您可以使用普通掩码，不过只有在编译时检测到这种情况才可以这样做。 这是当传递的数字是一个常数，也是2的幂(`n & (n -1) == 0`)的情况:

```
ecb_inline uint32_t
rndm (uint32_t n)
{
  return is_constant (n) && !(n & (n - 1))
    ? rndm16 () & (num - 1)
    : (n * (uint32_t)rndm16 ()) >> 16;
}
```

### ecb_expect (expr, value)

计算`expr`并返回它。此外，它告诉编译器`expr`的计算结果很多都是`value`，这可以用于静态分支优化。

通常，您希望使用更直观的`ecb_expect_true`和`ecb_expect_false`函数。

### bool ecb_expect_true (cond)
### bool ecb_expect_false (cond)

这两个函数期望表达式为true或false，并分别返回`1`或`0`. 因此当用于`if`或其他条件语句的条件时，它不会改变程序:

```
/* these two do the same thing */
if (some_condition) ...;
if (ecb_expect_true (some_condition)) ...;
```

但是，通过使用`ecb_expect_true`，您可以告诉编译器该条件大概率可能为真(对于`ecb_expect_false`，它大概率为假)。

例如，当你检查一个空指针，并期望它是一个罕见的，异常的，大小写，然后使用`ecb_expect_false`:

```
void my_free (void *ptr)
{
  if (ecb_expect_false (ptr == 0))
    return;
}
```

随后使用这些函数来标记异常情况，或者告诉编译器函数的热路径是什么，可以大大提高性能。

您可能知道名称为`likely`和`unlikely`的这些函数——尽管它们是常见的别名， 但我们发现，在快速浏览代码时，期望名称更容易理解。 如果您愿意，可以使用`ecb_likely`而不是`ecb_expect_true`和`ecb_unlikely`而不是`ecb_expect_false`—这些只是别名。

一个很好的例子是:在函数中,会预分配更多一些的内存来存储某些东西(例如,一个字符串流) ——那么每次添加东西的时候,你必须检查缓冲区溢出,但你认为大多数情况下,预分配的对于空间是够用的:

```
/* make sure we have "size" extra room in our buffer */
ecb_inline void
reserve (int size)
{
  if (ecb_expect_false (current + size > end))
    real_reserve_method (size); /* presumably noinline */
}
```

### ecb_assume (cond)

试图告诉编译器cond为真，即使它并不明显。这不是一个函数，而是一个语句:它不能被当做表达式使用。 PS:也就是说,它不能被放在if中做判断

这可以用来告诉编译器关于不变量或其他可能改善代码生成的条件，但不可能从代码本身推断出来。

例如，`ecb_expect_false`描述中的示例保留函数可以这样写(只添加了`ecb_assume`):

```
ecb_inline void
reserve (int size)
{
  if (ecb_expect_false (current + size > end))
    real_reserve_method (size); /* presumably noinline */

  ecb_assume (current + size <= end);
}
```

如果你调用这个函数2次,就像这样:

```
reserve (10);
reserve (1);
```

然后编译器_可能_能够完全优化第二个调用，因为它知道`current + 1 > end`是假的，调用将永远不会被执行。

### ecb_unreachable ()

这个函数本身什么都不做，除了告诉编译器它永远不会被执行。 除了在某些情况下不触发警告外，这个函数还可以用于实现`ecb_assume`或类似的功能。

### ecb_prefetch (addr, rw, locality)

告诉编译器预加载数据到内存`addr`ess为后续的读(`rw` = 0)或写(`rw` = 1)做准备。 `locality` `0`意味着只有一次访问,`3`意味着可能是会经常访问的数据,并且数据准备的彼此之间……在两者之间。 addr所指向的内存不需要是可访问的(例如，它可以是一个空指针)，但是`rw`和`locality`必须是编译时常量。

这是一个语句，而不是一个函数:你不能将它用作表达式的一部分。

一种明显的方法是在一个大数组中，在较远的地方预加载一些数据。 这将在之后预加载内存中的128个数组元素，希望当CPU到达这个位置时，这些元素就已经准备好了。

```
int sum = 0;

for (i = 0; i < N; ++i)
  {
    sum += arr [i]
    ecb_prefetch (arr + i + 128, 0, 0);
  }
```

一般很难预测预取的深度，但大多数CPU通常都能很好地预测这种行为。使用链表会变得更有趣，特别是当你对每个列表元素进行公平处理时:

```
for (node *n = start; n; n = n->next)
  {
    ecb_prefetch (n->next, 0, 0);
    ... do medium amount of work with *n
  }
```

处理该节点后，下一个节点(部分)可能已经在缓存中.

PS: 通过对数据手工预取的方法，减少了读取延迟，从而提高了性能，但该函数也需要 CPU 的支持。 其中参数 addr 是个内存指针，它指向要预取的数据，我们人工需要判定这些数据是很快能访问到的， 或者说是它们就在最近的内存中 --- 一般来说，对于链表而言，各个节点在内存中基本上是紧挨着的，所以我们容易预取链表节点里的指针项。

```
该函数还有两个可选参数，rw 和 locality 。rw 是个编译时的常数，或 1 或 0 。1 时表示写(w)，0 时表示读(r) 。

locality 必须是编译时的常数，也称为“时间局部性”(temporal locality) 。
时间局部性是指，如果程序中某一条指令一旦执行，则不久之后该指令可能再被执行；
如果某数据被访问，则不久之后该数据会被再次访问。该值的范围在 0 - 3 之间。为 0 时表示，它没有时间局部性，
也就是说，要访问的数据或地址被访问之后的不长的时间里不会再被访问；
为 3 时表示，被访问的数据或地址具有高 时间局部性，也就是说，在被访问不久之后非常有可能再次访问；
对于值 1 和 2，则分别表示具有低 时间局部性 和中等 时间局部性。该值默认为 3 。
```

## BIT FIDDLING / BIT WIZARDRY

### bool ecb_big_endian ()
### bool ecb_little_endian ()

当字节序为大端序(最高有效字节优先)时,ecb_big_endian返回true,反之(最低有效字节优先),ecb_little_endian返回true

在两者都不存在的系统上，它们的返回值是未指定的。

### int ecb_ctz32 (uint32_t x)
### int ecb_ctz64 (uint64_t x)
### int ecb_ctz (T x) [C++]

返回`x`中bit集中的最低有效位的索引(或相当于在bit集中最低有效位之前bit值为0的位数)，从0开始。如果`x`是0，结果是没有定义的。

对于小于`uint32_t`的类型，你可以安全地使用`ecb_ctz32`。

重载的c++`ecb_ctz`函数支持`uint8_t`， `uint16_t`， `uint32_t`和`uint64_t`类型。

For example:

```
ecb_ctz32 (3) = 0 // bit:0000 0011 所以最小有效位是0
ecb_ctz32 (6) = 1 // bit:0000 0110 所以最小有效位是1
```

### bool ecb_is_pot32 (uint32_t x)
### bool ecb_is_pot64 (uint32_t x)
### bool ecb_is_pot (T x) [C++]

返回true,如果`x`是2的幂或`x == 0`。

对于小于`uint32_t`的类型，你可以安全地使用`ecb_is_pot32`。

重载的c++ `ecb_is_pot`函数支持`uint8_t`， `uint16_t`，`uint32_t`和`uint64_t`类型。

### int ecb_ld32 (uint32_t x)
### int ecb_ld64 (uint64_t x)
### int ecb_ld64 (T x) [C++]

返回`x`中最高bit集的索引，或者该数字需要的二进制位数(等于`2**ld <= x < 2**(ld+1)`)。 如果`x`是0，结果是没有定义的。 一个常见的用例是计算整数二进制对数，例如`floor (log2 (n))`，以查看某个数字需要编码多少位。

此函数类似于“count前导零位数”函数，不同之处在于该函数返回数字(在给定的数据类型中)“前面”有多少个零位数， 而`ecb_ld`返回数字本身需要多少位。

对于小于`uint32_t`的类型，你可以安全地使用`ecb_ld32`。

重载的c++ `ecb_ld`函数支持`uint8_t`， `uint16_t`，`uint32_t`和`uint64_t`类型。

### int ecb_popcount32 (uint32_t x)
### int ecb_popcount64 (uint64_t x)
### int ecb_popcount (T x) [C++]

返回`x`的bit集中为1的位数。

对于小于`uint32_t`的类型，你可以安全地使用`ecb_popcount32`。

重载的c++ `ecb_popcount`函数支持uint8_t>， `uint16_t`，uint32_t>和uint64_t>类型。

For example:

```
ecb_popcount32 (7) = 3 //0000 0111
ecb_popcount32 (255) = 8 //1111 1111
```

### uint8_t ecb_bitrev8 (uint8_t x)
### uint16_t ecb_bitrev16 (uint16_t x)
### uint32_t ecb_bitrev32 (uint32_t x)

###  T ecb_bitrev (T x) [C++]

反转x的位，即MSB变成LSB, MSB-1变成LSB+1等等。

重载的C++ `ecb_bitrev`函数支持`uint8_t`， `uint16_t`和`uint32_t`类型。

Example:

```
ecb_bitrev8 (0xa7) = 0xea // 1010 0111 => 1110 1010 
ecb_bitrev32 (0xffcc4411) = 0x882233ff // 1111 1111 1100 1100 0100 0100 0001 0001 => 1000 1000 0010 0010 0011 0011 1111 1111

/*
 * 这两个好像颠倒的不一致
 * (0xffcc4411) = 0x882233ff
 *  1111 1111 1100 1100 0100 0100 0001 0001
 *  0001 0001 0100 0100 1100 1100 1111 1111 第一步颠倒16位字节
 *  1000 1000 0010 0010 0011 0011 1111 1111 第二步每个字节颠倒
 *   8    8    2    2    3    3    f    f
 * 所以0xa7好像有问题
 * 0xa7 = ?
 * 1010 0111
 * 0111 1010
 * 1110 0101
 *  e    5
 */
```

### T ecb_bitrev (T x) [C++]

重载的C++ bitrev函数,

`T` must be one of `uint8_t`, `uint16_t` or `uint32_t`.

`T` 必须是以下类型之一: `uint8_t`, `uint16_t` or `uint32_t`.

/* * 0x11223344 => 0x44332211 */

### uint32_t ecb_bswap16 (uint32_t x)
### uint32_t ecb_bswap32 (uint32_t x)
### uint64_t ecb_bswap64 (uint64_t x)

### T ecb_bswap (T x)

这些函数返回反转16位(32位、64位)之后的值.`x`在`ecb_bswap32`中0x11223344变为0x44332211

重载的c++ `ecb_bswap`函数支持`uint8_t`， `uint16_t`，`uint32_t`和`uint64_t`类型。

### uint8_t ecb_rotl8 (uint8_t x, unsigned int count)
### uint16_t ecb_rotl16 (uint16_t x, unsigned int count)
### uint32_t ecb_rotl32 (uint32_t x, unsigned int count)
### uint64_t ecb_rotl64 (uint64_t x, unsigned int count)
### uint8_t ecb_rotr8 (uint8_t x, unsigned int count)
### uint16_t ecb_rotr16 (uint16_t x, unsigned int count)
### uint32_t ecb_rotr32 (uint32_t x, unsigned int count)
### uint64_t ecb_rotr64 (uint64_t x, unsigned int count)

这两组函数在将所有位按`count`位置向右(`ecb_rotr`)或向左(`ecb_rotl`)旋转后返回`x`的值。 对值`count`没有限制，即0和等于或大于字宽的值都是正确的。 同样，尽管`count`是无符号的，但负数也能工作并向相反的方向移动。

当前的GCC/clang版本支持这些函数，并且通常将它们编译为“最优”代码(例如，在x86上一个`rol`或一个`shld`的组合)。

### T ecb_rotl (T x, unsigned int count) [C++]

### T ecb_rotr (T x, unsigned int count) [C++]

重载C++的 rotl/rotr函数

`T` must be one of `uint8_t`, `uint16_t`, `uint32_t` or `uint64_t`. `T` 必须是以下类型以下: `uint8_t`, `uint16_t`, `uint32_t` or `uint64_t`.

## BIT MIXING, HASHING

有时候你有一个整数，想把它的位分配好，例如，把它用作哈希表中的哈希。一个常见的例子是指针值，它通常只有一个有限的范围(例如，低位和高位通常为零)。

下面的函数尝试混合比特以得到一个良好的无偏置分布。它们主要是为指针而设计的，但是底层的函数也会对整数支持的很好。

另一个好处是,函数是可逆的.如果你得到这个值的是时候只是一个hash值,你可以从hash值恢复到原来的指针,此操作在32位和64位平台上都支持. (如果发现不支持的情况,报告给我们,我们将添加其他功能位宽度)。

unmix函数要比mix函数慢一些，所以在方便的时候存储原始值也是非常可取的。

底层的算法可能会发生变化，因此目前这些函数不适合持久化哈希表，因为它们的结果值可能会在libecb的不同版本之间发生变化。

### uintptr_t ecb_ptrmix (void *ptr)

混合指针的位，结果适合于哈希表查找。换句话说，这是哈希指针值。

### uintptr_t ecb_ptrmix (T *ptr) [C++]

重载 `ecb_ptrmix`函数用来支持C++的中任何指针.

### void *ecb_ptrunmix (uintptr_t v)

将哈希值恢复为原来的指针。这只在哈希值没有被截断的情况下才有效，即你使用`uintptr_t`(或等效的)来存储它。

### T *ecb_ptrunmix<T\> (uintptr_t v) [C++]

The somewhat less useful template version of `ecb_ptrunmix` for C++. Example:

	sometype *myptr;
	uintptr_t hash = ecb_ptrmix (myptr); //得到这个指针的hash值
	sometype *orig = ecb_ptrunmix<sometype> (hash); //从这个hash值恢复到原来的指针

### uint32_t ecb_mix32 (uint32_t v)
###  uint64_t ecb_mix64 (uint64_t v)

有时你没有指针，而是一个整数，它的值分布得很糟糕。在这种情况下，你可以使用针对整数版本的相应函数。目前没有提供c++模板。

### uint32_t ecb_unmix32 (uint32_t v)
### uint64_t ecb_unmix64 (uint64_t v)

与`ecb_mix`函数相反——它们接受mixed/hashed的值并恢复原始值。

## HOST ENDIANNESS CONVERSION

### uint_fast16_t ecb_be_u16_to_host (uint_fast16_t v)
### uint_fast32_t ecb_be_u32_to_host (uint_fast32_t v)
### uint_fast64_t ecb_be_u64_to_host (uint_fast64_t v)
### uint_fast16_t ecb_le_u16_to_host (uint_fast16_t v)
### uint_fast32_t ecb_le_u32_to_host (uint_fast32_t v)
### uint_fast64_t ecb_le_u64_to_host (uint_fast64_t v)

将一个16、32或64位的无符号值从大字节或小字节顺序转换为主机字节顺序。

命名约定为`ecb_`(`be`|`le`)`_u``16|32|64``_to_host`，其中`be`和`le`分别代表大端和小端。

### uint_fast16_t ecb_host_to_be_u16 (uint_fast16_t v)
### uint_fast32_t ecb_host_to_be_u32 (uint_fast32_t v)
### uint_fast64_t ecb_host_to_be_u64 (uint_fast64_t v)
### uint_fast16_t ecb_host_to_le_u16 (uint_fast16_t v)
### uint_fast32_t ecb_host_to_le_u32 (uint_fast32_t v)
### uint_fast64_t ecb_host_to_le_u64 (uint_fast64_t v)

像上面一样，但是将_from_主机字节顺序转换为指定的字节顺序。 =back

在c++中，支持以下额外的模板函数:

### T ecb_be_to_host (T v)
### T ecb_le_to_host (T v)
### T ecb_host_to_be (T v)
### T ecb_host_to_le (T v)

这些函数的工作方式与上面的C函数类似，但使用了模板，这使得它们在泛型代码中很有用。

`T`必须是其中一个`uint8_t`， `uint16_t`， `uint32_t`或`uint64_t`(所以不像他们的C对应，有一个版本的`uint8_t`，这在通用代码中也可以是有用的)。

## UNALIGNED LOAD/STORE

这些函数加载或存储未对齐的多字节值。

### uint_fast16_t ecb_peek_u16_u (const void *ptr)
### uint_fast32_t ecb_peek_u32_u (const void *ptr)
### uint_fast64_t ecb_peek_u64_u (const void *ptr)

这些函数从内存中加载一个unaligned, unsigned 16,32或64位的值.

### uint_fast16_t ecb_peek_be_u16_u (const void *ptr)
### uint_fast32_t ecb_peek_be_u32_u (const void *ptr)
### uint_fast64_t ecb_peek_be_u64_u (const void *ptr)
### uint_fast16_t ecb_peek_le_u16_u (const void *ptr)
### uint_fast32_t ecb_peek_le_u32_u (const void *ptr)
### uint_fast64_t ecb_peek_le_u64_u (const void *ptr)

与上面类似，但在此过程中，将大端字节顺序(`be`)或小端字节顺序(`le`)转换为主机字节顺序。

### ecb_poke_u16_u (void *ptr, uint16_t v)
### ecb_poke_u32_u (void *ptr, uint32_t v)
### ecb_poke_u64_u (void *ptr, uint64_t v)

这些函数将一个非对齐、无符号的16、32或64位值存储到内存中。

### ecb_poke_be_u16_u (void *ptr, uint_fast16_t v)
### ecb_poke_be_u32_u (void *ptr, uint_fast32_t v)
### ecb_poke_be_u64_u (void *ptr, uint_fast64_t v)
### ecb_poke_le_u16_u (void *ptr, uint_fast16_t v)
### ecb_poke_le_u32_u (void *ptr, uint_fast32_t v)
### ecb_poke_le_u64_u (void *ptr, uint_fast64_t v)

与上面类似，但在此过程中还要将主机字节顺序转换为大端字节顺序(`be`)或小端字节顺序(`le`)。

在c++中，支持以下额外的模板函数:

### T ecb_peek<T\> (const void *ptr)
### T ecb_peek_be<T\> (const void *ptr)
### T ecb_peek_le<T\> (const void *ptr)
### T ecb_peek_u<T\> (const void *ptr)
### T ecb_peek_be_u<T\> (const void *ptr)
### T ecb_peek_le_u<T\> (const void *ptr)

与C语言类似，这些函数从内存中加载无符号8、16、32或64位的值，并可选地进行大/小端字节的转换。

因为不能推断类型，所以必须显式指定它，例如。

```
uint_fast16_t v = ecb_peek<uint16_t> (ptr);
```

`T` must be one of `uint8_t`, `uint16_t`, `uint32_t` or `uint64_t`.

`T` 必须是 `uint8_t`, `uint16_t`, `uint32_t` or `uint64_t`之一.

与它们的C对等体不同，这些函数支持8位数量(`uint8_t`)，并且有一个对齐的版本(没有`_u`前缀)，所有这些都希望使它们在泛型代码中更有用。

### ecb_poke (void *ptr, T v)
### ecb_poke_be (void *ptr, T v)
### ecb_poke_le (void *ptr, T v)
### ecb_poke_u (void *ptr, T v)
### ecb_poke_be_u (void *ptr, T v)
### ecb_poke_le_u (void *ptr, T v)

同样，与C语言类似，这些函数将一个无符号8、16、32或z64位的值存储到内存中，并可选地将其转换为大/小端序。

`T` must be one of `uint8_t`, `uint16_t`, `uint32_t` or `uint64_t`.

`T` 必须是 `uint8_t`, `uint16_t`, `uint32_t` or `uint64_t`之一.

与它们的C对等体不同，这些函数支持8位数量(`uint8_t`)，并且有一个对齐的版本(没有`_u`前缀)，所有这些都希望使它们在泛型代码中更有用。

## FAST INTEGER TO STRING

Libecb定义了一组非常快的整数转换为十进制字符串(或整数到ascii，short `i2a`)函数。 它们的工作原理是将整数转换为定点表示，然后依次将最上面的数字乘出来。 与其他一些同样非常快的库不同，ecb的算法应该是完全位无关的，并且不依赖于特殊的cpu函数(如clz)的存在。

有一个高级API，它接受一个`int32_t`， `uint32_t`， `int64_t`或`uint64_t`作为参数， 和一个低级API，它更难使用，但支持稍微更多的格式化选项

### HIGH LEVEL API

高级API由四个函数组成，分别为`int32_t`， `uint32_t`， `int64_t`和`uint64_t`:

Example:

```
char buf[ECB_I2A_MAX_DIGITS + 1];
char *end = ecb_i2a_i32 (buf, 17262);
*end = 0;
// buf now contains "17262"
```

### ECB_I2A_I32_DIGITS (=11)

### char *ecb_i2a_u32 (char *ptr, uint32_t value)

使用`uint32_t` _value_并将其格式化为从_ptr_开始的十进制数，最多使用`ECB_I2A_I32_DIGITS`个字符。 返回指向生成的字符串后一位指针，通常将`0`字符作为结束符。这个函数输出最小位数。

### ECB_I2A_U32_DIGITS (=10)

### char *ecb_i2a_i32 (char *ptr, int32_t value)

类似于`ecb_i2a_u32`,但是参数支持`int32_t`类型的值,如果需要,也支持负数的"-".

### ECB_I2A_I64_DIGITS (=20)

### char *ecb_i2a_u64 (char *ptr, uint64_t value)

### ECB_I2A_U64_DIGITS (=21)

### char *ecb_i2a_i64 (char *ptr, int64_t value)

与32位的类似，这些参数为64位。

### ECB_I2A_MAX_DIGITS (=21)

不使用特定于类型长度的宏，您可以只使用`ECB_I2A_MAX_DIGITS`，这对于任何`ecb_i2a`函数都足够好了。

### [](https://github.com/xvhfeng/libecb/blob/master/ecb-zh.pod#low-level-api)LOW-LEVEL API

上面的函数使用了一些低级api，这些api有一些严格的限制， 但可以用作构建块(建议学习`ecb_i2a_i32`和相关函数)。

这里有3个函数簇: 1. 数字转换为固定数量的数字与补零(`ecb_i2a_0N`, `0`前置补零), 2. 函数生成到N位,前置不不零(`_N`) 3. 函数可以产生更多的数字,但领先的数字范围有限(`_xN`)。

没有一个函数处理负数。

Example: convert an IP address in an u32 into dotted-quad:

```
uint32_t ip = 0x0a000164; // 10.0.1.100
char ips[3 * 4 + 3 + 1];
char *ptr = ips;
ptr = ecb_i2a_3 (ptr,  ip >> 24        ); *ptr++ = '.';
ptr = ecb_i2a_3 (ptr, (ip >> 16) & 0xff); *ptr++ = '.';
ptr = ecb_i2a_3 (ptr, (ip >>  8) & 0xff); *ptr++ = '.';
ptr = ecb_i2a_3 (ptr,  ip        & 0xff); *ptr++ = 0;
printf ("ip: %s\n", ips); // prints "ip: 10.0.1.100"
```

### char *ecb_i2a_02 (char *ptr, uint32_t value) // 32 bit
### char *ecb_i2a_03 (char *ptr, uint32_t value) // 32 bit
### char *ecb_i2a_04 (char *ptr, uint32_t value) // 32 bit
### char *ecb_i2a_05 (char *ptr, uint32_t value) // 64 bit
### char *ecb_i2a_06 (char *ptr, uint32_t value) // 64 bit
### char *ecb_i2a_07 (char *ptr, uint32_t value) // 64 bit
### char *ecb_i2a_08 (char *ptr, uint32_t value) // 64 bit
### char *ecb_i2a_09 (char *ptr, uint32_t value) // 64 bit

`ecb_i2a_0_N_`函数接受一个无符号的_value_并将其转换为适当的_N_位的数字， 返回一个指向数字后面第一个字符的指针。_value_必须在一个范围内。 标记为_32 bit_的函数在内部以32位进行计算，标记为_64 bit_的函数在内部使用64位整数， 这在32位体系结构上可能会很慢(高级API使用`ECB_64BIT_NATIVE`决定32位和64位版本)。

### char *ecb_i2a_2 (char *ptr, uint32_t value) // 32 bit
### char *ecb_i2a_3 (char *ptr, uint32_t value) // 32 bit
### char *ecb_i2a_4 (char *ptr, uint32_t value) // 32 bit
### char *ecb_i2a_5 (char *ptr, uint32_t value) // 64 bit
### char *ecb_i2a_6 (char *ptr, uint32_t value) // 64 bit
### char *ecb_i2a_7 (char *ptr, uint32_t value) // 64 bit
### char *ecb_i2a_8 (char *ptr, uint32_t value) // 64 bit
### char *ecb_i2a_9 (char *ptr, uint32_t value) // 64 bit

类似地，`ecb_i2a__N_`函数接受一个无符号的_value_并将其转换为最多_N_位数字， 不包含前导零，并返回一个指向数字后第一个字符的指针。

### ECB_I2A_MAX_X5 (=59074)

### char *ecb_i2a_x5 (char *ptr, uint32_t value) // 32 bit

### ECB_I2A_MAX_X10 (=2932500665)

### char *ecb_i2a_x10 (char *ptr, uint32_t value) // 64 bit

`ecb_i2a_x_N_`功能类似于`ecb_i2a__N_`功能.只要数量范围内,它们就可以生成一个数字. 这是由符号`ECB_I2A_MAX_X5`(差不多16位范围)和`ECB_I2A_MAX_X10`(31位多一点范围)。

例如，32位有符号整数的数字部分刚好适合`ECB_I2A_MAX_X10`范围， 因此尽管`ecb_i2a_x10`不能转换十进制数字，但它可以转换所有32位有符号数字。 遗憾的是，对于32位无符号数来说，它还不够好。

## FLOATING POINT FIDDLING

### ECB_INFINITY [-UECB_NO_LIBM]

测试平台是否支持正无穷叔，不支持的话,则为一个真正巨大的数字。

### ECB_NAN [-UECB_NO_LIBM]

检测平台是否支持NAN,如果支持的话,直接就是NAN,反之为`ECB_INFINITY`.

### float ecb_ldexpf (float x, int exp) [-UECB_NO_LIBM]

与`ldexpf`相同，但始终可用。

### uint32_t ecb_float_to_binary16 (float x) [-UECB_NO_LIBM]
### uint32_t ecb_float_to_binary32 (float x) [-UECB_NO_LIBM]
### uint64_t ecb_double_to_binary64 (double x) [-UECB_NO_LIBM]

这些函数都接受原生`float`或`double`类型的实参， 并返回其IEEE 754位的表示(binary16/half、binary32/single或binary64/double precision)。

位的表示就像IEEE 754定义的那样，即符号位将是最重要的位，然后是指数和尾数。

即使本机浮点格式不符合IEEE标准，这个函数也可以工作，当然速度和代码大小会受到影响， 不过这也在合理的限制内(它试图转换nan、无穷大和非法线，但可能会将负0转换为正0)。

在所有现代平台上(`ECB_STDFP`为真)，编译器应该能够完全优化掉32位和64位函数。

这些函数在序列化浮点数到网络时很有用——你可以像一个正常的uint16_t/uint32_t/uint64_t一样序列化返回值，

这些函数的另一个用途是直接操作浮点值。

不太好的例子:切换浮点数的符号位。

```
/* On gcc-4.7 on amd64, */
/*这将导致一个添加指令来切换位，和4个额外的指令来移动浮点值到一个整数寄存器并返回。*／

x = ecb_binary32_to_float (ecb_float_to_binary32 (x) ^ 0x80000000U)
```

### float ecb_binary16_to_float (uint16_t x) [-UECB_NO_LIBM]
### float ecb_binary32_to_float (uint32_t x) [-UECB_NO_LIBM]
### double ecb_binary64_to_double (uint64_t x) [-UECB_NO_LIBM]

前一个函数的反向操作-将IEEE binary16、binary32或binary64的数字(half、single或double precision)的位表示转换为原生`float`或`double`格式。

这个函数应该即使本机IEEE浮点格式不兼容问题也不大,当然速度和代码大小会变差, 但也在合理的范围内(它试图将法线和denormals,和可能幸运无穷大,和非凡的运气,也为负0)。

在所有现代平台上(`ECB_STDFP`为真)，编译器应该能够完全优化这个函数。

### uint16_t ecb_binary32_to_binary16 (uint32_t x)
### uint32_t ecb_binary16_to_binary32 (uint16_t x)

将IEEE binary32/单精度转换为binary16/半格式. 反之亦然，并且正确处理所有细节(从最接近偶数到最接近偶数、次法线、无穷大和nan)。

这些函数可以在`-DECB_NO_LIBM`下使用，因为它们不依赖于平台浮点格式。 `ecb_float_to_binary16`和`ecb_binary16_to_float`函数通常是你想要的。

## ARITHMETIC

### x = ecb_mod (m, n)

返回`m`对`n`取模，与`m`和`n`之间的除法运算的正余数相同，使用底数除法。 不像C的运算符`%`,这个函数确保返回值总是正的. 两个数字_m_和_m' = m + I * n_的结果总是与_n_的取模是相同的——换句话说,`ecb_mod`实现数学模操作,这是语言中没有的。

`n`必须是严格的正数(即`>= 1`)，而`m`必须是可负的. 也就是说，`m`和`-m`必须在其类型中是可表示的(这通常排除了最小有符号整数值，与C中`/`和`%`的限制相同)。

当前的GCC/clang版本几乎在所有的cpu上都将其编译成一个高效的无分支序列。

例如，当你想遍历一个数组的成员`m`(可能是负的)，那么你应该使用`ecb_mod`，因为`%`运算符可能会给出负的结果，或者为负值改变方向:

```
for (m = -100; m <= 100; ++m)
  int elem = myarray [ecb_mod (m, ecb_array_length (myarray))];
```

### x = ecb_div_rd (val, div)
### x = ecb_div_ru (val, div)

返回`val`除以`div`后向下四舍五入或向上四舍五入的值。 `val`和`div`必须是整数类型，`div`必须是严格正的。 注意，这些函数是用C语言的宏和c++的函数模板实现的。

## UTILITY

### element_count = ecb_array_length (name)

返回数组`name`中的元素个数。例如:

```
int primes[] = { 2, 3, 5, 7, 11 };
int sum = 0;

for (i = 0; i < ecb_array_length (primes); i++)
  sum += primes [i];
```

## SYMBOLS GOVERNING COMPILATION OF ECB.H ITSELF

在第一次包含<ecb.h\>之前，需要定义这些符号。

### ECB_NO_THREADS

如果<ecb.h\>从来没有在多线程环境中使用，那么这个符号可以被定义， 在这种情况下，内存栅栏(和类似的结构)被完全移除，导致更高效的代码和更少的依赖。

将该符号设置为真值意味着`ECB_NO_SMP`。

### ECB_NO_SMP

较弱的版本的`ECB_NO_THREADS`,如果_ecb.h_在多线程中使用, 但从未并行(例如,如果系统程序只有一个CPU上运行一个核心,没有超线程等等), 那么这个符号可以被定义,导致更高效的代码和更少的依赖关系。

### ECB_NO_LIBM

当定义为`1`时，不要导出任何可能引入依赖于数学库的函数(通常称为_-lm_)——这些函数被标记为[-UECB_NO_LIBM]。

# UNDOCUMENTED FUNCTIONALITY

_ecb.h_还有很多没有文档化的功能，其中一些仅用于内部使用，一些我们"忘记"了文档化， 一些我们隐藏了，因为我们不确定是否会保持接口稳定。

虽然欢迎您四处翻找并使用任何您认为有用的东西(我们不想阻止您). 但请记住，我们将毫不犹豫地以不兼容的方式更改未文档化的功能，而我们对已文档化的东西要保守得多。

# AUTHORS

`libecb` is designed and maintained by:

```
Emanuele Giaquinta <e.giaquinta@glauco.it>
Marc Alexander Lehmann <schmorp@schmorp.de>
```

# POD ERRORS

Hey! **The above document had some coding errors, which are explained below:**

Around line 5:

Non-ASCII character seen before =encoding in 'Libecb目前是一个简单的头文件，可以在不需要任何配置的情况下加入到你自己的项目中。'. Assuming UTF-8

Around line 787:

You forgot a '=back' before '=head2'