
package dj.test.javalang.locale;

import java.util.ListResourceBundle;

public class NumberBundle extends ListResourceBundle
{
	@Override
	public Object[][] getContents(){
		return contents;
	}

	private Object[][] contents = {{"A", new Integer(102030)}, {"B", new Float(0.10203)}};
}
