import torch
import torch.nn as nn


# Определение модели LSTM
class LSTMModel(nn.Module):
	def __init__(self, input_size, hidden_size=128, output_size=3):
		super().__init__()

		self.lstm = nn.LSTM(input_size, hidden_size,
							batch_first=True,
							num_layers=3,
							dropout=0.4)
		self.attention = nn.Sequential(
			nn.Linear(hidden_size, hidden_size),
			nn.Tanh(),
			nn.Linear(hidden_size, 1),
			nn.Softmax(dim=1)
		)
		self.bn = nn.BatchNorm1d(hidden_size * 2)
		self.fc = nn.Linear(hidden_size, output_size)
		self.dropout = nn.Dropout(0.4)

	def forward(self, x):
		x = x.float()  # Гарантируем правильный тип

		# LSTM слой
		lstm_out, _ = self.lstm(x)  # [batch_size, seq_len, hidden_size]

		# Механизм внимания
		attention_weights = self.attention(lstm_out)  # [batch_size, seq_len, 1]
		attention_weights = attention_weights.squeeze(-1)  # [batch_size, seq_len]

		# Взвешенная сумма
		context = torch.bmm(attention_weights.unsqueeze(1), lstm_out).squeeze(1)  # [batch_size, hidden_size]

		# Классификация
		out = self.dropout(context)
		return torch.softmax(self.fc(out), dim=1)
