#!/usr/bin/env python3
"""Declared Binding/01 structural/crypto/reference test path, not domain-policy validation."""
import argparse
import base64
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

import rfc8785
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
MARKER = 'jep-tsto.binding'
ID = 'https://raw.githubusercontent.com/cognitive-emergence/tsto-spec/main/schemas/jep-tsto-binding-01.schema.json'
KID = 'urn:example:binding-01:TEST-KEY-DO-NOT-TRUST'
WHO = 'did:example:binding-01-test-actor'

def nodup(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj: raise ValueError('duplicate JSON member')
        obj[key] = value
    return obj

def parse(text):
    def invalid(value): raise ValueError('non-JSON number: ' + value)
    return json.loads(text, object_pairs_hook=nodup, parse_constant=invalid)

def read(path): return parse(Path(path).read_text())
def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
def b64(data): return base64.urlsafe_b64encode(data).decode().rstrip('=')
def unb64(text):
    raw = base64.b64decode(text + '=' * (-len(text) % 4), altchars=b'-_', validate=True)
    if b64(raw) != text: raise ValueError('noncanonical base64url')
    return raw
def canon(value): return rfc8785.dumps(value)
def event_hash(event): return 'sha256:' + hashlib.sha256(canon(event)).hexdigest()
def object_digest(value): return 'sha-256:' + b64(hashlib.sha256(canon(value)).digest())
def tref(tsto): return dict(kind='external_object', type='TargetStateTransition', spec='TSTO/00', id=tsto['id'], digest=tsto['integrity']['value'])
def get_ref(event): return event['what']['subject'] if event['verb'] == 'T' else event['ref']['value']
def validator(path):
    schema = read(path)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())

def sign(event, key, alg):
    event = copy.deepcopy(event)
    event.pop('sig', None)
    protected = b64(canon({'alg': alg, 'kid': KID}))
    event['sig'] = protected + '..' + b64(key.sign((protected + '.' + b64(canon(event))).encode('ascii')))
    return event

def verify_crypto(event, jwk, algorithm):
    if algorithm not in ('Ed25519', 'EdDSA'): raise ValueError('unknown test trust profile')
    protected, empty, signature = event['sig'].split('.')
    header = parse(unb64(protected).decode())
    if empty or header != {'alg': algorithm, 'kid': KID}: raise ValueError('header outside selected test profile')
    if jwk['kid'] != KID or jwk['kty'] != 'OKP' or jwk['crv'] != 'Ed25519' or event['who'] != WHO:
        raise ValueError('outside synthetic actor/key trust binding')
    unsigned = {k: v for k, v in event.items() if k != 'sig'}
    Ed25519PublicKey.from_public_bytes(unb64(jwk['x'])).verify(unb64(signature), (protected + '.' + b64(canon(unsigned))).encode('ascii'))

def validate(event, tsto, known, jwk, algorithm):
    validator(ROOT/'tests/upstream/jep-event-0.6.schema.json').validate(event)
    validator(ROOT/'schemas/jep-tsto-binding-01.schema.json').validate(event)
    if event.get('ext_crit'): raise ValueError('test profile implements no critical extensions')
    verify_crypto(event, jwk, algorithm)
    validator(ROOT/'schemas/tsto-00.schema.json').validate(tsto)
    unsigned_tsto = {k: v for k, v in tsto.items() if k != 'integrity'}
    if object_digest(unsigned_tsto) != tsto['integrity']['value']: raise ValueError('TSTO content digest mismatch')
    if get_ref(event) != tref(tsto): raise ValueError('TSTO id+digest resolution conflict')
    if event['verb'] == 'T':
        if event['what']['target'] != event['ref']: raise ValueError('termination target mismatch')
        target = known.get(event['ref'])
        if target is None or event_hash(target) != event['ref']: raise ValueError('unresolved target event')
        # This test profile supports delegation termination only.
        if event['what']['termination_scope'] != 'delegation' or target['verb'] != 'D': raise ValueError('unsupported target role')
        if get_ref(target) != event['what']['subject']: raise ValueError('different terminated TSTO')
    if event['verb'] == 'V' and event['what']['policy_ref'] != tsto['verification']['policy']:
        raise ValueError('different verification policy')
    return event_hash(event)

