#!/usr/bin/env python3
import argparse
import json
import subprocess as sp
import sys
import os.path
import re
import datetime

DATA_FILE = 'zoomlaunch.json'


# get meetings from json file
def get_meetings():
	if os.path.isfile(DATA_FILE):
		with open(DATA_FILE, 'r') as file:
			try:
				meetings = json.load(file)
			except json.JSONDecodeError:
				error(f'\'{DATA_FILE}\' is not a valid JSON file.')
		return meetings
	else:
		return []


def list_meetings():
	meetings = get_meetings()
	width = len(str(len(meetings) + 1))
	for index, meeting in enumerate(meetings):
		out_str = ('{:>' + str(width + 2) + '}').format(f'[{index + 1}]') # index of this entry
		out_str += '  ' + format_meeting_id(meeting["id"], True)
		out_str += '  ' + meeting["name"]
		print(out_str)


def show_meeting(index):
	meetings = get_meetings()
	if index <= 0 or index > len(meetings):
		error(f'\'{index}\' is not a valid index')
		return

	meeting = meetings[index - 1]
	join_url = get_join_url(meeting['id'], meeting['password'] if 'password' in meeting else None)
	print(f'Index:       {index}')
	print(f'Name:        {meeting["name"]}')
	print(f'Meeting ID:  {format_meeting_id(meeting["id"])}')
	print(f'Password:    {meeting["password"] if "password" in meeting else ""}')
	print(f'Join URL:    {join_url}')


# returns formatted meeting id
def format_meeting_id(meeting_id, pad=False):
	meeting_id = str(meeting_id).replace(' ', '')
	id_len = len(meeting_id)

	if id_len > 11:
		error(f'{meeting_id} is not a valid meeting id')
	elif id_len == 11:
		return meeting_id[0:3] + ' ' + meeting_id[3:7] + ' ' + meeting_id[7:11]
	else:
		# pad with zeros up to 10 digits length
		meeting_id.zfill(10)
		return (' ' if pad else '') + meeting_id[0:3] + ' ' + meeting_id[3:6] + ' ' + meeting_id[6:10]

	if type(meeting_id) is str:
		meeting_id = int(meeting_id.replace(' ', ''))
	return '{:03} {:03} {:04}'.format(meeting_id // (10 ** 7), (meeting_id % 10 ** 7) // 10 ** 4, meeting_id % (10 ** 4))


# generates zoom.us join url
def get_join_url(meeting_id, password = None):
	url = f"https://www.zoom.us/j/{meeting_id.replace(' ', '')}"
	if password:
		url += f'?pwd={password}'
	return url


# parses zoom.us join url
# returns tuple with (id, password=None)
def parse_join_url(url):
	regex = '.*zoom\.us\/j\/(\d+)(?:\/?\?.*?pwd=(.*?)(?:$|&))?'
	matches = re.match(regex, url)
	if not matches:
		return None
	return matches[1], matches[2] if matches[2] else None


def launch_meeting(meeting_id, password = None):
	meeting_id = str(meeting_id).replace(' ', '')
	url = f'zoommtg://zoom.us/join?confno={meeting_id}'
	if password:
		url += f'&pwd={password}'

	try:
		sp.run(['xdg-open', url], check=True, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
	except sp.CalledProcessError:
		error(f'Cannot launch \'xdg-open\'')
	exit()


# displays error to STDERR and exits
def error(message):
	print('Error: ' + message, file=sys.stderr)
	exit(2)


if __name__ == "__main__":
	os.chdir(sys.path[0])  # if program is run from another folder
	# parsing arguments
	parser = argparse.ArgumentParser(description='launches Zoom meetings and stores meeting ids')
	subparsers = parser.add_subparsers(dest='command')
	show_parser = subparsers.add_parser('show', help='show/list stored meeting(s)')
	show_parser.add_argument('index', help='meeting index to show', nargs='?')
	launch_parser = subparsers.add_parser('launch', help='launch a meeting')
	launch_parser.add_argument('id', help='index, meeting id or url')
	launch_parser.add_argument('password', help='password (not needed if used with url)', nargs='?')
	next_parser = subparsers.add_parser('next', help='launch next meeting (+/- 20min)')
	args = parser.parse_args()

	if not args.command or args.command == 'show':
		if 'index' not in args or not args.index:
			list_meetings()
		else:
			show_meeting(int(args.index))
	elif args.command == 'launch':
		arg = args.id
		arg_type = None
		meetings = get_meetings()

		# detect if index, id or url
		try:
			int_arg = int(arg.replace(' ', ''))
			if 0 < int_arg <= len(meetings):
				arg_type = 'index'
			else:
				arg_type = 'id'
		except:
			arg_type = 'url'

		if arg_type == 'index':
			meeting = get_meetings()[int_arg - 1]
			meeting_id = meeting['id']
			meeting_password = meeting['password'] if 'password' in meeting else None
		elif arg_type == 'id':
			meeting_id = int_arg
			meeting_password = args.password
		elif arg_type == 'url':
			data = parse_join_url(arg)
			if not data:
				error(f'\'{arg}\' is not valid')
			meeting_id, meeting_password = data

		launch_meeting(meeting_id, meeting_password)

	elif args.command == 'next':
		now = datetime.datetime.now()
		meetings = get_meetings()
		for meeting in meetings:
			if "time" in meeting:
				meetingstart = [int(i) for i in meeting["time"][1].split(':')]
				diff = datetime.timedelta(hours=now.time().hour, minutes=now.time().minute) - \
					   datetime.timedelta(hours=meetingstart[0], minutes=meetingstart[1])
				if now.weekday()+1 == meeting["time"][0] and abs(diff.total_seconds())/60 <= 20:
					launch_meeting(meeting['id'], meeting['password'] if 'password' in meeting else None)
		print("No meetings found!")
