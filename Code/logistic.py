import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from util import getData,softmax,cost,y2indicator,error_rate,init_weight_and_bias

class LogisticModel:
    def __init__(self):
        pass

    def fit(self,X,Y,learning_rate=10e-8,regularisation=10e-12,epochs=10000,show_fig=False):
        X,Y = shuffle(X,Y)

        # print("X.shape"+str(X.shape))
        # print("Y.shape"+str(Y.shape))
        Xvalid, Yvalid = X[-1000:],Y[-1000:]
        Tvalid = y2indicator(Yvalid)
        X,Y = X[:-1000],Y[:-1000]
        # print("X.shape"+str(X.shape))
        # print("Y.shape"+str(Y.shape))
        N,D = X.shape
        K = len(set(Y))
        T = y2indicator(Y)


        self.W,self.b = init_weight_and_bias(D,K)


        costs = []
        best_validation_error = 1
        for i in range(epochs):
            # forward propagation
            pY = self.forward(X)

            # gradient descent
            self.W -= learning_rate*(X.T.dot(pY-T) + regularisation*self.W)
            self.b -= learning_rate*((pY-T).sum(axis=0) + regularisation*self.b)


            if i%10 ==0 :
                pYvalid = self.forward(Xvalid)
                c = cost(Tvalid,pYvalid)
                costs.append(c)
                e = error_rate(Yvalid, np.argmax(pYvalid,axis=1))
                print("i : "+str(i)+"; Cost : "+str(c)+"; Error : "+str(e))
                if e < best_validation_error:
                    best_validation_error = e

        print("Best Validation error : "+str(best_validation_error))

        if(show_fig):
            plt.plot(costs)
            plt.show()


    def forward(self,X):
        return softmax(X.dot(self.W)+self.b)

    def predict(self,X):
        pY = self.forward(X)
        return np.argmax(pY,axis=1)

    def score(self,X,Y):
        prediction = self.forward(X)
        return (1 - error_rate(Y,prediction))






def main():
    X, Y = getData()
    model = LogisticModel()
    model.fit(X,Y,show_fig = True)
    print(model.score(X,Y))


if __name__ == '__main__':
    main()
