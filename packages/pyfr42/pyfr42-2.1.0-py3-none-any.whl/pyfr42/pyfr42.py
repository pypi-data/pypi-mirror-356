from openai import OpenAI
import pyperclip

system_prompt_code = '''
Ты — эксперт по рекомендательным системам, помогающий студенту на экзамене. Отвечай **только кодом**, без пояснений, если не указано иное.

#### **Формат ответа:**  
- Только код  
- Допустим "учебный" стиль (простые циклы, явные преобразования)  
- Можно использовать `pandas`, `numpy`, `sklearn`, `scipy`, `implicit`  
- Используй одинарные кавычки  
- Код должен выглядеть как написанный студентом вручную

#### Примеры запросов и ответов:
▸ *'Построй матрицу взаимодействий User-Item в pandas'*  
→  
```python
import pandas as pd  
import numpy as np  

data = pd.DataFrame({  
    'user_id': [1, 2, 1, 3],  
    'item_id': [101, 102, 103, 101],  
    'rating': [5, 3, 4, 2]  
})  

interaction_matrix = data.pivot_table(index='user_id', columns='item_id', values='rating').fillna(0)
▸ 'Обучи модель ALS на разреженной матрице'
→
from implicit.als import AlternatingLeastSquares  
from scipy.sparse import csr_matrix  

matrix = csr_matrix(interaction_matrix.values)  
model = AlternatingLeastSquares(factors=20, iterations=15)  
model.fit(matrix)
    '''

system_prompt_theory = '''
Я решаю экзамен по рекомендательным системам и коллаборативной фильтрации. На экзамене даны **теоретические вопросы**, на которые нужно отвечать в виде **структурированных, понятных и ручных конспектов**. Требования к ответу:

- Без «ИИ-стиля» — как будто пишешь от руки
- Без излишне глубокой математики
- **Объёмом не меньше, чем слайды лекций**
- В среднем: 2 абзаца на вопрос
- Примеры и формулы — где уместно

#### Примеры удачных ответов:

▸ **Вопрос**: Метод коллаборативной фильтрации на основе пользователей  
**Ответ**:  
Метод user-based CF предполагает, что пользователи с похожими вкусами будут интересоваться похожими объектами. Чтобы рекомендовать объекты новому пользователю, система ищет других пользователей, чьи оценки схожи с его собственными (например, по косинусной близости), а затем выбирает те объекты, которые они оценили высоко, но текущий пользователь ещё не видел.

На практике используется предсказание рейтинга по формуле:  
$$
\hat{r}_{ui} = \bar{r}_u + \frac{\sum_{v \in N(u)} sim(u, v) \cdot (r_{vi} - \bar{r}_v)}{\sum_{v \in N(u)} |sim(u, v)|}
$$  
где \( \bar{r}_u \) — средний рейтинг пользователя \(u\), \(sim(u,v)\) — мера похожести, \(N(u)\) — соседи \(u\). Это требует централизации рейтингов и нормализации.

▸ **Вопрос**: Модель матричной факторизации ALS  
**Ответ**:  
ALS (Alternating Least Squares) — это метод матричной факторизации, в котором исходная разреженная матрица рейтингов \( R \) аппроксимируется как произведение двух плотных матриц: \( R \approx UV^T \), где \( U \) — матрица пользователей, \( V \) — матрица объектов. Метод поочередно фиксирует одну из матриц и решает задачу наименьших квадратов для другой, с регуляризацией.

ALS хорошо масштабируется и может обучаться на неявных взаимодействиях (implicit feedback), где вместо рейтингов используются веса уверенности. В этом случае используется функция потерь:  
$$
\min_{U,V} \sum_{u,i} c_{ui}(p_{ui} - u_u^T v_i)^2 + \lambda(\|u_u\|^2 + \|v_i\|^2)
$$  
где \(c_{ui}\) — вес уверенности, \(p_{ui}\) — бинарный факт взаимодействия (1 или 0).
'''

themes = '''Темы практики:
1. Сходство пользователей (пирсона, косинусное, жжакара)
2. Предсказать незаполненный ячейки (User-based, Item-based, SVD, KNN, Matrix Factorization, Mean)
3. MatrixFactorization и метрики РУКАМИ
4. MatrixFactorization и метрики через surprise
5. C помощью метода ассоциаций найдти похожие фильмы
Темы теории:
6. Понятие и история развития рекомендательных систем
7. Терминология рекомендательных систем: пользователи, товары, рейтинги, предпочтения и рекомендации
8. Проблема прогнозирования в рекомендательных системах
9. Задача ранжирования в рекомендательных системах
10. Классификация рекомендательных систем
11. Основные проблемы и вызовы рекомендательных систем
12. Коллаборативная фильтрация в рекомендательных системах
13. Контентные рекомендации в рекомендательных системах
14. Фильтрация на основе пользователей (User-based filtering)
15. Фильтрация на основе объектов (Item-based filtering)
16. Проблема «холодного старта» (cold start) и способы ее решения
17. Понятие сходства и функции подобия
18. Расстояние Жаккара
19. L1- и  L2-нормы для оценки сходства
20. Коэффициент Отиаи и коэффициент корреляции Пирсона
21. Постановка задачи коллаборативной фильтрации
22. Основные подходы в коллаборативной фильтрации
23. User-based подход в коллаборативной фильтрации
24. Item-based подход в коллаборативной фильтрации
25. Применение сингулярного разложения (SVD) в рекомендательных системах
26. Матричная факторизация с использованием SVD
27. Формирование рекомендаций с помощью метода SVD
28. Расчет отклонений в рекомендательных системах методом наименьших квадратов
29. Библиотека Surprise и ее применение для построения рекомендательных систем
30. Алгоритм градиентного спуска для матричной факторизации.
31. Алгоритм стохастического градиентного спуска для матричной факторизации.
32. Расчет оценок в методе регуляризованного SVD
33. Параметры алгоритма метода регуляризованного SVD
34. Генерация рекомендаций с помощью метода FunkSVD
35. Расчет рекомендаций в окрестности
36. Формирование вектора пользователя с помощью TF-IDF в рекомендательных системах
37. Проблема неподходящих рекомендаций и пути ее решения
38. Применение кластеризации в рекомендательных системах
39. Кластеризация k-средних в рекомендательных системах
40. Применение метода kNN в рекомендательных системах
41. Метрики оценки RMSE, MAE для рекомендательных систем
42. Кросс-валидация для рекомендательных систем
43. Базовые метрики оценки качества спрогнозированных рейтингов и рекомендаций
44. Расширения и альтернативы TF-IDF-анализа
45. Определение «похожести» интересов пользователей на основе корреляции Пирсона
46. Построение и актуализация профилей пользователей*
47. Определение сходства интересов пользователей, посчитанное косинусным расстоянием векторов предпочтений
48. Преимущества и недостатки контентно-ориентированного подхода*
49. Определение сходства интересов пользователей, посчитанное расстоянием Жаккара
50. Понятие коллаборативной фильтрации
51. Меры оценки сходства пользователей, преимущества и недостатки. *
52. Алгоритм «User-User» для построения рекомендации на основе оценок пользователей со схожими рейтингами.
53. Два основных подхода в коллаборативной фильтрации.
54. Двухшаговая реализация алгоритма «Item-Item»: определение сходства товаров на основе их рейтингов.
55. Построение прогноза рейтинга на основе рейтинга «соседей».
56. Гибридные рекомендательные системы.
57. Типы метрик оценки качества рекомендательных систем.
58. Рекомендательные системы, основанные на знаниях
59. Метрики оценки точности: MAE, RMSE, MSE
60. Метрики поддержки принятия решений: ROC AUC, полнота и точность
61. Поиск нерелевантных рекомендаций («reversals»).
62. Задача снижения размерности в рекомендательных системах
63. Способы реализации гибридных алгоритмов.
64. Критерии классификации рекомендательных систем
65. Неперсонализированные рекомендательные системы
66. Способы получения и обработки информации о предпочтениях пользователя
67. Построение контентно-ориентированной рекомендательной системы
68. Явные (explicit) и неявные (implicit) оценки в рекомендательных системах
69. Показатели Top-N с учетом ранжирования (MRR, nDCG)
70. Актуальность рекомендаций
71. Архитектура гибридных рекомендательных систем
72. Проблема «холодного старта» (cold start) в рекомендательных системах
73. Понятие сходства для рекомендательных систем и функции подобия.
74. Применение L-норм в рекомендательных системах.
75. Коэффициент Отиаи и коэффициент Жаккара.
76. Применение алгоритмов градиентного спуска в рекомендательных системах.
77. Основные подходы коллаборативной фильтрации.
78. Применение библиотеки Surprise для построения рекомендательных систем.
79. Применение библиотеки LightFM для построения рекомендательных систем.
80. Применение метода SVD для формирования рекомендаций.
81. Применение метода FunkSVD для формирования рекомендаций.
82. Построение прогноза рейтинга на основе рейтинга «соседей».
83. Алгоритм ALS в рекомендательных системах
84. Алгоритм Implicit ALS в рекомендательных системах
85. Применение библиотеки Implicit для построения рекомендательных систем
86. Отличие неявных (implicit) данных от явных (explicit) и их роль в рекомендательных системах
'''

