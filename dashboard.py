import streamlit as st 
import pandas as pd 
import numpy as np
import folium
import geopandas
import plotly.express as px
import time as t
import plotly.graph_objects as go

from datetime import *
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from PIL import Image

(pd.set_option('display.float_format', lambda x: '%.2f' % x))
st.set_page_config(layout='wide')

image = Image.open('img/house.jpeg')
st.sidebar.image(image,use_column_width=True,caption='House Rocket Company')


options = st.sidebar.radio('Selecione a seção desejada.',('Home','Análise Descritiva','Portfólio de Densidade','Visualização de Dados','Insights de Negócio','Avaliação e Conclusão'))

if options == 'Home':
	my_bar = st.progress(0)

	for percentage_complete in range(100):
		t.sleep(0.01)
		my_bar.progress(percentage_complete+1)


	st.markdown("<h1 style='text-align: center; color: black;'>House Rocket Company</h1>", unsafe_allow_html=True)
	st.write("Esse é um projeto fícticio cuja empresa, as perguntas e o contexto de negócio não são reais. Os dados foram obtidos pela plataforma de competição Kaggle (https://www.kaggle.com/datasets/harlfoxem/housesalesprediction).")
	st.header('Descrição e Desafio')
	st.write('A House Rocket é uma plataforma digital que tem como modelo de negócio, a compra e venda de imóveis usando tecnologia.')
	st.write("Você é um Data Scientist contratado pela empresa para ajudar a encontrar as melhores \
			oportunidades de negócio no mercado de imóveis. O CEO da House Rocket gostaria de maximizar a receita da empresa. Sua principal estratégia é comprar boas casas em ótimas localizações com preços baixos e depois revendê-las posteriormente à preços mais altos. Quanto maior a diferença entre a compra e a venda, maior o lucro da empresa e portanto maior sua receita. Entretanto, as casas possuem muitos atributos que as tornam mais ou\
			 menos atrativas aos compradores e vendedores, a localização e o período do ano também podem influenciar os preços.")

	st.write('Como objetivo terão de ser respondidas as seguintes perguntas:')
	st.write('1. Quais casas o CEO da House Rocket deveria comprar e por qual preço ?')
	st.write('2. Uma vez a casa em posse da empresa, qual seria o preço da venda?')
	st.write('3. A House Rocket deveria fazer uma reforma para aumentar o preço da venda? Quais seriam as sugestões de mudanças?')
	
	st.header('Premissas de Negócio')
	st.write('Para realizar esse projeto as seguintes premissas de negócio foram adotadas:')
	st.write('* Atributos cuja natureza é considerada de tipo Inteira foram transformadas em tipos inteiros para simplificação do projeto (por ex: numero de banheiros, quartos e etc.')
	st.write('* Valores cujo ID eram duplicados foram removidos da base de dados.')
	st.write('* A coluna price significa o preço que a casa foi / será comprada pela empresa House Rocket.')
	st.write('* A coluna yr_renovated descreve o ano que as casas foram reformadas. Caso seja igual a 0 significa que o imóvel nunca foi reformado.')
	st.write('* A localidade e a condição do imóvel foram uma das características mais importantes na hora de compra ou não do imóvel.')

	st.header('Planejamento da Solução.')
	st.write('1. Identificar a causa raiz.')
	st.write('2. Coletar os Dados.')
	st.write('3. Tratamento e Limpeza dos Dados.')
	st.write('4. Levantamento de Hipóteses sobre o Comportamento do Negócio.')
	st.write('5. Realizar Análise Exploratória de Dados.')
	st.write('6. Descrever os Insights encontrados.')
	st.write('7. Soluções e Resultados para o Negócio.')


	st.header('Ferramentas Utilizadas')
	st.write('* Python, Pandas, Numpy.')
	st.write('* Geopandas, Plotly.')
	st.write('* Folium, Streamlit.')
	st.write('* Git, Github.')
	st.write('* Heroku.')

	st.header('Contato')
	st.write('Esse projeto foi realizado por Jordan Butkenicius Malheiros, para mais informações entrar em contato:')
	link_linkedin = '[JordanM - Linkedin](https://www.linkedin.com/in/jordan-butkenicius-malheiros-4a0266169/)'
	link_github = '[JordanM - GitHub](https://github.com/malheiros7j)'

	c1 ,c2 = st.columns(2)

	with c1:
		st.markdown(link_linkedin,unsafe_allow_html=True)
		st.markdown(link_github,unsafe_allow_html=True)


@st.cache(allow_output_mutation=True)
# Read the database from path 
def get_data(path):
	data = pd.read_csv(path)
	data = data.drop_duplicates(subset='id', keep="last")

	return data


@st.cache(allow_output_mutation=True)
def get_df_buy(path2):
    df_buy= pd.read_csv(path2)
    return df_buy

@st.cache(allow_output_mutation=True)
# Get the database of geofiles
def get_geofile(path):
	geofile = geopandas.read_file(path)

	return geofile

#Set new feature
def set_feature(data):
	#Transform sqft to sqm2
	data['sqmt_lot'] = data['sqft_lot'] / 10.764
	data['sqmt_living'] = data['sqft_living'] / 10.764
	data['price_m2'] = data['price'] / data['sqmt_lot']
	data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')

	return data

