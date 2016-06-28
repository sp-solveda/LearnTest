
package dj.test.javalang.trycatch;

public class TestMain
{
	public void testReturnInTry(){
		System.out.println("Return in try");

		try {
			System.out.println("In try");
			System.out.println("Before return");

			return;
		} finally {
			System.out.println("In finally");
		}
	}

	public void testReturnInCatch(){
		System.out.println("Return in catch");

		try {
			System.out.println("In try");
			System.out.println("Before throw");

			throw new Exception();
		} catch (Exception e) {
			System.out.println("In catch");
			System.out.println("Before return");

			return;
		} finally {
			System.out.println("In finally");
		}
	}

	public void testBreakInTry(){
		int count, max;
		count = 0;
		max = 2;

		System.out.println("Break in try");

		do {
			try {
				System.out.println("In try " + count);

				if (count >= max) {
					System.out.println("Before break");

					break;
				}
			} finally {
				System.out.println("In finally " + count);
			}

			count++;
		} while (true);
	}

	public void testThrowInCatch() throws Exception{
		System.out.println("Throw in catch");

		try {
			System.out.println("In try");
			System.out.println("Before throw");

			throw new Exception();
		} catch (Exception e) {
			System.out.println("In catch");
			System.out.println("Before throw again");

			throw e;
		} finally {
			System.out.println("In finally");
		}
	}

	public static void main(String[] args){
		TestMain test = new TestMain();

		System.out.println("========================================");
		test.testReturnInTry();

		System.out.println("========================================");
		test.testReturnInCatch();

		System.out.println("========================================");
		test.testBreakInTry();

		System.out.println("========================================");

		try {
			test.testThrowInCatch();
		} catch (Exception e) {
			e.printStackTrace();
		}

		System.out.println("========================================");
	}
}
