import csv
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

# file
file = 'abbot_tags.csv'

df = pd.read_csv(file)

# Ensure kaleido is available
pio.renderers.default = 'notebook'

# Sankey Diagram
labels = []
source = []
target = []
value = []

# Add objectives
objectives = df['objective'].unique()
for objective in objectives:
    if objective not in labels:
        labels.append(objective)
    obj_index = labels.index(objective)
    themes = df[df['objective'] == objective]['theme'].unique()
    
    for theme in themes:
        if theme not in labels:
            labels.append(theme)
        theme_index = labels.index(theme)
        source.append(obj_index)
        target.append(theme_index)
        value.append(len(df[(df['objective'] == objective) & (df['theme'] == theme)]))
        
        all_tags = df[(df['objective'] == objective) & (df['theme'] == theme)]['tags'].unique()
        
        for tags in all_tags:
            if tags not in labels:
                labels.append(tags)
            tag_index = labels.index(tags)
            source.append(theme_index)
            target.append(tag_index)
            value.append(len(df[(df['objective'] == objective) & (df['theme'] == theme) & (df['tags'] == tags)]))

# Create Sankey diagram
fig_sankey = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels
    ),
    link=dict(
        source=source,
        target=target,
        value=value
    )
))

fig_sankey.update_layout(title_text="Objectives, Themes, and Tags Hierarchical Flow", font_size=10)
fig_sankey.write_html('sankey_diagram.html')

# Prepare data for treemap
cleaned_df = df.dropna(subset=['objective', 'theme', 'tags'])
treemap_data = cleaned_df[['objective', 'theme', 'tags']].drop_duplicates()
treemap_data['Count'] = treemap_data.groupby(['objective', 'theme', 'tags']).size().reset_index(name='Count')['Count']

# Create the treemap
fig_treemap = px.treemap(treemap_data, 
                 path=['objective', 'theme', 'tags'], 
                 values='Count',
                 title='Treemap of Objectives, Themes, and Tags')

# Save Treemap as PNG and HTML
fig_treemap.write_html("abbott_treemap.html")
