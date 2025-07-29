import grpc
import os
import Oasys.gRPC

class Connection():

    def __init__(self, program, port, memory, hostname, debug=False):
        self.debug = debug

        self.dbg("Connecting to {} at {}:{}".format(program, hostname, port))

        self.program  = program
        self.hostname = hostname
        self.channel  = grpc.insecure_channel('{}:{}'.format(hostname, port))
        self.stub     = Oasys.gRPC.oasys_pb2_grpc.InterfaceStub(self.channel)
        self.build    = None
        self.version  = None
        self.dtor_h   = []
        self.dtor_s   = 50000
        if 'OASYS_PYTHON_DTOR_SIZE' in os.environ:
            try:
                self.dtor_s = int(os.environ['OASYS_PYTHON_DTOR_SIZE'])
            except:
                print("Invalid OASYS_PYTHON_DTOR_SIZE environment variable. Ignoring")

# Initialise
        request = Oasys.gRPC.oasys_pb2.Memory()
        request.size = memory
        self.dbg("Calling Initialise")
        response = self.stub.Initialise(request)

        self.dbg("Returned {} '{}' ({} bytes)".format(response.status, response.message, response.ByteSize()))
        assert response.status == Oasys.gRPC.oasys_pb2.STATUS_OK, response.message

        if response.value.HasField("dictarg"):
            dict = self.decode_dictarg(response.value.dictarg)
            self.version = dict.get('version')
            self.build   = dict.get('build')

        self.dbg("Connected to {} version {} build {}".format(self.program, self.version, self.build))

    def constructor(self, objtype, *args):
# Constructor
        request = Oasys.gRPC.oasys_pb2.ConstructorRequest()
        request.type = objtype


        self.dbg("Calling {} Constructor with {} args".format(request.type, len(args)))

        nargs = self.count_args(args)
        self.dbg("{} non default args".format(nargs))

        for a in range(nargs):
            self.add_request_arg(request, args[a])

        response = self.stub.Constructor(request)
        self.dbg("Returned {} '{}' ({} bytes)".format(response.status, response.message, response.ByteSize()))

        assert response.status == Oasys.gRPC.oasys_pb2.STATUS_OK, response.message
        assert response.value.HasField("itemarg"), "Constructor has not returned an item"
        self.dbg("Value {} handle {}".format(response.value.itemarg.t, response.value.itemarg.h))

        return response.value.itemarg.h


    def destructor(self, objtype, handle):
# Destructor

# Doing a gRPC request for every destructor is glacially slow because of the amount of "round trips" required.
# We buffer the handles to destroy and only do a request once we have a sufficient number
        self.dtor_h.append(handle)
        if len(self.dtor_h) < self.dtor_s:
            return

        request = Oasys.gRPC.oasys_pb2.DestructorRequest()

        request.h.extend(self.dtor_h)

        self.dbg("Calling Destructor with {} handles".format(len(self.dtor_h)))

        response = self.stub.Destructor(request)
        self.dbg("Returned {} '{}' ({} bytes)".format(response.status, response.message, response.ByteSize()))

        assert response.status == Oasys.gRPC.oasys_pb2.STATUS_OK, response.message
        self.dtor_h.clear()


    def functionCall(self, func, *args):
# Function call
        request = Oasys.gRPC.oasys_pb2.FunctionRequest()
        request.func = func


        self.dbg("Calling Function {} with {} args".format(func, len(args)))

        nargs = self.count_args(args)
        self.dbg("{} non default args".format(nargs))

        for a in range(nargs):
            self.add_request_arg(request, args[a])

        response = self.stub.Function(request)
        self.dbg("Returned {} '{}' ({} bytes)".format(response.status, response.message, response.ByteSize()))

        assert response.status == Oasys.gRPC.oasys_pb2.STATUS_OK, response.message

# Decode the response value
        return self.decode_response_value(response.value)


    def instanceGetter(self, objtype, handle, name):
