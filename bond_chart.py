import random
import plotly.graph_objects as go
from bond_calculator import bond_calc as bc

# generating random colours
def random_colour():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def plot_graph(bond: bc):
    # random colour for each coupon so I can stack the reinvested amount on top of principal so scatter and bar chart meet at break even rate
    colours = [random_colour() for year in bond.years_list]
    # random colour except first and last bar which will be the bond price and principal and we want them to be the same colour
    colours.insert(0, "blue")
    colours[-1] = "blue"
    # the actual graph
    fig = go.Figure()
    # bond bars
    fig.add_trace(go.Bar(x=[0] + bond.years_list, y=bond.bar_y, marker_color=colours, name="Bond"))
    # total value of coupons reinvested stakced on top of principal so scatter and bar chart meet at break even value
    fig.add_trace(go.Bar(x=[bond.years_list[-1]] * len(bond.reinvested_y), y=bond.reinvested_y, name="Reinvested Coupons", marker_color=colours[1:-1], hovertemplate="Coupon accumulation: £%{y:.2f}<extra></extra>"))
    # bank investment line
    fig.add_trace(go.Scatter(x=[0] + bond.years_list, y=bond.scatter_y, mode="lines+markers", name="Bank", line=dict(color="black", width=3)))
    fig.update_xaxes(title_text = "Year")
    fig.update_yaxes(title_text="Amount/£")
    # Stack reinvested coupons on top of principal.
    # # The bank investment line is added last so it appears over the bond bars.
    fig.update_layout(barmode="relative")
    # to render the final graph
    return fig
    


        
    
    
    