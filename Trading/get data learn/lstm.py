import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from indicator_manager import IndicatorManager
from triangle import Triangle
from datetime import datetime


# Определение модели LSTM
class LSTMModel(nn.Module):
   def __init__(self, input_size, hidden_size, output_size):
      super().__init__()
      self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
      self.fc = nn.Linear(hidden_size, output_size)
      self.sigmoid = nn.Sigmoid()
      print(
         f"[Модель] Инициализирована LSTM: input_size={input_size}, hidden_size={hidden_size}, output_size={output_size}")

   def forward(self, x):
      out, _ = self.lstm(x)
      out = self.fc(out[:, -1, :])
      return self.sigmoid(out)


def log_step(message):
   print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")


# 1. Загрузка данных
log_step("Начало загрузки данных...")
try:
   data = pd.read_csv("data/BTCUSDT_15.csv")
   log_step(f"Данные успешно загружены. Размер: {data.shape[0]} строк, {data.shape[1]} столбцов")
   print("Первые 5 строк данных:")
   print(data.head())
except Exception as e:
   log_step(f"Ошибка загрузки данных: {str(e)}")
   exit()

# 2. Разметка паттернов
log_step("Начало разметки паттернов...")


def detect_pattern(raw_data: pd.DataFrame) -> pd.DataFrame:
   detector = Triangle(raw_data)
   patterns = []
   log_step(f"Обработка {len(raw_data)} свечей для поиска паттернов...")

   for idx, row in raw_data.iterrows():
      detector.current_index = idx
      is_pattern = detector.find_pattern(
         open=row["open"],
         high=row["high"],
         low=row["low"],
         close=row["close"],
         volume=row["volume"]
      )
      patterns.append(1 if is_pattern else 0)

      # Вывод прогресса каждые 1000 свечей
      if idx % 1000 == 0 and idx > 0:
         log_step(f"Обработано {idx} свечей, найдено {sum(patterns)} паттернов")

   raw_data["pattern_label"] = patterns
   log_step(f"Разметка завершена. Всего найдено {sum(patterns)} паттернов")
   return raw_data


labeled_data = detect_pattern(data)
print("\nСтатистика паттернов:")
print(labeled_data["pattern_label"].value_counts())

# 3. Создание признаков
log_step("Создание признаков...")


def create_features(data: pd.DataFrame) -> pd.DataFrame:
   log_step("Вычисление базовых признаков свечей...")
   data["body"] = data["close"] - data["open"]
   data["upper_shadow"] = data["high"] - data[["open", "close"]].max(axis=1)

   log_step("Вычисление индикаторов...")
   data["SMA_20"] = IndicatorManager.SMA_series(data['close'].tolist(), 20)
   data["EMA_20"] = IndicatorManager.EMA_series(data['close'].tolist(), 20)
   data["SMA_50"] = IndicatorManager.SMA_series(data['close'].tolist(), 50)
   data["EMA_50"] = IndicatorManager.EMA_series(data['close'].tolist(), 50)
   data["RSI_14"] = IndicatorManager.RSI_series(data['close'].tolist(), 14)

   cleaned_data = data.dropna()
   log_step(f"Признаки созданы. Удалено {len(data) - len(cleaned_data)} строк с NaN")
   return cleaned_data


featured_data = create_features(labeled_data)
print("\nПример данных с признаками:")
print(featured_data[["open", "close", "body", "upper_shadow", "SMA_20", "RSI_14"]].head())

# 4. Подготовка последовательностей для LSTM
log_step("Подготовка последовательностей для LSTM...")
sequence_length = 60
features = ["body", "upper_shadow", "SMA_20", "RSI_14"]
X, y = [], []

log_step(f"Создание окон размером {sequence_length} свечей...")
for i in range(len(featured_data) - sequence_length):
   X.append(featured_data.iloc[i:i + sequence_length][features].values)
   y.append(featured_data.iloc[i + sequence_length]["pattern_label"])

   # Вывод прогресса
   if i % 1000 == 0 and i > 0:
      log_step(f"Создано {i} окон, найдено {sum(y)} целевых паттернов")

X = np.array(X)
y = np.array(y)
log_step(f"Создано {len(X)} последовательностей. Форма X: {X.shape}")

# 5. Разделение данных
split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]
log_step(
   f"Разделение данных: train={len(X_train)} ({len(X_train) / len(X) * 100:.1f}%), test={len(X_test)} ({len(X_test) / len(X) * 100:.1f}%)")

# 6. Конвертация в тензоры PyTorch
log_step("Конвертация в тензоры PyTorch...")
X_train_tensor = torch.FloatTensor(X_train)
y_train_tensor = torch.FloatTensor(y_train)
X_test_tensor = torch.FloatTensor(X_test)
y_test_tensor = torch.FloatTensor(y_test)
log_step(f"Форма тензоров: X_train={X_train_tensor.shape}, y_train={y_train_tensor.shape}")

# Параметры модели
input_size = len(features)
hidden_size = 64
output_size = 1
log_step(f"\nПараметры модели: input_size={input_size}, hidden_size={hidden_size}, output_size={output_size}")

# Инициализация модели
model = LSTMModel(input_size, hidden_size, output_size)
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
log_step(f"Используемый оптимизатор: {optimizer.__class__.__name__} с lr={optimizer.param_groups[0]['lr']}")

# Подготовка DataLoader
train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
log_step(f"DataLoader создан: batch_size={train_loader.batch_size}, всего батчей: {len(train_loader)}")

# 7. Обучение модели
log_step("\nНачало обучения модели...")
for epoch in range(50):
   epoch_loss = 0
   correct = 0
   total = 0

   for batch_x, batch_y in train_loader:
      optimizer.zero_grad()
      outputs = model(batch_x)
      loss = criterion(outputs.squeeze(), batch_y)
      loss.backward()
      optimizer.step()

      epoch_loss += loss.item()
      predicted = (outputs > 0.5).float()
      correct += (predicted.squeeze() == batch_y).sum().item()
      total += batch_y.size(0)

   # Вывод статистики после каждой эпохи
   train_acc = correct / total
   log_step(f"Эпоха {epoch + 1}/50: Loss={epoch_loss / len(train_loader):.4f}, Accuracy={train_acc:.2%}")

   # Валидация на тестовых данных каждые 5 эпох
   if (epoch + 1) % 5 == 0:
      with torch.no_grad():
         test_outputs = model(X_test_tensor)
         test_loss = criterion(test_outputs.squeeze(), y_test_tensor)
         test_predicted = (test_outputs > 0.5).float()
         test_correct = (test_predicted.squeeze() == y_test_tensor).sum().item()
         test_acc = test_correct / len(y_test_tensor)
         log_step(f"Тест после эпохи {epoch + 1}: Loss={test_loss.item():.4f}, Accuracy={test_acc:.2%}")

log_step("Обучение завершено!")

# 8. Сохранение модели
torch.save(model.state_dict(), "lstm_model.pth")
log_step("Модель сохранена в файл lstm_model.pth")