# Getter
        request = Oasys.gRPC.oasys_pb2.InstanceGetRequest()

        request.item.t   = objtype
        request.item.h   = handle
        request.property = name

        self.dbg("Calling {} Getter with handle {} property {}".format(objtype, handle, name))

        response = self.stub.InstanceGet(request)
        self.dbg("Returned {} '{}' ({} bytes)".format(response.status, response.message, response.ByteSize()))

        assert response.status == Oasys.gRPC.oasys_pb2.STATUS_OK, response.message

# Decode the response value
        return self.decode_response_value(response.value)


    def instanceSetter(self, objtype, handle, name, value):
# Setter
        request = Oasys.gRPC.oasys_pb2.InstanceSetRequest()

        request.item.t   = objtype
        request.item.h   = handle
        request.property = name

        self.encode_request_value(request, value)

        self.dbg("Calling {} Setter with handle {} property {}={}".format(objtype, handle, name, value))

        response = self.stub.InstanceSet(request)
        self.dbg("Returned {} '{}' ({} bytes)".format(response.status, response.message, response.ByteSize()))

        assert response.status == Oasys.gRPC.oasys_pb2.STATUS_OK, response.message


    def instanceMethod(self, objtype, handle, method, *args):
# Instance Method call
        request = Oasys.gRPC.oasys_pb2.InstanceMethodRequest()

        request.item.t = objtype
        request.item.h = handle
        request.method = method

        self.dbg("Calling {} with handle {} Instance method {} with {} args".format(objtype, handle, method, len(args)))

        nargs = self.count_args(args)
        self.dbg("{} non default args".format(nargs))

        for a in range(nargs):
            self.add_request_arg(request, args[a])

        response = self.stub.InstanceMethod(request)
        self.dbg("Returned {} '{}' ({} bytes)".format(response.status, response.message, response.ByteSize()))

        assert response.status == Oasys.gRPC.oasys_pb2.STATUS_OK, response.message

# Decode the response value
        return self.decode_response_value(response.value)


    def instanceMethodStream(self, objtype, handle, method, *args):
# Instance Method call
        request = Oasys.gRPC.oasys_pb2.InstanceMethodRequest()

        request.item.t = objtype
        request.item.h = handle
        request.method = method

        self.dbg("Calling {} with handle {} Instance streaming method {} with {} args".format(objtype, handle, method, len(args)))

        nargs = self.count_args(args)
        self.dbg("{} non default args".format(nargs))

        for a in range(nargs):
            self.add_request_arg(request, args[a])

        d = b''
        l = 0
        t = -1

        self.dbg("Starting for/in stream response loop")
        for stream_response in self.stub.InstanceMethodStream(request):
            self.dbg("Returned {} '{}' ({} bytes)".format(stream_response.status, stream_response.message, stream_response.ByteSize()))
            self.dbg("         total size {}".format(stream_response.size))
            self.dbg("         data size {}".format(len(stream_response.data)))

            l += len(stream_response.data)
            d = d + stream_response.data
            if t == -1:
                t = stream_response.size

            self.dbg("         current size {}".format(len(d)))

            assert stream_response.status == Oasys.gRPC.oasys_pb2.STATUS_OK, stream_response.message

        self.dbg("Finished for/in stream response loop")

# Check the stream length is correct
        assert l == t, "Stream size incorrect. Expected {} bytes, got {}".format(t, l)

# Deserialize the response
        response = Oasys.gRPC.oasys_pb2.Response()
        response.ParseFromString(d)

# Decode the response value
        return self.decode_response_value(response.value)



    def classGetter(self, objtype, name):
# Getter
        request = Oasys.gRPC.oasys_pb2.ClassGetRequest()

        request.type     = objtype
        request.property = name

        self.dbg("Calling {} Class Getter with property {}".format(objtype, name))

        response = self.stub.ClassGet(request)
        self.dbg("Returned {} '{}' ({} bytes)".format(response.status, response.message, response.ByteSize()))

        assert response.status == Oasys.gRPC.oasys_pb2.STATUS_OK, response.message

