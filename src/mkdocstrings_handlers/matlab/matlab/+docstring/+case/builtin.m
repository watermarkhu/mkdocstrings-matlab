function data = builtin(identifier)
    data.name = identifier;
    data.type = 'function';
    data.doc = help(identifier);
    data.location = string(which(identifier));
    data.inputs = struct.empty();
    data.outputs = struct.empty();
end
