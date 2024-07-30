try:
    from IMPORT import dash
    from dash import dcc, html, Input, Output, State
    from IMPORT import go
    # local files
    from calculations import Client
except ImportError:
    pass

# app text
app = dash.Dash(__name__)
server = app.server

client = Client('Example Client')

app.layout = html.Div([
    html.H1('Tax Calculation Interactive Dashboard'),

    html.Div([
        dcc.Slider(
            id='other-uk-income-slider',
            min=0,
            max=1000000,
            step=1000,
            value=0,
            marks={i: f'{i//1000}k' for i in range(0, 1000001, 100000)}
        ),
        dcc.Input(
            id='other-uk-income-input',
            type='number',
            value=0,
            min=0,
            max=1000000,
            step=1000,
            style={'margin-left': '20px'}
        ),
    ], style={'margin-top': 20}),
    html.Div(id='other-uk-income-output', style={'margin-top': 20}),

    html.Div([
        dcc.Slider(
            id='profit-on-sales-slider',
            min=0,
            max=1000000,
            step=1000,
            value=0,
            marks={i: f'{i//1000}k' for i in range(0, 1000001, 100000)}
        ),
        dcc.Input(
            id='profit-on-sales-input',
            type='number',
            value=0,
            min=0,
            max=1000000,
            step=1000,
            style={'margin-left': '20px'}
        ),
    ], style={'margin-top': 20}),
    html.Div(id='profit-on-sales-output', style={'margin-top': 20}),

    dcc.Graph(id='tax-bar-chart')
])

@app.callback(
    [Output('other-uk-income-slider', 'value'),
     Output('other-uk-income-input', 'value')],
    [Input('other-uk-income-slider', 'value'),
     Input('other-uk-income-input', 'value')]
)
def sync_other_uk_income(slider_value, input_value):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'other-uk-income-slider':
        # Slider triggered
        return slider_value, slider_value
    elif trigger_id == 'other-uk-income-input':
        # Input triggered
        return input_value, input_value

@app.callback(
    [Output('profit-on-sales-slider', 'value'),
     Output('profit-on-sales-input', 'value')],
    [Input('profit-on-sales-slider', 'value'),
     Input('profit-on-sales-input', 'value')]
)
def sync_profit_on_sales(slider_value, input_value):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'profit-on-sales-slider':
        # Slider triggered
        return slider_value, slider_value
    elif trigger_id == 'profit-on-sales-input':
        # Input triggered
        return input_value, input_value