def generate():
    # Public deterministic TEST seed. Never deploy this key or its trust binding.
    key = Ed25519PrivateKey.from_private_bytes(hashlib.sha256(b'JEP-TSTO-Binding-01-PUBLIC-TEST-ONLY').digest())
    jwk = dict(kid=KID, kty='OKP', crv='Ed25519', x=b64(key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)))
    tsto = read(ROOT/'examples/tsto/valid/ar-invoice-settlement.example.json')
    ref = tref(tsto)
    templates = [read(p) for p in [ROOT/'examples/jep/J-accept-tsto.example.json', ROOT/'examples/jep/D-delegate-tsto.example.json', ROOT/'examples/jep/T-terminate-delegation.example.json', ROOT/'examples/jep/V-verify-tsto.example.json']]
    profiles = []
    for alg in ['Ed25519', 'EdDSA']:
        events = []
        for i, template in enumerate(templates):
            e = copy.deepcopy(template); e['who'] = WHO; e['ext'] = {MARKER: {'id': ID}}
            e['nonce'] = f'10000000-0000-4000-8000-{i+1:012d}'
            e['ref'] = {'type': 'TargetStateTransition', 'value': ref}
            if e['verb'] == 'D' and 'constraints' in e['what']: e['what']['constraints'] = [e['what']['constraints']]
            if e['verb'] == 'T': e['ref'] = event_hash(events[1]); e['what']['target'] = e['ref']; e['what']['subject'] = ref
            if e['verb'] == 'V': e['what']['policy_ref'] = tsto['verification']['policy']
            events.append(sign(e,key,alg))
        profiles.append({'algorithm': alg, 'events': events, 'eventHashes': list(map(event_hash, events)), 'unsignedCanonicalUtf8': [canon({k:v for k,v in e.items() if k!='sig'}).decode() for e in events]})
    bad = []
    def hostile(name, index, mutate, *, resign=True, unresolved=False):
        e = copy.deepcopy(profiles[0]['events'][index]); mutate(e)
        if resign: e = sign(e,key,'Ed25519')
        bad.append(dict(name=name,event=e,signatureValid=resign,unresolved=unresolved))
    hostile('missing-marker',0,lambda e:e['ext'].pop(MARKER))
    hostile('unknown-version',0,lambda e:e['ext'][MARKER].update(id='urn:example:unknown-binding'))
    hostile('mixed-markers',0,lambda e:e['ext'].update({'prooftask.binding':{'id':'urn:prooftask:jep-tsto-binding:01-candidate:1'}}))
    hostile('bare-reference',0,lambda e:e.update(ref=e['ref']['value']))
    hostile('extra-reference-member',0,lambda e:e['ref']['value'].update(extra=True))
    hostile('different-object-id',0,lambda e:e['ref']['value'].update(id='urn:example:other'))
    hostile('different-object-digest',0,lambda e:e['ref']['value'].update(digest='sha-256:'+'A'*43))
    hostile('digest-domain-confusion',0,lambda e:e['ref']['value'].update(digest='sha256:'+'a'*64))
    hostile('object-constraints',1,lambda e:e['what'].update(constraints={'attempts':5}))
    hostile('missing-termination-target',2,lambda e:e['what'].pop('target'))
    hostile('different-termination-target',2,lambda e:e['what'].update(target='sha256:'+'a'*64))
    hostile('unresolved-termination-target',2,lambda e:None,unresolved=True)
    hostile('different-policy',3,lambda e:e['what']['policy_ref'].update(id='urn:example:other-policy'))
    hostile('unknown-critical-extension',0,lambda e:e.update(ext_crit=['urn:example:unsupported']))
    hostile('tampered-after-signing',0,lambda e:e['what'].update(decision='reject'),resign=False)
    vector={'10':1e-7,'2':1e20,'\U0001f600':-0.0,'\ue000':1e30,'text':'Unicode 王 / control\n'}
    bundle=dict(note='Synthetic public test vectors. Referenced external evidence and policy digests are illustrative; no domain result or production trust is asserted.',publicKey=jwk,tsto=tsto,profiles=profiles,hostile=bad,jcs={'input':vector,'expectedUtf8':canon(vector).decode(),'sha256':hashlib.sha256(canon(vector)).hexdigest()})
    dump(ROOT/'examples/binding-01/vectors.json',bundle)
    for e in profiles[0]['events']: dump(ROOT/f'examples/binding-01/{e["verb"]}-signed.json',e)

