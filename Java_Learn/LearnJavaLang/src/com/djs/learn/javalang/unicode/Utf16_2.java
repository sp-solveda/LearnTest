package com.djs.learn.javalang.unicode;
import java.util.Arrays;

public class Utf16_2
{
	public void test()
	{
		try
		{
			byte [] byayData = new byte []
			{ 78, 0, 78, -116, 78, 9, 86, -37, 78, -108, 81, 109, 78, 3, 81, 107, 78, 93, 83, 65 };
			String szData1 = new String( byayData, "UTF-8" );
			String szData2 = new String( byayData, "UTF-16" );

			System.out.println();
			System.out.println( "bytes (length) = (" + byayData.length + ") " + Arrays.toString( byayData ) );
			System.out.println( "-> string (UTF-8)  (length) = (" + szData1.length() + ") " + szData1 );
			System.out.println( "-> string (UTF-16) (length) = (" + szData2.length() + ") " + szData2 );

			System.out.println( "----------------------------------------" );
		}
		catch (Exception e)
		{
			System.err.println( "Exception =" + e );
		}

		/*
		bytes (length) = (20) [78, 0, 78, -116, 78, 9, 86, -37, 78, -108, 81, 109, 78, 3, 81, 107, 78, 93, 83, 65]
		-> string (UTF-8)  (length) = (20) N N�N	V�N�QmNQkN]SA
		-> string (UTF-16) (length) = (10) 一二三四五六七八九十
		 */
	}
}