def overview_data(data):
	if options == 'Análise Descritiva':
		my_bar = st.progress(0)

		for percentage_complete in range(100):
			t.sleep(0.1)
			my_bar.progress(percentage_complete+1)

		### DATA OVERVIEW
		#st.write(data.columns[0])
		st.markdown("<h1 style='text-align: center; color: Black;'>Visão Geral dos Dados</h1>", unsafe_allow_html=True)
		st.write('Esta seção é destinada para que possa ser observado como estão organizados os nossos dados e realizar algumas análises descritivas visando o auxílio do entendimento do negócio.')
		#st.title('Visão Geral dos Dados')

		####### Filter of properties by ZipCode and Attributes ######

		#Creating Filter Zipcode And Attributes
		st.sidebar.title('Filtros de Atributos e Região')
		f_attributes = st.sidebar.multiselect('Selecione os Atributos', data.columns)
		f_zipcode = st.sidebar.multiselect('Selecione o Zipcode', data['zipcode'].unique())

		#Define the conditions of the filters 
		if (f_zipcode != []) & (f_attributes != []):
			data = data.loc[data['zipcode'].isin(f_zipcode),f_attributes]

		elif (f_zipcode != []) & (f_attributes == []):
			data = data.loc[data['zipcode'].isin(f_zipcode), :]

		elif (f_zipcode == []) & (f_attributes != []):
			data = data.loc[:,f_attributes]
			
		else:
			data = data.copy()

		
		st.dataframe(data)

		#Format the table on the page
		c1, c2 = st.columns((1,1))
		##############################
		# Number of Attributes by ZIPCODE, CALCULATING AVG PRICE, AVG OF SQMT_LIVING , AVG PRICE, AVG PRICE BY SQUARE METER(M²)
		########################
		if 'id' or 'date' or 'price' or 'bathrooms' or 'sqft_living' or 'sqft_lot' or 'floors' or 'waterfront' or 'view' or 'condition' or 'grade' or 'sqft_above' or 'sqft_basement' or 'yr_built' or 'yr_renovated' or 'zipcode' or 'lat' or 'long' or 'sqft_living15' or 'sqft_lot15' or 'sqmt_lot' or 'sqmt_living' or 'price_m2' not in data:

			data['id'] = aux['id']
			data['date'] = pd.to_datetime(aux['date']).dt.strftime('%Y-%m-%d')
			data['price'] = aux['price']
			data['bathrooms'] = aux['bathrooms']
			data['sqft_living'] = aux['sqft_living']
			data['sqft_lot'] = aux['sqft_lot']
			data['floors'] = aux['floors']
			data['waterfront'] = aux['waterfront']
			data['view'] = aux['view']
			data['condition'] = aux['condition']
			data['grade'] = aux['grade']
			data['sqft_above'] = aux['sqft_above']
			data['sqft_basement'] = aux['sqft_basement']
			data['yr_built'] = aux['yr_built']
			data['yr_renovated'] = aux['yr_renovated']
			data['zipcode'] = aux['zipcode']
			data['lat'] = aux['lat']
			data['long'] = aux['long']
			data['sqft_living15'] = aux['sqft_living15']
			data['sqft_lot15'] = aux['sqft_lot15']
			data['sqmt_lot'] = aux['sqmt_lot']
			data['sqmt_living'] = aux['sqmt_living']
			data['price_m2'] = aux['price_m2']

		# Calculate the Number of Properties / AVG Price /  SQMT LIVING / PRICE PER SQMT(m2)
		num_properties = data[['id','zipcode']].groupby('zipcode').count().reset_index()
		media_price = data[['price','zipcode']].groupby('zipcode').mean().reset_index()
		media_sqmt_living = data[['sqmt_living','zipcode']].groupby('zipcode').mean().reset_index()
		media_price_m2 = data[['price_m2','zipcode']].groupby('zipcode').mean().reset_index()

		# Merge
		m1 = pd.merge(num_properties,media_price,on='zipcode', how='inner')
		m2 = pd.merge(m1,media_sqmt_living,on='zipcode', how='inner')
		df = pd.merge(m2,media_price_m2,on='zipcode', how='inner')

		#Define Column Names
		df.columns = ['ZipCode','NumberOfProperties', 'AVG Price','AVG Sqmt_Living','AVG Price by SQMT']

		c1.header('Valores Médios por ZIPCODE')
		c1.dataframe(df,height=600)

		## Descriptive Attributes
		num_attributes = data.select_dtypes(include=['int64','float64'])
		num_attributes = num_attributes.drop(['id','waterfront','view'],axis=1)
		media = pd.DataFrame(num_attributes.apply(np.mean))
		median = pd.DataFrame(num_attributes.apply(np.median))
		std = pd.DataFrame(num_attributes.apply(np.std))

		max_ = pd.DataFrame(num_attributes.apply(np.max))
		min_ = pd.DataFrame(num_attributes.apply(np.min))

		df1 = pd.concat([max_,min_,media,median,std],axis=1).reset_index()
		df1.columns= ['Attributes', 'Max', 'Min', 'AVG', 'Median', 'Std']

		c2.header('Análise Descritiva Estatística')
		c2.dataframe(df1,height=600)

		return None