# Decode the response value
        return self.decode_response_value(response.value)


    def classSetter(self, objtype, name, value):
# Setter
        request = Oasys.gRPC.oasys_pb2.ClassSetRequest()

        request.type     = objtype
        request.property = name

        self.encode_request_value(request, value)

        self.dbg("Calling {} Class Setter with property {}={}".format(objtype, name, value))

        response = self.stub.ClassSet(request)
        self.dbg("Returned {} '{}' ({} bytes)".format(response.status, response.message, response.ByteSize()))

        assert response.status == Oasys.gRPC.oasys_pb2.STATUS_OK, response.message


    def classMethod(self, objtype, method, *args):
# Class Method call
        request = Oasys.gRPC.oasys_pb2.ClassMethodRequest()

        request.type   = objtype
        request.method = method

        self.dbg("Calling {} Class method {} with {} args".format(objtype, method, len(args)))

        nargs = self.count_args(args)
        self.dbg("{} non default args".format(nargs))

        for a in range(nargs):
            self.add_request_arg(request, args[a])

        response = self.stub.ClassMethod(request)
        self.dbg("Returned {} '{}' ({} bytes)".format(response.status, response.message, response.ByteSize()))

        assert response.status == Oasys.gRPC.oasys_pb2.STATUS_OK, response.message

# Decode the response value
        return self.decode_response_value(response.value)


    def classMethodStream(self, objtype, method, *args):
# Class Method streaming call
        request = Oasys.gRPC.oasys_pb2.ClassMethodRequest()

        request.type   = objtype
        request.method = method

        self.dbg("Calling {} Class streaming method {} with {} args".format(objtype, method, len(args)))

        nargs = self.count_args(args)
        self.dbg("{} non default args".format(nargs))

        for a in range(nargs):
            self.add_request_arg(request, args[a])

        d = b''
        l = 0
        t = -1

        self.dbg("Starting for/in stream response loop")
        for stream_response in self.stub.ClassMethodStream(request):
            self.dbg("Returned {} '{}' ({} bytes)".format(stream_response.status, stream_response.message, stream_response.ByteSize()))
            self.dbg("         total size {}".format(stream_response.size))
            self.dbg("         data size {}".format(len(stream_response.data)))

            l += len(stream_response.data)
            d = d + stream_response.data
            if t == -1:
                t = stream_response.size

            self.dbg("         current size {}".format(len(d)))

            assert stream_response.status == Oasys.gRPC.oasys_pb2.STATUS_OK, stream_response.message

        self.dbg("Finished for/in stream response loop")

# Check the stream length is correct
        assert l == t, "Stream size incorrect. Expected {} bytes, got {}".format(t, l)

# Deserialize the response
        response = Oasys.gRPC.oasys_pb2.Response()
        response.ParseFromString(d)

# Decode the response value
        return self.decode_response_value(response.value)


    def finalise(self):
# Finalise
        noarg = Oasys.gRPC.oasys_pb2.NoArg()
        self.dbg("Calling Finalise")
        response = self.stub.Finalise(noarg)
        self.dbg("Returned {} '{}'".format(response.status, response.message))
        self.stub    = None
        self.channel = None


    def terminate(self):
# Close connection and terminate process
        noarg = Oasys.gRPC.oasys_pb2.NoArg()
        self.dbg("Calling Terminate")
        response = self.stub.Exit(noarg)
        self.dbg("Returned {} '{}'".format(response.status, response.message))
        self.stub    = None
        self.channel = None


    def count_args(self, args):
# Count the number of arguments in the gRPC request
# Arguments that have not been given will have the value Oasys.gRPC.defaultArg
# args is a tuple containing the arguments to check
        nargs = len(args)
        if nargs == 0:
            return 0

        for a in range(nargs, 0, -1):
