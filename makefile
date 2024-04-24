lsof:
	lsof -i :3000
ps-ports:
	ps aux | grep 'serve -s build -p 3000'
kill-pid:
	kill -9 {{pid}}
