package org.csapi.wsdl.parlayx.djs.sample.ext.wappush.v1_0._interface;

import javax.jws.WebMethod;
import javax.jws.WebParam;
import javax.jws.WebResult;
import javax.jws.WebService;
import javax.xml.bind.annotation.XmlSeeAlso;
import javax.xml.ws.RequestWrapper;
import javax.xml.ws.ResponseWrapper;

/**
 * This class was generated by Apache CXF 2.4.4
 * 2011-11-10T10:21:50.647+08:00
 * Generated source version: 2.4.4
 * 
 */
@WebService(targetNamespace = "http://www.csapi.org/wsdl/parlayx/djs/sample/ext/wappush/v1_0/interface", name = "ExtWapPush")
@XmlSeeAlso({org.csapi.schema.parlayx.common.v2_1.ObjectFactory.class, org.csapi.schema.parlayx.djs.sample.ext.wappush.v1_0.local.ObjectFactory.class, org.csapi.schema.parlayx.djs.sample.ext.wappush.v1_0.ObjectFactory.class})
public interface ExtWapPush {

    @WebResult(name = "wapPushResponse", targetNamespace = "http://www.csapi.org/schema/parlayx/djs/sample/ext/wappush/v1_0/local")
    @RequestWrapper(localName = "sendWapPush", targetNamespace = "http://www.csapi.org/schema/parlayx/djs/sample/ext/wappush/v1_0/local", className = "org.csapi.schema.parlayx.djs.sample.ext.wappush.v1_0.local.SendWapPush")
    @WebMethod
    @ResponseWrapper(localName = "sendWapPushResponse", targetNamespace = "http://www.csapi.org/schema/parlayx/djs/sample/ext/wappush/v1_0/local", className = "org.csapi.schema.parlayx.djs.sample.ext.wappush.v1_0.local.SendWapPushResponse")
    public org.csapi.schema.parlayx.djs.sample.ext.wappush.v1_0.WapPushRespData sendWapPush(
        @WebParam(name = "wapPushRequest", targetNamespace = "http://www.csapi.org/schema/parlayx/djs/sample/ext/wappush/v1_0/local")
        org.csapi.schema.parlayx.djs.sample.ext.wappush.v1_0.WapPushReqData wapPushRequest
    ) throws org.csapi.wsdl.parlayx.common.v2_0.faults.PolicyException, org.csapi.wsdl.parlayx.common.v2_0.faults.ServiceException;
}