# If the arg is a tuple then it must be the last arg (for varargs).
# If the length of the tuple is 0 then don't send it
            if isinstance(args[a-1], tuple) and len(args[a-1]) == 0:
                self.dbg("Argument {} is an empty (varargs) tuple. Skipping".format(a))
                return a-1
# Skip any trailing default args
            elif args[a-1] is not Oasys.gRPC.defaultArg:
                return a
            self.dbg("Argument {} is default value. Skipping".format(a))

# All the arguments are the default value so return 0
        return 0


    def add_request_arg(self, request, arg):
# Add an argument to the gRPC request
# The request can have multiple arguments
        newarg = request.args.add()

        self.add_request_arg_data(arg, newarg)


    def add_request_arg_data(self, arg, oneof):
# Add an argument to the gRPC request
# The request can have multiple arguments

        if arg is None:
            oneof.nullarg.n = True
        elif arg is Oasys.gRPC.defaultArg:
            oneof.nullarg.n = True
        elif isinstance(arg, bool):
            oneof.boolarg.b = arg
        elif isinstance(arg, int):
            oneof.intarg.i = arg
        elif isinstance(arg, float):
            oneof.dblarg.d = arg
        elif isinstance(arg, str):
            oneof.strarg.s = arg
        elif isinstance(arg, dict):
            if len(arg) == 0:
                oneof.edctarg.e = True
                return

            for key in arg:
                self.dbg("dict {}={} ({})".format(key, arg[key], type(arg[key])))
                if arg[key] is None:
                    oneof.dictarg.d[key].nullarg.n = True
                elif isinstance(arg[key], bool):
                    oneof.dictarg.d[key].boolarg.b = arg[key]
                elif isinstance(arg[key], int):
                    oneof.dictarg.d[key].intarg.i = arg[key]
                elif isinstance(arg[key], float):
                    oneof.dictarg.d[key].dblarg.d = arg[key]
                elif isinstance(arg[key], str):
                    oneof.dictarg.d[key].strarg.s = arg[key]
                elif isinstance(arg[key], Oasys.gRPC.OasysItem):
                    oneof.dictarg.d[key].itemarg.t = arg[key]._objtype
                    oneof.dictarg.d[key].itemarg.h = arg[key]._handle
                elif isinstance(arg[key], list):
                    lst = arg[key]
                    for index in range(len(lst)):
                        self.dbg("dict->list {}={} ({})".format(index, lst[index], type(lst[index])))
                        val = oneof.dictarg.d[key].listarg.values.add()
                        self.add_request_arg_data(lst[index], val)
                elif isinstance(arg[key], dict):
                    dct = arg[key]
                    for ky in dct:
                        self.dbg("dict->dict {}={} ({})".format(ky, dct[ky], type(dct[ky])))
                        self.add_request_arg_data(dct[ky], oneof.dictarg.d[key].dictarg.d[ky])
                else:
                    raise NotImplementedError("Unsupported dict type {}".format(type(arg[key])))
        elif isinstance(arg, list):
            if len(arg) == 0:
                oneof.elstarg.e = True
                return

            for index in range(len(arg)):
                self.dbg("list {}={} ({})".format(index, arg[index], type(arg[index])))

                value = oneof.listarg.values.add()

                if arg[index] is None:
                    value.nullarg.n = True
                elif isinstance(arg[index], bool):
                    value.boolarg.b = arg[index]
                elif isinstance(arg[index], int):
                    value.intarg.i = arg[index]
                elif isinstance(arg[index], float):
                    value.dblarg.d = arg[index]
                elif isinstance(arg[index], str):
                    value.strarg.s = arg[index]
                elif isinstance(arg[index], Oasys.gRPC.OasysItem):
                    value.itemarg.t = arg[index]._objtype
                    value.itemarg.h = arg[index]._handle
                elif isinstance(arg[index], list):
                    lst = arg[index]
                    for idx in range(len(lst)):
                        self.dbg("list->list {}={} ({})".format(index, lst[idx], type(lst[idx])))
                        val = value.listarg.values.add()
                        self.add_request_arg_data(lst[idx], val)
                elif isinstance(arg[index], dict):
                    dct = arg[index]
                    for ky in dct:
                        self.dbg("list->dict {}={} ({})".format(ky, dct[ky], type(dct[ky])))
                        self.add_request_arg_data(dct[ky], value.dictarg.d[ky])
                else:
                    raise NotImplementedError("Unsupported list type {}".format(type(arg[index])))
        elif isinstance(arg, tuple):    # Tuples used for varargs
            for index in range(len(arg)):
                self.dbg("tuple {}={} ({})".format(index, arg[index], type(arg[index])))

                value = oneof.listarg.values.add()

                if arg[index] is None:
                    value.nullarg.n = True
                elif isinstance(arg[index], bool):
                    value.boolarg.b = arg[index]
                elif isinstance(arg[index], int):
                    value.intarg.i = arg[index]
                elif isinstance(arg[index], float):
                    value.dblarg.d = arg[index]
                elif isinstance(arg[index], str):
                    value.strarg.s = arg[index]
                elif isinstance(arg[index], Oasys.gRPC.OasysItem):
                    value.itemarg.t = arg[index]._objtype
                    value.itemarg.h = arg[index]._handle
                else:
                    raise NotImplementedError("Unsupported tuple type {}".format(type(arg[index])))
        elif isinstance(arg, Oasys.gRPC.OasysItem):
            oneof.itemarg.t = arg._objtype
            oneof.itemarg.h = arg._handle
        else:
            raise NotImplementedError("Unsupported type {}".format(type(arg)))


    def encode_request_value(self, request, value):
