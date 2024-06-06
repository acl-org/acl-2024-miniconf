import markdown_to_json, re, json


base_dir = "../../../../acl-2024/_pages/"
REMOVETAGS = re.compile('<.*?>') 

def remove_html_tags(txt):
	txt = re.sub(REMOVETAGS, '', txt)
	return txt

def parse_tutorials(dump=True):
	fp = base_dir + "program/tutorials.md"
	with open(fp, 'r') as f:
		mdtxt = f.read().strip()

	mdtxt = re.sub(r'(?s)---.*?---', '', mdtxt)
	mdtxt = re.sub(r'(?s).*?<br><br>', '', mdtxt)

	tutorials = mdtxt.split("\n\n")
	tutorials = [t for t in tutorials if len(t) != 0]
	res = {}
	for i, tuto in enumerate(tutorials):
		tuto = remove_html_tags(tuto)
		lines = tuto.split("\n")
		title = lines[0].replace("**", "")
		chairs = [chair.strip() for chair in lines[1].split(", ")]
		abstract = lines[2].replace("* ", '')
		res[f"T{i+1}"] = {
			"anthology_url": None,
			"chairs": [],
			"description":abstract,
			"end_time": "2024-07-11T00:00:00+01:00",
			"id": f"T{i+1}",
			"link": None,
			"organizers": chairs,
			"paper_ids": [],
			"rocketchat_channel": f"tutorial-{i+1}",
			"room": None,
			"session": f"T{i+1}",
			"start_time": "2024-07-11T00:00:00+01:00",
			"title": title, 
			"track": "Tutorial",
			"tutorial_pdf": None,
			"type": "Tutorials"
		}
	
	if dump:
		with open('tutorials.json', 'w') as f: json.dump(res, f, indent=4)

	return res

def parse_workshops(dump=True):
	fp = base_dir + "program/workshops.md"
	with open(fp, 'r') as f:
		mdtxt = f.read().strip()

	mdtxt = re.sub(r'(?s)---.*?---', '', mdtxt)
	mdtxt = re.sub(r'(?s).*?<br>\n##', '##', mdtxt)

	workshops = mdtxt.split("\n\n")
	workshops = [w for w in workshops if len(w) != 0]
	res = {}
	date = None
	for i, workshop in enumerate(workshops):
		
		if workshop.strip().startswith('##'):
			date = workshop.replace('## ', '')
			continue

		workshop = remove_html_tags(workshop)
		lines = workshop.split("\n")
		if lines[0].startswith("[**"):
			description, workshop_site_url = lines[0].replace("[**", '').split("**](")
			workshop_site_url = workshop_site_url.replace(")", '')
		else:
			description = lines[0].replace("**", '').strip()
			workshop_site_url = ""
		location = lines[1].replace("Location :", '').strip()
		committee = []
		for member in lines[2:]:
			if ", " in member:
				infos = member.split(', ')
				name_mail, affiliation = infos[0], infos[1]
			else:
				name_mail, affiliation = member.strip(), None

			if "mailto" in name_mail:
				name, mail = name_mail.split("](mailto:")
				name = name.replace("* [", "")
				mail = mail.replace(")", '')
			else:
				name = name_mail.replace("* ", "")
				mail = None
			committee.append({
					"first_name": None,
					"full_name": name,
					"google_scholar": None,
					"last_name": None,
					"middle_name": None,
					"semantic_scholar": None,
					"affiliation": affiliation,
					"mail": mail
			})

		temp_id = "_".join(description.split(' '))
		
		res[temp_id] = {
			"anthology_venue_id": "",
			"booklet_id": "",
			"chairs": [],
			"committee": committee,
			"description": description,
			"end_time": None,
			"id": temp_id,
			"link": None,
			"paper_ids": [],
			"room": None,
			"session": temp_id,
			"short_name": temp_id,
			"start_time": None,
			"track": "Workshop",
			"type": "Workshops",
			"workshop_site_url": workshop_site_url,
			"location": location
		}

	if dump:
		with open("workshops.json", 'w') as f: json.dump(res, f, indent=4)

	return res

def generate_conference_json(dump=True):
	res = {"events":None, "papers": None, "plenaries": None, "sessions": None, "tutorials": None, "workshops": None}
	res["workshops"] = parse_workshops(dump=False)
	res["tutorials"] = parse_tutorials(dump=False)
	res["events"] = {"business-meeting_-computational-social-science-and-cultural-analytics-(poster)": {
            "chairs": [],
            "end_time": "2024-03-19T13:45:00+01:00",
            "id": "business-meeting_-computational-social-science-and-cultural-analytics-(poster)",
            "link": None,
            "paper_ids": [
                "5",
                "224",
                "340",
                "464"
            ],
            "room": "GatherTown",
            "session": "Business Meeting",
            "start_time": "2024-03-19T13:00:00+01:00",
            "track": "Computational Social Science and Cultural Analytics",
            "type": "Poster"
        }}
	res["papers"] = {"10": {
            "abstract": "",
            "anthology_url": None,
            "authors": [
                "Heejoon Koo"
            ],
            "category": "Poster",
            "demo_url": None,
            "display_track": "NLP Applications",
            "event_ids": [
                "session-11_-nlp-applications-(poster)",
                "session-9_-nlp-applications-(poster)"
            ],
            "id": "10",
            "is_paper": True,
            "keywords": [],
            "languages": [],
            "material": None,
            "paper_pdf": None,
            "paper_type": "Poster",
            "poster_pdf": None,
            "preview_image": None,
            "program": "Main",
            "similar_paper_ids": [],
            "slides_pdf": None,
            "title": "Next Visit Diagnosis Prediction via Medical Code-Centric Multimodal Contrastive EHR Modelling with Hierarchical Regularisation",
            "tldr": "",
            "track": "NLP Applications",
            "underline_id": None,
            "underline_url": None,
            "video_url": None
        }}
	res["plenaries"] = {}
	res["sessions"] = {}
	res["papers"] = {}

	if dump:
		with open("conference.json", "w") as f: json.dump(res, f, indent=4)
	
generate_conference_json()

