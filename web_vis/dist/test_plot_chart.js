// pie chart example
var pie_data = [
    {name: 'A', y: 10},
    {name: 'B', y: 30},
    {name: 'C', y: 50},
    {name: 'D', y: 10},
]
plot_pie_chart('pie_chart', pie_data)

// bar chart example
var categories = ['0~5', '5~10', '10~15', '15~20', '20~25']
var income = [300000, 400000, 500000, 300000, 200000]
plot_bar_chart('bar_chart', categories, income)