# Encode the value that we want to set in the class/instance setter
# for the gRPC request
        if value is None:
            request.value.nullarg.n = True
        elif isinstance(value, bool):
            request.value.boolarg.b = value
        elif isinstance(value, int):
            request.value.intarg.i = value
        elif isinstance(value, float):
            request.value.dblarg.d = value
        elif isinstance(value, str):
            request.value.strarg.s = value
        elif isinstance(value, Oasys.gRPC.OasysItem):
            request.value.itemarg.t = value._objtype
            request.value.itemarg.h = value._handle
        else:
            raise NotImplementedError("Unsupported type {}".format(type(arg)))
        


    def decode_response_value(self, response_value):
# Decode a response value from a gRPC call depending on the type
        if response_value.HasField("boolarg"):
            self.dbg("Bool value {}".format(response_value.boolarg.b))
            return response_value.boolarg.b
        elif response_value.HasField("intarg"):
            self.dbg("Integer value {}".format(response_value.intarg.i))
            return response_value.intarg.i
        elif response_value.HasField("dblarg"):
            self.dbg("Double value {}".format(response_value.dblarg.d))
            return response_value.dblarg.d
        elif response_value.HasField("strarg"):
            self.dbg("String value '{}'".format(response_value.strarg.s))
            return response_value.strarg.s
        elif response_value.HasField("nullarg"):
            self.dbg("Null value")
            return None
        elif response_value.HasField("dictarg"):
            return self.decode_dictarg(response_value.dictarg)
        elif response_value.HasField("listarg"):
            return self.decode_listarg(response_value.listarg)
        elif response_value.HasField("itemarg"):
            return self.decode_itemarg(response_value.itemarg)

        raise NotImplementedError("Unsupported type")


    def decode_itemarg(self, itemarg):
