
package com.djs.test.maven_sample;

import java.net.URL;
import java.util.ArrayList;
import java.util.List;

import javax.xml.namespace.QName;
import javax.xml.ws.handler.Handler;
import javax.xml.ws.handler.HandlerResolver;
import javax.xml.ws.handler.PortInfo;

import org.apache.log4j.Logger;

import com.singtel.ndp.ext.example_test.v1_0.service.PolicyException;
import com.singtel.ndp.ext.example_test.v1_0.service.SendDataPort;
import com.singtel.ndp.ext.example_test.v1_0.service.SendDataService;
import com.singtel.ndp.ext.example_test.v1_0.service.ServiceException;
import com.singtel.schema.example_test.local.SendDataRequest;
import com.singtel.schema.example_test.local.SendDataResponse;

public class BExampleTestTest
{
	private static Logger log = Logger.getLogger( BExampleTestTest.class );

	private SendDataPort api = null;

	// @Before
	public void setUp() throws Exception
	{
		String urlPart = "example_test/SendDataPort";
		SendDataService svc = null;

		try
		{
			svc =
			      new SendDataService( new URL( GeneralDefines.makeWsdlUrl( urlPart ) ), new QName( "http://singtel.com/ndp/ext/example_test/v1_0/service",
			              "SendDataService" ) );

			svc.setHandlerResolver( new HandlerResolver()
			{
				@Override
				public List<Handler> getHandlerChain( PortInfo portInfo )
				{
					List<Handler> handlerList = new ArrayList<Handler>();
					handlerList.add( new LoginSoapHandler() );
					handlerList.add( new SessionSoapHandler() );

					return handlerList;
				}
			} );

			api = svc.getSendDataPort();
		}
		catch (Exception e)
		{
			if (e instanceof ServiceException)
			{
				InfoHelper.showException( log, "", ((ServiceException)e).getFaultInfo() );
			}
			else if (e instanceof PolicyException)
			{
				InfoHelper.showException( log, "", ((PolicyException)e).getFaultInfo() );
			}
			else
			{
				InfoHelper.showException( log, "", e );
			}
		}
	}

	// @Ignore("Ignored")
	// @Test
	public void testSendData()
	{
		SendDataRequest request = null;
		SendDataResponse response = null;

		try
		{
			request = new SendDataRequest();

			request.setData( "6512345678" );
			request.setAddress( "tel:6512345678" );

			log.debug( "Data: " + request.getData() );
			log.debug( "Address: " + request.getAddress() );

			response = api.sendData( request );

			log.debug( "Response: " + response );
		}
		catch (Exception e)
		{
			if (e instanceof ServiceException)
			{
				InfoHelper.showException( log, "", ((ServiceException)e).getFaultInfo() );
			}
			else if (e instanceof PolicyException)
			{
				InfoHelper.showException( log, "", ((PolicyException)e).getFaultInfo() );
			}
			else
			{
				InfoHelper.showException( log, "", e );
			}
		}
	}
}
