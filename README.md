# Amazon-Project-3
**All internal Amazon confidential information has been removed from the code. The code only contains publicly available information

Summary: rate_tracker.py collects & calculates 17 different metrics & outputs the data in an excel file, which is saved on the computer

Problem: Amazon delivery station has many different indepedent delivery companies. Each delivery company has 30+ drivers working to deliver Amazon packages. Some drivers are fast & finish delivering their route way before their 10 hour shift. Other drivers are 'slow' & end up bringing back a lot of packages due to their pace. 
Amazon website shows all the drivers who are 'behind' & 'at risk' of being behind, but it does not provide actionable metrics. 

For example, information about a driver's delivery rate, how many stops a driver will deliver or not deliver based on how much time they have left in their shift & their delivery rate. How much actual delivery time they have left by subtracting planned end time from current time and subtracting the travel time from last stop to delivery station.

Solution: This python script opens up amazon website & loops through all the drivers who are behind & at risk. It then finds out first delivery time, latest delivery time, stops delivered, stops remaining, shift planned end time, time remaining in shift, travel time from last stop to delivery station

The following metrics are calculated from implementing GOOGLE MAPS API: DistanceFrmLastStopToStation, TravelTimeFrmLastStopToStation 

GOOGLE MAPS API takes origin & destination addresses as input. Destination address is the delivery station address which never changes. Origin address is different for each driver and it is the last stop/delivery address.

Once we loop through all drivers, the 17 metrics are stored in a PANDAS dataframe, which is exported to an excel file

17 different metrics extracted/calculated: RouteCode, Company Name, totalStops,StopsDelivered,Stopsremaining, FirstDeliveryTime, LatestDeliveryTime, TimeSpentDelivering_From_1st_Delivery, PlannedEndTime, TimeRemainingInShift,TimeRemainingInShift_MINUS_TRAVEL_TIME_TO_STATION, DistanceFrmLastStopToStation, TravelTimeFrmLastStopToStation, LastDeliveryAddress, Delivery rate- Stops/hr, StopsPredictedToDeliver, StopsPredictedToNotDeliver

