"""Temps de coupe pure depuis un programme Fanuc (lignes PCI : tournage G96/G97 + fraisage mm/min).

La fenetre de coupe = entre M2908 (debut enregistrement Montronix) et M2909 (fin), que ces codes soient
actifs ou entre parentheses. Les mouvements en avance (G01/G02/G03) hors fenetre sont rendus a part.

Tournage : F en mm/tr, X en diametre, G50 S = limite de broche en G96, W/U incrementaux.
Fraisage : F en mm/min, arcs G91 G03 (R ou J), perçage = G01 Z.
"""
import re, math, os, sys, json

TOK = re.compile(r'([A-Z])\s*(-?\s*\[[^\]]*\]|-?(?:\d+\.?\d*|\.\d+))')


def val(s, var):
    s = s.replace(' ', '')
    neg = s.startswith('-')
    s = s.lstrip('-')
    if s.startswith('['):
        e = re.sub(r'#(\d+)', lambda m: repr(var.get(int(m.group(1)), 0.0)), s)
        if not re.fullmatch(r'[\d.+\-*/()\[\] ]+', e):
            return None
        v = eval(e.replace('[', '(').replace(']', ')'))
    else:
        v = float(s)
    return -v if neg else v


def run(path, fraisage=False, sans_limite=False):
    prog = os.path.basename(path)
    st = dict(T='?', mode='G0', spin='G97', S=0.0, F=0.0, X=None, Z=None, Y=0.0, mon=False,
              lims=1e9, absolu=True)
    var = {}
    segs, dwell, hors = [], [], []
    for raw in open(path, encoding='latin-1'):
        line = raw.rstrip('\r\n')
        com = ' '.join(re.findall(r'\(([^)]*)\)', line))
        code = re.sub(r'\([^)]*\)', '', line).strip()
        if 'M2908' in line:
            st['mon'] = True
        close = 'M2909' in line
        mv = re.fullmatch(r'#(\d+)\s*=\s*(-?[\d.]+)', code.replace(' ', ''))
        if mv:
            var[int(mv.group(1))] = float(mv.group(2))
            continue
        if code.startswith('#') or not code or code in ('%',):
            if close:
                st['mon'] = False
            continue
        code = re.sub(r'^N\d+', '', code).strip()
        gs = [int(float(v)) for k, v in TOK.findall(code) if k == 'G']
        if any(g in (10, 28, 30, 53) for g in gs):
            if close:
                st['mon'] = False
            continue
        # outil
        mt = re.search(r'T(\d{2})(\d{2})(?!\d)', code)
        if fraisage:
            mt3 = re.search(r'T(\d{3})M6', code.replace(' ', ''))
            if mt3:
                st['T'] = 'T' + mt3.group(1)
        elif mt:
            st['T'] = 'T' + mt.group(1)
        new = {}
        for k, v in TOK.findall(code):
            x = val(v, var)
            if x is None:
                continue
            if k == 'G':
                continue
            if k in 'XYZUWVFSRIJP' :
                new.setdefault(k, x)
        for g in gs:
            if g in (0, 1, 2, 3):
                st['mode'] = 'G%d' % g
            elif g in (96, 97):
                st['spin'] = 'G%d' % g
            elif g == 90:
                st['absolu'] = True
            elif g == 91:
                st['absolu'] = False
        if 50 in gs:
            if 'S' in new and not sans_limite:
                st['lims'] = new['S']
            new.pop('S', None)
        if 'S' in new:
            st['S'] = new['S']
        if 'F' in new and 4 not in gs:
            st['F'] = new['F']

        def nrpm(D):
            if st['spin'] == 'G97':
                return st['S']
            return min(st['lims'], 1000.0 * st['S'] / (math.pi * max(abs(D), 1e-6)))

        info = dict(prog=prog, T=st['T'], mon=st['mon'], com=com)
        if 4 in gs:
            t = new.get('X', new.get('P', 0.0) / 1000.0 if 'P' in new else 0.0)
            dwell.append(dict(info, t=t))
        elif not fraisage and not st['absolu'] and False:
            pass
        elif not fraisage:
            x0, z0, y0 = st['X'], st['Z'], st['Y']
            x1 = new['X'] if 'X' in new else (x0 + new['U'] if ('U' in new and x0 is not None) else x0)
            z1 = new['Z'] if 'Z' in new else (z0 + new['W'] if ('W' in new and z0 is not None) else z0)
            y1 = new['Y'] if 'Y' in new else y0
            moved = any(k in new for k in 'XZUWY')
            if st['mode'] in ('G1', 'G2', 'G3') and moved and x0 is not None and z0 is not None and st['F'] > 0:
                dr = (x1 - x0) / 2.0
                L = math.sqrt(dr * dr + (z1 - z0) ** 2 + (y1 - y0) ** 2)
                if L > 1e-9:
                    n = 400
                    t = 0.0
                    ns = 0.0
                    for i in range(n):
                        D = x0 + (x1 - x0) * (i + .5) / n
                        N = nrpm(D)
                        t += (L / n) / (st['F'] * N)
                        ns += N / n
                    d0, d1 = abs(x0), abs(x1)
                    seg = dict(info, mode=st['mode'], L=L, F=st['F'], N=ns, t=t * 60,
                               d0=min(d0, d1), d1=max(d0, d1), Vc=st['S'] if st['spin'] == 'G96' else None,
                               S=st['S'], spin=st['spin'], lims=st['lims'],
                               capped=(st['spin'] == 'G96' and nrpm(min(d0, d1)) >= st['lims'] - 1e-6))
                    (segs if st['mon'] else hors).append(seg)
            if x1 is not None:
                st['X'] = x1
            if z1 is not None:
                st['Z'] = z1
            st['Y'] = y1
        else:
            # fraisage : G01 Z (percage) et arcs G02/G03 (fraisurage), F en mm/min
            z0 = st['Z']
            if st['mode'] == 'G1' and 'Z' in new and st['F'] > 0 and st['absolu'] and z0 is not None:
                L = abs(new['Z'] - z0)
                seg = dict(info, mode='G1', kind='percage', L=L, F=st['F'], t=L / st['F'] * 60, S=st['S'])
                (segs if st['mon'] else hors).append(seg)
            elif st['mode'] in ('G2', 'G3') and st['F'] > 0 and not st['absolu']:
                if 'R' in new and ('X' in new or 'Y' in new):
                    ch = math.hypot(new.get('X', 0.0), new.get('Y', 0.0))
                    R = abs(new['R'])
                    L = 2 * R * math.asin(min(1.0, ch / (2 * R)))
                elif 'J' in new or 'I' in new:
                    L = 2 * math.pi * math.hypot(new.get('I', 0.0), new.get('J', 0.0))
                else:
                    L = 0.0
                seg = dict(info, mode=st['mode'], kind='fraisurage', L=L, F=st['F'], t=L / st['F'] * 60, S=st['S'])
                (segs if st['mon'] else hors).append(seg)
            if 'Z' in new and st['absolu']:
                st['Z'] = new['Z']
        if close:
            st['mon'] = False
    return segs, dwell, hors


if __name__ == '__main__':
    p = sys.argv[1]
    fr = len(sys.argv) > 2 and sys.argv[2] == 'fraisage'
    segs, dwell, hors = run(p, fr)
    for s in segs:
        print(s['T'], s.get('kind', ''), s['mode'], 'L=%.2f' % s['L'], 'F=%g' % s['F'], 't=%.2f' % s['t'],
              'Vc=%s' % s.get('Vc'), 'S=%s' % s.get('S'), 'CAP' if s.get('capped') else '')
    print('dwell', [(d['T'], d['t'], d['mon']) for d in dwell])
    print('hors', [(h['T'], round(h['L'], 2), round(h['t'], 2)) for h in hors])