def run(jep_seed=None):
    data = read(ROOT/'examples/binding-01/vectors.json'); tsto=data['tsto']; jwk=data['publicKey']
    count=0
    for profile in data['profiles']:
        known={}
        for i,event in enumerate(profile['events']):
            h=validate(event,tsto,known,jwk,profile['algorithm'])
            assert h==profile['eventHashes'][i]
            assert canon({k:v for k,v in event.items() if k!='sig'}).decode()==profile['unsignedCanonicalUtf8'][i]
            known[h]=event;count+=1
    known={event_hash(e):e for e in data['profiles'][0]['events']}
    for case in data['hostile']:
        if case['signatureValid']: verify_crypto(case['event'],jwk,'Ed25519')
        try: validate(case['event'],tsto,{} if case['unresolved'] else known,jwk,'Ed25519')
        except Exception: pass
        else: raise AssertionError('hostile case accepted: '+case['name'])
    try: verify_crypto(data['profiles'][1]['events'][0],jwk,'Ed25519')
    except ValueError: pass
    else: raise AssertionError('algorithm profile silently widened')
    changed=copy.deepcopy(tsto); changed['id']='urn:example:altered-tsto'
    try: validate(data['profiles'][0]['events'][0],changed,known,jwk,'Ed25519')
    except Exception: pass
    else: raise AssertionError('altered TSTO accepted')
    for raw in ['{"verb":"J","verb":"T"}', '{"n":NaN}']:
        try: parse(raw)
        except ValueError: pass
        else: raise AssertionError('invalid JSON accepted')
    assert canon(data['jcs']['input']).decode()==data['jcs']['expectedUtf8']
    assert hashlib.sha256(canon(data['jcs']['input'])).hexdigest()==data['jcs']['sha256']
    legacy=validator(ROOT/'schemas/jep-tsto-binding-00.schema.json'); core=validator(ROOT/'tests/upstream/jep-event-0.6.schema.json')
    for path in (ROOT/'examples/jep').glob('*.json'):
        event=read(path);legacy.validate(event);assert not core.is_valid(event)
    baseline=None
    if jep_seed:
        spec=importlib.util.spec_from_file_location('upstream_jep',jep_seed);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        for event in data['profiles'][0]['events']:
            assert m.validate_event_obj(event,keys={KID:jwk},known_hashes=known)['valid']
        assert not m.validate_event_obj(data['profiles'][1]['events'][0],keys={KID:jwk})['valid']
        baseline=4
    report=dict(signedEvents=count,hostileCasesRejected=len(data['hostile']),legacyIncompatibilitiesReproduced=4,jcs=True,duplicateMemberRejection=True,algorithmSeparation=True,upstreamEd25519SeedPassed=baseline,scope='joint schemas, JCS, signatures under synthetic actor/key trust, exact TSTO id+digest and content integrity, T target resolution, policy-reference equality; no external policy evaluation')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--generate',action='store_true');parser.add_argument('--jep-seed');args=parser.parse_args()
    if args.generate: generate()
    run(args.jep_seed)
