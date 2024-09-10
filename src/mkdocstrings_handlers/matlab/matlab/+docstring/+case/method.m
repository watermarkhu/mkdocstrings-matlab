function data = method(identifier)

    object = matlab.internal.metafunction(identifier);
    data = docstring.metadata.func(object);
    data.type = 'method';
end
