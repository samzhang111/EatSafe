# EatSafe API 

This is an API endpoint for the [food inspection data](https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5) in the City of Chicago.

It is live at http://api.eatsafechicago.com/

/near?lat={lat}&long={long}&radius={meters}&max={number\_of\_restaurants}

Default: radius=5000.0, max=20

----

/place?id={restaurant\_id}

----

/instant?query={query}&lat={lat}&long={long}

----

Default: lat=41.903196, long=-87.625916

/inspection?id={inspection\_id}


