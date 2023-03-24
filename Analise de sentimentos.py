import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterClient(object):
    

    def __init__(self):
        #classe contrutora ou inicializadora do metodo
        consumer_key = 'Sua chave aqui'
        consumer_secret = 'Sua chave aqui'
        access_token = 'Sua chave aqui'
        access_token_secet = 'Sua chave aqui'

        # Tentando a autenticação das api
        try:
            # criando o objeto OAuthHandler
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # setando os access token e secret
            self.auth.set_access_token(access_token, access_token_secet)
            # criando o objeto da tweepy API para buscar os tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Erro: Autenticação falhou")
    
    def limpar_tweet(self, text): # str() sem isso da erro
        text = re.sub(r'@[A-Za-z0-9]+', '', str(text)) # Removendo @menções
        text = re.sub(r'#', '', str(text)) # Removendo o simbolo #
        text = re.sub(r'RT[\s]+', '', str(text)) # Removendo os RTs
        text = re.sub(r'https?:\/\/\S+', '', str(text)) # Removendo o hyper Link

        return text    

    def pegar_sentimentos(self, tweet):

        # utiliza a função para classificar os sentimentos passados no tweet usando o metodo de sentimentos do textblob
        analysis = TextBlob(self.limpar_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 'positivo'

        elif analysis.sentiment.polarity == 0:
            return 'neutro'
            
        else:
            return 'negativo'
        
    def pegar_tweets(self, query, count = 10):

        # funçao principal para buscar os tweets e os analisar

        # lista vazia para guardar os tweets
        tweets = []

        try:
            # chama a API do twitter para analizar os tweets
            tweets_buscados = self.api.search_tweets(q = query, count = count)

            # Analisando os tweets um por um
            for tweet in tweets_buscados:
            # dicionario vazio para guardar os parametros requisitados de um tweet
                tweets_analisados = {}

                # Salvando o texto do tweet
                tweets_analisados['text'] = tweet.text
                # Salvando o sentimento do tweet
                tweets_analisados['sentimento'] = self.pegar_sentimentos(tweet.text)

                # append() tweets analisados para a lista tweets
                if tweet.retweet_count > 0:
                    # se o tweet tiver re tweets, garanta que vai adicionar apenas uma vez
                    if tweets_analisados not in tweets:
                        tweets.append(tweets_analisados)
                    else:
                        tweets.append(tweets_analisados)
        # retornando as analizes
            return tweets
        
        except tweepy.errors.TweepyException as e:
            # print error (se tiver)
            print("Erro:" + str(e) )


def main():
    # Crianfo um objeto da calsse TwitterClient 
    api = TwitterClient()
    # Chamando a função pra pegar os tweets
    tweets = api.pegar_tweets(query= 'Gun control', count = 150)

     # Pegando os tweets positivos de tweets
    posiTweets = [tweet for tweet in tweets if tweet['sentimento'] == 'positivo']
    # Porcentagem de tweets positivo
    print("Porcentagem de tweets positivos: {} %".format(int(100*len(posiTweets)/len(tweets))))


    # Pegando os negativos
    negaTweets = [tweet for tweet in tweets if tweet['sentimento'] == 'negativo']
    # Porcentagem de tweets negativos
    print("Porcentagem de tweets negativos: {} %".format(int(100*len(negaTweets)/len(tweets))))

    # Porcentagem de tweets Neutros
    print("Porcentagem de tweets neutros: {} %".format(int(100*(len(tweets) - (len(negaTweets)+len(posiTweets)))/len(tweets))))


    # Mostrando os primeiros 10 positivos
    print("\nTweets Positivos:")
    for tweet in posiTweets[:10]:
        print(tweet['text'])

    # Mostrando os primeiros 10 negativos
    print("\nTweets Negativos")
    for tweet in negaTweets[:10]:
        print(tweet['text'])

if __name__ == "__main__":
    main()