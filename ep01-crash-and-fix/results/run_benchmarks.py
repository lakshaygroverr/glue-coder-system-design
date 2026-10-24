# Re-runs every setup from the video with 100 headless Locust users and writes results.md.
#   .venv\Scripts\python results\run_benchmarks.py      (from the episode folder)
import csv, os, subprocess, sys, time
from pathlib import Path

EP = Path(__file__).resolve().parent.parent
PY = sys.executable
RES = EP / 'results'


def start(*args):
    # output goes to a log file: a pipe nobody reads fills up and freezes the server mid-test
    log = open(RES / f"log_{'_'.join(args).replace('.py', '')}.txt", 'w')
    p = subprocess.Popen([PY, '-u', *args], cwd=EP, stdout=log, stderr=subprocess.STDOUT)
    p.log = log.name
    return p


def locust(name, kill=None):
    cmd = [PY, '-m', 'locust', '-f', 'locustfile.py', '--headless', '-u', '100', '-r', '20', '-t', '25s',
           '--host', 'http://localhost:8000', '--csv', str(RES / name), '--only-summary']
    p = subprocess.Popen(cmd, cwd=EP, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if kill:
        time.sleep(12)
        kill.kill()
    p.wait()
    with open(RES / f'{name}_stats.csv') as f:
        row = next(r for r in csv.DictReader(f) if r['Name'] == 'Aggregated')
    n, fails = int(row['Request Count']), int(row['Failure Count'])
    return {'median_ms': row['Median Response Time'], 'avg_ms': f"{float(row['Average Response Time']):.0f}",
            'rps': f"{float(row['Requests/s']):.1f}", 'fail_pct': f"{100 * fails / max(1, n):.1f}", 'requests': n}


def stop(*ps):
    for p in ps:
        p.kill()
    time.sleep(1)


results, lb_log = {}, ''
# 1) one worker
(EP / 'server_threads10.py').write_text((EP / 'server.py').read_text().replace('threads=1)', 'threads=10)'))
for name, script in [('1_one_worker', 'server.py'), ('2_ten_threads', 'server_threads10.py'), ('3_cached', 'server_cached.py')]:
    s = start(script, '8000'); time.sleep(3)
    results[name] = locust(name); stop(s)
(EP / 'server_threads10.py').unlink()

for name, kill in [('4_three_servers_lb', False), ('5_lb_kill_8002', True)]:
    servers = [start('server_cached.py', str(p)) for p in (8001, 8002, 8003)]
    lb = start('load_balancer.py'); time.sleep(3)
    results[name] = locust(name, kill=servers[1] if kill else None)
    stop(lb, *servers)
    out = open(lb.log).read()
    if kill:
        lb_log = next((l for l in out.splitlines() if 'down' in l), '(no down message)')

with open(RES.parent / 'results.md', 'w') as f:
    f.write('# Measured results (100 users, ramp 20/s, 25 s, Windows desktop)\n\n')
    f.write('| Setup | Median ms | Avg ms | Requests/s | Failures % | Requests |\n|---|---|---|---|---|---|\n')
    for k, r in results.items():
        f.write(f"| {k} | {r['median_ms']} | {r['avg_ms']} | {r['rps']} | {r['fail_pct']} | {r['requests']} |\n")
    f.write(f'\nLoad balancer log when 8002 was killed: `{lb_log}`\n')
print(open(RES.parent / 'results.md').read())
