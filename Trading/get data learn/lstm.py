import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

from triangle import Triangle  # Убедитесь, что класс Triangle реализован


# Определение модели LSTM
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return self.sigmoid(out)


# 1. Загрузка данных
data = pd.read_csv("candle_data.csv")  # Ваш файл с данными

# 2. Разметка паттернов
def detect_pattern(raw_data: pd.DataFrame) -> pd.DataFrame:
    detector = Triangle(raw_data)
    patterns = []
    for idx, row in raw_data.iterrows():
        is_pattern = detector.find_pattern(
            open=row["open"],
            high=row["high"],
            low=row["low"],
            close=row["close"],
            volume=row["volume"]
        )
        patterns.append(1 if is_pattern else 0)
        detector.reset_state()
    raw_data["pattern_label"] = patterns
    return raw_data

labeled_data = detect_pattern(data)

# 3. Создание признаков
def create_features(data: pd.DataFrame) -> pd.DataFrame:
    data["body"] = data["close"] - data["open"]
    data["upper_shadow"] = data["high"] - data[["open", "close"]].max(axis=1)
    data["SMA_20"] = data["close"].rolling(20).mean()
    data["RSI_14"] = 100 - (100 / (1 + (data["close"].diff().clip(lower=0).rolling(14).mean() /
                                   data["close"].diff().clip(upper=0).abs().rolling(14).mean())))
    return data.dropna()

featured_data = create_features(labeled_data)

# 4. Подготовка последовательностей для LSTM
sequence_length = 60  # 60 свечей как контекст
features = ["body", "upper_shadow", "SMA_20", "RSI_14"]
X, y = [], []

for i in range(len(featured_data) - sequence_length):
    X.append(featured_data.iloc[i:i+sequence_length][features].values)
    y.append(featured_data.iloc[i+sequence_length]["pattern_label"])

X = np.array(X)  # Форма: (num_samples, sequence_length, num_features)
y = np.array(y)

# 5. Разделение данных
split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# 6. Конвертация в тензоры PyTorch
X_train_tensor = torch.FloatTensor(X_train)  # Форма: (batch, seq_len, features)
y_train_tensor = torch.FloatTensor(y_train)  # Форма: (batch,)
# Параметры
input_size = 4  # Количество фичей: body, upper_shadow, SMA_20, RSI_14
hidden_size = 64
output_size = 1

# Инициализация модели
model = LSTMModel(input_size, hidden_size, output_size)
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# Обучение
for epoch in range(50):
    for batch_x, batch_y in train_loader:
        optimizer.zero_grad()
        outputs = model(batch_x)
        loss = criterion(outputs.squeeze(), batch_y)
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")