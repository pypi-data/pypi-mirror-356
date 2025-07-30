def choose_task_ml():
    print("1. Несколько способов на пропущенные значения\n\
        2. Визуализация распределения признаков\n\
        3. Бинарная классификация и выводы по первым значениям\n\
        4. Линейная модель, вывод коэффициентов и интерпретация\n\
        5. Модель регрессии с оптимизацией гиперпараметров по сетке\n\
        6. Множественная классификация с кросс-валидацией\n\
        7. Линейный SVM и метрики\n\
        8. Бинарная линейная классификация и гридсерч\n\
        9. Множественная классификация SVM poly с метриками\n\
        10. Регрессия с регуляризацией с гиперпараметрами")
    
def urls():
    print("https://github.com/maomaoshka/maomao\n\
          \n\
          ml\n\
          https://docs.google.com/document/d/17-gyyLW4rrcgTtNgHQCei_oDYEKpgekXvOJHqKu3Svg/edit?tab=t.0#heading=h.gwc88co4kx2l\n\
    https://github.com/koroteevmv/ML_course/blob/main/ML5.3%20categorical%20features/README.md\n\
    https://colab.research.google.com/drive/1xHOMo2Lo6gH3iVIRsuHqF-8tK_To3P9v\n\
    \n\
    econometrics:\n\
    https://colab.research.google.com/drive/1RdHEy9rQQ02fthHSJ83nvgSz81DNDjp2?usp=sharing#scrollTo=WTJzpww-HA7N\n\
    https://docs.google.com/document/d/1MKYxhMd6PvWtj-GS9dqUbnVqs6zPqbNxT2HJ7LmsWls/edit?tab=t.0#heading=h.ri0sh1y1lyon")
    
def taskml(n):
    if n==1:
        print("from sklearn.datasets import load_iris\n\
iris = load_iris()\n\
features = iris.data\n\
X = pd.DataFrame(features, columns = iris.feature_names)\n\
X.head()\n\
y = iris.target\n\
X.shape, y.shape\n\
data =pd.concat((X,pd.Series(y, name='target')),axis=1)\n\
data.head()\n\
np.unique(y)\n\
print(iris.DESCR) # проверяю, что действительно должно быть 3 класса\n\
data.info() # первый способ\n\
data.isna().sum(axis=0) # второй способ\n\
data.describe() # третий (почти первый, но со статистикой) - здесь же смотрим по смыслу\n\
# неотрицательность признаков (длина-ширина >0), иначе будем искать спецсимволы и заменять их\n\
# на наны, чтобы потом обработать как надо - условно data[data == -1] = np.nan\n\
sns.heatmap(data.isnull(), yticklabels=False, cbar=False)\n\
# визуальный способ - если бы были пропуски, тут были бы светлые полосочки\n\
# они очень удобные, потому что сразу видно строки, где много пропусков (помним примеры с датасета титаник)\n\
# это были объекты, где не было многих атрибутов, но тут все хорошо :)")
    elif n==2:
        print("from sklearn.datasets import load_diabetes\n\
dia = load_diabetes(scaled=False) # ОЧЕНЬ ВАЖНО СКЕЙЛД ФОЛС, А ТО БУДЕТ СРАЗУ НОРМАЛИЗОВАННЫЙ И ВСЕ\n\
features = dia.data\n\
X = pd.DataFrame(features, columns = dia.feature_names)\n\
X.head()\n\
y = dia.target\n\
X.shape, y.shape\n\
data =pd.concat((X,pd.Series(y, name='target')),axis=1)\n\
data.head()\n\
np.unique(y)\n\
print(dia.DESCR) # тут можно почитать, что значат все эти s1-s2\n\
sns.histplot(data.age)\n\
sns.histplot(data.sex)\n\
# вывод по такой гистограмме: внезапно - пола два, при этом они почему-то 1 и 2 , а не 0 и 1\n\
# очень странно, что это не просто результат работы какого-нибудь LabelEncoder'а, а прям изначально такой признак, судя по всему\n\
sns.histplot(data.s6, kde=True)\n\
sns.histplot(data.bmi)\n\
# табличка с интернетов по теме\n\
# Severe Thinness	< 16\n\
# Moderate Thinness	16 - 17\n\
# Mild Thinness	17 - 18.5\n\
# Normal	18.5 - 25\n\
# Overweight	25 - 30\n\
# Obese Class I	30 - 35\n\
# Obese Class II	35 - 40\n\
# Obese Class III	> 40")