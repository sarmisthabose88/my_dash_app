import dash
from dash import html
from dash import dash_table as dt
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import requests
import pandas as pd
import json



app = dash.Dash(__name__, external_stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css"])
server = app.server
app.layout = html.Div([
    html.H1("Government Spending Data Project"),
    html.P("This table shows the budget of the government agencies indexed by USASpending.gov"),
    html.Button('Fetch Data', id='get_data'),
    html.P(" "),
    html.Div(id='data_table1')
])

@app.callback(
    Output(component_id='data_table1', component_property='children'),
    [Input(component_id='get_data', component_property='n_clicks')]
)
def update_output(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        response = requests.get("https://api.usaspending.gov/api/v2/references/toptier_agencies/")
        df = convert_to_df(response.text)
        data = df.to_dict('records')
        columns =  [{"name": i, "id": i,} for i in (df.columns)]
        return dt.DataTable(data=data, columns=columns,sort_action="native")
def convert_to_df(resp_text):
    data = json.loads(resp_text)
    df = pd.json_normalize(data, record_path =['results'])
    return df
if __name__ == '__main__':
    app.run_server(debug=True)
