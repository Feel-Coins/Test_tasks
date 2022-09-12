import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def preparing_tz():
    # open dataframe
    df = pd.read_excel(io='test_task.xlsx')

    # drop the 'good' column
    df.drop(['good (1)'], axis=1, inplace=True)

    # making color column and add a colorname depending on cluster
    conditions = [
        (df['cluster'] == 0.0),
        (df['cluster'] == 1.0),
        (df['cluster'] == 2.0),
        (df['cluster'] == 3.0)]
    choices = ['red', 'yellow', 'green', 'purple']

    df['color'] = np.select(conditions, choices)

    # drop duplicates
    df = df.drop_duplicates(subset=['area', 'keyword'])

    # sorting
    df = df.sort_values(by=['area', 'cluster', 'cluster_name', 'count'], ascending=[True, True, True, False])

    # delete empty/incorrect row
    df['y'] = pd.to_numeric(df['y'], errors='coerce')
    df = df.dropna()

    # write dataframe to excel file
    df.to_excel("test_task_output.xlsx")


def scatter_plotting():
    # open the dataframe
    df = pd.read_excel(io='test_task_output.xlsx', index_col=False)
    df.drop(['Unnamed: 0'], axis=1, inplace=True)

    # split df to areas
    area_lst = []
    for zone in df.area.unique():
        area_lst.append(zone)

    # split areas to clusters
    cluster_lst = []
    for clust in df.cluster_name.unique():
        cluster_lst.append(clust)

    # for each area making the table
    for i in range(len(area_lst)):
        iter_areas = df[df['area'] == area_lst[i]]
        plt.figure(figsize=(16, 10))

        x = list(iter_areas.x)
        y = list(iter_areas.y)
        keywords = list(iter_areas.keyword)

        # Build the scatter for area[i] and colore dots depending on cluster_name
        for j in iter_areas.cluster.unique():
            plt.scatter(iter_areas[iter_areas.cluster == j].x, iter_areas[iter_areas.cluster == j].y,
                        color=iter_areas.color[iter_areas.cluster == j], label=iter_areas.cluster_name.unique()[j],
                        s=40, marker='o', linewidths=1, edgecolors='black')

        # Naming the dots by keyword
        for k in range(len(keywords)):
            if len(keywords[k]) >= 15:
                pretty_keyword = keywords[k].replace(' ', '\n')
            plt.annotate(pretty_keyword, xy=(x[k] + 0.2, y[k] + 0.2), fontsize=8)

        title = f'Graph of {area_lst[i]} area'
        if '\\' in title:
            title = title.replace('\\', '-')

        plt.title(title, {'fontsize': 10})
        plt.xlabel('X coordinates')
        plt.ylabel('Y coordinates')
        plt.legend(loc=0, bbox_to_anchor=(-0.53, -0.3, 0.5, 0.5))
        # plt.show()
        plt.savefig(f'{title}.png', format='png', dpi=150)
        plt.close()


# call functions
if __name__ == '__main__':
    preparing_tz()
    scatter_plotting()
