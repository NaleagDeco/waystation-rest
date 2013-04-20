[
	% if sightings:
		% include sighting sightings[0].to_dict()
		% for sighting in sightings[1:]:
,
			% include sighting sighting.to_dict()	
		% end
	% end
]