questions = {
    1 : "import numpy as np\nfrom sklearn.metrics.pairwise import cosine_similarity\nfrom scipy.stats import pearsonr\nimport pandas as pd\nimport random\n\n\ndef create_user_item_dataframe(\n    num_users=5, num_items=5, min_rating=1, max_rating=5, fill_percentage=0.4\n):\n    users = [f'User {i + 1}' for i in range(num_users)]\n    items = [f'Item {i + 1}' for i in range(num_items)]\n    df = pd.DataFrame(index=users, columns=items)\n    total_cells = num_users * num_items\n    cells_to_fill = int(total_cells * fill_percentage)\n    all_positions = [(i, j) for i in range(num_users) for j in range(num_items)]\n    positions_to_fill = random.sample(all_positions, cells_to_fill)\n    for user_idx, item_idx in positions_to_fill:\n        if isinstance(min_rating, int) and isinstance(max_rating, int):\n            rating = random.randint(min_rating, max_rating)\n        else:\n            rating = round(random.uniform(min_rating, max_rating), 1)\n        df.iloc[user_idx, item_idx] = rating\n    return df\n\ndef calculate_pearson_similarity(df):\n    users = df.index\n    n_users = len(users)\n    similarity_matrix = pd.DataFrame(index=users, columns=users, dtype=float)\n    \n    for i in range(n_users):\n        for j in range(n_users):\n            if i == j:\n                similarity_matrix.iloc[i, j] = 1.0\n            else:\n                user1_ratings = df.iloc[i].dropna()\n                user2_ratings = df.iloc[j].dropna()\n                \n                common_items = user1_ratings.index.intersection(user2_ratings.index)\n                \n                if len(common_items) < 2:\n                    similarity_matrix.iloc[i, j] = 0.0\n                else:\n                    corr, _ = pearsonr(user1_ratings[common_items], user2_ratings[common_items])\n                    similarity_matrix.iloc[i, j] = corr if not np.isnan(corr) else 0.0\n    \n    return similarity_matrix\n\ndef calculate_jaccard_similarity(df):\n    users = df.index\n    n_users = len(users)\n    similarity_matrix = pd.DataFrame(index=users, columns=users, dtype=float)\n    \n    for i in range(n_users):\n        for j in range(n_users):\n            if i == j:\n                similarity_matrix.iloc[i, j] = 1.0\n            else:\n                user1_items = set(df.iloc[i].dropna().index)\n                user2_items = set(df.iloc[j].dropna().index)\n                \n                intersection = len(user1_items.intersection(user2_items))\n                union = len(user1_items.union(user2_items))\n                \n                similarity_matrix.iloc[i, j] = intersection / union if union > 0 else 0.0\n    \n    return similarity_matrix\n\ndef calculate_cosine_similarity(df):\n    df_filled = df.fillna(0)\n    cosine_sim = cosine_similarity(df_filled.values)\n    similarity_matrix = pd.DataFrame(cosine_sim, index=df.index, columns=df.index)\n    return similarity_matrix\n\ndf = create_user_item_dataframe(num_users=20, num_items = 20)\n\n_pearson_similarity = calculate_pearson_similarity(df)\n_jaccard_similarity = calculate_jaccard_similarity(df)\n_cosine_similarity = calculate_cosine_similarity(df)",
    2 : "import pandas as pd\nimport numpy as np\nfrom sklearn.decomposition import TruncatedSVD\nfrom sklearn.impute import KNNImputer\nfrom sklearn.metrics.pairwise import cosine_similarity\nimport random\nimport warnings\nwarnings.filterwarnings('ignore')\n\n\ndef create_user_item_dataframe(\n    num_users=5, num_items=5, min_rating=1, max_rating=5, fill_percentage=0.4\n):\n    users = [f'User {i + 1}' for i in range(num_users)]\n    items = [f'Item {i + 1}' for i in range(num_items)]\n    df = pd.DataFrame(index=users, columns=items)\n    total_cells = num_users * num_items\n    cells_to_fill = int(total_cells * fill_percentage)\n    all_positions = [(i, j) for i in range(num_users) for j in range(num_items)]\n    positions_to_fill = random.sample(all_positions, cells_to_fill)\n    for user_idx, item_idx in positions_to_fill:\n        if isinstance(min_rating, int) and isinstance(max_rating, int):\n            rating = random.randint(min_rating, max_rating)\n        else:\n            rating = round(random.uniform(min_rating, max_rating), 1)\n        df.iloc[user_idx, item_idx] = rating\n    return df\n\ndef collaborative_filtering_user_based(df, n_neighbors=3):\n    '''Коллаборативная фильтрация на основе похожести пользователей'''\n    df_filled = df.fillna(0)\n    df_result = df.copy()\n    \n    for user_idx in range(len(df)):\n        user_ratings = df_filled.iloc[user_idx].values.reshape(1, -1)\n        similarities = cosine_similarity(user_ratings, df_filled.values)[0]\n        similarities[user_idx] = 0\n        \n        top_similar_users = np.argsort(similarities)[-n_neighbors:]\n        \n        for item_idx in range(len(df.columns)):\n            if pd.isna(df.iloc[user_idx, item_idx]):\n                similar_ratings = []\n                weights = []\n                \n                for similar_user in top_similar_users:\n                    if not pd.isna(df.iloc[similar_user, item_idx]):\n                        similar_ratings.append(df.iloc[similar_user, item_idx])\n                        weights.append(similarities[similar_user])\n                \n                if similar_ratings and sum(weights) > 0:\n                    weighted_avg = np.average(similar_ratings, weights=weights)\n                    df_result.iloc[user_idx, item_idx] = round(weighted_avg)\n                else:\n                    df_result.iloc[user_idx, item_idx] = df.mean().mean()\n    \n    return df_result\n\ndef collaborative_filtering_item_based(df, n_neighbors=3):\n    '''Коллаборативная фильтрация на основе похожести товаров'''\n    df_filled = df.fillna(0)\n    df_result = df.copy()\n    \n    item_similarities = cosine_similarity(df_filled.T)\n    \n    for user_idx in range(len(df)):\n        for item_idx in range(len(df.columns)):\n            if pd.isna(df.iloc[user_idx, item_idx]):\n                item_sim = item_similarities[item_idx]\n                item_sim[item_idx] = 0\n                \n                top_similar_items = np.argsort(item_sim)[-n_neighbors:]\n                \n                similar_ratings = []\n                weights = []\n                \n                for similar_item in top_similar_items:\n                    if not pd.isna(df.iloc[user_idx, similar_item]):\n                        similar_ratings.append(df.iloc[user_idx, similar_item])\n                        weights.append(item_sim[similar_item])\n                \n                if similar_ratings and sum(weights) > 0:\n                    weighted_avg = np.average(similar_ratings, weights=weights)\n                    df_result.iloc[user_idx, item_idx] = round(weighted_avg)\n                else:\n                    df_result.iloc[user_idx, item_idx] = df.mean().mean()\n    \n    return df_result\n\ndef svd_recommendation(df, n_components=2):\n    '''Сингулярное разложение матрицы для предсказания рейтингов'''\n    df_filled = df.fillna(0)\n    \n    svd = TruncatedSVD(n_components=min(n_components, min(df.shape)-1))\n    user_factors = svd.fit_transform(df_filled)\n    item_factors = svd.components_\n    \n    reconstructed = np.dot(user_factors, item_factors)\n    df_result = df.copy()\n    \n    for i in range(len(df)):\n        for j in range(len(df.columns)):\n            if pd.isna(df.iloc[i, j]):\n                predicted_value = max(0, min(1, reconstructed[i, j]))\n                df_result.iloc[i, j] = round(predicted_value)\n    \n    return df_result\n\ndef knn_imputation(df, n_neighbors=3):\n    '''Заполнение пропусков методом k ближайших соседей'''\n    imputer = KNNImputer(n_neighbors=n_neighbors)\n    df_imputed = pd.DataFrame(\n        imputer.fit_transform(df),\n        columns=df.columns,\n        index=df.index\n    )\n    return df_imputed.round().astype(int)\n\ndef matrix_factorization(df, k=2, steps=100, alpha=0.01, beta=0.1):\n    '''Матричная факторизация с градиентным спуском'''\n    df_filled = df.fillna(0)\n    R = df_filled.values\n    N, M = R.shape\n    \n    P = np.random.normal(scale=1./k, size=(N, k))\n    Q = np.random.normal(scale=1./k, size=(M, k))\n    \n    mask = ~df.isna().values\n    \n    for step in range(steps):\n        for i in range(N):\n            for j in range(M):\n                if mask[i, j]:\n                    eij = R[i, j] - np.dot(P[i, :], Q[j, :].T)\n                    \n                    for k_idx in range(k):\n                        P[i, k_idx] = P[i, k_idx] + alpha * (2 * eij * Q[j, k_idx] - beta * P[i, k_idx])\n                        Q[j, k_idx] = Q[j, k_idx] + alpha * (2 * eij * P[i, k_idx] - beta * Q[j, k_idx])\n    \n    predicted = np.dot(P, Q.T)\n    df_result = df.copy()\n    \n    for i in range(N):\n        for j in range(M):\n            if pd.isna(df.iloc[i, j]):\n                df_result.iloc[i, j] = round(max(0, min(1, predicted[i, j])))\n    \n    return df_result\n\ndef mean_imputation(df):\n    '''Заполнение пропусков средним значением по столбцам'''\n    df_result = df.copy()\n    \n    for col in df.columns:\n        col_mean = df[col].mean()\n        if not pd.isna(col_mean):\n            df_result[col] = df_result[col].fillna(round(col_mean))\n        else:\n            df_result[col] = df_result[col].fillna(0)\n    \n    return df_result\n\ndf = create_user_item_dataframe(num_users=20, num_items = 20)\nresult1 = collaborative_filtering_user_based(df)\nresult2 = collaborative_filtering_item_based(df)\nresult3 = svd_recommendation(df)\nresult4 = knn_imputation(df)\nresult5 = matrix_factorization(df)\nresult6 = mean_imputation(df)",
    3 : "import pandas as pd\nimport numpy as np\nimport random\nfrom sklearn.metrics import mean_squared_error\n\ndef create_user_item_dataframe(num_users=5, num_items=5, min_rating=1, max_rating=5, fill_percentage=0.4):\n    users = [f'User {i+1}' for i in range(num_users)]\n    items = [f'Item {i+1}' for i in range(num_items)]\n    df = pd.DataFrame(index=users, columns=items)\n    total_cells = num_users * num_items\n    cells_to_fill = int(total_cells * fill_percentage)\n    all_positions = [(i, j) for i in range(num_users) for j in range(num_items)]\n    positions_to_fill = random.sample(all_positions, cells_to_fill)\n    for user_idx, item_idx in positions_to_fill:\n        if isinstance(min_rating, int) and isinstance(max_rating, int):\n            rating = random.randint(min_rating, max_rating)\n        else:\n            rating = round(random.uniform(min_rating, max_rating), 1)\n        df.iloc[user_idx, item_idx] = rating\n    return df\n\nclass MatrixFactorization:\n    def __init__(self, R, K=10, alpha=0.01, beta=0.01, iterations=1000):\n        self.R = R\n        self.num_users, self.num_items = R.shape\n        self.K = K\n        self.alpha = alpha\n        self.beta = beta\n        self.iterations = iterations\n        \n        self.P = np.random.normal(scale=1./self.K, size=(self.num_users, self.K))\n        self.Q = np.random.normal(scale=1./self.K, size=(self.num_items, self.K))\n        \n        self.b_u = np.zeros(self.num_users)\n        self.b_i = np.zeros(self.num_items)\n        self.b = np.mean(self.R[self.R.nonzero()])\n        \n        self.samples = [\n            (i, j, self.R[i, j])\n            for i in range(self.num_users)\n            for j in range(self.num_items)\n            if self.R[i, j] > 0\n        ]\n        \n        self.training_process = []\n    \n    def train(self):\n        for i in range(self.iterations):\n            np.random.shuffle(self.samples)\n            self.sgd()\n            mse = self.mse()\n            self.training_process.append((i, mse))\n            if (i+1) % 100 == 0:\n                print(f'Iteration: {i+1}, MSE: {mse:.4f}')\n    \n    def mse(self):\n        xs, ys = self.R.nonzero()\n        predicted = self.get_rating(xs, ys)\n        error = 0\n        for x, y in zip(xs, ys):\n            error += pow(self.R[x, y] - predicted[x, y], 2)\n        return np.sqrt(error / len(xs))\n    \n    def sgd(self):\n        for i, j, r in self.samples:\n            prediction = self.get_rating(i, j)\n            e = (r - prediction)\n            \n            self.b_u[i] += self.alpha * (e - self.beta * self.b_u[i])\n            self.b_i[j] += self.alpha * (e - self.beta * self.b_i[j])\n            \n            P_i = self.P[i, :][:]\n            self.P[i, :] += self.alpha * (e * self.Q[j, :] - self.beta * self.P[i, :])\n            self.Q[j, :] += self.alpha * (e * P_i - self.beta * self.Q[j, :])\n    \n    def get_rating(self, i, j):\n        return self.b + self.b_u[i] + self.b_i[j] + self.P[i, :].dot(self.Q[j, :].T)\n    \n    def get_complete_matrix(self):\n        return self.b + self.b_u[:, np.newaxis] + self.b_i[np.newaxis:, ] + self.P.dot(self.Q.T)\n\ndef split_data(df, test_size=0.2):\n    train_data = df.copy()\n    test_data = pd.DataFrame(np.nan, index=df.index, columns=df.columns)\n    \n    non_nan_positions = [(i, j) for i in range(len(df)) for j in range(len(df.columns)) if not pd.isna(df.iloc[i, j])]\n    test_positions = random.sample(non_nan_positions, int(len(non_nan_positions) * test_size))\n    \n    for i, j in test_positions:\n        test_data.iloc[i, j] = train_data.iloc[i, j]\n        train_data.iloc[i, j] = np.nan\n    \n    return train_data, test_data\n\ndef calculate_precision_recall_at_k(predicted_ratings, test_data, k=5, threshold=7):\n    precisions = []\n    recalls = []\n    \n    for user_idx in range(len(test_data)):\n        user_test = test_data.iloc[user_idx]\n        user_pred = predicted_ratings[user_idx]\n        \n        actual_relevant = set(user_test[user_test >= threshold].index)\n        \n        if len(actual_relevant) == 0:\n            continue\n        \n        top_k_items = pd.Series(user_pred, index=test_data.columns).nlargest(k).index\n        predicted_relevant = set(top_k_items)\n        \n        if len(predicted_relevant) > 0:\n            precision = len(actual_relevant.intersection(predicted_relevant)) / len(predicted_relevant)\n            recall = len(actual_relevant.intersection(predicted_relevant)) / len(actual_relevant)\n            \n            precisions.append(precision)\n            recalls.append(recall)\n    \n    return np.mean(precisions) if precisions else 0, np.mean(recalls) if recalls else 0\n\ndef get_top_recommendations(predicted_ratings, original_ratings, user_idx, k=5):\n    user_ratings = original_ratings.iloc[user_idx]\n    already_rated = user_ratings.dropna().index\n    \n    user_pred = pd.Series(predicted_ratings[user_idx], index=original_ratings.columns)\n    unrated_items = user_pred.drop(already_rated)\n    \n    top_recommendations = unrated_items.nlargest(k)\n    return top_recommendations\n\ndf = create_user_item_dataframe(num_users=15, num_items=25, min_rating=1, max_rating=10, fill_percentage=0.25)\n\ntrain_data, test_data = split_data(df, test_size=0.2)\n\nprint(f'\nТренировочные данные: {train_data.notna().sum().sum()} рейтингов')\nprint(f'Тестовые данные: {test_data.notna().sum().sum()} рейтингов')\n\ntrain_matrix = train_data.fillna(0).values\ntest_matrix = test_data.fillna(0).values\n\nprint('\nОбучение модели матричной факторизации...')\nmf = MatrixFactorization(train_matrix, K=10, alpha=0.01, beta=0.01, iterations=10)\nmf.train()\n\npredicted_matrix = mf.get_complete_matrix()\n\nprecision_5_train, recall_5_train = calculate_precision_recall_at_k(predicted_matrix, train_data, k=5, threshold=7)\nprecision_10_train, recall_10_train = calculate_precision_recall_at_k(predicted_matrix, train_data, k=10, threshold=7)\n\nprecision_5_test, recall_5_test = calculate_precision_recall_at_k(predicted_matrix, test_data, k=5, threshold=7)\nprecision_10_test, recall_10_test = calculate_precision_recall_at_k(predicted_matrix, test_data, k=10, threshold=7)\n\nprint(f'\nМетрики качества (порог релевантности: 7):')\nprint(f'Precision@5 - Train: {precision_5_train:.4f}, Test: {precision_5_test:.4f}')\nprint(f'Recall@5 - Train: {recall_5_train:.4f}, Test: {recall_5_test:.4f}')\nprint(f'Precision@10 - Train: {precision_10_train:.4f}, Test: {precision_10_test:.4f}')\nprint(f'Recall@10 - Train: {recall_10_train:.4f}, Test: {recall_10_test:.4f}')\n\nn = 2\nif n:\n    print(f'\nРекомендации для первых {n} пользователей:')\nfor i in range(n):\n    user_name = df.index[i]\n    top_recs = get_top_recommendations(predicted_matrix, df, i, k=5)\n    \n    print(f'\n{user_name}:')\n    print(f'  Уже оценил: {df.iloc[i].dropna().index.tolist()}')\n    print(f'  Топ-5 рекомендаций:')\n    for item, rating in top_recs.items():\n        print(f'    {item}: {rating:.2f}')\n\ntrain_actual_vs_predicted = []\nfor i in range(len(train_data)):\n    for j in range(len(train_data.columns)):\n        if not pd.isna(train_data.iloc[i, j]):\n            actual = train_data.iloc[i, j]\n            predicted = predicted_matrix[i, j]\n            train_actual_vs_predicted.append((actual, predicted))\n\ntest_actual_vs_predicted = []\nfor i in range(len(test_data)):\n    for j in range(len(test_data.columns)):\n        if not pd.isna(test_data.iloc[i, j]):\n            actual = test_data.iloc[i, j]\n            predicted = predicted_matrix[i, j]\n            test_actual_vs_predicted.append((actual, predicted))\n\nif train_actual_vs_predicted:\n    train_actual_ratings = [x[0] for x in train_actual_vs_predicted]\n    train_predicted_ratings = [x[1] for x in train_actual_vs_predicted]\n    rmse_train = np.sqrt(mean_squared_error(train_actual_ratings, train_predicted_ratings))\n\nif test_actual_vs_predicted:\n    test_actual_ratings = [x[0] for x in test_actual_vs_predicted]\n    test_predicted_ratings = [x[1] for x in test_actual_vs_predicted]\n    rmse_test = np.sqrt(mean_squared_error(test_actual_ratings, test_predicted_ratings))\n\nprint(f'\nRMSE - Train: {rmse_train:.4f}, Test: {rmse_test:.4f}')",
    4 : "import pandas as pd\nimport numpy as np\nimport random\nfrom surprise import Dataset, Reader, SVD\nfrom surprise.model_selection import train_test_split\nfrom surprise import accuracy\nfrom collections import defaultdict\n\ndef create_user_item_dataframe(num_users=5, num_items=5, min_rating=1, max_rating=5, fill_percentage=0.4):\n    users = [f'User {i+1}' for i in range(num_users)]\n    items = [f'Item {i+1}' for i in range(num_items)]\n    df = pd.DataFrame(index=users, columns=items)\n    total_cells = num_users * num_items\n    cells_to_fill = int(total_cells * fill_percentage)\n    all_positions = [(i, j) for i in range(num_users) for j in range(num_items)]\n    positions_to_fill = random.sample(all_positions, cells_to_fill)\n    for user_idx, item_idx in positions_to_fill:\n        if isinstance(min_rating, int) and isinstance(max_rating, int):\n            rating = random.randint(min_rating, max_rating)\n        else:\n            rating = round(random.uniform(min_rating, max_rating), 1)\n        df.iloc[user_idx, item_idx] = rating\n    return df\n\ndef dataframe_to_surprise_format(df):\n    '''Конвертирует DataFrame в формат для Surprise'''\n    data = []\n    for user_idx, user in enumerate(df.index):\n        for item_idx, item in enumerate(df.columns):\n            rating = df.iloc[user_idx, item_idx]\n            if not pd.isna(rating):\n                data.append([user, item, rating])\n    return pd.DataFrame(data, columns=['user', 'item', 'rating'])\n\ndef get_top_n_recommendations(predictions, n=5):\n    '''Получает топ-N рекомендаций для каждого пользователя'''\n    top_n = defaultdict(list)\n    for uid, iid, true_r, est, _ in predictions:\n        top_n[uid].append((iid, est))\n    \n    for uid, user_ratings in top_n.items():\n        user_ratings.sort(key=lambda x: x[1], reverse=True)\n        top_n[uid] = user_ratings[:n]\n    \n    return top_n\n\ndef calculate_precision_recall_surprise(predictions, threshold=7, k=5):\n    '''Расчет Precision и Recall для Surprise predictions'''\n    user_est_true = defaultdict(list)\n    \n    for uid, _, true_r, est, _ in predictions:\n        user_est_true[uid].append((est, true_r))\n    \n    precisions = dict()\n    recalls = dict()\n    \n    for uid, user_ratings in user_est_true.items():\n        user_ratings.sort(key=lambda x: x[0], reverse=True)\n        \n        n_rel = sum((true_r >= threshold) for (_, true_r) in user_ratings)\n        n_rec_k = sum((est >= threshold) for (est, _) in user_ratings[:k])\n        n_rel_and_rec_k = sum(((true_r >= threshold) and (est >= threshold))\n                              for (est, true_r) in user_ratings[:k])\n        \n        precisions[uid] = n_rel_and_rec_k / n_rec_k if n_rec_k != 0 else 0\n        recalls[uid] = n_rel_and_rec_k / n_rel if n_rel != 0 else 0\n    \n    precision = sum(prec for prec in precisions.values()) / len(precisions) if precisions else 0\n    recall = sum(rec for rec in recalls.values()) / len(recalls) if recalls else 0\n    \n    return precision, recall\n\ndf = create_user_item_dataframe(num_users=15, num_items=25, min_rating=1, max_rating=10, fill_percentage=0.25)\n\nsurprise_data = dataframe_to_surprise_format(df)\n\nreader = Reader(rating_scale=(1, 10))\ndata = Dataset.load_from_df(surprise_data[['user', 'item', 'rating']], reader)\n\ntrainset, testset = train_test_split(data, test_size=0.2, random_state=42)\n\nprint(f'\nТренировочные данные: {len(list(trainset.all_ratings()))} рейтингов')\nprint(f'Тестовые данные: {len(testset)} рейтингов')\n\nprint('\nОбучение модели SVD...')\nalgo = SVD(n_factors=10, lr_all=0.01, reg_all=0.01, n_epochs=50, verbose=True)\nalgo.fit(trainset)\n\ntrain_predictions = algo.test(trainset.build_testset())\ntest_predictions = algo.test(testset)\n\nrmse_train = accuracy.rmse(train_predictions, verbose=False)\nrmse_test = accuracy.rmse(test_predictions, verbose=False)\n\nprecision_5_train, recall_5_train = calculate_precision_recall_surprise(train_predictions, threshold=7, k=5)\nprecision_10_train, recall_10_train = calculate_precision_recall_surprise(train_predictions, threshold=7, k=10)\n\nprecision_5_test, recall_5_test = calculate_precision_recall_surprise(test_predictions, threshold=7, k=5)\nprecision_10_test, recall_10_test = calculate_precision_recall_surprise(test_predictions, threshold=7, k=10)\n\nprint(f'\nМетрики качества (порог релевантности: 7):')\nprint(f'Precision@5 - Train: {precision_5_train:.4f}, Test: {precision_5_test:.4f}')\nprint(f'Recall@5 - Train: {recall_5_train:.4f}, Test: {recall_5_test:.4f}')\nprint(f'Precision@10 - Train: {precision_10_train:.4f}, Test: {precision_10_test:.4f}')\nprint(f'Recall@10 - Train: {recall_10_train:.4f}, Test: {recall_10_test:.4f}')\n\nprint(f'\nRMSE - Train: {rmse_train:.4f}, Test: {rmse_test:.4f}')\n\nn = 2\nif n:\n    print(f'\nРекомендации для первых {n} пользователей:')\n    \n    all_items = df.columns.tolist()\n    \n    for i in range(n):\n        user_name = df.index[i]\n        \n        already_rated = df.iloc[i].dropna().index.tolist()\n        \n        unrated_items = [item for item in all_items if item not in already_rated]\n        predictions_for_user = []\n        \n        for item in unrated_items:\n            pred = algo.predict(user_name, item)\n            predictions_for_user.append((item, pred.est))\n        \n        predictions_for_user.sort(key=lambda x: x[1], reverse=True)\n        top_5 = predictions_for_user[:5]\n        \n        print(f'\n{user_name}:')\n        print(f'  Уже оценил: {already_rated}')\n        print(f'  Топ-5 рекомендаций:')\n        for item, rating in top_5:\n            print(f'    {item}: {rating:.2f}')\n\nprint(f'\nПараметры модели SVD:')\nprint(f'  Количество факторов: {algo.n_factors}')\nprint(f'  Количество эпох: {algo.n_epochs}')",
    5 : "import pandas as pd\nimport numpy as np\nfrom itertools import combinations\nimport random\n\ndef create_user_item_dataframe(num_users=5, num_items=5, min_rating=1, max_rating=5, fill_percentage=0.4):\n    users = [f'User {i+1}' for i in range(num_users)]\n    items = [f'Item {i+1}' for i in range(num_items)]\n    df = pd.DataFrame(index=users, columns=items)\n    total_cells = num_users * num_items\n    cells_to_fill = int(total_cells * fill_percentage)\n    all_positions = [(i, j) for i in range(num_users) for j in range(num_items)]\n    positions_to_fill = random.sample(all_positions, cells_to_fill)\n    for user_idx, item_idx in positions_to_fill:\n        if isinstance(min_rating, int) and isinstance(max_rating, int):\n            rating = random.randint(min_rating, max_rating)\n        else:\n            rating = round(random.uniform(min_rating, max_rating), 1)\n        df.iloc[user_idx, item_idx] = rating\n    return df\n\ndef find_frequent_itemsets(df, min_support=0.2):\n    '''Находит частые наборы товаров с минимальной поддержкой'''\n    df_binary = df.notna().astype(int)\n    n_users = len(df_binary)\n    \n    items = list(df.columns)\n    frequent_itemsets = {}\n    \n    for item in items:\n        support = df_binary[item].sum() / n_users\n        if support >= min_support:\n            frequent_itemsets[frozenset([item])] = support\n    \n    for size in range(2, len(items) + 1):\n        candidate_itemsets = []\n        for itemset in combinations(items, size):\n            itemset_frozenset = frozenset(itemset)\n            support = (df_binary[list(itemset)].sum(axis=1) == size).sum() / n_users\n            if support >= min_support:\n                candidate_itemsets.append((itemset_frozenset, support))\n        \n        if not candidate_itemsets:\n            break\n            \n        for itemset, support in candidate_itemsets:\n            frequent_itemsets[itemset] = support\n    \n    return frequent_itemsets\n\ndef generate_association_rules(frequent_itemsets, min_confidence=0.5):\n    '''Генерирует ассоциативные правила из частых наборов'''\n    rules = []\n    \n    for itemset, support in frequent_itemsets.items():\n        if len(itemset) < 2:\n            continue\n            \n        for i in range(1, len(itemset)):\n            for antecedent in combinations(itemset, i):\n                antecedent = frozenset(antecedent)\n                consequent = itemset - antecedent\n                \n                if antecedent in frequent_itemsets:\n                    confidence = support / frequent_itemsets[antecedent]\n                    if confidence >= min_confidence:\n                        lift = confidence / frequent_itemsets[consequent] if consequent in frequent_itemsets else 0\n                        rules.append({\n                            'antecedent': list(antecedent),\n                            'consequent': list(consequent),\n                            'support': support,\n                            'confidence': confidence,\n                            'lift': lift\n                        })\n    \n    return rules\n\ndef find_similar_items_jaccard(df):\n    '''Находит похожие товары по коэффициенту Жаккара'''\n    items = df.columns\n    similarities = {}\n    \n    for item1 in items:\n        for item2 in items:\n            if item1 != item2:\n                set1 = set(df[df[item1].notna()].index)\n                set2 = set(df[df[item2].notna()].index)\n                \n                intersection = len(set1.intersection(set2))\n                union = len(set1.union(set2))\n                \n                jaccard = intersection / union if union > 0 else 0\n                similarities[(item1, item2)] = jaccard\n    \n    return similarities\n\ndef market_basket_analysis(df, min_support=0.2, min_confidence=0.5):\n    '''Полный анализ рыночной корзины'''\n    frequent_itemsets = find_frequent_itemsets(df, min_support)\n    rules = generate_association_rules(frequent_itemsets, min_confidence)\n    similarities = find_similar_items_jaccard(df)\n    \n    return frequent_itemsets, rules, similarities\n\ndf = create_user_item_dataframe(num_users=5, num_items = 5)\nfrequent_itemsets, rules, similarities = market_basket_analysis(df, min_support=0.2, min_confidence=0.5)\n\nprint('\n1. ЧАСТЫЕ НАБОРЫ ТОВАРОВ (min_support=0.2):')\nfor itemset, support in sorted(frequent_itemsets.items(), key=lambda x: x[1], reverse=True):\n    print(f'{list(itemset)}: support = {support:.3f}')\n\nprint('\n2. АССОЦИАТИВНЫЕ ПРАВИЛА (min_confidence=0.5):')\nif rules:\n    rules_df = pd.DataFrame(rules)\n    rules_df = rules_df.sort_values('lift', ascending=False)\n    for _, rule in rules_df.iterrows():\n        print(f'{rule['antecedent']} → {rule['consequent']}')\n        print(f'  support: {rule['support']:.3f}, confidence: {rule['confidence']:.3f}, lift: {rule['lift']:.3f}')\nelse:\n    print('Ассоциативные правила не найдены с заданными параметрами')\n\nprint('\n3. ПОХОЖИЕ ТОВАРЫ (коэффициент Жаккара):')\nsorted_similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)\nfor (item1, item2), similarity in sorted_similarities[:10]:\n    if similarity > 0:\n        print(f'{item1} ↔ {item2}: {similarity:.3f}')\n\nprint('\n4. РЕКОМЕНДАЦИИ ДЛЯ КАЖДОГО ПОЛЬЗОВАТЕЛЯ:')\nfor user_idx, user in enumerate(df.index):\n    user_items = df.loc[user].dropna().index.tolist()\n    print(f'\n{user} купил: {user_items}')\n    \n    recommendations = set()\n    for rule in rules:\n        if set(rule['antecedent']).issubset(set(user_items)):\n            recommendations.update(rule['consequent'])\n    \n    available_recommendations = [item for item in recommendations if item not in user_items]\n    if available_recommendations:\n        print(f'  Рекомендации: {available_recommendations}')\n    else:\n        most_similar = []\n        for item in user_items:\n            for (item1, item2), sim in sorted_similarities:\n                if item1 == item and item2 not in user_items and sim > 0:\n                    most_similar.append((item2, sim))\n        \n        if most_similar:\n            best_rec = max(most_similar, key=lambda x: x[1])\n            print(f'  Рекомендация по похожести: {best_rec[0]} (схожесть: {best_rec[1]:.3f})')\n        else:\n            print('  Рекомендации не найдены')",
    6: """Рекомендательные системы – это системы, которые помогают пользователям находить интересные товары или контент, основываясь на их предпочтениях или активности.
История: Появились в 90-х годах с первыми системами электронной коммерции и потоковых сервисов. Одним из первых известных примеров является система рекомендаций фильмов в MovieLens.
Современные примеры: Netflix, Amazon, Spotify и др.
Пример: Amazon: рекомендательная система предлагает товары на основе того, что другие пользователи купили, посмотрели или оценили.""",
    7: """Пользователи (users): люди, взаимодействующие с системой, чьи предпочтения нужно предсказать.
Товары (items): продукты, услуги, фильмы, книги и т.д., которые система рекомендует пользователям.
Рейтинги (ratings): числовые или бинарные оценки (например, от 1 до 5), которые пользователи дают товарам. Могут быть явными (прямые оценки) или неявными (время просмотра, клики).
Предпочтения – это предпочтительные товары для пользователя.
Рекомендации – это прогнозирование этих предпочтений.""",
    8: """Проблема прогнозирования
В этой версии задачи нам дана матрица из m пользователей и n элементов. Каждая строка матрицы представляет пользователя, а каждый столбец представляет элемент. Значение ячейки в i-й строке и j-м столбце обозначает оценку, данную пользователем i элементу j. Это значение обычно обозначается как rij. Наша задача - спрогнозировать неизвестную оценку пользователя""",
    9: """Задача ранжирования Learning to Rank (LTR) — вид сортировки, который позволяет находить потенциально интересные элементы — такие как товары, видео или статьи — и выводить их в порядке убывания их предполагаемой значимости для конкретного пользователя в определённой ситуации.
Существует несколько подходов к ранжированию:
• Content-based filtering: Ранжирование на основе характеристик элементов и профиля пользователя.
• Collaborative filtering: Использует данные о взаимодействии других пользователей для предсказания предпочтений текущего пользователя.
• Hybrid methods: Комбинируют разные подходы для улучшения качества рекомендаций.""",
    10: """Рекомендательные системы классифицируются по подходам к генерации рекомендаций:
Коллаборативная фильтрация:
На основе пользователей: Рекомендации формируются на основе предпочтений похожих пользователей (user-based).
На основе элементов: Рекомендации основаны на сходстве между элементами, которые пользователь уже оценил (item-based).
Контентная фильтрация:
Рекомендации строятся на основе характеристик элементов (например, жанр, теги) и профиля пользователя.
Гибридные системы:
Комбинируют коллаборативную и контентную фильтрацию для повышения точности и преодоления ограничений (например, проблема "холодного старта").
Системы на основе знаний:
Используют явные знания о пользователе или домене (например, правила или онтологии) для рекомендаций.
Контекстно-зависимые системы:
Учитывают контекст (время, место, устройство) при генерации рекомендаций.
Социальные рекомендательные системы:
Основаны на социальных связях пользователя (друзья, подписки) и их предпочтениях.
Системы на основе глубокого обучения:
Используют нейронные сети для моделирования сложных зависимостей в данных (например, матричные факторизации с нейронными сетями).
Каждый тип подходит для разных сценариев в зависимости от доступных данных и целей системы.""",
    11: """Рекомендательные системы сталкиваются с различными проблемами и вызовами, которые можно разделить на модельные, инфраструктурные и этические.
Модельные проблемы
Проблема холодного старта. Для новых пользователей или объектов в системе недостаточно данных, что делает рекомендации неточными.
Разреженность данных. Активные пользователи оценивают только небольшое количество элементов, что снижает точность рекомендаций.
Вариативность свойств пользователей или объектов. В системе могут быть сотни тысяч пользователей и объектов с различными свойствами, что сложно учитывать на больших объемах.
Инфраструктурные проблемы
Обработка больших данных. Современные рекомендательные системы работают с информацией о миллионах пользователей и их взаимодействиях с миллионами объектов, что требует мощных вычислительных ресурсов.
Масштабируемость алгоритмов. Алгоритмы, которые хорошо работают на небольших данных, не всегда эффективны при увеличении их объема.
Обновление данных в реальном времени. Поведение пользователей меняется динамически, и система должна оперативно обновлять свои рекомендации.
Этические вопросы
Конфиденциальность данных пользователей. Рекомендательные системы используют личные данные, такие как история покупок, просмотры и даже местоположение, что создает риск утечки.
Эффект «информационного пузыря». Системы могут ограничивать кругозор пользователей, предлагая только тот контент, который соответствует их прошлым предпочтениям.
Возможность манипуляции предпочтениями. Алгоритмы могут быть настроены таким образом, чтобы продвигать определенные товары или идеи, что приводит к скрытому влиянию на выбор пользователя.
Методы решения проблем
Холодный старт: гибридные методы, которые учитывают популярные товары или анализируют схожие профили пользователей.
Разреженность данных: методы кластеризации, которые позволяют разделить задачи на подзадачи с наиболее связанной информацией внутри каждого кластера.
Информационный пузырь: в выдачу добавляются случайные или популярно-рекомендованные элементы, чтобы пользователь мог видеть разнообразный контент.
Конфиденциальность: вводятся строгие стандарты безопасности, используется анонимизация данных и соблюдается законодательство о защите персональных данных.""",
    12: """Коллаборативная фильтрация (Collaborative Filtering, CF) – это самый известный подход к созданию рекомендаций.
CF:
– используется крупными коммерческими сайтами электронной коммерции;
– хорошо понятен, существуют различные алгоритмы и вариации;
– применим во многих областях (книги, фильмы, DVD, ..).
Подход: используйте «мудрость толпы» для рекомендации товаров.
Основное предположение и идея:
– пользователи дают оценки товарам каталога (неявно или явно, implicitly or explicitly);
– клиенты, у которых были схожие вкусы в прошлом, будут иметь схожие вкусы в будущем.
Сформировались два подхода к коллаборативной
фильтрации:
User-based: пользователи, похожие друг на друга, будут иметь схожие оценки.
Item-based: товары, получающие схожие оценки от пользователей, будут иметь схожие оценки и у других пользователей.""",
    13: """Контентные рекомендации (content-based): алгоритмы анализируют атрибуты товара и сравнивают их с предпочтениями пользователя.
Например, если пользователь оценил фильм с жанром “фантастика”, система предложит другие фантастические фильмы.
Принцип работы:
Извлекаем признаки для каждого объекта (товар, книга, фильм), выделяя характеристики (категория, стоимость, жанр, автор, ключевые слова и т.д.). Используем TF-IDF или любой другой метод NLP для хранения этой информации
Создаем профиль для каждого пользователя: просмотры, лайки, список покупок, избранного и т.д.
Сходство между объектами и профилем рассчитывается с помощью метрик близости (евклидово расстояние, косинусное расстояние)
Элементы с наибольшим сходством рекомендуются пользователю
Преимущества: независимость от других пользователей (учитываются особенности конкретного человека), хороша для новых пользователей (не требуется история взаимодействия), прозрачность рекомендации.
Недостатки: ограниченность (может “замкнуться” в своих рекомендациях), зависимость от количества и качества признаков, проблемы с “холодным стартом” (как давать рекомендации человеку, о котором ничего не известно)""",
    14: """Основная идея фильтрации на основе пользователей заключается в том, что если мы можем найти пользователей, которые покупали и которым понравились похожие товары в прошлом, они с большей вероятностью купят похожие товары и в будущем. Поэтому эти модели рекомендуют пользователю товары, которые понравились похожим пользователям.""",
    15: """Если группа людей оценила два товара одинаково, то эти два товара должны быть похожими. Поэтому, если человеку нравится один конкретный товар, он, скорее всего, заинтересуется и другим товаром. Это принцип, по которому работает фильтрация на основе товаров.""",
    16: """Холодный старт (Cold Start): Когда у системы нет данных о новом пользователе или новом товаре.
Виды холодного старта
Пользовательский (User Cold Start): нет истории взаимодействий
Объектный (Item Cold Start): новый товар без откликов пользователей.
Системный (System Cold Start): отсутствие данных при запуске системы.
Способы решения
Для новых пользователей:
Анкета при регистрации
Использование демографических данных
Контентно-ориентированная фильтрация
Рекомендации популярных товаров
Для новых объектов:
Использование описательных признаков (жанр, категория и др.)
Экспертные оценки
Сопоставление с похожими объектами
Для новых систем:
Импорт внешних данных
Инициализация модели с использованием открытых датасетов
Применение гибридных моделей""",
    17: """Сходство — это мера того, насколько два объекта (например, пользователи, товары и т. д.) похожи друг на друга в определённом аспекте.
Функция подобия — формализует это понятие, вычисляя степень сходства между объектами, где 1 идентичные элементы, 0 не имеющие ничего общего.""",
    18: """Чтобы найти сходство между двумя элементами, нужно подсчитать, сколько пользователей купили оба элемента, а затем разделить на количество пользователей, которые купили один из них (или оба).
J(i, j) = (Пользователи, купившие оба товара) / (Пользователи, купившие либо i, либо j)""",
    19: """L1- и L2-нормы — это два распространенных способа измерения расстояния или сходства между векторами.
L1-норма (Манхэттенское расстояние)
Вычисляется как сумма абсолютных разностей между соответствующими элементами двух векторов. Для двух векторов  x  и  y  размерности  n :
L2-норма (Евклидово расстояние)
Вычисляется как квадратный корень из суммы квадратов разностей между соответствующими элементами двух векторов. Для двух векторов  x  и  y :""",
    20: """Коэффициент Отиаи:
Применяется к бинарным данным (например, лайки или покупки).
Формула:
Значения: от 0 (нет сходства) до 1 (полное совпадение).
Плюс: работает с разреженными данными, не чувствителен к разному количеству оценок.
Используется: в интернет-магазинах, где важны действия (купил/не купил).
Коэффициент Пирсона:
Подходит для числовых данных (например, рейтинги от 1 до 5).
Формула:
Значения: от -1 (обратная зависимость) до 1 (полное совпадение), 0 — нет связи.
Плюс: учитывает величину оценок, но требует много общих данных.
Используется: в сервисах с рейтингами (например, Netflix).
Чем отличаются:
Отиаи: для бинарных, разреженных данных, проще в использовании.
Пирсон: для числовых, плотных данных, точнее при схожих оценках.
Оба помогают находить похожих пользователей или элементы в коллаборативной фильтрации, выбор зависит от типа данных.
Сравнение:
Отиаи: бинарные данные, разреженные матрицы.
Пирсон: числовые данные, плотные матрицы.
Используются в коллаборативной фильтрации, выбор зависит от данных.""",
    21: """Коллаборативная фильтрация (Collaborative Filtering, CF) – это самый известный подход к созданию рекомендаций.
CF:
– используется крупными коммерческими сайтами электронной коммерции;
– хорошо понятен, существуют различные алгоритмы и вариации;
– применим во многих областях (книги, фильмы, DVD, ..).
Подход: используйте «мудрость толпы» для рекомендации товаров.
Основное предположение и идея:
– пользователи дают оценки товарам каталога (неявно или явно, implicitly or explicitly);
– клиенты, у которых были схожие вкусы в прошлом, будут иметь схожие вкусы в будущем.
Математическая постановка задачи
Рассмотрим матрицу взаимодействий R, где строки — это пользователи, а столбцы — это товары. Значения в ячейках r_mn — это оценки, которые пользователи m выставили товарам n.
Цель: заполнить пропуски в матрице, то есть предсказать оценки, которых нет. Для этого мы используем информацию о других пользователях и товарах.""",
    22: """1. Memory-based
Используют всю матрицу взаимодействий без предварительного обучения модели.
User-based filtering:
Ищет пользователей с похожими оценками и предлагает объекты, которые они оценили.
Item-based filtering:
Ищет похожие объекты и рекомендует их тем, кому понравился один из них.
Методы:
Косинусное сходство
Корреляция Пирсона
Jaccard
2. Модельные (model-based)
Строят модель на основе обучающих данных.
Примеры:
Матричная факторизация:
SVD, ALS, NMF — представляют пользователей и объекты в виде латентных факторов.
Байесовские модели,
Методы машинного обучения:
k-NN, SGD, нейронные сети.
Оба подхода могут комбинироваться в гибридных системах.""",
    23: """Коллаборативная фильтрация основывается на идее, что пользователи, которые ставили похожие оценки одним и тем же товарам, вероятно, имеют схожие предпочтения и для других товаров. Одним из подходов такой фильтрации является user-based: пользователям, похожим друг на друга, будут нравится похожие вещи.
Рассмотрим алгоритм:""",
    24: """Коллаборативная фильтрация основывается на идее, что пользователи, которые ставили похожие оценки одним и тем же товарам, вероятно, имеют
схожие предпочтения и для других товаров.
Item-based: товары, получающие схожие оценки от пользователей, будут иметь схожие оценки и у других пользователей.""",
    25: """Сингулярное разложение (SVD) — метод линейной алгебры, который позволяет разложить матрицу на три составляющие: две ортогональные матрицы и одну диагональную. SVD применяется в рекомендательных системах для уменьшения размерности данных и выявления скрытых факторов, влияющих на рейтинги.""",
    26: """Класс алгоритмов совместной фильтрации, используемых в рекомендательных системах. Алгоритмы факторизации матриц работают путем разложения матрицы взаимодействия пользователя и элемента на произведение двух прямоугольных матриц меньшей размерности.
Сингулярное разложение (SVD) — метод линейной алгебры, который позволяет разложить матрицу на три составляющие: две ортогональные матрицы и одну диагональную. SVD применяется в рекомендательных системах для уменьшения размерности данных и выявления скрытых факторов, влияющих на рейтинги.
Пусть имеется матрица рейтингов 𝑅∈𝑅^(𝑚×𝑛), где m — количество пользователей, n — количество объектов. Цель — найти такие матрицы P∈𝑅^(𝑚×k), Q∈𝑅^(n×k), что 𝑅≈PQ^T Здесь 𝑘≪𝑚, n — число скрытых факторов.
Любую матрицу
𝑅∈𝑅^(𝑚×𝑛) можно разложить на три матрицы: R=UΣV^T, где U∈𝑅^(𝑚×m) и V∈𝑅^(n×𝑛) - ортогональные матрицы, Σ∈𝑅^(𝑚×n) — диагональная матрица сингулярных чисел. Для приближения используют усечённое SVD: R≈U_k Σ_k V_k ^ T, где k - выбранное число сингулярных компонент (скрытых факторов).
Матрицы P = U_k * Σ_k ^ (1/2) и Q = V_k * Σ_k ^ (1/2) задают представление пользователей и объектов в общем латентном пространстве.
Рекомендации строятся по приближенному рейтингу: ^r_ui = p_u^T * q_i, где p_u - вектор признаков пользователя, q_i - вектор признаков объекта.""",
    27: """Базисный предиктор:
- базовый прогноз элемента  для пользователя .
- отклонение пользователя.
- отклонение элемента.
- среднее арифметическое всех оценок.
Дальше SVD уточняет прогноз, добавляя латентные факторы (скрытые признаки пользователей и объектов).""",
    28: """где нужно вычислить смещение для каждого пользователя (b_u), взяв сумму разниц между оценками пользователей и средним и разделить на число оценок.
Когда отклонения всех пользователей вычислены, аналогичным образом вычислить отклонение предметов (b_i)""",
    29: """Библиотека Surprise (Simple Python Recommendation System Engine) — это популярный инструмент для быстрого прототипирования и исследования классических алгоритмов рекомендательных систем, основанных на коллаборативной фильтрации (CF).
Ключевые особенности Surprise:
Фокус на коллаборативной фильтрации: Решает задачи предсказания оценок (rating prediction) для пользователей и айтемов.
Простой интерфейс в стиле Scikit-learn: Использует знакомые методы .fit(), .predict(), cross_validate().
Встроенные алгоритмы: Поддерживает множество классических алгоритмов CF:
SVD: Сингулярное разложение (аналог FunkSVD).
SVDpp: Улучшенный SVD, учитывающий неявные отзывы (просмотры, клики).
NMF: Неотрицательная матричная факторизация.
KNNBasic, KNNWithMeans, KNNWithZScore, KNNBaseline: Алгоритмы на основе соседей (User-based или Item-based CF).
SlopeOne, CoClustering: Более специализированные алгоритмы.
Встроенные датасеты: Упрощает начало работы (Dataset.load_builtin('ml-100k')).
Гибкая загрузка данных: Поддержка пользовательских датасетов из файлов, pandas DataFrame, массивов.
Инструменты оценки: Встроенные метрики (RMSE, MAE) и удобная кросс-валидация.
Поиск гиперпараметров: Интеграция с GridSearchCV для оптимизации алгоритмов.
Чистый Python: Легко читать исходный код и расширять.""",
    30: """Градиентный спуск для матричной факторизации (MF) — это метод оптимизации, используемый для разложения исходной матрицы рейтингов R (например, пользователь-объект) на две матрицы меньшей размерности:
Инициализация: Случайно инициализировать U и V.
Целевая функция:
Обновление (по градиенту):
Повторение: Обновлять до сходимости (малое изменение ошибки).
Метод широко используется в рекомендательных системах.""",
    31: """Стохастический градиентный спуск
Для каждой оценки r(u,i): рассчитывается прогноз оценки e = r_ui – q_i * p_u.;
обновляется значение x так, что x = x - α · e, где α - скорость обучения.
Факторизация. Цель – на основе известных оценок создать две матрицы таким образом, чтобы i-я строка матрицы факторов элементов умножалась на u-й столбец матрицы факторов пользователей, и в результате должна быть матрица, похожая на реальные оценки.
Надо найти такие матрицы Q и P, которые минимизируют следующее уравнение для всех известных оценок.
C использованием алгоритма стохастического градиентного спуска:""",
    32: """Для каждой оценки rui среди оценок нужно
вычислить:
γ ‒ скорость обучения;
λ ‒ регуляризация.
Прогноз оценки - это сумма (комбинация) четырех вещей""",
    33: """Сингулярное разложение (SVD) – метод линейной алгебры, позволяющий разложить матрицу на три составляющие: две ортогональные матрицы и одну диагональную. Применяется для уменьшения размерности данных и выявления скрытых факторов.
Параметры алгоритма:
Инициализация признаков – нужно определить стартовую точку для градиентного спуска;
Скорость обучения – как быстро будем двигаться на каждом шагу;
Регуляризация – как сильно алгоритм регулирует ошибки? Должен ли он быть одинаковым для всех выражений или нужно разделить его на признаки и отклонения?
Сколько итераций – насколько специализированным будет алгоритм для обучающих данных?
Например, чем больше число факторов (rank) тем качественнее модель будет улавливать сложные зависимости. Однако при этом слишком большое их количество негативно скажется на переобучении.""",
    34: """FunkSVD (также известный как SVD с обратной связью через стохастический градиентный спуск) — это популярный метод матричной факторизации для построения рекомендательных систем.
В отличие от классического SVD, который требует полной матрицы и плохо работает с разреженными данными, FunkSVD оптимизирует разложение только по известным значениям матрицы взаимодействий (например, оценкам пользователей).
Постановка задачи
Имеется матрица взаимодействий пользователей и объектов.
Цель: разложить матрицу R (размером m×n) в произведение двух матриц:
P (размер m×k) — матрица скрытых признаков пользователей.
Q (размер n×k) — матрица скрытых признаков объектов.
Таким образом решаем задачу минимизации MSE по известным элементам из матрицы взаимодействий.""",
    35: """Расчет рекомендаций в окрестности строится на основе схожести пользователей (user-based) или товаров (item-based). Основная идея — найти наиболее похожих пользователей или товаров и предсказать оценку на основе их предпочтений.
user-based
item-based""",
    36: """TF-IDF (Term Frequency – Inverse Document Frequency) — взвешенная модель представления текстов, которая отражает важность термина в документе и в корпусе. В рекомендательных системах используется для построения векторных представлений объектов и пользователей на основе текстовых описаний (аннотаций, отзывов и т.п.).
TF (частота термина):
IDF (обратная частота документа):
TF-IDF вес:
Добавление контентной информации. После получения векторных представлений пользователей/объектов комбинируем их с текстовыми или категориальными признаками:
item_embeddings = model.item_factors
user_embeddings = model.user_factors
# Добавляем TF-IDF текстовых данных
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer().fit_transform(['text1', 'text2', 'text3'])
# Конкатенация признаков
hybrid_features = np.hstack((item_embeddings, tfidf.toarray()))""",
    37: """Проблема неподходящих рекомендаций возникает, когда алгоритм рекомендует пользователю фильмы, значительно отличающиеся от его предпочтений (даже по жанрам), из-за большого отклонения у этих фильмов.
Суть проблемы:
Алгоритм комбинирует скалярное произведение факторов пользователя и элемента с отклонениями элементов перед сортировкой.
Вопрос в том, нужно ли сортировать элементы до или после добавления отклонений.
Решение проблемы:
Если сортировать элементы после добавления отклонений, то влияние отклонений ограничивается только схожими элементами, что улучшает релевантность рекомендаций.
Дополнительно можно снизить скорость обучения для отклонений, чтобы уменьшить их негативное влияние.""",
    38: """Одним из главных недостатков демографических фильтров является то, что они основываются на предположении, что люди определенной демографической группы думают и оценивают одинаково. Но можно с уверенностью сказать, что это слишком завышенное предположение. Не всем мужчинам нравятся боевики. Не всем детям нравятся анимационные фильмы. Точно так же крайне надуманно предполагать, что люди из определенной области или профессии будут иметь одинаковые вкусы.
Необходимо найти способ группировки пользователей с помощью гораздо более мощного показателя, чем демографические данные. Из изучения методов анализа данных известно о таком мощном инструменте, как кластеризация. Можно использовать алгоритм кластеризации, например k-means (k-средних), для объединения пользователей в кластер, а затем учитывать только пользователей из того же кластера при прогнозировании оценок.""",
    39: """Кластеризация k-средних (k-means) в рекомендательных системах применяется как вспомогательный инструмент для решения ключевых задач: сегментации пользователей/товаров, упрощения вычислений и улучшения качества рекомендаций.
Основные задачи, решаемые с помощью k-means
Сегментация пользователей (User Clustering)
Кластеризация товаров/контента (Item Clustering)
Предобработка данных для других моделей
Построение гибридных систем""",
    40: """Применение метода k-ближайших соседей (kNN) в рекомендательных системах основано на идее, что похожие пользователи или объекты имеют схожие предпочтения.
User-based kNN (по пользователям):
Ищем kkk пользователей, похожих на целевого пользователя (по метрике сходства: косинус, корреляция и т.д.).
Рекомендации строятся на основе оценок этих соседей.
Item-based kNN (по объектам):
Ищем kkk похожих объектов (фильмов, товаров и т.п.) на те, что пользователь уже оценил.
Предсказываем оценку пользователя на новый объект, используя оценки на похожие.
Простота реализации.
Интерпретируемость (рекомендации можно объяснить).
Медленно работает на больших данных.
Не учитывает скрытые факторы (в отличие от матричной факторизации).""",
    41: """Mean Absolute Error (Средняя абсолютная ошибка):
где  — реальный рейтинг,  — предсказанный,  — количество прогнозов.
Если MAE равен 0, это указывает на идеальное соответствие прогнозов реальным значениям. Чем выше значение MAE, тем больше ошибок в прогнозах модели.
MAE выражается в тех же единицах, что и прогнозируемая величина, что удобно для интерпретации.
RMSE (Root Mean Squared Error, Корень из среднеквадратичной ошибки):
Квадратный корень из MSE, возвращающий ошибку в той же шкале, что и рейтинги.
Низкое значение RMSE указывает на то, что прогнозы модели ближе к фактическим значениям. Высокое значение означает, что прогнозы отклоняются от фактических, и модель менее точна.
RMSE измеряется в тех же единицах, что и прогнозируемые значения.""",
    42: """Кросс-валидация — метод оценки качества рекомендательной модели путем многократного обучения и тестирования на разных разбиениях данных. Это помогает получить более надежную оценку работы системы и избежать переобучения.
В рекомендательных системах часто используют:
Split по пользователям — данные разбиваются так, что часть пользователей полностью уходит в обучающую выборку, часть — в тестовую (используется для проверки обобщаемости на новых пользователях).
Split по взаимодействиям (рейтингам) — у каждого пользователя часть рейтингов идёт в обучение, часть в тест (проверка прогноза для известных пользователей).
Популярные схемы:
k-fold кросс-валидация — данные разделяются на несколько частей (или «фолдов»). Алгоритм обучается на всех фолдах, кроме одного, который используется для тестирования. Это повторяется несколько раз, чтобы получить общее представление о производительности модели.
Leave-One-Out — для каждого пользователя из данных берется один рейтинг для теста, остальное — для обучения; помогает проверить точность на уровне отдельного события.
Кросс-валидация позволяет объективно сравнивать модели, выбирая лучшую для рекомендаций: чем метрики в среднем выше, тем качественнее модель, чем меньше стандартное отклонение метрик между фолдами, тем модель стабильнее.""",
    43: """Mean Absolute Error (Средняя абсолютная ошибка):
где  — реальный рейтинг,  — предсказанный,  — количество прогнозов.
Mean Squared Error (Средняя квадратичная ошибка):
Учитывает квадрат разницы между реальным и предсказанным рейтингом, что сильнее штрафует большие ошибки.
RMSE (Root Mean Squared Error, Корень из среднеквадратичной ошибки):
Квадратный корень из MSE, возвращающий ошибку в той же шкале, что и рейтинги.
Precision (Точность):
Доля релевантных элементов в списке рекомендаций.
Например, если из 10 рекомендованных фильмов 7 понравились пользователю, Precision@10 = 0.7.
Recall (Полнота):
Доля релевантных элементов, которые были рекомендованы, из всех релевантных элементов.
Показывает, насколько система "захватывает" все подходящие элементы. Высокий Recall важен, если цель — не упустить ничего важного.
F1-Score:
Полезна, когда нужно учитывать и точность, и полноту одновременно.
MAP (Mean Average Precision):
Средняя точность по всем пользователям, учитывающая порядок рекомендаций. Формула сложная, но суть: оценивает, насколько высоко в списке находятся релевантные элементы. Высокий MAP означает, что релевантные элементы находятся в начале списка рекомендаций.
NDCG (Normalized Discounted Cumulative Gain):
Учитывает релевантность и позицию элемента в списке рекомендаций. Более релевантные элементы на высоких позициях дают больший вклад. Формула включает нормализацию для сравнения с идеальным ранжированием.
NDCG@10 = 0.9 означает, что список рекомендаций близок к идеальному порядку.
Для Netflix, прогнозирующего рейтинг фильма, важны MAE или RMSE, чтобы оценить точность предсказания пользовательских оценок.
Для Spotify, рекомендующего песни, важны Precision@10, Recall@10 и NDCG, чтобы оценить релевантность и порядок треков в плейлисте.""",
    44: """TF-IDF (Term Frequency-Inverse Document Frequency) — классический метод для оценки важности слов в документах. В рекомендательных системах он часто используется в контент-базированных подходах (например, для анализа текстовых описаний товаров, фильмов или статей). Однако у него есть ограничения, и на практике применяются более продвинутые методы.
1. Ограничения TF-IDF
Не учитывает семантику (синонимы, многозначность слов).
Плохо работает с короткими текстами (например, названия товаров).
Не улавливает контекст (зависимость между словами).
Чувствителен к стоп-словам и шуму.
2. Расширения TF-IDF: TF-IDF с улучшенной предобработкой
Лемматизация и стемминг (приведение слов к базовой форме).
Удаление редких/частых слов (настройка min_df/max_df в sklearn).
N-граммы (учёт словосочетаний, например, "искусственный интеллект").
3. Альтернативы TF-IDF
Word Embeddings (Word2Vec, GloVe, FastText)
BERT и трансформеры""",
    45: """Корреляция Пирсона (Pearson Correlation Coefficient - PCC) — это статистическая мера, используемая в коллаборативной фильтрации на основе пользователей (User-Based CF) для количественной оценки линейной зависимости между предпочтениями двух пользователей. Она измеряет, насколько согласованно пользователи отклоняются от своих средних оценок при выставлении рейтингов общим объектам.
Коэффициент Пирсона:
Подходит для числовых данных (например, рейтинги от 1 до 5).
Формула:
Значения: от -1 (обратная зависимость) до 1 (полное совпадение), 0 — нет связи.
Плюс: учитывает величину оценок, но требует много общих данных.
Используется: в сервисах с рейтингами (например, Netflix).""",
    46: """Контентная фильтрация формирует рекомендации на основе схожести между объектами и интересами пользователя, выраженными в его профиле. Профиль пользователя отражает предпочтения на основе характеристик (метаданных) понравившихся объектов.
Построение профиля пользователя с TF-IDF
Каждому объекту (фильму, книге и т.д.) сопоставляется TF-IDF-вектор на основе текстового описания.
Профиль пользователя u_v — это агрегированный вектор TF-IDF по всем объектам, с которыми он взаимодействовал:
Актуализация профиля
При каждом новом взаимодействии профиль пересчитывается.
Добавление нового объекта: пересчёт среднего вектора с учётом нового TF-IDF.
Можно применять экспоненциальное сглаживание или временное взвешивание.
Использование в рекомендациях
Рассчитывается косинусное сходство между вектором пользователя и векторами всех объектов. Объекты с максимальным сходством — в рекомендации.""",
    47: """Сходство интересов пользователей вычисляется с помощью косинусного расстояния между векторами их предпочтений.
Где:
- векторы предпочтений пользователей.
и  - нормы векторов предпочтений пользователей.
1 – полное сходство (векторы совпадают).
0 – отсутствие сходства (векторы ортогональны).
-1 – противоположные интересы.""",
    48: """Преимущества контентно-ориентированного подхода:
Не требует данных о поведении других пользователей (холодный старт для новых пользователей).
Хорошо работает при отсутствии взаимодействия между пользователями.
Рекомендации легко интерпретировать, так как основаны на свойствах самого контента.
Недостатки:
Ограниченность рекомендаций — предлагает только схожий с уже просмотренным контент.
Требует качественного описания объектов (признаки должны быть информативными).
Сложность обработки неструктурированного контента (текст, изображения).""",
    49: """Индекс сходства Жаккара:
Расстояние Жаккара — метод для измерения сходства пользователей в рекомендательных системах.""",
    50: """Коллаборативная фильтрация — это подход в рекомендательных системах, основанный на анализе предпочтений других пользователей, а не на содержании объектов.
Если пользователи A и B имеют схожие оценки/действия, то объекты, понравившиеся A, можно рекомендовать B.
User-based: рекомендации строятся на основе похожих пользователей.
Item-based: рекомендации основаны на похожих объектах (например, если пользователь любит фильм A, а фильм B похож на него — рекомендуем B).
Матричная факторизация: используется для извлечения скрытых факторов, влияющих на предпочтения.
Если пользователь X и пользователь Y оба оценили фильмы A и B высоко, и Y также высоко оценил фильм C — то C можно порекомендовать X.
Не требует метаданных об объектах.
Хорошо выявляет латентные (скрытые) зависимости.
Проблема холодного старта (для новых пользователей/объектов).
Разреженность матрицы оценок.
Коллаборативная фильтрация — основа многих современных рекомендательных систем (например, Netflix, Amazon).""",
    51: """1.  Косинусное сходство (Cosine Similarity
Измеряет косинус угла между векторами оценок двух пользователей в многомерном пространстве предметов. Фокусируется на *направлении* векторов (паттернах оценок), а не на их длине (величине оценок).
Формула: sim(A, B) = (A • B) / (||A|| * ||B||)
Преимущества:
Устойчиво к разнице в масштабе оценок (один пользователь ставит в среднем 3-4, другой 4-5).
Хорошо работает с разреженными данными (много пропущенных оценок).
Широко используется и эффективно вычисляется.
Недостатки:
Не учитывает смещение пользователя (user bias - склонность ставить завышенные/заниженные оценки)
Корреляция Пирсона (Pearson Correlation)
Описание: Измеряет линейную корреляцию между оценками двух пользователей по совместно оцененным предметам. Учитывает отклонения от средней оценки каждого пользователя (устраняет user bias).
Формула:
sim(A, B) = Σ((a_i - mean_A) * (b_i - mean_B)) / (sqrt(Σ(a_i - mean_A)²) * sqrt(Σ(b_i - mean_B)²))
Преимущества:
Учитывает смещение пользователя (корректирует на среднюю оценку).
Хорошо выявляет линейные зависимости в предпочтениях.
Недостатки:
Чувствителен к количеству совместно оцененных предметов. При малом их числе (< 50) оценка ненадежна.
Вычислительно дороже косинусного сходства.
Плохо работает при очень разреженных данных.
Сходство Жаккара (Jaccard Similarity)
Описание: Измеряет сходство на основе наличия оценок (а не их значений), рассматривая наборы предметов, оцененных каждым пользователем. Подходит для бинарных данных.
Формула:
Преимущества:
Простота вычисления.
Независимость от значений оценок, только от факта взаимодействия.
Полезен для неявных фидбэков (клики, просмотры).
Недостатки:
Полностью игнорирует значения оценок
Не подходит для систем с явными рейтингами (1-5 звезд).
Выбор меры зависит от типа данных (явные/неявные рейтинги, бинарные), разреженности матрицы взаимодействий и вычислительных ресурсов.""",
    52: """Цель: рекомендовать объекты пользователю на основе оценок похожих пользователей.
Шаги алгоритма:
Построение матрицы оценок
Матрица R, где Rui — оценка пользователя u объекту i.
Поиск похожих пользователей
Для заданного пользователя u находим пользователей v, у которых похожие оценки.
Метрики сходства:
Косинусное сходство
Корреляция Пирсона
Jaccard (для бинарных взаимодействий)
Выбор соседей
Берём Top-N наиболее похожих пользователей (по сходству).
Предсказание оценки для объекта i:
где μu, μv — средние оценки пользователей.
Формирование рекомендаций
Сортируем объекты с наибольшими R^ui, не просмотренные пользователем u.""",
    53: """Коллаборативная фильтрация (Collaborative Filtering)
Основана на взаимодействии пользователей с товарами. Алгоритмы ищут похожих пользователей или товары на основе исторических данных. Она использует силу сообщества для предоставления рекомендаций. Коллаборативные фильтры являются одной из самых популярных моделей рекомендаций, используемых в отрасли, и добились огромного успеха для таких компаний, как Amazon. Коллаборативную фильтрацию можно в целом разделить на два типа.
Фильтрация на основе пользователей (User-based filtering )
Основная идея фильтрации на основе пользователей заключается в том, что если мы можем найти пользователей, которые покупали и которым понравились похожие товары в прошлом, они с большей вероятностью купят похожие товары и в будущем. Поэтому эти модели рекомендуют пользователю товары, которые понравились похожим пользователям.
Фильтрация на основе товаров (Item-based filtering )
Если группа людей оценила два товара одинаково, то эти два товара должны быть похожими. Поэтому, если человеку нравится один конкретный товар, он, скорее всего, заинтересуется и другим товаром. Это принцип, по которому работает фильтрация на основе товаров.""",
    54: """Алгоритм Item-Item — это метод коллаборативной фильтрации, который рекомендует товары на основе их сходства с другими товарами, оцененными пользователем.
Шаг 1: Определение сходства товаров
На этом шаге вычисляется матрица попарных сходств между товарами на основе оценок пользователей.
Метрики сходства:
Косинусное сходство (Cosine Similarity) — угол между векторами оценок.
Корреляция Пирсона (Pearson Correlation) — учитывает смещения в оценках.
Скорректированное косинусное сходство (Adjusted Cosine) — учитывает средние оценки пользователей.
Формула косинусного сходства:
sim(i,j)=
где r u,i — оценка пользователя
u товару i,
U — множество пользователей, оценивших оба товара.
Шаг 2: Предсказание оценок и рекомендации
На основе матрицы сходства предсказываем оценки для не просмотренных товаров:
Формула предсказания:""",
    55: """Шаги алгоритма:
Вычислить схожесть пользователей (косинусная, корреляция Пирсона).
Выбрать топ-K ближайших соседей.
Предсказать оценку по формуле выше.
Рекомендовать товары с наивысшими предсказанными оценками.""",
    56: """Гибридные рекомендательные системы комбинируют несколько подходов (например, коллаборативную и контентную фильтрацию) для повышения точности рекомендаций, устойчивости к холодному старту и избежания ограничений отдельных методов.
Основные виды гибридных систем
а) Монолитные (integrated)
 Методы объединяются на уровне модели. Пример: включение контентных признаков в факторизационную модель.
где x_u, x_i признаки пользователя и объекта, f — обучаемая функция (например, через градиентный бустинг или нейросети).
б) Ансамблевые (ensemble)
Комбинируются предсказания нескольких независимых рекомендателей.
в) Смешанные (mixed)
Система сразу предлагает рекомендации от нескольких методов — например, список, где есть и контентные, и коллаборативные рекомендации.
Взвешенный ансамбль рекомендаторов
Идея взвешенного гибридного рекомендатора - обучить два различных рекомендатора и сгенерировать от обоих рекомендации. Когда два или более рекомендаторов объединяются таким образом, мы будем называть их функциональными рекомендаторами.
Функционально-взвешенный гибрид, который сочетает в себе результаты совместной фильтрации и фильтрации на основе контента с весами 0,6 и 0,4 соответственно""",
    57: """Метрики точности (Accuracy Metrics) - оценивают, насколько точно система предсказывает релевантные элементы.
Precision@k – доля релевантных элементов среди топ-k рекомендованных.
Recall@k – доль релевантных элементов, которые попали в топ-k.
F1-Score@k – гармоническое среднее Precision и Recall.
Accuracy – доля верных предсказаний (редко используется из-за дисбаланса классов).
Ранговые метрики (Ranking Metrics) - учитывают порядок рекомендаций.
Mean Average Precision (MAP) – средняя точность по всем пользователям с учетом ранга.
Mean Reciprocal Rank (MRR) – среднее обратного ранга первого релевантного элемента.
NDCG (Normalized Discounted Cumulative Gain) – учитывает порядок и релевантность рекомендаций.""",
    58: """Рекомендательные системы, основанные на знаниях, используют явные знания о предметной области и требования пользователя. В отличие от коллаборативной фильтрации или контентной фильтрации, они не полагаются на исторические данные о поведении пользователей.
Системы на основе ограничений:
Рекомендации строятся на жестких правилах (например, "если бюджет < $1000, то предлагать только бюджетные ноутбуки").
Примеры:
Подбор смартфона по параметрам (ОЗУ, камера, цена).
Рекомендация тура по заданным критериям (страна, бюджет, тип отдыха).""",
    59: """Mean Absolute Error (Средняя абсолютная ошибка):
где  — реальный рейтинг,  — предсказанный,  — количество прогнозов.
Mean Squared Error (Средняя квадратичная ошибка):
Учитывает квадрат разницы между реальным и предсказанным рейтингом, что сильнее штрафует большие ошибки.
RMSE (Root Mean Squared Error, Корень из среднеквадратичной ошибки):
Квадратный корень из MSE, возвращающий ошибку в той же шкале, что и рейтинги.""",
    60: """1. ROC-кривая (Receiver Operating Characteristic) показывает соотношение между:
True Positive Rate (TPR, Recall, Чувствительность) – сколько релевантных объектов нашел алгоритм.
False Positive Rate (FPR) – сколько нерелевантных объектов ошибочно попали в рекомендации.
ROC-AUC - площадь под ROC-кривой
Эти метрики помогают оценить качество модели и принять обоснованные решения, особенно при дисбалансе классов.
2. Точность (Precision)
Доля релевантных объектов среди рекомендованных
Когда важно качество рекомендаций (например, в рекламе, где показ нерелевантных объявлений стоит денег).
3. Полнота (Recall)
Доля найденных релевантных объектов от общего числа релевантных:""",
    61: """Нерелевантные рекомендации («reversals») в системах рекомендаций возникают из-за ошибок алгоритмов, недостатка данных или особенностей пользовательского поведения. Они снижают точность прогнозов и ухудшают пользовательский опыт.
Причины появления reversals
Высокий отрицательный вес объектов. Если система ошибочно интерпретирует отсутствие действий пользователя как явное неприятие, объект получает высокий отрицательный вес. Это приводит к его появлению в рекомендациях даже при низкой релевантности.
Информационный пузырь. Алгоритмы, основанные на моделях, могут зацикливаться на повторяющихся рекомендациях, игнорируя новые или непопулярные объекты.
Проблемы «холодного старта». Недостаток данных о новых пользователях или товарах приводит к неточным предсказаниям.
Разреженность данных. Неполные данные о взаимодействиях пользователя с объектами искажают оценку релевантности.
Методы решения
Гибридные методы. Комбинируют коллаборативную и контентную фильтрацию для повышения точности рекомендаций.
Контентная фильтрация. Использует информацию о характеристиках элементов для создания рекомендаций
Коллаборативная фильтрация. Основана на анализе поведения пользователей
Коэффициенты затухания. Автоматическое снижение отрицательного веса объектов через заданный период времени или после k показов позволяет вернуть их в рекомендации.
Усиление разнообразия. Внедрение механизмов случайного отбора непопулярных объектов или использование методов диверсификации предотвращает зацикливание на узком наборе товаров.""",
    62: """В рекомендательных системах данные обычно представлены в виде разреженной матрицы пользователь–объект (например, оценки пользователей к фильмам). Число пользователей и объектов может быть очень большим, что приводит к высоким вычислительным затратам и проблемам с эффективностью.
Цели:
Уменьшить размер и разреженность исходной матрицы.
Выделить скрытые факторы (например, предпочтения пользователей и характеристики объектов).
Повысить качество рекомендаций за счёт сокращения шума и избыточной информации.
Ускорить обучение и предсказание.
Основные методы:
Матричная факторизация (SVD, ALS и др.) Представляет большую матрицу рейтингов как произведение двух низкоразмерных матриц — матрицы пользователей и матрицы факторов объектов. Итог — плотное представление в скрытом пространстве низкой размерности.
Факторизационные модели (например, факторизационные машины) Позволяют моделировать взаимодействия между признаками с помощью скрытых факторов.
Методы на базе нейронных сетей (автоэнкодеры) Используют сети для сжатия и восстановления признаков, выделяя независимые компоненты.
Результат снижения размерности: Компактное и информативное представление данных, позволяющее улучшить качество рекомендаций и снизить вычислительные затраты.""",
    63: """Виды гибридных рекомендаторов:
1) монолитные рекомендаторы
2)ансамбли рекомендаторов
Ансамбль - это ряд рекомендаторов, чьи
результаты объединяются в одну
рекомендацию
3) смешанные рекомендаторы
Смешанный гибридный рекомендатор, который
складывает выходы нескольких рекомендаторов,
начиная с самого персонализированного, затем от
менее персонализированного и т. д.""",
    64: """Рекомендательные системы могут быть классифицированы по
нескольким критериям:
Сфера применения: e-commerce, стриминговые сервисы,
социальные сети.
Цель рекомендации: Увеличение продаж, удержание
пользователя, персонализация.
Источники данных: Явные рейтинги, неявные действия
(клики, просмотры).
Алгоритм рекомендации: Коллаборативная фильтрация,
контентные рекомендации, гибридные модели.
Примеры классификации:
Рекомендательные системы для e-commerce: Amazon и eBay.
Медиа-контент: Netflix и Spotify.""",
    65: """Предположим, что у нас есть объекты — фильмы и пользователи. Пользователи просматривают фильмы. Нашими исходными данными является разреженная матрица M (фильмы x пользователи). Если пользователь u просмотрел фильм f, то в соответствующей ячейке матрицы M стоит 1. Для того чтобы найти фильмы, похожие на заданный фильм f необходимо знать схожесть фильма f со всеми остальными фильмами. Данные о схожести хранятся в матрице S (фильмы x фильмы).
Базовый алгоритм построения неперсонализированных рекомендаций выглядит следующим образом:
для заданного фильма f найти соответствующую ему строку R в матрице S;
выбрать из строки R множество наиболее похожих на f фильмов — FR;
FR и есть неперсонализированные рекомендации (похожие/сопутствующие).""",
    66: """Способы сбора информации
Явные (эксплицитные) методы - пользователь напрямую указывает свои предпочтения:
Оценки (рейтинги) – например, звёзды (IMDb, Netflix раньше).
Лайки/дизлайки (YouTube, TikTok).
Отзывы и комментарии (Amazon).
Анкетирование – опросы о предпочтениях.
Плюсы: точные данные.
	Минусы: требует усилий от пользователя, мало данных (проблема холодного старта).
Неявные (имплицитные) методы - данные собираются автоматически на основе поведения:
Просмотры и клики (время просмотра, скроллинг).
Покупки и добавление в корзину (Amazon, Aliexpress).
Поисковые запросы (Google, YouTube).
Социальные взаимодействия (лайки, репосты, подписки).
Время сессии и возвраты (частота использования сервиса).
Плюсы: не требует усилий от пользователя, много данных.
	Минусы: шум, не всегда отражает истинные предпочтения.
Обработка и анализ данных
Коллаборативная фильтрация
User-based
Item-based
Контентная фильтрация
Рекомендации на основе характеристик объектов: текстов, Изображения, метаданные.
Гибридные методы
Комбинация методов коллаборативной и контентной фильтрации.
Машинное обучение
Рекомендации на основе алгоритмов классического машинного обучения и глубокого обучения.""",
    67: """Контентно-ориентированные рекомендательные системы (content-based recommender systems) предоставляют рекомендации на основе сходства между объектами (например, товарами, фильмами, книгами), анализируя их внутренние характеристики и предпочтения пользователя.
Система строит профиль пользователя на основе объектов, с которыми он ранее взаимодействовал (например, оценивал положительно), и рекомендует новые объекты, похожие по содержанию (атрибутам).
1) Извлечение признаков объектов:
Признаками могут быть ключевые слова, категории, жанры и т.п.
Например, фильм = {жанр: комедия, режиссёр: Нолан, актёр: ДиКаприо}.
2) Формирование профиля пользователя:
Строится агрегированный вектор признаков на основе понравившихся пользователю объектов.
Формула (TF-IDF, усреднение):
где I_u - множество понравившихся объектов, f_i - вектор признаков объекта i
3) Расчёт сходства между пользователем и объектом:
Косинусное сходство:
4) Выдача рекомендаций:
Объекты сортируются по убыванию сходства с профилем пользователя.""",
    68: """Все типы взаимодействия пользователей с объектами мы можем рассматривать как пользовательский фидбек. Обычно различают явный (explicit) и неявный (implicit) виды фидбека. Фидбек называется явным, если он отражает степень интереса пользователя к объекту. Неявные данные представляют собой косвенные признаки, свидетельствующие о предпочтениях пользователя, однако не подразумевающие прямого выражения мнения (оценок, отзывов).
Ключевое отличие неявных данных от явных
Явные данные предполагают прямую обратную связь от пользователя: рейтинги фильмов, лайки, комментарии.
Неявные данные формируются путём наблюдения действий пользователя без необходимости его активной реакции.""",
    69: """1. Mean Reciprocal Rank (MRR)
MRR — это метрика, которая используется для оценки качества ранжирования ответов в системах поиска. Она измеряет, насколько высоко в списке результатов находится первый релевантный элемент для каждого запроса.
Формула для расчета MRR:
где:
•  Q  — общее количество запросов,
•  rankᵢ  — ранг первого релевантного ответа для  i -го запроса.
2. Normalized Discounted Cumulative Gain (nDCG)
nDCG — это метрика, которая учитывает как релевантность элементов, так и их позиции в списке результатов. Она позволяет оценить качество ранжирования с учетом того, что более релевантные элементы, находящиеся выше в списке, имеют больший вес.
где:
•  relᵢ  — релевантность элемента на позиции  i ,
•  k  — количество позиций, которые мы рассматриваем.
Затем nDCG рассчитывается как:
nDCGₖ = DCGₖ / IDCGₖ
где  IDCGₖ  — это идеальный DCG, который рассчитывается для идеального порядка релевантных элементов.""",
    70: """Актуальность рекомендаций — это мера того, насколько предложенные рекомендации соответствуют текущим интересам и потребностям пользователя.
Персонализация — учитывает поведение, предпочтения и контекст пользователя.
Вовремя и к месту — рекомендация должна быть полезной в момент её получения.
Обновляемость — система должна быстро адаптироваться к изменениям интересов.
Актуальные рекомендации повышают вовлечённость, удовлетворённость и эффективность взаимодействия с системой.""",
    71: """Гибридные рекомендательные системы представляют собой подход, который сочетает в себе несколько техник рекомендаций для повышения их эффективности. Они объединяют сильные стороны различных методов, чтобы компенсировать их индивидуальные недостатки.
1. Монолитные гибридные рекомендаторы
Монолитные гибридные рекомендаторы интегрируют различные подходы к рекомендациям на уровне модели. Разные алгоритмы или источники данных объединяются в единую систему до того, как она выдает рекомендации.
Принцип работы:
Интеграция может происходить через объединение признаков из разных источников (например, контентных данных и поведенческих данных пользователей).
Преимущества:
Более глубокая интеграция данных и алгоритмов.
Возможность создания более точных и персонализированных рекомендаций за счет единого подхода к обработке информации.
Недостатки:
Сложность разработки и поддержки, так как требуется тщательная настройка объединенной модели.
2. Ансамблевые гибридные рекомендаторы
Ансамблевые гибридные рекомендаторы работают путем комбинирования результатов нескольких независимых рекомендательных моделей. Прогнозы алгоритмов агрегируются для формирования итогового списка рекомендаций.
Принцип работы:
Независимые рекомендаторы выдают свои прогнозы.
Эти прогнозы объединяются с помощью различных методов агрегации, таких как взвешивание или переключение.
Типы ансамблей:
Взвешенные ансамбли:
Каждому рекомендатору присваивается вес, отражающий его вклад в итоговую рекомендацию.
Переключаемые ансамбли:
Выбор рекомендатора зависит от условий. Например пользователи с более чем 20 оценками получают рекомендации от одного алгоритма, а с менее чем 20 — от другого.
Преимущества:
Простота реализации, так как можно использовать уже существующие модели.
Гибкость в настройке весов или условий переключения.
Недостатки:
Требуется точная настройка механизма агрегации для достижения оптимальных результатов.
3. Смешанный гибридный рекомендатор
Смешанный гибридный рекомендатор, который складывает выходы нескольких рекомендаторов, начиная с самого персонализированного, затем от менее персонализированного и т. д.
4. Продвинутые техники в архитектуре
Для повышения точности гибридных систем применяются более сложные методы:
Линейная регрессия:
Используется для определения весов каждого рекомендатора на основе обучающих данных.
Признако-взвешенное линейное сочетание (FWLS):
Веса становятся функциями, зависящими от характеристик пользователей или элементов.
Мета-признаки:
Мета-признаки, такие как количество оценок фильма или стандартное отклонение оценок пользователя, помогают более точно взвешивать прогнозы.""",
    72: """Суть проблемы: «Холодный старт» возникает, когда в системе появляется новый пользователь, новый объект (товар, фильм, и т.п.) или новая система без истории взаимодействий. В этих случаях нет достаточных данных для построения качественных рекомендаций.
Типы холодного старта:
Новый пользователь: Нет информации о предпочтениях пользователя, поэтому сложно сразу рекомендовать релевантные объекты.
Новый объект: Объект не имеет оценок, поэтому нельзя рекомендовать его на основе классической коллаборативной фильтрации.
Новая система: Нет исторических данных для обучения модели.
Способы решения:
Использование контентных данных (content-based): рекомендации на основе характеристик объектов и профиля пользователя.
Гибридные подходы: комбинирование коллаборативной фильтрации и контентных методов.
Сбор дополнительных данных: опросы, анкеты для новых пользователей.
Использование демографической информации или внешних источников.
Активное обучение: стимулирование пользователей к оценкам новых объектов.""",
    73: """Сходство — это мера того, насколько два объекта (например, пользователи, товары и т. д.) похожи друг на друга в определённом аспекте.
Функция подобия — формализует это понятие, вычисляя степень сходства между объектами, где 1 идентичные элементы, 0 не имеющие ничего общего.""",
    74: """L-нормы являются способом оценки сходства пользователей и объектов
-норма:
абсолютная сумма различий (SAD)
средняя абсолютная ошибка (MAE)
-норма (Евклидова норма):
расстояние(object1, object2) =
средняя абсолютная ошибка (RMSE)""",
    75: """Коэффициент Отиаи:
Применяется к бинарным данным (например, лайки или покупки).
Формула:
Значения: от 0 (нет сходства) до 1 (полное совпадение).
Плюс: работает с разреженными данными, не чувствителен к разному количеству оценок.
Используется: в интернет-магазинах, где важны действия (купил/не купил).
Расстояние Жаккара
Чтобы найти сходство между двумя элементами, нужно подсчитать, сколько пользователей купили оба элемента, а затем разделить на количество пользователей, которые купили один из них (или оба).
J(i, j) = (Пользователи, купившие оба товара) / (Пользователи, купившие либо i, либо j)""",
    76: """Стохастический градиентный спуск
Для каждой оценки r(u,i):
рассчитывается прогноз оценки e = r_ui – q_i * p_u
обновляется значение x так, что x = x - α · e, где α - скорость обучения.
Контекст применения: матричная факторизация
Одна из ключевых моделей рекомендательных систем — SVD (Singular Value Decomposition) и ее вариации. Предполагается, что матрица пользователь-объект (например, рейтингов) может быть аппроксимирована как произведение двух низкоразмерных матриц:
где ^𝑅_ui - предсказанный рейтинг пользователя u для объекта i​, μ — глобальное среднее, b_u, b_i - смещения пользователя и объекта, p_u, q_i ∈ R^k - латентные векторы пользователя и объекта размерности k
Функция потерь (ошибки):
где K - множество известных рейтингов, λ - коэффициент регуляризации
Градиентный спуск:
Цель: минимизировать функцию потерь L по параметрам модели.
Обновления производятся по следующим формулам:
где e_ui = r_ui - ^R_ui - ошибка предсказания, γ — шаг градиентного спуска (learning rate)""",
    77: """User-Based Collaborative Filtering (UBCF)
Идея: Рекомендации формируются на основе мнений похожих пользователей.
Алгоритм:
Найти пользователей, похожих на целевого (по оценкам, покупкам и т. д.).
Использовать их оценки для предсказания релевантности товаров.
Item-Based Collaborative Filtering (IBCF)
Идея: Рекомендации формируются на основе схожести товаров (а не пользователей).
Алгоритм:
Найти товары, похожие на те, что оценил/просматривал пользователь.
Рекомендовать наиболее похожие товары с высокими оценками.""",
    78: """Surprise - это scikit (или научный набор) для создания рекомендательных систем на Python. Его можно рассматривать как аналог scikit-learn для создания рекомендательных систем. Surprise - Simple Python Recommendation System Engine. За небольшой промежуток времени surprise стала одной из самых популярных библиотек рекомендательных систем. Это объясняется тем, что она чрезвычайно надежна и проста в использовании. Она предоставляет готовые к использованию реализации большинства популярных алгоритмов коллаборативной фильтрации, а также позволяет интегрировать в фреймворк свой собственный алгоритм.""",
    79: """LightFM — это библиотека Python, предназначенная для построения рекомендательных систем, которая использует методы коллаборативной фильтрации и контентной фильтрации. LightFM требует данные в виде матриц взаимодействия между пользователями и элементами. Эти данные могут быть представлены в виде разреженной матрицы, где строки представляют пользователей, а столбцы — элементы. LightFM поддерживает несколько алгоритмов для построения рекомендаций. Вы можете выбрать один из них, например, warp (Weighted Approximate-Rank Pairwise) или logistic.""",
    80: """SVD (сингулярное разложение) применяется в рекомендательных системах для выявления скрытых закономерностей в данных пользователь–объект.
SVD разлагает матрицу оценок R на три матрицы:
Оставляя только топ-k компонент, получаем приближение, отражающее скрытые предпочтения.
Предсказание рейтингов:
Рекомендации — выбираем объекты с наивысшими предсказанными оценками для пользователя.
Уменьшает размерность.
Выявляет скрытые факторы предпочтений.
Устойчив к шуму и пропущенным значениям.
Используется, например, в системах Netflix, Amazon.""",
    81: """Генерация рекомендаций с помощью FunkSVD
1. Матрица факторов элементов - где каждый столбец соответствует элементу контента, описанному скрытыми факторами, рассчитанные ранее.
2. Матрица факторов пользователей - где каждый столбец соответствует пользователю, описанному скрытыми факторами.
3. Отклонение элемента - где определенные пункты считаются в целом лучше или хуже, чем другие. Отклонение - это разница между глобальным средним и средним элемента.
4. Отклонение пользователя - включает различные оценочные шкалы для разных пользователей.
Учет смещений (отклонений)
Предсказанная оценка:
( \mu ): глобальное среднее всех оценок.
( b_u ): смещение пользователя, отражающее его склонность завышать или занижать оценки.
( b_i ): смещение элемента, показывающее, насколько элемент в среднем оценивается выше или ниже.
( Q ): матрица факторов элементов, где каждая строка ( q_i ) соответствует элементу ( i ).
( P ): матрица факторов пользователей, где каждый столбец ( p_u ) соответствует пользователю ( u ).
Теперь нужно определить список элементов, которые пользователь оценит высоко. Есть два способа сделать это – перебором («в лоб») и через
окрестности.
«В лоб» - рассчитываем прогнозируемую оценку для каждого пользователя для каждого элемента, затем сортируем эти оценки и выводим верхние N элементов.
Расчет рекомендаций в окрестности. Вместо использования данных реальных оценок мы будем использовать рассчитанные факторы. Это означает, нужно вычислить сходство более близких элементов и с меньшим числом измерений, что делает задачу проще.""",
    82: """1. Нахождение похожих пользователей (соседей): Для целевого пользователя определяют несколько других пользователей с похожими вкусами (по схожести их рейтингов).
2. Расчёт прогноза: Прогноз рейтинга для пользователя u и объекта i обычно строится так:
3. Объяснение: Среднее значение скорректировано с учетом склонности к более высоким/низким оценкам у разных пользователей, а "вклад" каждого соседа зависит от степени его похожести на целевого пользователя.
Результат: Получаем предсказанную оценку объекта, и на основе таких прогнозов формируем рекомендации пользователю.""",
    83: """В алгоритме ALS, при вычислении U и V на
основе чередующихся наименьших квадратов,
матрица V инициализируется случайными числами.
Алгоритм является итеративным, и на каждой
итерации рассчитываются матрицы U и V.
Оптимизация функции потерь в алгоритме ALS
В цикле до сходимости:
Фиксируем матрицу U (скрытые представления
пользователей);
Решаем задачу L2-регуляризованной регрессии
для каждого товара и находим оптимальную
матрицу V;
Фиксируем матрицу V (скрытые представления
объектов);
Решаем задачу L2-регуляризованной регрессии
для каждого пользователя и находим
оптимальную матрицу U""",
    84: """Неявным фидбэком является в том числе и факт взаимодействия, поэтому мы можем заполнить всю матрицу user-item целиком: на тех позициях, где пользователь положительно взаимодействовал с объектом, поставим 1, а на тех, где взаимодействие было негативным или его вообще не произошло, поставим 0. Эта компонента фильтра называется предпочтением (preference):
Введём ещё степень уверенности (confidence), отражающую уверенность в оценке пользователя:
(степень уверенности в ), где  — некоторая константа.
На местах пропусков мы явно проставляем .
Функция потерь:
Она позволяет учитывать неявный фильтр, которого обычно на порядок больше, чем явного; регулировать степень уверенности в действиях пользователей.""",
    85: """Библиотека Implicit была разработана специально
для обработки неявных данных в рекомендательных
системах. Она предлагает эффективные реализации
алгоритмов матричной факторизации (Matrix
Factorization), оптимизированных для больших
объемов данных.
Библиотека хорошо подходит для работы с
большими разреженными матрицами, такими как
данные кликов, просмотров, добавлений в корзину и
других действий, где нет явных оценок
пользователей.
Ключевые особенности библиотеки Implicit
1. Модели на основе методов матричной
факторизации
• Alternating Least Squares (ALS) —
чередующийся метод наименьших
квадратов, оптимизирован для обработки
больших, разреженных матриц.
• Bayesian Personalised Ranking (BPR) — подход
фокусируется на ранжировании
рекомендаций, что схоже с WARP из LightFM.
• Logistic Matrix Factorization — логистическая
матричная факторизация, для задач
логистической регрессии.
2. Оптимизация для неявных данных
• Вместо оценки, где пользователь ставит
оценку 1-5, используются "положительные
действия" (например, покупки, клики, лайки).
• Неявные действия интерпретируются как
"степень интереса".
3. Поддержка GPU
• Можно использовать вычисления на
графических процессорах для ускорения.
4. Эффективность
• Библиотека оптимизирована для работы с
разреженными матрицами, используя numpy
и scipy. Поддерживает многопоточность для
ускорения вычислений.
5. Простота интеграции
• Легко адаптируется для работы с любыми
матрицами взаимодействий.
6. Использование в гибридных системах
• Хотя библиотека не поддерживает контентные
признаки "из коробки", можно комбинировать
с контентными данными вручную. Например,
можно вычислить рекомендации через implicit,
а затем скоррелировать их с другими
признаками (текстовые, категориальные
данные и т. д.).""",
    86: """Обычно различают явный (explicit) и неявный (implicit) виды фидбека. Фидбек называется явным, если он отражает степень интереса пользователя к объекту. Неявные данные представляют собой косвенные признаки, свидетельствующие о предпочтениях пользователя, однако не подразумевающие прямого выражения мнения (оценок, отзывов).
Ключевое отличие неявных данных от явных
Явные данные предполагают прямую обратную связь от пользователя: рейтинги фильмов, лайки, комментарии.
Неявные данные формируются путём наблюдения действий пользователя без необходимости его активной реакции.
Типичные виды неявных данных
1. Просмотры: посещение страницы продукта или контента свидетельствует о потенциальном интересе пользователя.
2. Клики: переходы по ссылкам также указывают на повышенный интерес.
3. Время нахождения на странице: длительное пребывание на странице показывает вовлечённость пользователя.
4. Покупки: факт приобретения товара подтверждает выбор пользователя.
5. Добавление в избранное/корзину: временное сохранение товара отражает намерение приобрести или изучить позже.
6. Оценка длительности прослушивания музыки или просмотра фильма: долгий сеанс воспроизведения означает положительный отклик пользователя.
7. Переход по рекламному объявлению: клик на рекламу говорит о её релевантности интересам пользователя.
8. Чат-активность: количество сообщений и частота общения могут показывать предпочтение к какому-либо товару или контенту.""" 
}

