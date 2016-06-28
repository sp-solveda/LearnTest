
package com.djs.test.helloworld;

import javax.jws.WebMethod;
import javax.jws.WebService;

import org.apache.log4j.Logger;

/*
 * http://localhost:8088/WsTomcatSample1/hello
 */
@WebService()
public class HelloWorld
{
	public static Logger log = Logger.getLogger(HelloWorld.class);

	@WebMethod()
	public String sayHello(String name)
	{
		if (log.isInfoEnabled())
		{
			log.info("Hello: " + name);
		}

		return "Hello " + name + "!";
	}
}