@app.callback(
    [Output('other-uk-income-output', 'children'),
     Output('profit-on-sales-output', 'children'),
     Output('tax-bar-chart', 'figure')],
    [Input('other-uk-income-slider', 'value'),
     Input('profit-on-sales-slider', 'value'),
     Input('other-uk-income-input', 'value'),
     Input('profit-on-sales-input', 'value')]
)
def update_chart(other_uk_income_slider, profit_on_sales_slider, other_uk_income_input, profit_on_sales_input):
    other_uk_income = other_uk_income_input if other_uk_income_input is not None else other_uk_income_slider
    profit_on_sales = profit_on_sales_input if profit_on_sales_input is not None else profit_on_sales_slider

    client.OtherUkIncome.set(other_uk_income)
    client.ProfitOnSales.set(profit_on_sales)

    # Check for None data and Set Defaults
    if client.OtherUkIncome.value is None:
        client.OtherUkIncome.set(default_MoneyInputValue)
    if client.ProfitOnSales.value is None:
        client.ProfitOnSales.set(default_MoneyInputValue)

    client.DividendsTax.calculate()
    client.AssetsSalesTax.calculate()

    dividends_data = [
        client.DividendsTax.PersonalAllowance.personal_allowance_tax_due,
        client.DividendsTax.BasicRate.basic_rate_tax_due,
        client.DividendsTax.HigherRate.higher_rate_tax_due,
        client.DividendsTax.AdditionalRate.additional_rate_tax_due
    ]

    assets_sales_data = [
        client.AssetsSalesTax.PersonalAllowance.personal_allowance_tax_due,
        client.AssetsSalesTax.BasicRate.basic_rate_tax_due,
        client.AssetsSalesTax.HigherRate.higher_rate_tax_due,
        client.AssetsSalesTax.AdditionalRate.additional_rate_tax_due
    ]

    less_tax_paid_at_source = client.DividendsTax.dividends_tax_due_total

    # Calculate the total tax due for Dividends and Assets Sales
    total_dividends_due = sum(dividends_data)
    total_assets_sales_due = sum(assets_sales_data)

    bars = [
        go.Bar(
            name='Personal Allowance',
            x=['Dividends', 'Assets Sales'],
            y=[dividends_data[0], assets_sales_data[0]],
            hovertemplate='Personal Allowance: %{y:.2f}<extra></extra>'
        ),
        go.Bar(
            name='Basic Rate',
            x=['Dividends', 'Assets Sales'],
            y=[dividends_data[1], assets_sales_data[1]],
            hovertemplate='Basic Rate: %{y:.2f}<extra></extra>'
        ),
        go.Bar(
            name='Higher Rate',
            x=['Dividends', 'Assets Sales'],
            y=[dividends_data[2], assets_sales_data[2]],
            hovertemplate='Higher Rate: %{y:.2f}<extra></extra>'
        ),
        go.Bar(
            name='Additional Rate',
            x=['Dividends', 'Assets Sales'],
            y=[dividends_data[3], assets_sales_data[3]],
            hovertemplate='Additional Rate: %{y:.2f}<extra></extra>'
        ),
        go.Bar(
            name='Less Tax Paid at Source',
            x=['Dividends (After Less)'],
            y=[less_tax_paid_at_source],
            hovertemplate='Less Tax Paid at Source: %{y:.2f}<extra></extra>',
            marker_color='rgba(255, 99, 71, 0.6)'
        )
    ]

    annotations = []

    # Add annotations for non-zero values
    for i, (d, a) in enumerate(zip(dividends_data, assets_sales_data)):
        if d > 0:
            annotations.append(
                dict(
                    x='Dividends',
                    y=sum(dividends_data[:i]) + (d / 2),
                    text=f'${d:.2f}',
                    showarrow=False,
                    font=dict(color='white')
                )
            )
        if a > 0:
            annotations.append(
                dict(
                    x='Assets Sales',
                    y=sum(assets_sales_data[:i]) + (a / 2),
                    text=f'${a:.2f}',
                    showarrow=False,
                    font=dict(color='white')
                ))

    if less_tax_paid_at_source > 0:
        annotations.append(
            dict(
                x='Dividends (After Less)',
                y=less_tax_paid_at_source / 2,
                text=f'${less_tax_paid_at_source:.2f}',
                showarrow=False,
                font=dict(color='white')
            )
        )

    # Add annotations for the total values
    annotations.extend([
        dict(
            x='Dividends',
            y=0,
            text=f'Total: ${total_dividends_due:.2f}',
            showarrow=False,
            font=dict(color='black'),
            yshift=-20
        ),
        dict(
            x='Assets Sales',
            y=0,
            text=f'Total: ${total_assets_sales_due:.2f}',
            showarrow=False,
            font=dict(color='black'),
            yshift=-20
        ),
        dict(
            x='Dividends (After Less)',
            y=0,
            text=f'Total: ${less_tax_paid_at_source:.2f}',
            showarrow=False,
            font=dict(color='black'),
            yshift=-20
        )
    ])

    figure = go.Figure(data=bars)
    figure.update_layout(
        barmode='stack',
        title='Tax Breakdown',
        yaxis_title='Amount ($USD)',
        annotations=annotations
    )

    return (f'Other UK Income: ${other_uk_income}',
            f'Profit on Sales: ${profit_on_sales}',
            figure)

if __name__ == '__main__':
    app.run_server(debug=True)
