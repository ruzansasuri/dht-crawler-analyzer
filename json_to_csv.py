import json
import sys
# import matplotlib as mat
# mat.use('cairo')
from matplotlib import pyplot as plt
import numpy as np

limit = sys.maxsize
markersize = 1
group_size = 1
# json_str = '{"id":"32f54e697351ff4aec29cdbaabf2fbe3467cc267","from":"7c8d34f02826589d26b1d65fd05bc0306c860cbb","query":"10813423cd59f3021a4c20e1f81a62f481489fdd","address":"67.215.246.10:6881","time_discovered":1542433756829,"metadata":{"ip":"67.215.246.10","hostname":"67.215.246.10.static.quadranet.com","type":"ipv4","continent_code":"NA","continent_name":"North America","country_code":"US","country_name":"United States","region_code":"CA","region_name":"California","city":"Los Angeles","zip":"90014","latitude":34.0494,"longitude":-118.2641,"location":{"geoname_id":5368361,"capital":"Washington D.C.","languages":[{"code":"en","name":"English","native":"English"}],"country_flag":"http://assets.ipstack.com/flags/us.svg","country_flag_emoji":"🇺🇸","country_flag_emoji_unicode":"U+1F1FA U+1F1F8","calling_code":"1","is_eu":false},"time_zone":{"id":"America/Los_Angeles","current_time":"2018-11-18T16:37:38-08:00","gmt_offset":-28800,"code":"PST","is_daylight_saving":false},"currency":{"code":"USD","name":"US Dollar","plural":"US dollars","symbol":"$","symbol_native":"$"},"connection":{"asn":8100,"isp":"QuadraNet Enterprises LLC"}}}'


def file_check(file, permission):
    """
    Creates a file handler.
    :param file: Name of the file
    :param permission: Permission
    :return: File handler
    """
    try:
        f = open(file, permission, encoding='utf-8')
        return f
    except FileNotFoundError:
        print("File", file, "does not exist...")
        exit()


def plot_by_isp(json_dicts):
    isp_dict = dict()
    for json_dict in json_dicts:
        isp = json_dict["metadata"]["connection"]["isp"]
        if isp is None:
            continue
        if isp not in isp_dict:
            isp_dict[isp] = 0
        isp_dict[isp] += 1
    print(isp_dict)
    draw_total_time_hist_sub(isp_dict, "Count by ISP")


def plot_by_continent(json_dicts):
    continent_dict = dict()
    for json_dict in json_dicts:
        cont = json_dict["metadata"]["continent_code"]
        if cont is None:
            continue
        if cont not in continent_dict:
            continent_dict[cont] = 0
        continent_dict[cont] += 1
    print(continent_dict)
    draw_total_time_hist_sub(continent_dict, "Count by continent")


def plot_by_region(json_dicts):
    region_dict = dict()
    for json_dict in json_dicts:
        country_code = json_dict["metadata"]["country_code"]
        region = json_dict["metadata"]["region_code"]
        if country_code != 'US' or region is None:
            continue
        if region not in region_dict:
            region_dict[region] = 0
        region_dict[region] += 1
    print(region_dict)
    draw_total_time_hist_sub(region_dict, "Count by regions in US")


def draw_total_time_hist_sub(y_dict, name, xticks=None, xlabel='x', ylabel='y', labels=None, explore_only=None):
    # min_y = int(min(min_max) - (min(min_max) % 10))
    # max_y = int(max(min_max) - (max(min_max) % 10) + 1)
    # f, a = plt.subplots()
    plt.title(name)
    plt.grid(zorder=0)
    width = 0.2
    # xs = [None]
    i = 0
    keys = list(y_dict.keys())
    vals = [y_dict[c] for c in keys]
    x = np.arange(len(keys))
    # for i in range(len(conts)):
        # print(x, x + (width * i))
    plt.bar(x, vals, align='center', alpha=0.5)
        # i += 1
    # y_ticks = [i for i in range(200, 400, 100)]
    # if explore_only is not None:
    #     for i in range(len(explore_only)):
    #         print('e', i, explore_only[i])
    #         bars.append(a.axhline(y=explore_only[i], color='grey', label='Explore Only'))
    #     y_ticks.append(explore_only[0])
    # if xticks is not None:
    plt.xticks(x, keys)
    # for t in a.get_xticklabels():
    #     t.set_rotation(0)
    # a.set_yticks(y_ticks)
    # a.text(0, explore_only[0], 'Explore Only')
    # a.set_yscale('log')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    # a.legend(labels)  # , 'upper right')
    plt.show()
    # return bars


def plot_maps(x, y):
    # x_list = []
    # y_list = []
    plt.figure("Map")
    plt.title('Map')

    for idx in range(len(x)):
        plt.plot(float(x[idx]), float(y[idx]), 'b^', markersize=markersize)
    # for point in data:
    #     # x_list.append(point[idx])
    #     # y_list.append(point[idx + 1])
    #     if point[idx] != '' and point[idx + 1] != '':
    #         matplot.plot(float(point[idx]), float(point[idx + 1]))
    plt.show()


def json_to_dict(json_str):
    return json.loads(json_str)


def file_to_json(file_name):
    file = file_check(file_name, 'r')
    json_dicts = []
    i=0
    for line in file:
        if i >= limit:
            break
        i += 1
        json_dicts.append(json_to_dict(line))
    # print(json_str)
    return json_dicts


def map_dicts(json_dicts):
    y = []
    x = []
    for json_dict in json_dicts:
        lat = json_dict['metadata']['latitude']
        lon = json_dict['metadata']['longitude']
        if lat is not None and lon is not None:
            y.append(lat)
            x.append(lon)
    return x, y


def create_heat_map(x, y):
    min_vals = [-90, -180]
    max_vals = [90, 180]
    map = [[0 for _ in range(min_vals[1], max_vals[1] + 1, group_size)]
           for _ in range(min_vals[0], max_vals[0] + 1, group_size)]
    print('size', len(map), len(map[0]))
    max_heat = 0
    for i in range(len(x)):
        int_x, int_y = int(x[i]), int(y[i])
        x_c, y_c = (int_x - min_vals[0]) // group_size, (int_y - min_vals[1]) // group_size
        # print('x, y', x_c, y_c)  # , map[x_c][y_c])
        map[x_c][y_c] += 1
        if map[x_c][y_c] > max_heat:
            max_heat = map[x_c][y_c]
    print('heat', max_heat)
    for i in range(len(map)):
        for j in range(len(map[i])):
            map[i][j] /= max_heat

    print(map)
    heat_map(np.array(map))


def heat_map(numpy_arr):
    print('Mapping')
    # a = np.random.random((16, 16))
    # print(numpy_arr)
    plt.figure('Heat Map', (300, 200))
    plt.xticks([i for i in range(-90, 90, group_size)])
    plt.yticks([i for i in range(-180, 180, group_size)])
    plt.imshow(numpy_arr, cmap='hot', interpolation='bicubic')
    plt.show()


def main():
    # a = np.random.random((16, 16))
    if len(sys.argv) < 2:
        print('Please enter the file name as a parameter.')
        return
    file_name = sys.argv[1]
    json_dicts = file_to_json(file_name)
    # json_dicts = json_to_dict(json_str)
    # print(json_dicts['metadata']['latitude'])
    # x, y = map_dicts(json_dicts)
    # print(x)
    # print(y)
    print('Plotting...')
    # plot_maps(x, y)
    # create_heat_map(y, x)
    # plot_by_continent(json_dicts)
    plot_by_region(json_dicts)
    # plot_by_isp(json_dicts)


if __name__ == '__main__':
    main()
