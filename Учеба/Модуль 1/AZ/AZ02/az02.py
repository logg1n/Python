import pandas as pd
import numpy as np


data = {
    'Ученик': [f'Ученик_{i}' for i in range(1, 11)],
    'Математика': np.random.randint(2, 6, size=10),
    'Физика': np.random.randint(2, 6, size=10),
    'Химия': np.random.randint(2, 6, size=10),
    'Литература': np.random.randint(2, 6, size=10),
    'История': np.random.randint(2, 6, size=10)
}

df = pd.DataFrame(data).set_index('Ученик')

print(df.head())
print("\n" + "="*50 + "\n")

print("Средние оценки по предметам:")
print(df.mean().to_string(float_format="%.2f"))
print("\n" + "="*50 + "\n")

print("Медианные оценки по предметам:")
print(df.median().to_string())
print("\n" + "="*50 + "\n")

Q1_math = df['Математика'].quantile(0.25)
Q3_math = df['Математика'].quantile(0.75)
IQR_math = Q3_math - Q1_math

print(f"Q1 (25-й перцентиль) по математике: {Q1_math}")
print(f"Q3 (75-й перцентиль) по математике: {Q3_math}")
print(f"IQR по математике: {IQR_math}")
print("\n" + "="*50 + "\n")

print("Стандартное отклонение по предметам:")
print(df.std().to_string(float_format="%.2f"))