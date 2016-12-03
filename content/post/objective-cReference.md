+++
title       = "Objective-C 语法总结"
categories  = ["Miscellaneous"]
tags        = ["Objective-C"]
date        = "2014-05-04"
+++

最近在学习 Objective-C。产生学习 Objective-C 的想法已经很久了，但是以前每次看到 Objective-C 代码就会觉得语法非常奇怪，于是学习的动力就受到的打击。恰逢放假，可以平心静气地学习 Objective-C。

在看过了 Objective-C 的基本语法之后，明白了为什么之前会觉得 Objective-C 的语法奇怪。绝大部分的面向对象的程序语言，包括 C++、Java、Python 等在调用方法的格式都是 `object.method(argument1, argument2...)`。然而 Objective-C 的格式却是 `[object method: argument1 andArg: argument2...]`。所以长期使用 C++, Java 的程序员在第一次看到 Objective-C 代码时，对这些语法肯定有一些不适应。但是适应这些语法并仔细研究之后感觉 Objective-C 的语法也有它的优点。
<!--more-->

----
废话不多说，上干货。下面以 Java 作比对，总结一下 Objective-C 的语法。

### 1. 基本语法

#### 1.1 创建对象

**Java:**

```
obj = new MyClass();
```

**Objective-C:**

```
MyClass *obj = [[MyClass alloc] init];
```

#### 1.2 调用方法
**Java:**

```
obj.method1() // 没有参数
obj.method2(arg1) // 一个参数
obj.method3(arg1,arg2) // 多个参数
```

**Objective-C:**

```
[obj method1] // 没有参数
[obj method2:arg1] // 一个参数
[obj method3:arg2 andArg: arg2] // 多个参数
```

### 2. 类的定义
**Java:**

```
public class MyClass extend SuperClass {

    private int attr1;

    public void method1() {
        ...
    }
}
```

**Objective-C:**

Objectove-C 定义一个类时需要两个文件，分别是负责声明的 Header File 和负责具体实现的 Implementation File。

MyClass.h

```
@interface MyClass : SuperClass
{
    int attr1;
}
- (void) method1;
- (void) method2: int arg1;
- (void) method3: int arg1 andArg: (NSString *) arg2;
+ (void) classMethod; // 相当于 Java 中的 static 方法
@end
```

MyClass.m

```
#import"MyClass.h"
@implementation MyClass
- (void) method1
{
    ...
}
...
@end
```

此外，Objective-C 还有一个非常方便的 “语法糖”——`@property` 和 `@synthesize` 两个关键字。使用这两个关键字之后可以让编译好器自动编写一个与数据成员同名的方法声明从而省去读写方法的声明。
在头文件中加上 `@property int attr1;` 就等同于声明了两个方法：

```
	- (int)attr1;
	- (void)setAttr1:(int)newAttr1;
```

实现文件里加上 `@synthesize attr1;` 就等同于定义了两个方法：

```
- (int)attr1
{
	return attr1;
}
-(void)setAttr1:(int)newAttr1
{
   	attr1 = newAttr1;
}
```

### 3. 协议（接口）的定义
**Java:**
定义接口

```
public interface MyInterface {
	public void aInterfaceMethod();
	public void anotherInterfaceMethod();
}
```

实现接口

```
public class MyClass extend SuperClass implements MyInterface {
	// method declarations
}
```

**Objective-C:**
在 Objective-C 中，用关键字 `@protocol` 定义协议，也就是 Java 中的接口。

```
@protocol MyProtocol
- (void) aProtocolMethod;
- (void) anotherProcotolMethod;
@end
```

当一个类需要实现协议时，

```
#import "MyProtocol.h"
@interface MyClass : SuperClass <MyProtocol, AnotherProtocol>
	// method declarations
@end
```

-------
由于我也是初学 Objective-C，难免有错误和总结不全面的地方，恳请指正。