def portfolio_density(data,geofile):

	if options == 'Portfólio de Densidade':
		my_bar = st.progress(0)

		for percentage_complete in range(100):
			t.sleep(0.1)			
			my_bar.progress(percentage_complete+1)

		st.markdown("<h1 style='text-align: center; color: Black;'> Portfólio de Densidade</h1>", unsafe_allow_html=True)
		

		st.header('Visão Geral de Dados por Região Geográfica')
		st.write('Esta seção é destinada a visualização geográfica da base de dados, com objetivo de oferecer um aspecto de análise das regiões dos imóveis por meio da ilustração de 2 tipos de mapas:')
		st.write('- Densidade de Portfólio: consiste na representação dos imóveis agrupados de acordo com sua localização geográfica.')
		st.write('- Densidade de Preço: representação do preço médio dos imóveis de cada região geograficamente.')

		c1, c2 = st.columns((1,1))

		c1.subheader('Densidade de Portólio')

		#Create copy of data to make the maps
		df = data

		#Base Map - Folium
		density_map = folium.Map(location=[data['lat'].mean(),data['long'].mean()],
				   default_zoom_start = 15)

		#Create Cluster to show Portfolio Density
		marker_cluster = MarkerCluster().add_to(density_map)
		for name, row in df.iterrows():
			folium.Marker([row['lat'],row['long']],
				popup='Price R${0} on: {1}. Features: {2} sqft, {3} bedrooms, {4} bathrooms, year_built: {5}'.format(row['price'],
																													 row['date'],
																													 row['sqft_living'],
																													 row['bedrooms'],
																													 row['bathrooms'],
																													 row['yr_built'])).add_to(marker_cluster)

		with c1:
			folium_static(density_map)


		# Region Price Map
		c2.subheader('Densidade de Preço')

		df = data[['price','zipcode']].groupby('zipcode').mean().reset_index()
		df.columns = ['ZIP','PRICE']

		geofile = geofile[geofile['ZIP'].isin(df['ZIP'].tolist())]
		region_price_map = folium.Map(location=[data['lat'].mean(),data['long'].mean()],
				   				default_zoom_start = 15)

		folium.Choropleth(data = df,
						  geo_data = geofile,
						  columns=['ZIP', 'PRICE'],
						  key_on='feature.properties.ZIP',
						  fill_color='YlOrRd',
						  fill_opacity = 0.7,
						  line_opacity = 0.2,
						  legend_name='AVG PRICE').add_to(region_price_map)

		with c2:
			folium_static(region_price_map)

		return None


def commercial_distribution(data):
	if options == 'Visualização de Dados':
		my_bar = st.progress(0)

		for percentage_complete in range(100):
			t.sleep(0.1)
			my_bar.progress(percentage_complete+1)

		st.title('Atributos Comerciais')

		st.write('Essa seção é destinada a apresentação de dashboards de diferentes atributos da base de dados visando o maior entendimento do negócio como um todo.')
		st.sidebar.title('Opções Comerciais')

		c1,c2 = st.columns(2)

		data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')

		min_year_built = int(data['yr_built'].min())
		max_year_built = int(data['yr_built'].max())


		#Create the filters (Max yr_built)
		c1.header('Average Price by Construction Year')

		#Create sidebar and define the bar
		st.sidebar.subheader('Select Max Year Built')
		f_yr_built = st.sidebar.slider('Year Built',min_year_built,max_year_built,min_year_built)

		#Validate the data with the filters
		df = data.loc[data['yr_built'] <= f_yr_built]
		df = df[['price','yr_built']].groupby('yr_built').mean().reset_index()

		#Plot the AVG Price by year 
		fig = px.line(df,x='yr_built',y='price')
		c1.plotly_chart(fig,use_container_width=True)

		##Create Filter (Max Date)
		min_date = datetime.strptime(data['date'].min(), '%Y-%m-%d')
		max_date = datetime.strptime(data['date'].max(), '%Y-%m-%d')

		st.sidebar.subheader('Select Max Date')
		f_max_date = st.sidebar.slider('Max Date',min_date, max_date,min_date)

		#Transform data['date'] to datetime
		data['date'] = pd.to_datetime(data['date'])

		df = data.loc[data['date'] <= f_max_date]
		df = df[['date','price']].groupby('date').mean().reset_index()

		#Plot
		c2.header('Average Price per day')
		fig2 = px.line(df,x='date',y='price')
		c2.plotly_chart(fig2,use_container_width=True)

		#------------------------ Histograma
		st.header('Price Distribution')
		st.sidebar.subheader('Select Max Price')

		#filter 
		min_price = int(data["price"].min())
		max_price = int(data["price"].max())
		avg_price = int(data["price"].mean())
		#data filtering
		f_price=st.sidebar.slider('Price',min_price,max_price,avg_price)
		df= data.loc[data['price'] <= f_price]
		#data plot
		fig=px.histogram(df,x='price',nbins=50)
		st.plotly_chart(fig,use_container_width=True)

		return None


