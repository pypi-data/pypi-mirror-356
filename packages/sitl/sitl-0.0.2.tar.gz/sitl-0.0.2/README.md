# Python Wrapper for the Betaflight SITL

```
pip install sitl
```

Run
```
ui-server
```

Navigate to [http://localhost:13337](http://localhost:13337)

New terminal: Run
```
sitl-websockify
```

Navigate to [https://app.betaflight.com](https://app.betaflight.com). `Options` => `Enable manual connection mode`. Port: `Manual Selection` and paste `ws://127.0.0.1:6761`

New terminal: Run
```
sitl
```


# Troubleshooting

Ports in use:

```
netstat -tulpn | grep 13337
netstat -tulpn | grep 6761
netstat -tulpn | grep 5761
netstat -tulpn | grep 9002
netstat -tulpn | grep 9003
netstat -tulpn | grep 9004
```

```
kill -9 {PID (last number in row)}
```
