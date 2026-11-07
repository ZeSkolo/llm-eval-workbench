import json, re

def evaluate(c, text):
    if not isinstance(text, str) or len(text) > 50000:
        raise ValueError('Responses must be strings below 50000 characters')
    checks = []
    for phrase in c.get('must_include', []):
        checks.append({'rule': 'contains:' + phrase, 'pass': phrase.casefold() in text.casefold()})
    for phrase in c.get('must_not_include', []):
        checks.append({'rule': 'excludes:' + phrase, 'pass': phrase.casefold() not in text.casefold()})
    if c.get('citation'):
        checks.append({'rule': 'citation', 'pass': bool(re.search('\\[[\\w.-]+:\\d+\\]', text))})
    if c.get('refusal'):
        checks.append({'rule': 'refusal', 'pass': any((x in text.casefold() for x in ['cannot help', 'can’t help', 'unable to', 'cannot provide']))})
    if 'json_keys' in c:
        try:
            obj = json.loads(text)
            valid = isinstance(obj, dict) and all((k in obj for k in c['json_keys']))
        except (ValueError, TypeError):
            valid = False
        checks.append({'rule': 'json_keys', 'pass': valid})
    if not checks:
        raise ValueError('Each case needs at least one rubric rule')
    return {'checks': checks, 'score': sum((c['pass'] for c in checks)) / len(checks), 'passed': all((c['pass'] for c in checks))}

def run(p):
    cases = p.get('cases', [])
    candidate = p.get('candidate', {})
    baseline = p.get('baseline', {})
    threshold = p.get('threshold', 1.0)
    if not isinstance(cases, list) or not 1 <= len(cases) <= 200 or (not 0 <= threshold <= 1):
        raise ValueError('1–200 cases and threshold 0–1 required')
    ids = [c.get('id') for c in cases]
    if any((not isinstance(i, str) or not i for i in ids)) or len(set(ids)) != len(ids):
        raise ValueError('Case IDs must be unique')
    results = []
    for c in cases:
        if c['id'] not in candidate:
            raise ValueError('Missing candidate response: ' + c['id'])
        result = dict(id=c['id'], **evaluate(c, candidate[c['id']]))
        if c['id'] in baseline:
            before = evaluate(c, baseline[c['id']])
            result['baseline_score'] = before['score']
            result['regression'] = result['score'] < before['score']
        results.append(result)
    mean = sum((x['score'] for x in results)) / len(results)
    return {'mean_score': mean, 'passed_cases': sum((x['passed'] for x in results)), 'total_cases': len(results), 'release_passed': mean >= threshold and (not any((x.get('regression') for x in results))), 'results': results}
