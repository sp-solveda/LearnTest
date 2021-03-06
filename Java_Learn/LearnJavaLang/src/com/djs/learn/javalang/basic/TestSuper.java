
package com.djs.learn.javalang.basic;

/**
 * <pre>
============================================================
com.djs.learn.javalang.basic.InnerA:InnerA
com.djs.learn.javalang.basic.OuterA:OuterA
--------------------
com.djs.learn.javalang.basic.InnerA:InnerA
com.djs.learn.javalang.basic.OuterA:OuterA:123
--------------------
com.djs.learn.javalang.basic.InnerA:InnerA
com.djs.learn.javalang.basic.InnerA:InnerA:Ok
com.djs.learn.javalang.basic.OuterA:OuterA:Ok
--------------------
com.djs.learn.javalang.basic.InnerB:InnerB:Hello
com.djs.learn.javalang.basic.OuterB:OuterB:Hello
============================================================
 * </pre>
 */
public class TestSuper
{
	public void testInit(){
		new OuterA();

		System.out.println("--------------------");

		new OuterA(123);

		System.out.println("--------------------");

		new OuterA("Ok");

		System.out.println("--------------------");

		new OuterB();
	}

	public static void main(String[] args){
		TestSuper testMain = new TestSuper();

		System.out.println("============================================================");

		testMain.testInit();

		System.out.println("============================================================");
	}
}

class InnerA
{
	public InnerA(){
		System.out.println(InnerA.class.getName() + ":InnerA");
	}

	public InnerA(String msg){
		this();
		System.out.println(InnerA.class.getName() + ":InnerA:" + msg);
	}
}

class InnerB
{
	public InnerB(String msg){
		System.out.println(InnerB.class.getName() + ":InnerB:" + msg);
	}
}

class OuterA extends InnerA
{
	public OuterA(){
		System.out.println(OuterA.class.getName() + ":OuterA");
	}

	public OuterA(int i){
		System.out.println(OuterA.class.getName() + ":OuterA:" + i);
	}

	public OuterA(String msg){
		super(msg);
		System.out.println(OuterA.class.getName() + ":OuterA:" + msg);
	}
}

class OuterB extends InnerB
{
	public OuterB(){
		super("Hello");
		System.out.println(OuterB.class.getName() + ":OuterB:Hello");
	}
}
