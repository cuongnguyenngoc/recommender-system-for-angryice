import pandas as pd

df1 = pd.read_csv("Ukiyo-e captions/ukiyo-captions.csv", index_col=False)
df2 = pd.read_csv("Ukiyo-e captions/fliplr_ukiyo-captions.csv")

df = pd.merge(df1, df2, on='url', suffixes=('_1', '_2'))

df = pd.read_csv("Ukiyo-e captions/uki-captions-pythia.csv", index_col=False)

result = dict()
names = []
for url in df['url']:
    names.append(url.rsplit('/', 1)[-1])

result['name'] = names
result['url'] = df['url']
resultdf = pd.DataFrame(result, columns= ['url', 'name'])

df = pd.merge(df, resultdf, on='url')


print(df.loc[df['name'] == 'arcUP6218.jpg']['caption_1'].values[0])
df.to_csv('Ukiyo-e captions/uki-captions-pythia.csv', index=None)


