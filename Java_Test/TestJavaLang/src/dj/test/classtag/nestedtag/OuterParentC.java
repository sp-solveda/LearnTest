
package dj.test.classtag.nestedtag;

public class OuterParentC
{
	int count = 0;

	public OuterParentC(){
		System.out.println("OuterParentC:OuterParentC");
	}

	public int getCount(){
		System.out.println("OuterParentC:getCount");

		return ++count;
	}

	public void printCount(){
		System.out.println("OuterParentC:printCount");
		System.out.println("Count = " + count);
	}

	public void testLocalClass(final int age){ // Must be final to be used by local class.
		System.out.println("OuterParentC:testLocalClass");

		// Must be final to be used by local class.
		final int score = 80;

		int year = 2015;

		// Illegal. No static for inner class.
		// static int age = 0;

		class LocalParentC
		{
			// If name as "count", it will hide the one in outer class.
			int count2 = 10;

			// Illegal. No static for inner class.
			// static int age = 0;

			void printCount(){
				System.out.println("OuterParentC.LocalParentC:printCount");
				System.out.println("Param out = " + count);
				System.out.println("Param Local = " + count2);
				System.out.println("Param method input = " + age);
				System.out.println("Param method = " + score);
				// Illegal. Cannot see non-final method param.
				// System.out.println("Param method = " + year);
			}

			void testOuterClass(){
				System.out.println("OuterParentB.LocalParentA:testOuterClass");

				new OuterParentC().printCount();
			}
		}

		new LocalParentC().printCount();

		System.out.println("----------");

		new LocalParentC().testOuterClass();
	}
}
