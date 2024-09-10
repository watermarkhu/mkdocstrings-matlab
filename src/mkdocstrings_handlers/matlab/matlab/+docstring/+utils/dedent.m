function parsedDoc = dedent(doc)
%DEDENT Summary of this function goes here
%   Detailed explanation goes here
arguments
    doc (1,1) string
end

lines = cellstr(splitlines(doc));

for iLine = numel(lines):-1:1
    line = lines{iLine};
    if ~isempty(line) && ~all(line == ' ')
        indentations(iLine) = find(line~= ' ', 1);
    else
        indentations(iLine) = inf;
    end
end

indentation = min(indentations);

for iLine = 1:numel(lines)
    line = lines{iLine};
    if isempty(line) || numel(line) <= indentation
        lines{iLine} = '';
    else
        lines{iLine} = line(indentation:end);
    end
end

parsedDoc = string(strjoin(lines, '\n'));

end

