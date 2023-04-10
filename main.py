import psutil
print(*psutil.net_connections(), sep='\n\n')