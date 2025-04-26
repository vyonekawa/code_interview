# Modelagem Dimensional com PySpark (Português)

Este projeto realiza a transformação de uma tabela bruta de vendas em um modelo dimensional usando o esquema estrela, com PySpark.

**Observação:** Este código foi elaborado para rodar em ambiente **Windows** localmente, utilizando o sistema de arquivos nativo. Para execução em ambientes Cloud ou Linux, é necessário ajustar os caminhos de entrada e saída.

## 📂 Estrutura do Projeto

```
.
├── data/
│   ├── dados_brutos.csv               # Arquivo de entrada
│   ├── dim_customer.csv               # Dimensão cliente
│   ├── dim_product.csv                # Dimensão produto
│   ├── dim_date.csv                   # Dimensão tempo
│   └── fact_sales.csv                 # Fato vendas
├── main/
│   └── modeling.py                    # Script principal
├── README.md                          # Este arquivo
```

## ⚙️ Como Executar

### Pré-requisitos

- Python 3.8+
- Apache Spark instalado e no PATH
- PySpark: `pip install -r requirements.txt` ou `pip install pyspark`

### Rodar com Spark Submit

```bash
spark-submit main/modeling.py
```

### Alternativa: executar na IDE

1. Configure o interpretador com PySpark instalado
2. Abra `modeling.py`
3. Rode com o botão ▶️

## 🧱 Modelagem Dimensional

O modelo segue o esquema estrela:

### ⭐ Fato: `fact_sales.csv`

| sale_id | customer_id | product_id | date_id | quantity_sold | total_value |
|---------|-------------|------------|---------|----------------|-------------|

### 📘 Dimensões

- `dim_customer.csv`: nome_cliente, cidade, estado
- `dim_product.csv`: nome_produto, categoria, fabricante
- `dim_date.csv`: data, ano, mês, dia

## 📌 Decisões Tomadas

- Chaves surrogate geradas com `monotonically_increasing_id()`
- `.coalesce(1)` para gerar arquivos únicos por tabela
- Arquivos exportados no formato `.csv`

## 🧰 Tecnologias Utilizadas

- Apache Spark
- PySpark (DataFrame + SQL)
- Python 3.8+
- Git e GitHub

## Observações

- O modelo foi desenvolvido com base no esquema estrela.
- O foco foi demonstrar a criação e transformação dos dados de forma limpa e compreensível.
- Código com comentários e variáveis em inglês, visando facilitar a adaptação para um contexto global. 



