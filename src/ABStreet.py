import json
import requests
import http

class ABStreet():
    '''
    ABStreet simulation wrapper. Initialized on a per-map basis, can be reused for
    changes to map edits. Edits can be provided upon construction 
    '''
    def __init__(self, api, map_args=None, mods=None, edits=None, verbose=False):
        if map_args is None:
            map_args = {
                'country_code': 'us',
                'city_name':    'seattle',
                'map_name':     'montlake',
            }

        self.api = api
        self.map_args = map_args
        self.verbose = verbose
        self.modifiers = mods if mods else []
        self.core_edits = edits
        self.edits = edits

        self.scenario = 'data/system/{}/{}/scenarios/{}/weekday.bin'.format(
            map_args['country_code'],
            map_args['city_name'],
            map_args['map_name'],
        )

        self.load()

    def reset(self, flush_edits=True):
        '''
        Note: edits explicitly loaded during scenario config will be reapplied by the AB
        street after reset i.e. will be reset to initial state as seen in constructor.
        '''
        if flush_edits:
            self.edits = self.core_edits

        requests.get(self.api + '/sim/reset')
        self.load()

    def load(self):
        # load sim configuration
        requests.post(self.api + '/sim/load', json={
            'scenario':  self.scenario,
            'modifiers': self.modifiers,
            'edits':     self.edits,
        })

    def run(self, hours):
        '''
        Runs the configured scenario, using current edits. Both live and retroactive edits
        made during prior runs will be applied.

        Note: even if a simulation has not started, edits to road or intersection geometry
        require a scenario reload. Live edits (like traffic signal changes) are fine to
        apply and run without a reset. Either way, reset is called and all changes are
        carried over to take effect following the call to run().

        Note: still need to implement persisting live edits and merging with static edits.
        Could always reset and set edits to current edits + explicitly saved edits
        '''
        # reset with current edits
        #self.reset(flush_edits=False)

        requests.post(self.api + '/sim/goto-time', params={
            't': '{}:00:00'.format(hours)
        })

    def data(self):
        finished_trips = requests.get(self.api + '/data/get-finished-trips').json()
        road_thruput   = requests.get(self.api + '/data/get-road-thruput').json()

        trips = {}
        for trip in finished_trips:
            if trip['duration'] is not None and trip.get('id'):
                trips[trip['id']] = trip['duration']

        # get total thruput by agent type
        thruput = {}
        for road in road_thruput['counts']:
            if road[1] not in thruput: thruput[road[1]] = 0
            thruput[road[1]] += road[3]

        return {
            'num_completed_trips': len(trips),
            'avg_trip_duration': sum([d for d in trips.values()])/len(trips),
            'thruput_by_agent': thruput,
        }

    def get_map_edits(self):
        '''
        Returns current map edits. Useful for getting proper edits in change
        signal timing, which are necessarily applied live. Road and
        intersection edits must be added retroactively during a reset.
        '''
        return requests.get(self.api + '/map/get-edits').json()

    def get_traffic_signal_stages(self, sid):
        return requests.get(self.api + '/traffic-signals/get', params={'id': sid}).json()

    def set_traffic_signal_stages(self, sid, stage_timing):
        '''
        Traffic signals can have two stage types: fixed or variable. 

        - Fixed stage: `timing` is single numerical value (seconds), stage always lasts that
          fixed amount of time
        - Variable stage: `timing` is a list with 3 numerical values

        Takes a dictionary indexed by stage ID. Values for each ID are dictionaries with
        'stage_type' and 'timing' keys. For example, given an intersection with 4 stages,
        the input
        
        stage_timing = {
            '1': { 'Fixed': 30000 },
            '3': { 'Variable': [10000, 2000, 8000] },
        }

        will change the 2nd and 4th stages to fixed (30s) wait time and variable (with 10s min
        wait, 2s protected turn check wait for +8s max), respectively.
        '''
        ts = self.get_traffic_signal_stages(sid)

        for stage, settings in stage_timing.items():
            ts['stages'][stage]['stage_type'] = settings

        # apply live
        try:
            r = requests.post(self.api + '/traffic-signals/set', json=ts)
            return r.status_code
        except requests.exceptions.ConnectionError:
            print('Invalid traffic signal setting (likely too little time for crosswalk. Restart the ABStreet server')
            return -1

    def save_edits(self, out):
        with open(out, 'w') as f:
            json.dump(self.get_map_edits(), f)