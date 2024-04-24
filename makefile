lsof:
	lsof -i :3000
ps-ports:
	ps aux | grep 'serve -s build -p 3000'
kill-pid:
	kill -9 {{pid}}

install-npm:
	sudo add-apt-repository universe && sudo apt install nodejs npm

install-npm-server:
	sudo npm install -g serve
