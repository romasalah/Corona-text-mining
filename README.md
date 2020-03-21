# Corona-text-mining
This will be my trial to text mine thousands of research articles related to COVID19 virus.

 I'm not an expert in text mining, natural language processing or deep learning. I will provide all the data and code. 

# dataset
a combiation of 9000 research article that contanin certain keywords related to corona virus. each article is divided into metadata(title and author),abstract,body, (more about the dataset source later...)

Note: because of the overlap between "coronary artery" and "corona", excpect to see some "coronary article" research articles in the original dataset, I tried to filter them as much as possible in the preprocessed dataset.

1. First 
Since experimental research article abstracts usually report the finidings or the conclusion of the experiment, I thought it was a good way to start is to textmine article abstracts instead of the body.

# filtering
filtering steps were as follows:
1. Removing supplementary material documents by removing all articles with titles that included either  {'Supplementary','appendi*','material*','figure*'}.
2. Removing articles with empty abstracts (they are probably supplementary materials).
3. filtering out review articles by looking for abstracts with the keywords{'review','overview','surv'}.
4. Keeping in ONLY abstracts that contain Corona virus related keywords(trying to exclude coronary artery keywords) {'SARS-CoV-2','corona ','COVID','coronavirus'} and I need More recoomendations on that.
    
# preprocessing
 
