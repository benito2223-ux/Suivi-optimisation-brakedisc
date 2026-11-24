import re, sys, math, os, json

TOK = re.compile(r'([A-Z]+)=?([-+]?[\d.]+(?:[-+][\d.]+)*)')
def num(s):
    return sum(float(x) for x in re.findall(r'[-+]?[\d.]+', s))

SKIP = ('WHEN', 'DEF ', 'E_STEP', 'E_JUMP', 'E_STRADDLE', 'CR_BD', 'STOPRE', 'SETMS',
        'LABEL', 'REPEAT', '$P_UIFR', 'R102', 'R125', 'RET', 'MSG')

def run(path):
    prog = os.path.basename(path)
    st = dict(T='?', D=1, h81=0, mode='G0', spin='G97', S=0.0, F=0.0, X=None, Z=None,
              mon=False, lims=1e9)
    segs, dwell, hors = [], [], []
    tags = {}
    for raw in open(path, encoding='latin-1'):
        line = raw.rstrip('\n')
        code, _, com = line.partition(';')
        ag = re.findall(r'AG\d+\.\d+', com)
        code = code.strip()
        if not code:
            continue
        m = re.search(r'T="T(\d+S?)_"', code)
        if m:
            st['T'] = 'T' + m.group(1)
            code = code.replace(m.group(0), '').replace('<<$P_CHANNO', '')
        if any(k in code for k in SKIP):
            continue
        m = re.search(r'H81=(\d+)', code)
        if m:
            st['h81'] = int(m.group(1)); code = code.replace(m.group(0), '')
        code = re.sub(r'M1=\d+', '', code)
        code = re.sub(r'^N\d+\s*', '', code)
        toks = TOK.findall(code)
        if not toks:
            continue
        mcodes = re.findall(r'\bM(\d+)\b', code)
        if '870' in mcodes:
            st['mon'] = True
        new = {}
        gs = []
        for k, v in toks:
            val = num(v)
            if k == 'G': gs.append(int(val))
            elif k == 'D': st['D'] = int(val)
            elif k in 'XZFS' and len(k) == 1: new[k] = val
            elif k == 'CR': new['CR'] = val
            elif k == 'LIMS': st['lims'] = val
        for g in gs:
            if g in (0, 1, 2, 3): st['mode'] = 'G%d' % g
            if g in (96, 97): st['spin'] = 'G%d' % g
        if 'S' in new and 4 not in gs: st['S'] = new['S']
        if 'F' in new and 4 not in gs: st['F'] = new['F']
        def nrpm(D):
            if st['spin'] == 'G97': return st['S']
            return min(st['lims'], 1000.0 * st['S'] / (math.pi * max(abs(D), 1e-6)))
        if 4 in gs:
            d = {}
            if 'S' in new:
                x = abs(st['X'] if st['X'] is not None else 100)
                d = dict(rev=new['S'], t=new['S'] / nrpm(x) * 60)
            elif 'F' in new:
                d = dict(t=new['F'])
            d.update(T=st['T'], D=st['D'], h81=st['h81'], mon=st['mon'], prog=prog)
            dwell.append(d)
        elif 53 in gs:
            pass
        else:
            x1 = abs(new['X']) if 'X' in new else (abs(st['X']) if st['X'] is not None else None)
            z1 = new.get('Z', st['Z'])
            if st['mode'] in ('G1', 'G2', 'G3') and ('X' in new or 'Z' in new) \
               and st['X'] is not None and st['Z'] is not None and st['F'] > 0:
                x0, z0 = abs(st['X']), st['Z']
                dr = (x1 - x0) / 2.0
                dz = (z1 - z0)
                chord = math.hypot(dr, dz)
                if st['mode'] in ('G2', 'G3') and 'CR' in new:
                    R = new['CR']
                    L = R * 2 * math.asin(min(1, chord / (2 * R)))
                else:
                    L = chord
                n = 400; t = 0.0; nsum = 0.0
                for i in range(n):
                    D = x0 + (x1 - x0) * (i + .5) / n
                    N = nrpm(D)
                    t += (L / n) / (st['F'] * N)
                    nsum += N / n
                seg = dict(prog=prog, T=st['T'], D=st['D'], h81=st['h81'], mode=st['mode'],
                           L=L, F=st['F'], N=nsum, t=t * 60, x0=x0, x1=x1,
                           capped=(st['spin'] == 'G96' and nrpm(min(x0, x1)) >= st['lims'] - 1e-6),
                           Vc=st['S'] if st['spin'] == 'G96' else None, ag=ag)
                (segs if st['mon'] else hors).append(seg)
            if 'X' in new: st['X'] = new['X']
            if 'Z' in new: st['Z'] = new['Z']
        if '890' in mcodes:
            st['mon'] = False
    return segs, dwell, hors

if __name__ == '__main__':
    d = sys.argv[1]
    out = {}
    for f in sorted(os.listdir(d)):
        if f.upper().endswith('.SPF'):
            out[f] = run(os.path.join(d, f))
    json.dump(out, open(sys.argv[2], 'w'), indent=1)
    for f, (segs, dwell, hors) in out.items():
        print('=====', f)
        for s in segs:
            print('%-6s D%d h81=%-3d %s L=%7.2f F=%.2f N=%6.0f t=%6.2fs %s %s' % (
                s['T'], s['D'], s['h81'], s['mode'], s['L'], s['F'], s['N'], s['t'],
                'CAP' if s['capped'] else '', ','.join(s['ag'])))
        print(' dwell in-window:', [(x['T'], x['D'], round(x['t'], 2)) for x in dwell if x['mon']])
        print(' dwell hors fenetre:', [(x['T'], x['D'], round(x['t'], 2)) for x in dwell if not x['mon']])
        print(' avances hors fenetre:')
        for s in hors:
            print('   %-6s D%d h81=%-3d L=%7.2f F=%.2f t=%5.2fs' % (s['T'], s['D'], s['h81'], s['L'], s['F'], s['t']))