def attributes_distribution(data):
	if options == 'Visualização de Dados':
		# ---------- Distribuição Imoveis por preço, num quartos, num banhieors, numero andres, vista para agua
		# Properties Distribution by Price, Number of Bedrooms, Number of Bathrooms, Number of Floors, Waterview front
		c1,c2 = st.columns(2)

		st.sidebar.title('Attributes Options')
		st.title('House Attributes')

		######################################################
		############## Houses per Bedroom ####################
		st.sidebar.subheader('Select Number of Bedrooms')
		f_bedrooms = st.sidebar.selectbox('Bedrooms', sorted(set(data['bedrooms'].unique())))
		df = data.loc[data['bedrooms'] <= f_bedrooms]

		#Plot
		c1.header('Houses per Bedroom')
		fig4 = px.histogram(df,x='bedrooms',nbins=19)
		c1.plotly_chart(fig4,use_container_width=True)


		######################################################
		############## Houses per Bathroom ###################
		st.sidebar.subheader('Select Number of Bathroom')
		f_bathrooms = st.sidebar.selectbox('Bathrooms', sorted(set(data['bathrooms'].unique())))
		df = data.loc[data['bathrooms'] <= f_bathrooms]

		# Plot
		c2.header('Houses per Bathrooms')
		fig5 = px.histogram(df,x='bathrooms',nbins=19)
		c2.plotly_chart(fig5,use_container_width=True)


		######################################################
		############## Houses per Floor ######################
		c3,c4 = st.columns(2)

		st.sidebar.subheader('Select Number of Floors')
		f_floors = st.sidebar.selectbox('Floors', sorted(set(data['floors'].unique())))
		df = data.loc[data['floors'] <= f_floors]

		#Plot 
		c3.header('Houses per Floor')
		fig6 = px.histogram(df,x='floors',nbins=19)
		c3.plotly_chart(fig6,use_container_width=True)

		######################################################
		############## Houses with Waterview #################
		st.sidebar.subheader('Select WaterFront View')
		f_waterview = st.sidebar.checkbox('Only Houses With Water View')

		if f_waterview:
			df = data[data['waterfront'] == 1]
		else:
			df = data.copy()

		c4.header('Houses with Waterview')
		fig7 = px.histogram(df,x='waterfront',nbins=19)
		c4.plotly_chart(fig7,use_container_width=True)
		return None

def var_percentage(var1,var2):
	var_percentage = round((var1/var2 - 1) * 100,2)

	return var_percentage 

def to_buy(data):
	if options == 'Insights de Negócio':
		#Calcula a mediana do preço dos imoveis por ZIPCODE(Regiao)
		df = pd.DataFrame()
		df[['zipcode','price_median_zipcode']] = data[['zipcode','price']].groupby('zipcode').median().reset_index()
		data = pd.merge(data,df,on='zipcode',how='inner')

		# Cria coluna buy 
		# Se preço < preco_mediana da regiao & condition >=2 --> Compra
		# Se preço < preco_mediana da regiao --> Nao Compra
		data['buy'] = data.apply(lambda x:'yes' if (x['price'] < x['price_median_zipcode']) & (x['condition'] >= 2 ) else 'no',axis=1)

		#Cria as colunas de sazonalidade
		data['month'] = pd.to_datetime(data['date']).dt.month
		data['season'] = data['month'].apply(lambda x:'summer' if (x==6) | (x==7) | (x == 8) else
													'autumn' if (x==9) | (x==10) | (x == 11) else
													'winter' if (x==12) | (x==1) | (x == 2) else
													'spring')

		#Calcula a mediana de precos por ZIPCODE e ESTACAO(SEASON)
		df2 = pd.DataFrame()
		df2[['zipcode','season','price_median_zip_season']] = data[['zipcode','season','price']].groupby(['zipcode','season']).median().reset_index()
		data = pd.merge(data,df2,on=['zipcode','season'],how='inner')

		# Se preço da compra de compra for maior que o preço da mediana da regiao + sazonalidade -> Preço Venda: +10%, else -> Preço Venda:+30%
		data['sell_price'] = data.apply(lambda x:x['price']*1.1 if (x['price'] > x['price_median_zip_season'] ) else x['price']* 1.3 ,axis=1)

		# Calcula o lucro da venda adotando os novos preços de acorda com o preco medio de zipcode/season
		data['profit'] = data.apply(lambda x: x['price']*0.1 if x['price'] > x['price_median_zip_season'] else x['price']* 0.3,axis=1)

		# print(data[['id','price','zipcode','price_median_zipcode','condition','buy','zipcode','month','season','price','price_median_zip_season','sell_price','profit']])


		return data

