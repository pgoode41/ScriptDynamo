import sys
import os
from git import Repo
import codecs
import shutil
import requests
import json
import stat
import subprocess
from pprint import pprint
from shutil import copyfileobj

###############################################################################################
###############################################################################################

url = "https://swapi.co/api/people"
response = requests.request("GET", url)
json = response.json()
json_results = json['results']
json_attributes = json_results[0]
json_names = json_attributes['name']

#pprint(json_names)

###############################################################################################
#Edit Here to integreate with another Synology server.
###############################################################################################



ScriptMakerPath = "/opt/ScriptDynamo"
MergeTemplates = ScriptMakerPath+"/MergeTemplates"
header_filepath = ScriptMakerPath+"/Headers/"
merge_path = ScriptMakerPath+"/Merged"

if not os.path.exists(ScriptMakerPath):
	#os.makedirs(ScriptMakerPath+"/ScriptBuilder")
	os.makedirs(ScriptMakerPath+"/Headers/")
	os.makedirs(ScriptMakerPath+"/Merged")
	#os.makedirs(ScriptMakerPath+"/TEMPLATES")

if os.path.exists(MergeTemplates):
	shutil.rmtree(MergeTemplates)

Repo.clone_from("https://github.com/pgoode41/bashTemplates.git", MergeTemplates)

bashTemplatesRepo = ScriptMakerPath+"/MergeTemplates/Templates"


###############################################################################################
###############################################################################################

for names in json_results:
	name_list = names
	#May have to change 'name' to something else, depending on the JSON source!!!
	company_info = names['name']
	logname = company_info.title().strip().replace(" ", "")
	log_path = "/Volumes/TS_Funstick/Logs/Enrollment_Logs/" + logname + "/LER_" + logname + ".txt"
	watchman_group_name = company_info.strip().title()
	password = "SYS" + company_info.strip().replace(" ", "").lower() + "admiN"
	namesync = company_info.title().strip().replace(" ", "")
	for file in os.listdir(bashTemplatesRepo):
		filename = file.replace(".sh", "")
		os.chdir(header_filepath)
		sys.stdout = open(namesync+"_"+filename+"_header"+".sh","w+")
		print("#!/bin/bash")
		print("##########################################################################################################################################")
		print("#This is a generated script header designed to pull data from a database or API and generate dynamic scripts.")
		print("#This scripts merges this generated header to bash script templates")
		print("#Variables are generated from ScriptDynamo and stored in the header file (Almost like an ENV var but only accessable in the script)")
		print("#######################################################################################################################################")
		print("\n")
		print("#######################################################################################################################################")
		print("#######################################################################################################################################")
		print("#This pulls data gatherd from python variable generator script.")
		print("#After this section is configured, the script can use those values as variables in the script.")
		print("\n")
		print("\n")
		print("password="+"'"+password+"'")
		print("watchmangroup="+"'"+watchman_group_name+"'")
		print("namesync="+"'"+namesync+"'")
		print("\n")
		print("#######################################################################################################################################")
		print("#######################################################################################################################################")
		print("\n")
		print("\n")
		header_origin = header_filepath+namesync+"_"+filename+"_header.sh"
		target = merge_path+"/"+namesync+"_"+filename+".sh"
		#for filename in os.listdir(bashTemplatesRepo):
		body = bashTemplatesRepo+"/"+filename+".sh"
		os.chdir(merge_path)
		sys.stdout = open(namesync+"_"+filename+".sh","w+")
		with open(target, 'w+') as header_output, open(header_origin, 'r') as header_input, open(body, 'r') as body_input:
			copyfileobj(header_input, header_output)
			copyfileobj(body_input, header_output)
