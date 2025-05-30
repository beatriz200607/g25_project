from flask import render_template, session
import pandas as pd
import plotly.express as px

def apps_plotly_cuisine():
    df = pd.read_csv("trabalho.csv")


    df = df[df['order_date'].notna() & df['quantity'].notna() & df['price'].notna() & df['cuisine'].notna()]


    df['order_date'] = pd.to_datetime(df['order_date'])
    df['total_revenue'] = df['quantity'] * df['price']


    cuisine_data = df.groupby('cuisine').agg({
        'quantity': 'sum',
        'total_revenue': 'sum'
    }).reset_index()


    fig = px.scatter(
        cuisine_data,
        x='quantity',
        y='total_revenue',
        size='total_revenue',
        color='cuisine',
        hover_name='cuisine',
        title='Quantidade vs Receita por Cozinha',
        labels={'quantity': 'Quantidade Vendida', 'total_revenue': 'Receita Total'}
    )


    plot_div = fig.to_html(full_html=False, div_id='cuisine-plot')

    return render_template('plotly.html', plot_div=plot_div, ulogin=session.get("user"))