def bussiness_hypothesis(data):
	if options == 'Insights de Negócio':
		my_bar = st.progress(0)

		for percentage_complete in range(100):
			t.sleep(0.01)
			my_bar.progress(percentage_complete+1)

		st.markdown("<h1 style='text-align: center; color: black;'>House Rocket Company</h1>", unsafe_allow_html=True)
		st.write('Esta seção é destinada ao entendimento e descoberta de Insights de Negócio, promovendo o desenvolvimento do negócio por meio de estratégia criadas com base em análise de dados, que podem se transformar em decisões e, posteriormente em ações.')

		st.markdown("<h1 style='text-align: center; color: black;font-size:40px;'>Testando Hipóteses de Negócio </h1>", unsafe_allow_html=True)



		######## H1: Properties that overlook the water, are 30% more expensive, on average?#####################
		#########################################################################################################
		#########################################################################################################
		c1,c2 = st.columns(2)

		waterfront_price = data.loc[data['waterfront'] == 1,'price'].mean()
		no_waterfront_price = data.loc[data['waterfront'] == 0,'price'].mean()

		var_waterfront = var_percentage(waterfront_price,no_waterfront_price)
		# print('Properties that overlook water are, {}% more expensive, on average'.format(var_waterfront))

		h1 = data[['price','waterfront']].groupby('waterfront').mean().reset_index()

		colors = ['lightslategray','crimson']
		#h1_plot = go.Figure(h1=[go.Bar(x='waterfront',y='price',marker_color='crimson')])

		####################
		c1.subheader('Hipótese 1: Imóveis que possuem vista para água, são em média 30% mais caros.')
		c1.write('* FALSO, imóveis com vista para água são em média 212% mais caras que os imóveis que não possuem esse tipo de atributo.')

		h1_plot = px.bar(h1,x='waterfront',y='price',color=colors,labels={"waterfront": "Visão para água","price" : "Preço"},template='simple_white')
		h1_plot.update_layout(showlegend=False)
		c1.plotly_chart(h1_plot,use_container_width=True)

		######## H2: Properties with a year of construction until 1955 are 50% cheaper, on average.#####################
		################################################################################################################
		################################################################################################################
		yr_built_before = data.loc[data['yr_built'] < 1955,'price'].mean()
		yr_built_after = data.loc[data['yr_built'] >= 1955,'price'].mean()

		# print(yr_built_before,yr_built_after)

		var_yr_built = var_percentage(yr_built_after,yr_built_before)
		# print('Houses built before 1955 are {}% cheaper,on average.'.format(var_yr_built))

		data['construction'] = data['yr_built'].apply(lambda x:' < 1955' if x < 1955 else ' >= 1955')

		h2 = data[['price','construction']].groupby('construction').mean().reset_index()

		c2.subheader('Hipótese 2: Imóveis construídos antes do ano de 1955 são 50% mais baratos na média.')
		c2.write('* FALSO, como podemos ver nos gráficos da base de dados, o preço médio das casas construídas antes e depois de 1955 estão basicamente na mesma faixa de preço.')

		h2_plot = px.bar(h2,x='construction',y='price',color='construction',labels={"construction":"Ano de Construção","price":"Preço"},template='simple_white')
		h2_plot.update_layout(showlegend=False)
		c2.plotly_chart(h2_plot,use_container_width=True)


		######## H3: Properties that have living room size above avg are 50% expensive, on averge.######################
		################################################################################################################
		################################################################################################################

		c3,c4 = st.columns(2)

		#H3: Casas com sala de estar (sqft_living) acima da média são 50% mais caras que as casas com menores (sqft_living).
		avg_living = data['sqft_living'].mean()

		above_avg_living = data.loc[data['sqft_living'] >= avg_living,'price'].mean()
		under_avg_living = data.loc[data['sqft_living'] < avg_living,'price'].mean()

		var_living = var_percentage(above_avg_living,under_avg_living)

		# print('Properties that have above avg living room size area are {}% more expensive, on avarege'.format(var_living))

		data['living_room'] = data['sqft_living'].apply(lambda x:'above_avg' if x >= avg_living else 'under_avg')
		h3 = data[['price','living_room']].groupby('living_room').mean().reset_index()

		c3.subheader('Hipótese 3: Imóveis com tamanho da sala de estar acima da média são 50% mais caras que casas com sala abaixo da média')
		c3.write('* FALSO, Imóveis com sala de estar maior que a média são 88.58% mais caras que imóveis com sala de estar abaixo da média.')

		h3_plot = px.bar(h3,x='living_room',y='price',color='living_room',labels={'living_room':'Sala de Estar','price':'Preço'},template='simple_white')
		h3_plot.update_layout(showlegend=False)
		c3.plotly_chart(h3_plot,use_container_width=True)

		
		######## H4: Properties that are bougth on summer are 10% more expensive, on average. ##########################
		################################################################################################################
		################################################################################################################
		summer = data.loc[data['season'] == 'summer','price'].mean()
		winter = data.loc[data['season'] == 'winter','price'].mean()

		var_season = var_percentage(summer,winter)

		# print('Properties bought on summer season are {}% more expensive than on winter'.format(var_season))

		h4 = data[['price','season']].groupby('season').mean().reset_index()

		c4.subheader('Hipótese 4: Imóveis disponibilizados no verão são vendidos 5% mais caro em média que os imóveis disponibilizados no inverno.')
		c4.write('* VERDADEIRO, imóveis disponibilizados no verão são vendidos 5.3% mais caros em média que os imóveis disponibilizados no inverno')
		#c4.write('* + Imóveis vendidos na primavera também são vendidos 6% mais caros em média que os de inverno.')


		h4_plot = px.bar(h4,x='season',y='price',color='season',labels={'season':'estação','price':'Preço'},template='simple_white')
		h4_plot.update_layout(showlegend=False)
		c4.plotly_chart(h4_plot,use_container_width=True)

		######## H5: Properties that got renovated are 40% more expensive, on average. #################################
		################################################################################################################
		################################################################################################################
		c5,c6 = st.columns(2)

		#H5: Imóveis com data de renovação são 40% mais caros que imóveis sem nenhuma reforma.
		no_renovation = data.loc[data['yr_renovated'] == 0,'price'].mean()
		renovation = data.loc[data['yr_renovated'] != 0,'price'].mean()

		var_renovation = var_percentage(renovation,no_renovation)
		# print('Properties that got renovated are {}% more expensive, on average'.format(var_renovation))

		data['got_renovated'] = data['yr_renovated'].apply(lambda x:'yes' if x != 0 else 'no')
		h5 = data[['price','got_renovated']].groupby('got_renovated').mean().reset_index()

		c5.subheader('Hipótese 5: Imóveis com data de renovação são 40% mais caros em média que imóveis sem nenhuma reforma.')
		c5.write('* VERDADEIRO, imóveis com renovação são 43.37% mais caros em média que imóveis sem renovação.')

		h5_plot = px.bar(h5,x='got_renovated',y='price',color='got_renovated',labels={'got_renovated':'Reforma','price':'Preço'},template='simple_white')
		h5_plot.update_layout(showlegend=False)
		c5.plotly_chart(h5_plot,use_container_width=True)


		######## H3: Properties without basement are 20% bigger, on average ############################################
		################################################################################################################
		################################################################################################################

		no_basement = data.loc[data['sqft_basement'] == 0,'sqft_lot'].mean()
		with_basement = data.loc[data['sqft_basement'] != 0,'sqft_lot'].mean()

		var_basement = var_percentage(no_basement,with_basement)

		# print('Properties without basement are {}% bigger, on average'.format(var_basement))

		data['basement'] = data['sqft_basement'].apply(lambda x:'no' if x == 0 else 'yes')
		h6 = data[['basement','sqmt_lot']].groupby('basement').mean().reset_index()

		c6.subheader('Hipótese 6: Imóveis sem porão possuem área total 20% maior que os imóveis com porão.')
		c6.write('* VERDADEIRO, imóveis sem porão tem em média 22.5% maior área total comparado as que tem.')

		h6_plot = px.bar(h6,x='basement',y='sqmt_lot',color='basement',labels={'basement':'Porão','sqmt_lot':'Área Lote(M²)'},template='simple_white')
		h6_plot.update_layout(showlegend=False)
		c6.plotly_chart(h6_plot,use_container_width=True)


		######## H7: Properties that have number of bedrooms above average are 50% expensive, on average.###############
		################################################################################################################
		################################################################################################################
		c7,c8 = st.columns(2)
		#H7: Casas com bedrooms acima da média são 20% mais caras que casas com bedrooms abaixo da média.
		avg_bedrooms = data['bedrooms'].mean()	
		above_avg_bedrooms = data.loc[data['bedrooms'] >= avg_bedrooms,'price'].mean()
		under_avg_bedrooms = data.loc[data['bedrooms'] < avg_bedrooms,'price'].mean()

		var_bedrooms = var_percentage(above_avg_bedrooms,under_avg_bedrooms)

		# print('Properties that have number of bedrooms above average are {}% more expensive, on average.'.format(var_bedrooms))

		data['bedroom_avg'] = data['bedrooms'].apply(lambda x:'above' if x >= avg_bedrooms else 'under')
		h7 = data[['price','bedroom_avg']].groupby('bedroom_avg').mean().reset_index()

		c7.subheader('Hipótese 7: Imóveis com número de quartos acima da média são 50% mais em média.')
		c7.write('* VERDADEIRO, imóveis com número de banheiro acima da média são 49.16% mais caras em média.')

		h7_plot = px.bar(h7,x='bedroom_avg',y='price',color='bedroom_avg',labels={'bedroom_avg':'Media dos Quartos','price':'Preço'},template='simple_white')
		h7_plot.update_layout(showlegend=False)
		c7.plotly_chart(h7_plot,use_container_width=True)

		######## H8: Properties that have above average in total(sqmt_lot - M²) are 50% expensive, on average.##########
		################################################################################################################
		################################################################################################################
		avg_sqmt_lot = data['sqmt_lot'].mean()

		above_avg_sqmt_lot = data.loc[data['sqmt_lot'] >= avg_sqmt_lot,'price'].mean()
		under_avg_sqmt_lot = data.loc[data['sqmt_lot'] < avg_sqmt_lot,'price'].mean()

		var_sqmt_lot = var_percentage(above_avg_sqmt_lot,under_avg_sqmt_lot)

		# print('Properties that have above average area in total(M² Lot) are {}% more expensive, on average.'.format(var_sqmt_lot))

		data['sqmt_lot_avg'] = data['sqmt_lot'].apply(lambda x:'above' if x >= avg_sqmt_lot else 'under')
		h8 = data[['price','sqmt_lot_avg']].groupby('sqmt_lot_avg').mean().reset_index()

		c8.subheader('Hipótese 8: Imóveis que possuem área total aciama da média são 50% mais caras em média.')
		c8.write('* FALSO, imóveis que possuem área total acima da média são 41.28% mais caras em média.')

		h8_plot = px.bar(h8,x='sqmt_lot_avg',y='price',color='sqmt_lot_avg',labels={'sqmt_lot_avg':'Area Lote(M²)','price':'Preço'},template='simple_white')
		h8_plot.update_layout(showlegend=False)
		c8.plotly_chart(h8_plot,use_container_width=True)

		return None

