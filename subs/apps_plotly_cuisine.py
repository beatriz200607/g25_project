import pandas as pd
import plotly.express as px
from flask import render_template, session

def apps_plotly_cuisine():
    # Lê os dados exportados do CSV
    df = pd.read_csv('data/trabalho.csv')
    df = df.dropna(subset=['quantity', 'price', 'cuisine'])
    df['total_revenue'] = df['quantity'] * df['price']

    # Agrupa por cozinha
    cuisine_data = (
        df.groupby('cuisine')
          .agg(quantity=('quantity','sum'), total_revenue=('total_revenue','sum'))
          .reset_index()
    )

    # Cria gráfico interativo com Plotly
    fig = px.scatter(
        cuisine_data,
        x='quantity', y='total_revenue',
        size='total_revenue', color='cuisine',
        hover_name='cuisine',
        title='Quantidade vs Receita por Cozinha',
        labels={'quantity': 'Quantidade Vendida', 'total_revenue': 'Receita Total'}
    )

    plot_div = fig.to_html(full_html=False, div_id='cuisine-plot')

    return render_template(
        'plot.html',
        plot_div=plot_div,
        ulogin=session.get('user')
    )
