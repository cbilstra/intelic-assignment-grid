# intelic-assignment-grid
Optimizing drone paths over a grid. 
Features:
- Support for N drones
- Support for N workers (concurrent execution)
- Support for multiple exploration strategies (three implemented)

I spent for about 3 hours total.

## Getting started
```bash
cp .env.example .env
mkdir data

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

python3 main.py 20 5 1 0,0#3,3 --strategy random
```
Don't forget to put {20/100/1000}.txt in the data folder.