def to_buy(data):
	if options == 'Insights de Negócio':
		#Calcula a mediana do preço dos imoveis por ZIPCODE(Regiao)
		df = pd.DataFrame()
		df[['zipcode','price_median_zipcode']] = data[['zipcode','price']].groupby('zipcode').median().reset_index()
		data = pd.merge(data,df,on='zipcode',how='inner')

		# Cria coluna buy 
		# Se preço < preco_mediana da regiao & condition >=2 --> Compra
		# Se preço < preco_mediana da regiao --> Nao Compra
		data['buy'] = data.apply(lambda x:'yes' if (x['price'] < x['price_median_zipcode']) & (x['condition'] >= 2 ) else 'no',axis=1)

		#Cria as colunas de sazonalidade
		data['month'] = pd.to_datetime(data['date']).dt.month
		data['season'] = data['month'].apply(lambda x:'summer' if (x==6) | (x==7) | (x == 8) else
													'autumn' if (x==9) | (x==10) | (x == 11) else
													'winter' if (x==12) | (x==1) | (x == 2) else
													'spring')

		#Calcula a mediana de precos por ZIPCODE e ESTACAO(SEASON)
		df2 = pd.DataFrame()
		df2[['zipcode','season','price_median_zip_season']] = data[['zipcode','season','price']].groupby(['zipcode','season']).median().reset_index()
		data = pd.merge(data,df2,on=['zipcode','season'],how='inner')

		# Se preço da compra de compra for maior que o preço da mediana da regiao + sazonalidade -> Preço Venda: +10%, else -> Preço Venda:+20%
		data['sell_price'] = data.apply(lambda x:x['price']*1.1 if (x['price'] > x['price_median_zip_season'] ) else x['price']* 1.25 ,axis=1)

		# Calcula o lucro da venda adotando os novos preços de acorda com o preco medio de zipcode/season
		data['profit'] = data.apply(lambda x: x['price']*0.1 if x['price'] > x['price_median_zip_season'] else x['price']* 0.25,axis=1)

		# print(data[['id','price','zipcode','price_median_zipcode','condition','buy','zipcode','month','season','price','price_median_zip_season','sell_price','profit']])
		# print(data.columns)

		data.to_csv('df_buy.csv',index=False)

		return data


