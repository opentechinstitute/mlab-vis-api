# -*- coding: utf-8 -*-
'''
Data class for accessing data for API calls.
'''
from mlab_api.data.base_data import Data
from mlab_api.constants import TABLE_KEYS
from mlab_api.data.table_config import get_table_config
from mlab_api.decorators import add_id
import mlab_api.data.data_utils as du
import mlab_api.data.bigtable_utils as bt
from mlab_api.stats import statsd

class LocationData(Data):
    '''
    Connect to BigTable and pull down data.
    '''

    def get_location_info(self, location_id):
        '''
        Get info about specific location
        '''

        table_config = get_table_config(self.table_configs,
                                        None,
                                        du.list_table('locations'))
        # add empty field to get child location in there
        location_key_fields = du.get_key_fields(["info", location_id], table_config)

        row_key = du.BIGTABLE_KEY_DELIM.join(location_key_fields)
        row = ""
        with statsd.timer('location.info.get_row'):
            row = bt.get_row(table_config, self.get_pool(), row_key)

        row["meta"]["id"] = location_id

        return row

    @add_id('parent_location_key')
    def get_location_children(self, location_id, type_filter=None):
        '''
        Return information about children regions of a location
        '''
        table_config = get_table_config(self.table_configs,
                                        None,
                                        du.list_table('locations'))
        location_key_fields = du.get_location_key_fields(location_id, table_config)

        location_key_field = du.BIGTABLE_KEY_DELIM.join(location_key_fields)

        results = []
        with statsd.timer('locations.children.scan_table'):
            results = bt.scan_table(table_config, self.get_pool(), prefix=location_key_field)
            if type_filter:
                results = [r for r in results if r['meta']['type'] == type_filter]

        return {"results": results}

    @add_id('client_asn_number')
    def get_location_clients(self, location_id, include_data):
        '''
        Get list and info of client isps for a location
        '''
        return self.get_list_data(location_id, 'locations', 'clients', include_data)


    @add_id('server_asn_number')
    def get_location_servers(self, location_id, include_data):
        '''
        Get list and info of server isps for a location
        '''
        return self.get_list_data(location_id, 'locations', 'servers', include_data)

    def get_location_client_isp_info(self, location_id, client_isp_id):
        '''
        Get static information about
        '''
        config_id = du.list_table('clients', 'locations')
        table_config = get_table_config(self.table_configs, None, config_id)

        key_fields = du.get_key_fields([location_id, client_isp_id], table_config)

        row_key = du.BIGTABLE_KEY_DELIM.join(key_fields)

        results = []
        with statsd.timer('locations.clientisps_info.scan_table'):
            results = bt.get_row(table_config, self.get_pool(), row_key)
        results["meta"]["id"] = client_isp_id
        return results

    def get_location_metrics(self, location_id, timebin, starttime, endtime):
        '''
        Get data for specific location at a specific
        frequency between start and stop times.
        '''

        table_config = get_table_config(self.table_configs, timebin, TABLE_KEYS["locations"])

        location_key_fields = du.get_location_key_fields(location_id, table_config)
        formatted = bt.get_time_metric_results(location_key_fields, self.get_pool(), timebin, starttime, endtime, table_config, "locations")

        # set the ID to be the location ID
        formatted["meta"]["id"] = location_id

        return formatted

    def get_location_client_metrics(self, location_id, client_id,
                                        timebin, starttime, endtime):
        '''
        Get data for specific location + client at a specific
        frequency between start and stop times for a
        specific client ISP.
        '''
        # Create Row Key
        agg_name = TABLE_KEYS["clients"] + '_' + TABLE_KEYS["locations"]

        table_config = get_table_config(self.table_configs, timebin, agg_name)

        key_fields = du.get_key_fields([client_id, location_id], table_config)
        formatted = bt.get_time_metric_results(key_fields, self.get_pool(), timebin, starttime, endtime, table_config, "locations_clients")

        # set the ID to be the Client ISP ID
        formatted["meta"]["id"] = "_".join([location_id, client_id])

        return formatted

    def get_location_server_metrics(self, location_id, server_id,
                                        timebin, starttime, endtime):
        '''
        Get data for specific location + server at a specific
        frequency between start and stop times for a
        specific client ISP.
        '''
        # Create Row Key
        agg_name = TABLE_KEYS["servers"] + '_' + TABLE_KEYS["locations"]

        table_config = get_table_config(self.table_configs, timebin, agg_name)

        # TODO: the direction of the keys don't match the table name
        key_fields = du.get_key_fields([location_id, server_id], table_config)
        formatted = bt.get_time_metric_results(key_fields, self.get_pool(), timebin, starttime, endtime, table_config, "locations_servers")

        # set the ID to be the Client ISP ID
        formatted["meta"]["id"] = "_".join([location_id, server_id])

        return formatted

    def get_location_client_server_metrics(self, location_id, client_id, server_id,
                                        timebin, starttime, endtime):
        '''
        Get data for specific location + client + server at a specific
        frequency between start and stop times for a
        specific client ISP.
        '''
        # Create Row Key
        agg_name = "{0}_{1}_{2}".format(TABLE_KEYS["servers"], TABLE_KEYS["clients"], TABLE_KEYS["locations"])

        table_config = get_table_config(self.table_configs, timebin, agg_name)

        key_fields = du.get_key_fields([location_id, client_id, server_id], table_config)
        formatted = bt.get_time_metric_results(key_fields, self.get_pool(), timebin, starttime, endtime, table_config, "locations_clients_servers")

        # set the ID to be the Client ISP ID
        formatted["meta"]["id"] = "_".join([location_id, client_id, server_id])

        return formatted
