import re
import json

# Читаем сырой текст чека
with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Извлечь все цены (например, форматы 123.45, 67,89, $12.34)
prices = re.findall(r'\d+[.,]?\d*', text)
prices = [float(p.replace(',', '.')) for p in prices]

# 2. Найти все названия продуктов (например, строки перед ценой)
product_pattern = re.compile(r'([A-Za-z\s]+)\s+\d+[.,]?\d*')
products = product_pattern.findall(text)

# 3. Общая сумма
total_amount = sum(prices)

# 4. Извлечь дату и время (форматы: DD/MM/YYYY, HH:MM)
dates = re.findall(r'\b\d{2}/\d{2}/\d{4}\b', text)
times = re.findall(r'\b\d{2}:\d{2}\b', text)

# 5. Метод оплаты (например, "Cash", "Card")
payment_method = re.findall(r'\b(Cash|Card|Credit|Debit)\b', text, re.IGNORECASE)

# Структурированный вывод
parsed_data = {
    "products": products,
    "prices": prices,
    "total_amount": total_amount,
    "dates": dates,
    "times": times,
    "payment_method": payment_method
}

print(json.dumps(parsed_data, indent=4))
