import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from torch.optim.lr_scheduler import ReduceLROnPlateau
from sklearn.metrics import classification_report, f1_score
from indicator_manager import IndicatorManager
from triangle import Triangle
from collections import deque
from enum import Enum
import operator
import logging

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 1. Улучшенная модель LSTM
class EnhancedLSTMModel(nn.Module):
   def __init__(self, input_size, hidden_size, output_size):
      super().__init__()
      self.lstm1 = nn.LSTM(input_size, hidden_size,
                           batch_first=True,
                           dropout=0.3)
      self.lstm2 = nn.LSTM(hidden_size, hidden_size // 2,
                           batch_first=True)
      self.attention = nn.Sequential(
         nn.Linear(hidden_size // 2, 1),
         nn.Softmax(dim=1))
      self.fc = nn.Linear(hidden_size // 2, output_size)
      self.sigmoid = nn.Sigmoid()

   def forward(self, x):
      out, _ = self.lstm1(x)
      out, _ = self.lstm2(out)

      # Механизм внимания
      attn_weights = self.attention(out)
      context = torch.sum(attn_weights * out, dim=1)

      out = self.fc(context)
      return self.sigmoid(out)


# 2. Улучшенный детектор паттернов
class EnhancedTriangle(Triangle):
   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.pattern_window = deque(maxlen=self.min_kline * 3)

   def find_pattern(self, open: float, high: float, low: float, close: float, volume: float) -> bool:
      current_candle = {
         'open': open,
         'high': high,
         'low': low,
         'close': close,
         'volume': volume
      }
      self.pattern_window.append(current_candle)

      # Автосброс при неактуальности паттерна
      if len(self.pattern_window) == self.pattern_window.maxlen:
         self.reset_state()

      # Основная логика детекции
      self._update_extremes(high, low)

      if self._should_reset():
         return False

      return self._check_main_conditions(current_candle)


# 3. Функция создания расширенных признаков
def create_enhanced_features(data: pd.DataFrame) -> pd.DataFrame:
   # Базовые признаки
   data["body"] = data["close"] - data["open"]
   data["upper_shadow"] = data["high"] - data[["open", "close"]].max(axis=1)
   data["lower_shadow"] = data[["open", "close"]].min(axis=1) - data["low"]
   data["body_pct"] = data["body"] / data["open"] * 100

   # Индикаторы тренда
   data["SMA_20"] = IndicatorManager.SMA_series(data['close'].tolist(), 20)
   data["EMA_20"] = IndicatorManager.EMA_series(data['close'].tolist(), 20)
   data["SMA_50"] = IndicatorManager.SMA_series(data['close'].tolist(), 50)
   data["MACD"] = IndicatorManager.MACD(data['close'].tolist(), 12, 26, 9)

   # Моментум
   data["RSI_14"] = IndicatorManager.RSI_series(data['close'].tolist(), 14)
   data["Stoch_14"] = IndicatorManager.Stochastic(
      data['high'].tolist(),
      data['low'].tolist(),
      data['close'].tolist(),
      14)

   # Объем
   data["volume_ma"] = data["volume"].rolling(5).mean()
   data["volume_pct"] = data["volume"] / data["volume_ma"] * 100

   return data.dropna()


# 4. Улучшенный пайплайн обучения
def train_model():
   # Загрузка данных
   data = pd.read_csv("candle_data.csv")

   # Разметка паттернов
   detector = EnhancedTriangle(data)
   labeled_data = detect_pattern(data, detector)

   # Создание признаков
   featured_data = create_enhanced_features(labeled_data)

   # Подготовка последовательностей
   sequence_length = 60
   features = ["body", "upper_shadow", "lower_shadow", "SMA_20",
               "RSI_14", "MACD", "volume_pct"]
   X, y = prepare_sequences(featured_data, sequence_length, features)

   # Разделение данных
   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

   # Конвертация в тензоры
   X_train_tensor = torch.FloatTensor(X_train)
   y_train_tensor = torch.FloatTensor(y_train)
   X_test_tensor = torch.FloatTensor(X_test)
   y_test_tensor = torch.FloatTensor(y_test)

   # Инициализация модели
   model = EnhancedLSTMModel(
      input_size=len(features),
      hidden_size=64,
      output_size=1
   )

   # Функция потерь с учетом дисбаланса классов
   pos_weight = torch.tensor([len(y_train) / sum(y_train)])
   criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)

   # Оптимизатор и планировщик
   optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=1e-4)
   scheduler = ReduceLROnPlateau(optimizer, 'min', patience=5)

   # Обучение
   train_loader = DataLoader(
      TensorDataset(X_train_tensor, y_train_tensor),
      batch_size=64,
      shuffle=True
   )

   best_f1 = 0
   for epoch in range(100):
      model.train()
      for batch_x, batch_y in train_loader:
         optimizer.zero_grad()
         outputs = model(batch_x).squeeze()
         loss = criterion(outputs, batch_y)
         loss.backward()
         optimizer.step()

      # Валидация
      model.eval()
      with torch.no_grad():
         val_outputs = model(X_test_tensor).squeeze()
         val_loss = criterion(val_outputs, y_test_tensor)
         val_preds = (val_outputs > 0.5).float()
         val_f1 = f1_score(y_test_tensor.numpy(), val_preds.numpy())

      scheduler.step(val_loss)

      if val_f1 > best_f1:
         best_f1 = val_f1
         torch.save(model.state_dict(), "best_model.pth")

      logger.info(f"Epoch {epoch + 1}, Loss: {loss.item():.4f}, Val F1: {val_f1:.4f}")

   # Загрузка лучшей модели
   model.load_state_dict(torch.load("best_model.pth"))

   # Финальная оценка
   evaluate_model(model, X_test_tensor, y_test_tensor, features)


# 5. Дополнительные утилиты
def prepare_sequences(data, seq_len, features):
   X, y = [], []
   for i in range(len(data) - seq_len):
      X.append(data.iloc[i:i + seq_len][features].values)
      y.append(data.iloc[i + seq_len]["pattern_label"])
   return np.array(X), np.array(y)


def evaluate_model(model, X_test, y_test, feature_names):
   model.eval()
   with torch.no_grad():
      outputs = model(X_test).squeeze()
      preds = (outputs > 0.5).float()

      print("\nClassification Report:")
      print(classification_report(y_test.numpy(), preds.numpy()))

      # SHAP анализ (только для CPU)
      if torch.cuda.is_available():
         logger.warning("SHAP не поддерживает GPU. Переключитесь на CPU для анализа.")
      else:
         import shap
         background = X_test[:100]
         explainer = shap.DeepExplainer(model, background)
         shap_values = explainer.shap_values(X_test[:50])
         shap.summary_plot(shap_values, X_test[:50], feature_names=feature_names)


if __name__ == "__main__":
   train_model()