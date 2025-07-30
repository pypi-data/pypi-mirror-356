def import_models():
    print('from sklearn.linear_model import LinearRegression\n\
          ')

def import_metrics():
    print('from sklearn.metrics import r2_score, mean_squared_error\nr2_score(y1, m1.predict(X1))\n\
          ')

def import_other():
    print('from sklearn.preprocessing import PolynomialFeatures\n\
poly = PolynomialFeatures(5).fit_transform(X)')

def import_dataset():
    print("data1 =sklearn.datasets.fetch_openml(name ='laser')\ndata1\n\
          data1.keys()\
          \ny1 =data1.target\
          \nX1 =data1.data\nX1.describe()\ny1.describe()\nX1.info()\ny1.info()\
          \nX1.isna().sum()\ny1.isna().sum()")

def metrics_written():
    print("def MSE(self, x, y):\n\
        return (((y - self.predict(x)).T @ (y - self.predict(x))) / (2 * x.shape[0])).values\n\
    def MAE(self, x, y):\n\
        return (abs(y - self.predict(x)).mean()).values\n\
    def MAPE(self, x, y):\n\
        return (abs((y - self.predict(x))/y).mean()).values")
    
def lr():
    print("lr1 =LinearRegression()\n\
lr1.fit(X1,y1)\n\
plt.scatter(np.array(lr1.predict(X1)),y1)\n\
plt.plot([y1.min(),y1.max()],[y1.min(),y1.max()], color='r')\n\
lr1.coef_\n\
lr1.intercept_ - константа")

