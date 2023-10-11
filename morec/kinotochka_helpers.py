import json


def embed_values(data):
    values_list = []

    try:
        for i in data:
            values_list.extend(i)

    except TypeError:
        values_list = data.tolist()

    return set(values_list)


def data_metrics(
        data=None,
        mode='count',
        columns=None
):
    if columns is None:
        columns = [
            'user',
            'movie_id',
            'genres',
            'actors',
            'favorited_genres',
            'directors',
            'countries'
        ]
    if mode == 'count' or mode == 'dump' or mode == 'write':
        mins = {}
        maxs = {}
        ns = {}
        lens = {}
        for i in columns:
            mins[i] = min(embed_values(data[i]))
            maxs[i] = max(embed_values(data[i]))
            ns[i] = len(embed_values(data[i]))
            try:
                lens[i] = int(data[i].apply(len).max())
            except TypeError:
                pass

        count = {'min': mins, 'max': maxs, 'n': ns, 'len': lens}

        if mode == 'dump' or mode == 'write':
            with open('analytics/model/data_metrics.json', 'w') as f:
                json.dump(count, f)

        else:
            return count

    elif mode == 'read' or mode == 'load':
        with open('analytics/model/data_metrics.json', 'r') as f:
            loaded_data = json.load(f)

        return loaded_data

    else:
        pass

