import gensim.downloader as api
from sklearn.manifold import TSNE
import pandas as pd
from sklearn.manifold import TSNE


golve = api.load("glove-wiki-gigaword-50")
words = []
word_vectors = []
for word in golve.index_to_key  :
    words.append(word)

    word_vectors.append(golve[word])

df = pd.DataFrame(word_vectors)
df['word'] = words
x = df.iloc[:, :-1].values

print(x.shape)

tsne = TSNE(n_components=2,perplexity=50,n_iter=250, random_state=42)
x = tsne.fit_transform(x)

df = pd.DataFrame(x, columns=['x', 'y'])


df.to_csv('word_embeddings_2d.csv', index=False)
