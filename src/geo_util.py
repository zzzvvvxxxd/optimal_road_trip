#! /usr/bin/env python2.7
# coding=utf-8
__author__ = 'bulu_dog'

import googlemaps
from itertools import combinations
from way_points import all_waypoints
waypoint_distances = {}
waypoint_durations = {}

gmaps = googlemaps.Client(key="AIzaSyBsfqWcyiILUbBQ8rhnTsGJu-QnbdFPiEE")

for (waypoint1, waypoint2) in combinations(all_waypoints, 2):
    try:
        route = gmaps.distance_matrix(origins=[waypoint1],
                                      destinations=[waypoint2],
                                      mode='driving',    #bicycling or walking or driving or transit
                                      language="English",
                                      units="metric"     #or imperial
                                      )
        #print route
        #距离的单位是meter
        distance = route["rows"][0]["elements"][0]["distance"]["value"]
        #时间的单位为s
        duration = route["rows"][0]["elements"][0]["duration"]["value"]

        waypoint_distances[frozenset([waypoint1, waypoint2])] = distance
        waypoint_durations[frozenset([waypoint1, waypoint2])] = duration
    except Exception as ex:
        print ("Error with finding the route between %s and %s.") % (waypoint1, waypoint2)

#将结果写入文件，避免反复调用API
with open("../data/my-waypoints-dist-dur.tsv","wb") as out_file:
    out_file.write("\t".join(["waypoint1",
                              "waypoint2",
                              "distance_m",
                              "duration_s"]))
    for (waypoint1, waypoint2) in waypoint_distances.keys():
        out_file.write("\n" + "\t".join([waypoint1, waypoint2,
                                        str(waypoint_distances[frozenset([waypoint1, waypoint2])]),
                                        str(waypoint_durations[frozenset([waypoint1, waypoint2])])]))

