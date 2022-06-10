# House Rocket Insight's Project

Esse é um projeto fícticio cuja empresa, as perguntas e o contexto de negócio não são reais. Os dados foram obtidos pela plataforma de competição Kaggle. 
(https://www.kaggle.com/datasets/harlfoxem/housesalesprediction)

Link to Heroku Project: https://jbm-analytics-house-rocket.herokuapp.com/

# 1.0 Descrição e Desafio
A House Rocket é uma plataforma digital que tem como modelo de negócio, a compra e venda de imóveis usando tecnologia.

Você é um Data Scientist contratado pela empresa para ajudar a encontrar as melhores oportunidades de negócio no mercado de imóveis. O CEO da House Rocket gostaria de maximizar a receita da empresa. Sua principal estratégia é comprar boas casas em ótimas localizações com preços baixos e depois revendê-las posteriormente à preços mais altos. Quanto maior a diferença entre a compra e a venda, maior o lucro da empresa e portanto maior sua receita. Entretanto, as casas possuem muitos atributos que as tornam mais ou menos atrativas aos compradores e vendedores, a localização e o período do ano também podem influenciar os preços.

Como objetivo terão de ser respondidas as seguintes perguntas:

1. Quais casas o CEO da House Rocket deveria comprar e por qual preço ?
2. Uma vez a casa em posse da empresa, qual seria o preço da venda?
3. A House Rocket deveria fazer uma reforma para aumentar o preço da venda? Quais seriam as sugestões de mudanças?


# 2.0 Atributos e Premissas Do Negócio
## 2.1 Atributos
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

## 2.2 Premissas do Negócio
Para realizar esse projeto as seguintes premissas de negócio foram adotadas:

* Atributos cuja natureza é considerada de tipo Inteira foram transformadas em tipos inteiros para simplificação do projeto (por ex: numero de banheiros, quartos e etc.
* Valores cujo ID eram duplicados foram removidos da base de dados.
* A coluna price significa o preço que a casa foi / será comprada pela empresa House Rocket.
* A coluna yr_renovated descreve o ano que as casas foram reformadas. Caso seja igual a 0 significa que o imóvel nunca foi reformado.
* A localidade e a condição do imóvel foram uma das características mais importantes na hora de compra ou não do imóvel.

# 3. Planejamento da Solução 
1. Identificar a causa raiz
   * Descobrir a real causa do problema? Porque o CEO fez essas perguntas? 
   * Anotar as causas.
   
2. Coletar os Dados
   * Coletar base de Dados do Kaggle.
 
3. Tratamento e Limpeza dos Dados
   * Entender as variáveis disponíveis, possíveis valores faltantes, realizar estatística descritiva para entender melhor os dados.
   * Tratar possíveis erros e realizar adequações.
  
4. Levantamento de Hipóteses sobre o Comportamento do Negócio
   * Levantar hipóteses que possam agregar o entendimento do negócio.
   
5. Realizar Análise Exploratória de Dados
   * Verificar quais das hipóteses geradas são verdadeiras.
   * Quais as correlações entre as variáveis e a variável resposta (preço).
   
6. Descrever os Insights encontrados
7. Soluções e Resultados para o Negócio

# 4. Insights do Negócio
| Hipótese  | Condição | Ação |
|:--|:---:|:---:|
| H1:  Imóveis que possuem vista para água, são em média 30% mais caros | FALSA | Investir em imóveis com vista para água (são 200% mais caros) |
| H2:  Imóveis construídos antes do ano de 1955 são 50% mais baratos na média. | FALSA | Não investir baseado no ano de construção |
| H3:  Imóveis com tamanho da área habitável acima da média são 50% mais caras que casas com área de habitação abaixo da média | FALSA | Investir em imóveis com tamanho de área habitável acima da média |
| H4:  Imóveis disponibilizados no verão são vendidos 5% mais caro em média que os imóveis disponibilizados no inverno. | VERDADEIRA | Investir em imóveis no périodo de inverno |
| H5:  Imóveis com data de renovação são 40% mais caros em média que imóveis sem nenhuma reforma. | VERDADEIRA | Investir em imóveis sem renovação para possível reforma |
| H6:  Imóveis sem porão possuem área total 20% maior que os imóveis com porão. | VERDADEIRA | Investir em imóveis sem porão |
| H7:  Imóveis com número de quartos acima da média são 50% mais em média. | VERDADEIRA | Investir em imóveis com número de quartos acima da média  |
| H8:  Imóveis que possuem área total acima da média são 50% mais caras em média.  | FALSA | Não investir em imóveis baseado somente na área total |

# 5. Questões de Negócio
## 5.1 Questões de Negócio
### 5.1.1 Quais os imóveis o CEO da House Rocket deveria comprar e por qual preço de compra?
Analisado a base de dados da House Rocket foi feita a seleção de alguns imóveis baseados na mediana dos preços de cada região e pelas condições dos imóveis, foram selecionadas ao total 10631 imóveis com alto potencial de futura venda.
### 5.1.2 2. Uma vez o imóvel em posse da empresa, qual o melhor momento para vendê-las e qual seria o preço da venda?
Para a análise da venda de imóveis comprados foi observado o valor dos imóveis se comparado ao ano anterior assim como a sua estação do ano, para isso foi realizado a mediana dos preços para cada região durante cada estação do ano:

* Se o preço da compra for maior que o preço da mediana da região da estação o preço de venda será 10% maior que o preço da compra.
* Se o preço da compra for menor que o preço da mediana da região da estação o preço de venda será 25% maior que o preço da compra.

### 5.1.3 A House Rocket deveria fazer uma reforma para aumentar o preço da venda? Quais seriam as sugestões de mudanças??

Conforme observado na seção de Insights de Negócio obtivemos uma informação bem relevante:

Imóveis com ano de renovação ( reforma ) são 40% mais caras.
Tendo em vista esse descoberta, seria interessante sim a empresa House Rocket selecionar os melhores imóveis que possibilitam reformas como forma de aumentar seu lucro. Na resolução da 2º questão de negócio já selecionamos os melhores imóveis que possibilitam reformas, que são os imóveis que possuem os atributos mais relevantes na maximização do preço, cujas características são:

- Imóveis que não foram reformadas.
- Imóveis com número de banheiros abaixo da média.
- Imóveis com área de habitação abaixo da média.

# 6. Avaliação Imobiliária
Dentre a quantidade de imóveis selecionados como de alto potencial de venda foi feita mais uma análise baseada nos Insights de Negócio observados, sendo os principais deles:

  * Imóveis com reforma (yr_renovated) são 40% mais caros.
  * Imóveis com número de quartos (bedrooms) acima da média são 50% mais caros.
  * Imóveis com área de habitação acima da média são 90% mais caras.

Dentre os 150 imóveis com maior margem de lucro, foram selecionados outros imóveis com potencial de reforma utilizando os Insights encontrados. No total selecionamos 20 imóveis que não foram reformados, com número de quartos abaixo da média e área de habitação abaixo da média para que posteriormente a empresa possa realizar uma reforma contemplando esses atributos maximizando o seu preço de venda.

|   | Valor US$ |
|:-:|:-:|
| Investimento Inicial | 19,672,750.00 |
| Lucro Esperado | 4,918,187.50 |

O retorno do valor investido caso fosse implementado essa solução seria de 25% por cento, isso sem contar as possíveis reformas que podem maximizar esse lucro. Se definido um orçamento limitado de investimento, outras estratégias de seleção dos imóveis mais rentáveis a empresa podem ser tomadas.

# 7.0 Conclusão e Trabalhos Futuros
Os objetivos iniciais foram alcançados. Foi realizado a seleção dos imóveis baseada na mediana dos preços de cada região e pelas condições dos imóveis (>= 3 boa).

No total foram selecionados 10631 com alto potencial de venda futura das quais foram selecionadas os top 150 imóveis que gerariam maior lucro na venda, e dentre esses foram selecionados mais 20 imóveis que tem condições favoráveis para se realizar uma reforma e assim maximizar o seu preço de venda e consequentemente o lucro da empresa.

Se adotada as medidas descritas nesse projeto, o lucro de retorno seria de 25% do valor total investido inicialmente. Isso sem considerar a alteração no valor caso fossem realizadas as reformas nos imóveis sugeridos.

### Trabalhos Futuros
Como trabalhos futuros poderíamos incrementar algumas coisas ao nosso projeto:

Avaliação do Incremento do valor da venda pós reforma.
Implementação de um Algoritmo que realiza a previsão do preço de venda de imóvel.
Explorar e tentar definir qual a melhor época para se vender os imóveis.
Analisar se imóveis com condições ruins são benéficos para se comprar e realizar uma reforma agregando valor e gerando um bom lucro na hora da venda.
