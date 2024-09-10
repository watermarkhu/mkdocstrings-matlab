function data = script(object)
%SCRIPT Summary of this function goes here
%   Detailed explanation goes here

    arguments
        object (1,1) matlab.metadata.MetaData
    end

    data.type = 'script';
    data.Name = object.Name;
    data.docstring = docstring.utils.parse_doc(object);
    data.path = object.Location;

end

