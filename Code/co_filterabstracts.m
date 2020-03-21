function co_filterabstracts(datafolder)
textdir=dir([datafolder filesep '*.json']);
textfilenames={textdir(:).name};
for i=1:size(textfilenames,2)
    try
        temp=co_readjson([textdir filesep textfilenames{i}]);
        textmat(i).title=temp.metadata.title;
        f={temp.metadata.authors(:).first};
        m={temp.metadata.authors(:).middle};
        l={temp.metadata.authors(:).last};
        textmat(i).authors=[f;m;l];
        textmat(i).abstract=temp.abstract.text;
    end
end
clearvars -except textmat
abstracts={textmat(:).abstract};
titles={textmat(:).title};
%% remove supplementary
suppkeywords={'Supplementary','appendi*','material*','figure*'};
findsupp=zeros(1,size(textmat,2));
for suppi=1:size(suppkeywords,2)
    findsupp=plus(findsupp,double(contains(titles,suppkeywords{suppi},'IgnoreCase',true)));
end
noabstractindx=cellfun(@isempty,abstracts);
usableindx=~(double(noabstractindx)+findsupp);
abstractsmat=textmat(usableindx);
abstractsnonsupp={abstractsmat(:).abstract};
%% remove reviews
reviewkeywords={'review','overview','surv'};
findrev=zeros(1,size(abstractsnonsupp,2));
for rev_i=1:size(reviewkeywords,2)
    findrev=plus(findrev,double(contains(abstractsnonsupp,reviewkeywords{rev_i},'IgnoreCase',true)));
end
norevabstracts=abstractsmat(~findrev);
%% select abstracts including covid
abstractsnonrev={norevabstracts(:).abstract};
covidkeywords={'SARS-CoV-2','corona ','COVID','coronavirus'};
findcovidabs=zeros(1,size(abstractsnonrev,2));
for covidabs_i=1:size(covidkeywords,2)
    findcovidabs=plus(findcovidabs,double(contains(abstractsnonrev,covidkeywords{covidabs_i},'IgnoreCase',true)));
end
covidtext=norevabstracts(find(findcovidabs~=0));
covidabs=abstractsnonrev(find(findcovidabs~=0));
readyresultsindx=contains(covidabs,'esults: ','IgnoreCase',true);
readyresultsabstracts={covidtext(readyresultsindx).abstract};
resultskeywords={'esults: ','found ','emonstrate','etermine',...
    'xplain','show','uggest','rovide*','shed light',...
    'eveal','ncover','onclusion','conclude','verall',...
    'ummary','ropose','eport','illustrat','identified'...
    'present','indicate'};
findabsresults=zeros(1,size(covidabs,2));
readyabstext={};
for i2=1:size(covidabs,2)
    for i=1:size(resultskeywords,2)
        if contains(covidabs{i2},resultskeywords{i},'IgnoreCase',true)
            stri=strfind(covidabs{i2},resultskeywords{i});
            sentend=[-1, strfind(covidabs{i2},'. ')];
            prevsent=sentend(sentend<=stri(end));
            lastsent=max(prevsent);
            readyabstext{i2}=covidabs{i2}(lastsent+2:end);
            break
        end
    end
end
readyabsnoresults_idx=find(cellfun(@isempty,readyabstext)==1);
readyabsresults_idx=find(~cellfun(@isempty,readyabstext)==1);
readyabsnoresults=array2table(covidabs(readyabsnoresults_idx)');
readyabsresults=array2table(readyabstext(readyabsresults_idx));
writetable(readyabsresults,'corona_abstracts_results.xls');
writetable(readyabsnoresults,'corona_abstracts_noresults.xls');
save('corona_abstracts.mat','readyabsresults')
save('corona_abstracts_noresults.mat','readyabsnoresults')
end
