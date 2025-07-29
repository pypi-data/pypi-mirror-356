import logging
from typing import Dict, Any
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from machine_learn.model_base import ModelBase
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV


class TSA(ModelBase):
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        super().__init__(config, logger)
        self.logger.info("TSA模型初始化完成")

    def start(self):
        self.logger.info("TSA模型开始运行")
        import pandas as pd

        # 加载数据
        df = pd.read_csv("data/AAPL_2024.csv", parse_dates=["Date"])
        # df = yf.download("AAPL", start="2024-01-01", end="2024-12-01")

        # 创建时间特征
        df["day_num"] = np.arange(len(df))  # 线性时间趋势
        df["month"] = df["Date"].dt.month
        df["quarter"] = df["Date"].dt.quarter

        # 创建目标变量 - 未来30天收益率
        df["future_30d_return"] = df["Close"].pct_change(30).shift(-30)

        # 删除缺失值
        df = df.dropna()

        # 特征选择
        features = ["day_num", "Volume", "month", "quarter"]
        X = df[features]
        y = df["future_30d_return"]

        # 标准化
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # 划分训练测试集(按时间顺序)
        split_idx = int(0.8 * len(df))
        X_train, X_test = X_scaled[:split_idx], X_scaled[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]

        # 1.线性回归模型
        self.logger.info("训练LinearRegression模型")
        lr = LinearRegression()
        lr.fit(X_train, y_train)

        # 预测
        y_pred_lr = lr.predict(X_test)

        # 评估
        self.logger.info(f"LR MSE: {mean_squared_error(y_test, y_pred_lr):.6f}")
        self.logger.info(f"LR R²: {r2_score(y_test, y_pred_lr):.4f}")

        # 系数分析
        self.logger.info(
            pd.DataFrame({"feature": features, "coefficient": lr.coef_}).sort_values(
                "coefficient", key=abs, ascending=False
            )
        )

        # 2.岭回归模型
        self.logger.info("训练RidgeRegression模型")

        # 超参数调优
        ridge = Ridge()
        params = {"alpha": [0.001, 0.01, 0.1, 1, 10, 100]}
        grid = GridSearchCV(ridge, params, cv=5, scoring="neg_mean_squared_error")
        grid.fit(X_train, y_train)

        # 最佳模型
        best_ridge = grid.best_estimator_
        y_pred_ridge = best_ridge.predict(X_test)

        # 评估
        print(
            f"Ridge(alpha={best_ridge.alpha}) MSE: {mean_squared_error(y_test, y_pred_ridge):.6f}"
        )
        print(f"Ridge R²: {r2_score(y_test, y_pred_ridge):.4f}")

        # 系数分析
        self.logger.info(
            pd.DataFrame(
                {"feature": features, "coefficient": best_ridge.coef_}
            ).sort_values("coefficient", key=abs, ascending=False)
        )

        self.logger.info("TSA模型运行结束")
