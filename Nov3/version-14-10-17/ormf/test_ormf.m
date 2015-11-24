function [] = test_ormf(data_file, model_file, output_file)

load(model_file);
[dim, n_words] = size(P);

text_test = load(data_file);
if size(text_test,1) ~= 0
    text_test = spconvert(text_test);
    n_docs = size(text_test,2);
    text_test(n_words,1) = 0;
    V = zeros(dim,n_docs);
else
    n_docs = 0;
    V = zeros(dim,0);
end

pptw = P*P'*w_m;
for j = 1:n_docs
    [words,~,vals] = find(text_test(:,j));
    pv = P(:,words);
    V(:,j) = (pptw + pv*pv'*(1-w_m) + lambda*eye(dim))  \  (pv*vals);
end


fid = fopen(output_file, 'w');
for i=1:n_docs
    for k=1:dim
        fprintf(fid, '%f ', V(k,i));
    end
    fprintf(fid, '\n');
end

fclose(fid);

exit;
end
