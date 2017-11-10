def main():

    '''
    This function uses data generated by the neighbors.py algorithim to
    add a neighbors column to the eurostat panel data.

    Returns panel, a df.
    '''

    import eurostat_data
    import pandas as pd

    panel = eurostat_data.main()

    '''
    Using neighbors.py algorithim by Ujaval Gandhi implemented by QGIS:
    http://www.qgistutorials.com/en/docs/find_neighbor_polygons.html

    To generate a csv which lists all regions that a given region borders by
    NUTS 2 region code.

    The 1st 2 elements of the NUTS 2 code gives the country (e.g. AT = Austria).

    Therefore, I can designate a region as being along a country border
    if it has a neighbor with a different country code.
    '''

    neighbors = pd.read_csv("neighbors.csv", usecols = [0, 4]).fillna(value="None")

    # pick neighbors to only include countries in the eurostat data
    neighbors = neighbors[neighbors["NUTS_ID"].isin(
                          list(panel["NUTS_ID"]))].reset_index(drop=True)

    # merge neighbors df into panel df
    panel = panel.merge(neighbors, how='outer', on="NUTS_ID")

    # list of country codes for countries that joined the EU in 2004
    '''
    Czech Republic: CZ
    Estonia: EE
    Hungary: HU
    Latvia: LV
    Lithuania: LT
    Malta: MT
    Poland: PL
    Slovakia: SK
    Slovenia: SI
    '''

    eurojoin_04 = ['CZ', 'EE', 'HU', 'LV', 'LT',
                   'MT', 'PL', 'SK', 'SI']

    # set a value of TRUE if a region borders a country which joined the EU in '04

    panel['neighbor_joined'] = [any([el in N for el in eurojoin_04])
                                for N in list(panel.NEIGHBORS)]
    return panel
