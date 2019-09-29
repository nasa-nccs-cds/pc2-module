from pc2base.module.handler.base import Module, TaskHandle, Status, TaskResult, CelerySyncTaskHandle
from pc2base.module.util.config import PC2Logger
from typing import Sequence, List, Dict, Mapping, Optional, Any, Union, Iterable
import traceback, atexit, xarray as xa

def ensureIterable( obj: Any ) -> Iterable:
    try: iter(obj)
    except TypeError: return [obj]
    return obj

class DemoModule(Module):

    def __init__(self, **kwargs ):
        super(DemoModule, self).__init__()
        self.logger = PC2Logger.getLogger()
        self.process = "demo"
        self.handlers = {}
        self.processManager = None
        self._epas = [ "demo*" ]
        atexit.register( self.shutdown, "ShutdownHook Called" )

    def epas( self ) -> List[str]: return self._epas

    def init( self ):
        pass

    def capabilities(self, type: str, **kwargs  ) -> Dict:
        if type == "epas":
            return dict( epas = self._epas )
        else: raise Exception( f"Unknown capabilities type: {type}" )

    def addHandler(self, submissionId, handler ):
        self.handlers[ submissionId ] = handler
        return handler

    def removeHandler(self, submissionId ):
        try:
            del self.handlers[ submissionId ]
        except:
            self.logger.error( "Error removing handler: " + submissionId + ", existing handlers = " + str(self.handlers.keys()))

    def defaultResponseType( self, runargs:  Dict[str, Any] )-> str:
         status = bool(str(runargs.get("status","false")))
         return "file" if status else "xml"

    def sendErrorReport( self, clientId: str, responseId: str, msg: str ):
        self.logger.info("@@Portal-----> SendErrorReport[" + clientId +":" + responseId + "]: " + msg )

    def sendFile( self, clientId: str, jobId: str, name: str, filePath: str, sendData: bool ):
        self.logger.debug( "@@Portal: Sending file data to client for {}, filePath={}".format( name, filePath ) )

    def request( self, requestSpec: Dict, inputs: Union[TaskResult,List[TaskResult]] = None, **kwargs ) -> TaskHandle:
        inputList: List[TaskResult] = ensureIterable( inputs )
        self.logger.info(f"Executing DemoModule, NINputs = {len(inputList)}")
        for result in inputList:
            dsets: List[xa.Dataset] = result.data
            self.logger.info(f"Completed Request, NResults = {len(dsets)}")
            for index, dset in enumerate(dsets):
                fileName = f"/tmp/edas_endpoint_test_result-{index}.nc"
                self.logger.info(f"Got result[{index}]: Saving to file {fileName}, Variables: ")
                for vname in dset.variables:
                    self.logger.info(f"   -> Variable[{vname}]: Shape = {dset[vname].shape}")
                dset.to_netcdf(fileName)
        return CelerySyncTaskHandle( inputList[0] )

    def shutdown( self, *args, **kwargs ):
        self.logger.info( "Shutdown: " + str(args) )



