from models import Visual, Category, Document
from django.core.files.uploadedfile import InMemoryUploadedFile
import StringIO
import pandas as pd


def create_visual(corpus):
    """ This function creates a visual model from a submitted corpus """
    
    # Load data
    cats = Category.objects.filter(corpus=corpus)
    
    dataset = pd.DataFrame(columns=['meta_category', 'meta_title', 'meta_body'])
    
    for cat in cats:
        for doc in Document.objects.filter(category=cat):
            doc.file.open()
            s = doc.file.read()
            doc.file.close()
            
            dp = {
                'meta_category': cat.name,
                'meta_title': doc.name,
                'meta_body': s
            }
            
            dataset = dataset.append(dp, ignore_index=True)    
    
    
    # TF-IDF the dataset
    from sklearn.feature_extraction.text import TfidfVectorizer

    vec = TfidfVectorizer()
    
    tf_idf_vec = vec.fit_transform(dataset['meta_body'])
    
    # Convert the tf_idf matrix into a data frame with labels
    tf_idf_df = pd.DataFrame(columns=vec.get_feature_names(), data=tf_idf_vec.toarray())
    
    # Combine the original data set with the tf_idf dataframe
    X_set = dataset.join(tf_idf_df).drop('meta_body', 1)
    
    from sklearn.decomposition import TruncatedSVD
    
    svd = TruncatedSVD(n_components=2)
    svd.fit(X_set.drop(['meta_category', 'meta_title'], 1))
    
    svd_plotdata = []
    
    display_color = []
    markers = []
    
    for cat in cats:
        svd_plotdata.append(svd.transform(X_set.loc[X_set['meta_category'] == cat.name].drop(['meta_category', 'meta_title'], 1)))
        display_color.append(str(cat.color))
        markers.append(str(cat.mark))
        
        
    # Graph the results on a 2D plane
    import matplotlib.pyplot as plt
    
    #plt.figure(figsize=(100,100))
    plt.figure(figsize=(10,8), dpi=300)
    plt.ylabel('LSA #1')
    plt.xlabel('LSA #0')
    plt.ylim(ymin=-1, ymax=1)
    plt.title('Clusters of Texts')
        
    
    # Color index
    ci = 0
    for plotdata in svd_plotdata:
        plt.scatter(plotdata[:, 0], plotdata[:,1], color=display_color[ci], marker=markers[ci])
        ci += 1

    filename = 'figure_'+str(corpus.id)+'.png'
    
    figure = StringIO.StringIO()

    plt.savefig(figure, format="png")
    figure.seek(0)

    content_file = InMemoryUploadedFile(figure, None, filename, 'image/png', figure.len, None)
    #content_file = ImageFile(Image.open(figure))
    


    # If visual already exists, delete it so we can replace it with a new one
    vis, created = Visual.objects.get_or_create(corpus=corpus)
    if not created:
        vis.file.delete()
    
    vis.file.save(filename, content_file)