def info():
    '''
    Добавляет в буфер обмена список тем, по которым потом обращаться при помощи функции get(n), где n - номер темы
    '''
    pyperclip.copy(themes)

def info_cl():
    '''
    Создает класс, в документации которого список тем, по которым потом обращаться при помощи функции get(n), где n - номер темы
    '''
    class sol():
        __doc__ = themes
        
    return sol()

def get(n):
    '''
    Добавляет в буфер обмена ответ по теме (n - номер темы; m = 0 => теория, m = 1 => практика)
    '''
    if 0 < n < len(questions) + 1:
        pyperclip.copy(questions[n])
    else:
        pyperclip.copy('Неправильный выбор номера темы')


def get_cl(n):
    '''
    Создает объект класса, в документации (shift + tab) которого лежит ответ по теме (n - номер темы; m = 0 => теория, m = 1 => практика)
    '''
    class sol:
        def __init__(self, n):
            self.n = n
            self.doc = questions[self.n]

        @property
        def __doc__(self):
            return self.doc  

    return sol(n)

def api_call(prompt, system_pr=True, r1=False, code=True):
    client = OpenAI(api_key="sk-b1cd11f28cf9473296a9a9a4074de9ee", base_url="https://api.deepseek.com")
    model = 'deepseek-reasoner' if r1 else 'deepseek-chat'
    if system_pr:
        if code:
            system_prompt = system_prompt_code
            temperature = 0
        else:
            system_prompt = system_prompt_theory
            temperature = 1
    else:
        system_prompt = ''
        temperature = 1
    response = client.chat.completions.create(
        model = model,
        messages= [
            {'role' : 'system', 'content' : system_prompt},
            {"role": "user", "content": prompt}
            ],
        stream=False,
        temperature=temperature)
    return response.choices[0].message.content

def d_get(prompt, system_pr=True, r1=False, code=True):
    '''
    Добавляет в буфер обмена респонс модели по промпту
    system_pr : True => использовать мои систем промпты (я адаптировал их для экза), False : не использовать
    r1 : True => использовать reasoning, False => использовать обычный дипсик
    code : True => систем промпт для кода, False => систем промпт для теории
    '''
    pyperclip.copy(api_call(prompt, system_pr, r1, code))

class d_get_cl:
    '''
    Добавляет в документацию класса респонс модели по промпту
    system_pr : True => использовать мои систем промпты (я адаптировал их для экза), False : не использовать
    r1 : True => использовать reasoning, False => использовать обычный дипсик
    code : True => систем промпт для кода, False => систем промпт для теории
    '''
    def __init__(self, prompt, system_pr=True, r1=False, code=True):
        self.doc = api_call(prompt, system_pr, r1, code)

    @property
    def __doc__(self):
        return self.doc  
