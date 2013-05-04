{
	'lat': {{ lat }},
	'lng': {{ lng }},
	'name': {{ name }},
	'timestamp': {{ timestamp }},
	'country': {{ country }},
	'stateprov': {{ stateprov }},
	'city': {{ city }}
	% if photo:
	,'photo': {{ photo }}
	% end
}
