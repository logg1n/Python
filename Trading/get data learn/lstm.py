import os
import glob
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset, random_split
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from triangle import Triangle
from indicator_manager import IndicatorManager


# Определение функции логирования
def log_step(message):
   print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")


# Определение модели LSTM
class LSTMModel(nn.Module):
   def __init__(self, input_size, hidden_size, output_size):
      super().__init__()
      self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
      self.fc = nn.Linear(hidden_size, output_size)
      self.sigmoid = nn.Sigmoid()
      log_step(f"Инициализирована LSTM: input_size={input_size}, hidden_size={hidden_size}, output_size={output_size}")

   def forward(self, x):
      out, _ = self.lstm(x)
      out = self.fc(out[:, -1, :])
      return self.sigmoid(out)


# Класс для управления обучением и дообучением
class ModelTrainer:
   def __init__(self, model_path="lstm_model.pth"):
      self.model_path = model_path
      self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
      self.best_loss = float('inf')
      self.features = ["body", "upper_shadow", "SMA_20", "RSI_14"]
      self.sequence_length = 60

   def initialize_model(self, input_size=4, hidden_size=64, output_size=1):
      """Инициализация или загрузка существующей модели"""
      model = LSTMModel(input_size, hidden_size, output_size).to(self.device)

      if os.path.exists(self.model_path):
         model.load_state_dict(torch.load(self.model_path, map_location=self.device))
         log_step(f"Загружена существующая модель из {self.model_path}")
      else:
         log_step("Инициализирована новая модель")

      return model

   def load_and_preprocess_data(self, file_path):
      """Загрузка и предварительная обработка данных из файла"""
      try:
         data = pd.read_csv(file_path)
         log_step(f"Данные успешно загружены. Размер: {data.shape[0]} строк, {data.shape[1]} столбцов")

         # Разметка паттернов
         data = self.detect_pattern(data)

         # Создание признаков
         data = self.create_features(data)

         return data
      except Exception as e:
         log_step(f"Ошибка загрузки данных: {str(e)}")
         raise

   def detect_pattern(self, raw_data: pd.DataFrame) -> pd.DataFrame:
      """Разметка паттернов в данных"""
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

         if idx % 1000 == 0 and idx > 0:
            log_step(f"Обработано {idx} свечей, найдено {sum(patterns)} паттернов")

      raw_data["pattern_label"] = patterns
      log_step(f"Разметка завершена. Всего найдено {sum(patterns)} паттернов")
      return raw_data

   def create_features(self, data: pd.DataFrame) -> pd.DataFrame:
      """Создание признаков для модели"""
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

   def prepare_sequences(self, data: pd.DataFrame):
      """Подготовка последовательностей для LSTM"""
      X, y = [], []
      log_step(f"Создание окон размером {self.sequence_length} свечей...")

      for i in range(len(data) - self.sequence_length):
         X.append(data.iloc[i:i + self.sequence_length][self.features].values)
         y.append(data.iloc[i + self.sequence_length]["pattern_label"])

         if i % 1000 == 0 and i > 0:
            log_step(f"Создано {i} окон, найдено {sum(y)} целевых паттернов")

      X = np.array(X)
      y = np.array(y)
      log_step(f"Создано {len(X)} последовательностей. Форма X: {X.shape}")
      return X, y

   def create_dataloaders(self, X, y, val_split=0.2):
      """Создание DataLoader для обучения и валидации"""
      # Разделение данных
      split_idx = int(len(X) * (1 - val_split))
      X_train, X_val = X[:split_idx], X[split_idx:]
      y_train, y_val = y[:split_idx], y[split_idx:]

      log_step(
         f"Разделение данных: train={len(X_train)} ({len(X_train) / len(X) * 100:.1f}%), val={len(X_val)} ({len(X_val) / len(X) * 100:.1f}%)")

      # Конвертация в тензоры
      X_train_tensor = torch.FloatTensor(X_train).to(self.device)
      y_train_tensor = torch.FloatTensor(y_train).to(self.device)
      X_val_tensor = torch.FloatTensor(X_val).to(self.device)
      y_val_tensor = torch.FloatTensor(y_val).to(self.device)

      log_step(f"Форма тензоров: X_train={X_train_tensor.shape}, y_train={y_train_tensor.shape}")

      # Создание DataLoader
      train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
      val_dataset = TensorDataset(X_val_tensor, y_val_tensor)

      train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
      val_loader = DataLoader(val_dataset, batch_size=32)

      return train_loader, val_loader

   def train_model(self, model, train_loader, val_loader, epochs=50, initial_lr=0.001):
      """Процедура обучения модели"""
      criterion = nn.BCELoss()
      optimizer = optim.Adam(model.parameters(), lr=initial_lr)
      scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=5)

      log_step(f"\nНачало обучения на {len(train_loader.dataset)} примерах")

      for epoch in range(epochs):
         model.train()
         train_loss, correct, total = 0, 0, 0

         for batch_x, batch_y in train_loader:
            optimizer.zero_grad()
            outputs = model(batch_x).squeeze()
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()

            train_loss += loss.item()
            predicted = (outputs > 0.5).float()
            correct += (predicted == batch_y).sum().item()
            total += batch_y.size(0)

         # Валидация
         val_loss, val_acc = self.validate_model(model, val_loader, criterion)
         scheduler.step(val_loss)

         # Логирование
         log_step(
            f"Эпоха {epoch + 1}/{epochs}: "
            f"Train Loss: {train_loss / len(train_loader):.4f}, Acc: {correct / total:.2%} | "
            f"Val Loss: {val_loss:.4f}, Acc: {val_acc:.2%} | "
            f"LR: {optimizer.param_groups[0]['lr']:.2e}"
         )

         # Сохранение лучшей модели
         if val_loss < self.best_loss:
            self.best_loss = val_loss
            torch.save(model.state_dict(), self.model_path)
            log_step(f"Новая лучшая модель сохранена в {self.model_path}")

      return model

   def validate_model(self, model, val_loader, criterion):
      """Валидация модели"""
      model.eval()
      val_loss, correct, total = 0, 0, 0

      with torch.no_grad():
         for batch_x, batch_y in val_loader:
            outputs = model(batch_x).squeeze()
            val_loss += criterion(outputs, batch_y).item()
            predicted = (outputs > 0.5).float()
            correct += (predicted == batch_y).sum().item()
            total += batch_y.size(0)

      return val_loss / len(val_loader), correct / total

   def find_data_files(self, pattern="data/*_15.csv"):
      """Поиск файлов с данными"""
      data_files = glob.glob(pattern)
      if not data_files:
         raise FileNotFoundError(f"Не найдено файлов по шаблону: {pattern}")

      log_step(f"Найдено {len(data_files)} файлов для обработки:")
      for file in data_files:
         log_step(f" - {file}")

      return data_files

   def train_on_all_data(self, initial_epochs=50, incremental_epochs=10):
      """Полный цикл обучения на всех данных"""
      try:
         data_files = self.find_data_files()
      except FileNotFoundError as e:
         log_step(str(e))
         return None

      # Если модель не существует, создаем новую
      if not os.path.exists(self.model_path):
         log_step("Инициализация нового обучения...")
         initial_data = self.load_and_preprocess_data(data_files[0])
         X, y = self.prepare_sequences(initial_data)
         train_loader, val_loader = self.create_dataloaders(X, y)

         model = self.initialize_model()
         model = self.train_model(model, train_loader, val_loader, epochs=initial_epochs)
         remaining_files = data_files[1:]
      else:
         log_step("Обнаружена существующая модель, начинаем дообучение")
         remaining_files = data_files

      # Постепенное дообучение на остальных файлах
      for file in remaining_files:
         try:
            log_step(f"\nДообучение на файле: {file}")
            new_data = self.load_and_preprocess_data(file)
            X_new, y_new = self.prepare_sequences(new_data)
            train_loader, val_loader = self.create_dataloaders(X_new, y_new)

            model = self.initialize_model()
            model = self.train_model(
               model,
               train_loader,
               val_loader,
               epochs=incremental_epochs,
               initial_lr=0.0001  # Меньше LR для дообучения
            )
         except Exception as e:
            log_step(f"Ошибка при обработке {file}: {str(e)}")
            continue

      return model


# Основной блок выполнения
if __name__ == "__main__":
   try:
      trainer = ModelTrainer()

      # Полный цикл обучения
      trainer.train_on_all_data(
         initial_epochs=50,
         incremental_epochs=10
      )

      log_step("Обучение завершено успешно!")
   except Exception as e:
      log_step(f"Критическая ошибка: {str(e)}")