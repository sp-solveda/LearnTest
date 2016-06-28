
package com.djs.test.spring_sample;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

import com.djs.test.spring_sample.greeting.GreetingService;
import com.djs.test.spring_sample.knightI.Knight;

public class AppMain
{
	public static void main( String [] args ) throws Exception
	{
		// Notes: AOP doesn't work while using XmlBeanFactory!
		// BeanFactory factory = new XmlBeanFactory( new FileSystemResource( "application-context.xml" ) );
		// BeanFactory factory = new XmlBeanFactory( new ClassPathResource( "application-context.xml" ) );

		ApplicationContext appContext = new ClassPathXmlApplicationContext( new String []
		{ "greeting.xml", "knight.xml", "music.xml", "db.xml" } );

		GreetingService greetingService = (GreetingService)appContext.getBean( "greetingService" );
		greetingService.sayGreeting();

		Knight knightA = (Knight)appContext.getBean( "knightA" );
		knightA.embarkOnQuest();

		Knight knightB = (Knight)appContext.getBean( "knightB" );
		knightB.embarkOnQuest();
	}
}
