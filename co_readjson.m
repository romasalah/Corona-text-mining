function out=co_readjson(fname)
fid = fopen(fname); 
raw = fread(fid,inf); 
str = char(raw'); 
fclose(fid); 
out = jsondecode(str);
end