
class CameraException(ValueError):
    def __init__(self, sdk=None, message="", code=0x00160000):
        if len(message) and code:
            self.message = "CameraException {}: {}".format(hex(0xFFFFFFFF & code), message)
        if len(message) and not code:
            self.message = "CameraException: {}".format(message)
        if not len(message) and code:
            from pco.sdk import Sdk
            if isinstance(sdk, Sdk):
                self.message = "CameraException {}: {}".format(hex(0xFFFFFFFF & code), sdk.get_error_text(code))
            else:
                self.message = "CameraException {}".format(hex(0xFFFFFFFF & code))

        if not len(message) and not code:
            self.message = "CameraException has been raised without error code or message."
        
        self._code = code
        super().__init__(self.message)
    
    @property
    def error_code(self):
        return self._code

class XCiteException(ValueError):
    def __init__(self, sdk=None, message="", code=0x00160000):
        if len(message) and code:
            self.message = "CameraException {}: {}".format(hex(0xFFFFFFFF & code), message)
        if len(message) and not code:
            self.message = "XCiteException: {}".format(message)
        if not len(message) and code:
            from pco.sdk import Sdk
            if isinstance(sdk, Sdk):
                self.message = "XCiteException {}: {}".format(hex(0xFFFFFFFF & code), sdk.get_error_text(code))
            else:
                self.message = "XCiteException {}".format(hex(0xFFFFFFFF & code))

        if not len(message) and not code:
            self.message = "XCiteException has been raised without error code or message."
        
        self._code = code
        super().__init__(self.message)
    
    @property
    def error_code(self):
        return self._code
    