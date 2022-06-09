# House Rocket Insight's Project

Esse é um projeto fícticio cuja empresa, as perguntas e o contexto de negócio não são reais. Os dados foram obtidos pela plataforma de competição Kaggle. 
(https://www.kaggle.com/datasets/harlfoxem/housesalesprediction)


# 1.0 Descrição e Desafio
A House Rocket é uma plataforma digital que tem como modelo de negócio, a compra e venda de imóveis usando tecnologia.

Você é um Data Scientist contratado pela empresa para ajudar a encontrar as melhores oportunidades de negócio no mercado de imóveis. O CEO da House Rocket gostaria de maximizar a receita da empresa. Sua principal estratégia é comprar boas casas em ótimas localizações com preços baixos e depois revendê-las posteriormente à preços mais altos. Quanto maior a diferença entre a compra e a venda, maior o lucro da empresa e portanto maior sua receita. Entretanto, as casas possuem muitos atributos que as tornam mais ou menos atrativas aos compradores e vendedores, a localização e o período do ano também podem influenciar os preços.

Como objetivo terão de ser respondidas as seguintes perguntas:

1. Quais casas o CEO da House Rocket deveria comprar e por qual preço ?
2. Uma vez a casa em posse da empresa, qual seria o preço da venda?
3. A House Rocket deveria fazer uma reforma para aumentar o preço da venda? Quais seriam as sugestões de mudanças?


# 2.0 Atributos e Premissas Do Negócio

Os dados e a descrição dos dados para esse projeto estão localizados na plataforma da comunidade de Data Science e Machine Learning chamada Kaggle e pode ser encontrada no seguinte link (https://www.kaggle.com/datasets/harlfoxem/housesalesprediction/discussion/207885)

| Atributo  | Descrição |
|:---:|:-----:|
|id| Identificador único de cada imóvel  |
|date| Data de Venda do imóvel  |
|price| Preço do imóvel Vendido  |
|bedrooms| Número de Quartos  |
|bathrooms| Número de Banheiros  |
|sqft_living| Medida em Pé Quadrado do espaço de habitação do imóvel|
|sqft_lot| Medida em Pé Quadrado do lote do imóvel|
|floors| Número de andares  |
|waterfront| Variável que indica se imóvel tem ou não visão para água (1 = sim, 0 = não)  |
|view| Um índice de 0 a 4 de quão boa é a vista da propriedade (0 = ruim, 4 = excelente)  |
|condition| Um índice de 1 a 5 que indica condição da casa. (1 = ruim, 5 = excelente)  |
|grade| Um índice de 1 a 13, onde 1-3 fica aquém da construção e projeto do edifício (qualidade inferior), 7 tem um nível médio de construção e projeto e 11-13 tem um alto nível de qualidade de construção e projeto.  |
|sqft_above| Medida em Metro Quadrado do espaço interior da habitação que está acima do nível do solo  |
|sqft_basement| Medida em Metro Quadrado d o espaço interior da habitação que está abaixo do nível do solo |
|yr_built| Ano de Construção do imóvel  |
|yr_renovated| Ano de reforma de cada imóvel  |
|zipcode| CEP do imóvel  |
|lat| Latitude da localidade do imóvel  |
|long| Longitude da localidade do imóvel  |
|sqft_living15|Medida em Pés Quadrado do espaço interno de habitação para os 15 vizinhos mais próximos |
|sqft_lot15|Medida em Pés Quadrado dos lotes de terra dos 15 vizinhos mais próximos  |

