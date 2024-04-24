ps-ports:
	lsof -i :3000
kill-pid:
	kill -9 {{pid}}
