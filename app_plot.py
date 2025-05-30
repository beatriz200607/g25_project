
from flask import render_template, session
import pandas as pd
import plotly.express as px

def apps_plotly_monthly():
    df = pd.read_csv("trabalho.csv")


    df = df[df['order_date'].notna() & df['quantity'].notna() & df['price'].notna()]


    df['order_date'] = pd.to_datetime(df['order_date'])
    df['total_revenue'] = df['quantity'] * df['price']
    df['month'] = df['order_date'].dt.strftime('%B')


    monthly_revenue = df.groupby('month')['total_revenue'].sum().reset_index()


    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly_revenue['month'] = pd.Categorical(monthly_revenue['month'], categories=month_order, ordered=True)
    monthly_revenue = monthly_revenue.sort_values('month')


    fig = px.line(monthly_revenue, x='month', y='total_revenue', markers=True,
                  title='Faturamento por Mês (Interativo)',
                  labels={'month': 'Mês', 'total_revenue': 'Receita Total'})

    plot_div = fig.to_html(full_html=False, div_id='monthly-plot')

    return render_template('plotly.html', plot_div=plot_div, ulogin=session.get("user"))