# Decode an itemarg response value
        self.dbg("Item value type {} handle {}".format(itemarg.t, itemarg.h))

        if self.program == "PRIMER":
            import Oasys.PRIMER
            return Oasys.PRIMER.createInstance(itemarg.t, itemarg.h)
        elif self.program == "D3PLOT":
            import Oasys.D3PLOT
            return Oasys.D3PLOT.createInstance(itemarg.t, itemarg.h)
        elif self.program == "T/HIS":
            import Oasys.THIS
            return Oasys.THIS.createInstance(itemarg.t, itemarg.h)
        elif self.program == "REPORTER":
            import Oasys.REPORTER
            return Oasys.REPORTER.createInstance(itemarg.t, itemarg.h)

        raise NotImplementedError("Unknown program")


    def decode_listarg(self, listarg):
# Decode a listarg response value
        self.dbg("List value")
        l = []
        for value in listarg.values:
            if value.HasField("boolarg"):
                self.dbg("  {}={} (bool)".format(len(l), value.boolarg.b))
                l.append(value.boolarg.b)
            elif value.HasField("intarg"):
                self.dbg("  {}={} (int)".format(len(l), value.intarg.i))
                l.append(value.intarg.i)
            elif value.HasField("dblarg"):
                self.dbg("  {}={} (double)".format(len(l), value.dblarg.d))
                l.append(value.dblarg.d)
            elif value.HasField("strarg"):
                self.dbg("  {}={} (string)".format(len(l), value.strarg.s))
                l.append(value.strarg.s)
            elif value.HasField("nullarg"):
                self.dbg("  {}=None (None)".format(len(l)))
                l.append(None)
            elif value.HasField("itemarg"):
                self.dbg("  {} (item)".format(len(l)))
                l.append(self.decode_itemarg(value.itemarg))
            elif value.HasField("listarg"):
                self.dbg("  {} (list)".format(len(l)))
                l.append(self.decode_listarg(value.listarg))
            elif value.HasField("dictarg"):
                self.dbg("  {} (dict)".format(len(l)))
                l.append(self.decode_dictarg(value.dictarg))
            else:
                raise NotImplementedError("Unsupported type for list arg {}".format(len(l)))
        return l


    def decode_dictarg(self, dictarg):
# Decode a dictarg response value
        self.dbg("Dict value")
        d = {}
        for key in dictarg.d:
            if dictarg.d[key].HasField("boolarg"):
                d[key] = dictarg.d[key].boolarg.b
                self.dbg("  '{}'={} (bool)".format(key, dictarg.d[key].boolarg.b))
            elif dictarg.d[key].HasField("intarg"):
                d[key] = dictarg.d[key].intarg.i
                self.dbg("  '{}'={} (int)".format(key, dictarg.d[key].intarg.i))
            elif dictarg.d[key].HasField("dblarg"):
                d[key] = dictarg.d[key].dblarg.d
                self.dbg("  '{}'={} (double)".format(key, dictarg.d[key].dblarg.d))
            elif dictarg.d[key].HasField("strarg"):
                d[key] = dictarg.d[key].strarg.s
                self.dbg("  '{}'={} (string)".format(key, dictarg.d[key].strarg.s))
            elif dictarg.d[key].HasField("nullarg"):
                d[key] = None
                self.dbg("  '{}'=None (None)".format(key))
            elif dictarg.d[key].HasField("listarg"):
                d[key] = self.decode_listarg(dictarg.d[key].listarg)
                self.dbg("  '{}' (list)".format(key))
            elif dictarg.d[key].HasField("itemarg"):
                d[key] = self.decode_itemarg(dictarg.d[key].itemarg)
                self.dbg("  '{}' (item)".format(key))
            elif dictarg.d[key].HasField("dictarg"):
                d[key] = self.decode_dictarg(dictarg.d[key].dictarg)
                self.dbg("  '{}' (dict)".format(key))
            else:
                raise NotImplementedError("Unsupported type for dict {} arg".format(key))
        return d


    def dbg(self, message):
# Print debug messages if enabled

        if not self.debug:
            return

        print(message)