def evaluation_house_rocket(df):
	if options == 'Avaliação e Conclusão':
		my_bar = st.progress(0)

		for percentage_complete in range(100):
			t.sleep(0.01)
			my_bar.progress(percentage_complete+1)


		selected = df.loc[df['buy'] == 'yes']
		# print(selected.shape)
		selected_final = selected[['id','price']].sort_values(by=['price'],ascending=True)
		selected_final = selected_final.reset_index(drop=True)


		st.markdown("<h1 style='text-align: center; color: black;'>House Rocket Company</h1>", unsafe_allow_html=True)
		st.write('A House Rocket é uma plataforma digital que tem como modelo de negócio, a compra e venda de imóveis. A empresa busca as melhores oportunidades de compra no mercado visando o lucro na revenda desses \
			imóveis. Diante disso, o objetivo do Cientista de Dados é orientar e definir quais são as melhores estratégias e alternativas de compra e revenda do mercado, definir as melhores oportunidades de negócio e com isso maximizar o lucro da empresa.')

		st.markdown("<h1 style='text-align: center; color: black;font-size:35px;'> Avaliação e Questões do Negócio </h1>", unsafe_allow_html=True)


		st.subheader('1. Quais os imóveis o CEO da House Rocket deveria comprar e por qual preço de compra?')
		st.write('Analisado a base de dados da House Rocket foi feita a seleção de alguns imóveis baseados na mediana dos preços de cada região e pelas condições dos imóveis, foram selecionadas ao total 10631 imóveis com alto potencial de futura venda.')

		st.dataframe(selected_final)

		st.subheader('2. Uma vez o imóvel em posse da empresa, qual o melhor momento para vendê-las e qual seria o preço da venda?')
		st.write('Para a análise da venda de imóveis comprados foi observado o valor dos imóveis se comparado ao ano anterior assim como a sua estação do ano, para isso \
			foi realizado a mediana dos preços para cada região durante cada estação do ano:')
		st.write('* Se o preço da compra for maior que o preço da mediana da região da estação o preço de venda será 10% maior que o preço da compra.')
		st.write('* Se o preço da compra for menor que o preço da mediana da região da estação o preço de venda será 25% maior que o preço da compra.')


		st.markdown("<h1 style='color: black;font-size:20px;'> Esses são os top 150 imóveis mais lucrativos de se comprar e vender: </h1>", unsafe_allow_html=True)
		#st.sub('Esses são os top 100 imóveis mais lucrativos de se comprar e vender:')

		profit = selected.sort_values(by='profit',ascending=False).reset_index(drop=True).head(150)
		st.dataframe(profit[['id','date','season','price','price_median_zip_season','sell_price','profit']])


		selected_insight = profit.loc[(profit['yr_renovated'] == 0) & (profit['bedroom_avg'] == 'under') & (profit['living_room'] == 'under_avg')].sort_values(by='profit',ascending=False).reset_index(drop=True).head(20)
		selected_insight_map = selected_insight


		selected_insight = selected_insight[['id','price','yr_renovated','bedroom_avg','living_room','sell_price','profit']]

		
		investimento = selected_insight['price'].sum()
		lucro = selected_insight['profit'].sum()


		st.markdown("<h1 style='font-size:20px;color: black;'>Dentre a quantidade de imóveis selecionados como de alto potencial de venda foi feita mais uma análise baseada nos Insights de Negócio observados, sendo os principais deles:</h1>", unsafe_allow_html=True)
		st.write('* Imóveis com reforma (yr_renovated) são 40% mais caros.')
		st.write('* Imóveis com número de quartos (bedrooms) acima da média são 50% mais caros.')
		st.write('* Imóveis com sala de estar acima da média são 90% mais caras.')

		st.write('Dentre os 150 imóveis com maior margem de lucro, foram selecionados outros imóveis com potencial de reforma utilizando os Insights encontrados. No total selecionamos 20 imóveis\
			que não foram reformados, com número de quartos abaixo da média e área da sala de estar abaixo da média para que posteriormente a empresa possa realizar uma reforma contemplando esses atributos maximizando o seu preço de venda.')
		
		st.subheader('Tabela de Imóveis sugeridos para compra e venda.')
		st.dataframe(selected_insight)

		dic={"Investimento Inicial":investimento,'Lucro Esperado':lucro}
		money=pd.Series(dic).to_frame('Valor US$')
		st.table(money)

		st.markdown("<h1 style='font-size:20px;color: black;'>O retorno do valor investido caso fosse implementado essa solução seria de 25% por cento, isso sem contar as possíveis reformas que \
					podem maximizar esse lucro. Se definido um orçamento limitado de investimento, outras estratégias de seleção dos imóveis mais rentáveis a empresa podem ser tomadas.</h1>", unsafe_allow_html=True)
		
		if st.checkbox('Mostrar Localização dos Imóveis'):

			df = selected_insight_map

			c1,c2 = st.columns((1,1))

			houses_map = folium.Map(location=[selected_insight_map['lat'].mean(),selected_insight_map['long'].mean()],zoom_start = 12)

			#the_map = MarkerCluster().add_to(houses_map)

			for name, row in df.iterrows():
				folium.Circle([row['lat'],row['long']],radius=50,fill=True,fill_opacity = 1,
					popup='id: {0} Price: US$ {1}. Sell Price: US$ {2} Profit: US$ {3}'.format(row['id'],row['price'],row['sell_price'],row['profit'])).add_to(houses_map)

			with c1:
				folium_static(houses_map)

		st.subheader('3. A House Rocket deveria fazer uma reforma para aumentar o preço da venda? Quais seriam as sugestões de mudanças??')
		st.write('Conforme observado na seção de Insights de Negócio obtivemos uma informação bem relevante:')
		st.write('* Imóveis com ano de renovação ( reforma ) são 40% mais caras.')
		st.write('Tendo em vista esse descoberta, seria interessante sim a empresa House Rocket selecionar os melhores imóveis que possibilitam reformas como forma de aumentar seu lucro. Na resolução da 2º questão de negócio já selecionamos os melhores imóveis que possibilitam \
			reformas, que são os imóveis que possuem os atributos mais relevantes na maximização do preço, cujas características são:')

		st.markdown("<h1 style='font-size:15px;color: black;'> - Imóveis que não foram reformadas.</h1>", unsafe_allow_html=True)
		st.markdown("<h1 style='font-size:15px;color: black;'> - Imóveis com número de banheiros abaixo da média.</h1>", unsafe_allow_html=True)
		st.markdown("<h1 style='font-size:15px;color: black;'> - Imóveis com tamanho de sala de estar abaixo da média.</h1>", unsafe_allow_html=True)


		st.write('')
		st.write('')
		st.write('')

		st.markdown("<h1 style='color: black;text-align:center;'> Conclusão </h1>", unsafe_allow_html=True)
		st.write('Os objetivos iniciais foram alcançados. Foi realizado a seleção dos imóveis baseada na mediana dos preços de cada região e pelas condições dos imóveis (>= 3 boa).')
		st.write(' No total foram selecionados 10631 com alto potencial de venda futura\
			das quais foram selecionadas os top 150 imóveis que gerariam maior lucro na venda, e dentre esses foram selecionados mais 20 imóveis que tem condições favoráveis para se realizar uma reforma e assim maximizar o seu preço de venda e consequentemente o lucro da empresa.')

		st.write('Se adotada as medidas descritas nesse projeto, o lucro de retorno seria de 25% do valor total investido inicialmente. Isso sem considerar a alteração no valor caso fossem realizadas as reformas nos imóveis sugeridos.')
		
		st.write('')
		st.write('')
		st.write('')

		st.subheader('Trabalhos Futuros')
		st.write('Como trabalhos futuros poderíamos incrementar algumas coisas ao nosso projeto:')
		st.write('* Avaliação do Incremento do valor da venda pós reforma.')
		st.write('* Implementação de um Algoritmo que realiza a previsão do preço de venda de imóvel.')
		st.write('* Explorar e tentar definir qual a melhor época para se vender os imóveis.')
		st.write('* Analisar se imóveis com condições ruins são benéficos para se comprar e realizar uma reforma agregando valor e gerando um bom lucro na hora da venda.')



		return None
		
if __name__ == '__main__':
	path = 'kc_house_data.csv'
	path_geo = 'Zip_Codes.geojson'
	data = get_data(path) 
	aux = get_data(path)
	geofile = get_geofile(path_geo)	
	data = set_feature(data)
	overview_data(data)
	portfolio_density(data,geofile)
	commercial_distribution(data)
	attributes_distribution(data)
	to_buy(data)
	path2 = 'df_buy.csv'
	df_buy = get_df_buy(path2)
	bussiness_hypothesis(df_buy)
	evaluation_house_rocket(df_buy)
	
