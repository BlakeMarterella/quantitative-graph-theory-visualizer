'''         Step 1: Data Preparation        '''
# Load Data: Use Pandas to load your datasets into DataFrame objects.
import pandas as pd
data_files = ['AAPL.csv', 'GOOGL.csv', 'AMZN.csv', 'GOOGL.csv', 'JP-MORGN.csv', 'MSFOT.csv', 'TSLA.csv', 'VISA.csv', 'WL-MART.csv', 'NVDA.csv']
data_frames = {}

for file_name in data_files:
    df = pd.read_csv(f'../data/{file_name}')
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')  # Adjust format here
    df.ffill(inplace=True)  # Forward fill to handle missing values
    data_frames[file_name] = df

# Compute Correlations: Calculate the correlation between stock returns.
# Convert prices to returns
returns = {name: df['Close'].pct_change() for name, df in data_frames.items()}
returns_df = pd.DataFrame(returns)

# Compute correlation matrix
correlation_matrix = returns_df.corr()

'''         Step 2: Graph Construction      '''
import networkx as nx

threshold = 0.5  # Define your own threshold
G = nx.Graph()
for stock1 in correlation_matrix.columns:
    for stock2 in correlation_matrix.index:
        if stock1 != stock2 and correlation_matrix.loc[stock1, stock2] > threshold:
            G.add_edge(stock1, stock2, weight=correlation_matrix.loc[stock1, stock2])


'''         STEP 3: Applying Extremal Graph Theory          '''
# Analyze Graph Properties: Investigate properties like maximum degree, diameter, or other relevant metrics that can be derived from extremal graph theory.
print(correlation_matrix)
degree_sequence = dict(G.degree()).values()

if degree_sequence:
    max_degree = max(degree_sequence)
else:
    print('No edges found in the graph')
    
# max_degree = max(dict(G.degree()).values())
diameter = nx.diameter(G)
# Add more analyses as needed


'''         Step 4: Visualization       '''
import matplotlib.pyplot as plt
# Use your graph G from previous steps
pos = nx.spring_layout(G)  # Positions for all nodes

# Draw the graph (nodes and edges)
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=700, 
        edge_color='gray', linewidths=0.5,
        font_size=10)

# Prepare edge labels, truncated to 4 decimal places
edge_labels = {(u, v): f"{d['weight']:.4f}" for u, v, d in G.edges(data=True)}

# Draw edge labels
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

plt.axis('off')  # Turn off the axis
plt.show()  # Display the graph
