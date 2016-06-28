package com.djs.test.wsclient.example_test;

import javax.jws.WebMethod;
import javax.jws.WebParam;
import javax.jws.WebResult;
import javax.jws.WebService;
import javax.jws.soap.SOAPBinding;
import javax.xml.bind.annotation.XmlSeeAlso;

/**
 * This class was generated by Apache CXF 2.4.4
 * 2011-11-10T11:36:22.971+08:00
 * Generated source version: 2.4.4
 * 
 */
@WebService(targetNamespace = "http://singtel.com/ndp/ext/example_test/v1_0/interface", name = "SendDataPort")
@XmlSeeAlso({org.csapi.schema.parlayx.common.v2_1.ObjectFactory.class, ObjectFactory.class})
@SOAPBinding(parameterStyle = SOAPBinding.ParameterStyle.BARE)
public interface SendDataPort {

    @WebResult(name = "sendDataResponse", targetNamespace = "http://singtel.com/schema/example_test/local", partName = "result")
    @WebMethod
    public SendDataResponse sendData(
        @WebParam(partName = "parameters", name = "sendDataRequest", targetNamespace = "http://singtel.com/schema/example_test/local")
        SendDataRequest parameters
    ) throws ServiceException, PolicyException;
}
