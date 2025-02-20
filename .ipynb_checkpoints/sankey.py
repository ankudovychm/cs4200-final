import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('data.csv')

df['decade'] = (df['year'] // 10) * 10

df['artists'] = df['artists'].apply(eval)  # Converts string list to actual list

# Explode the 'artists' column so each artist gets its own row
df_exploded = df.explode('artists')

# Count occurrences of each artist per decade
top_artists_per_decade = df_exploded.groupby(['decade', 'artists']).size().reset_index(name='count')

# Sort and keep only the top 10 artists per decade
top_artists_per_decade = top_artists_per_decade.sort_values(['decade', 'count'], ascending=[True, False])
top_artists_per_decade = top_artists_per_decade.groupby('decade').head(10)

# Create label mappings
unique_labels = list(top_artists_per_decade['decade'].unique()) + list(top_artists_per_decade['artists'].unique())
label_to_index = {label: i for i, label in enumerate(unique_labels)}

# Define Sankey sources, targets, and values
sources = top_artists_per_decade['decade'].map(label_to_index)
targets = top_artists_per_decade['artists'].map(label_to_index)
values = top_artists_per_decade['count']

# Create Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15, thickness=20, line=dict(color="black", width=0.5),
        label=unique_labels
    ),
    link=dict(source=sources, target=targets, value=values)
)])

fig.update_layout(title_text="Sankey Diagram of Top Artists by Releases per Decade", font_size=10)
fig.show()
