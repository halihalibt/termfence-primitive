"""Offline protocol checks with a scripted nondeterministic boundary; not network consensus."""
import importlib.util
import json
from pathlib import Path
import sys
import types
import unittest
from copy import deepcopy

class Return:
    def __init__(self, value): self.calldata = value

class TreeMap:
    def __class_getitem__(cls, item): return dict

responses = []
def prompt(*args, **kwargs):
    value = responses.pop(0)
    if isinstance(value, Exception): raise value
    return value

def nondet(leader, validator):
    value = leader()
    if not validator(Return(value)): raise Exception('CONSENSUS_REJECTED')
    return value

fake = types.ModuleType('genlayer')
fake.TreeMap = TreeMap
fake.u32 = int
fake.gl = types.SimpleNamespace(Contract=object, public=types.SimpleNamespace(view=lambda f:f, write=lambda f:f),
    message=types.SimpleNamespace(sender_address='0xaaa'), nondet=types.SimpleNamespace(exec_prompt=prompt),
    vm=types.SimpleNamespace(Return=Return,run_nondet_unsafe=nondet))
sys.modules['genlayer'] = fake
spec = importlib.util.spec_from_file_location('term_fence', Path(__file__).parents[1]/'contracts/term_fence.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
UNITS = ['Members may borrow up to three books for fourteen days.', 'Reference books cannot be borrowed under any circumstances.']
GOOD = 'Members may borrow up to 3 books for 14 days, excluding reference books.'
BAD = 'Members may borrow three books for fourteen days.'
OK = {'units':['KEPT','KEPT'],'addition':'NONE'}
NO = {'units':['KEPT','LOST'],'addition':'NONE'}

class Protocol(unittest.TestCase):
    def setUp(self):
        fake.gl.message.sender_address = '0xaaa'
        responses.clear()
        self.c=m.TermFence(); self.c.records={};self.c.counts={}
        self.rid=self.c.seal('library',json.dumps(UNITS))
    def record(self): return json.loads(self.c.get_record(self.rid))
    def assess(self, d, candidate=GOOD, own=None, revision=None):
        responses.extend([deepcopy(d),deepcopy(d if own is None else own)])
        return json.loads(self.c.assess(self.rid,self.record()['revision'] if revision is None else revision,candidate))
    def test_complete_lifecycle(self):
        r=self.assess(NO,BAD);self.assertEqual(r['state'],'ASSESSED')
        r=self.assess(OK);self.assertEqual(r['state'],'READY')
        r=json.loads(self.c.publish(self.rid,2,1));self.assertEqual((r['state'],r['revision'],r['published']),('PUBLISHED',3,1))
        with self.assertRaisesRegex(Exception,'TERMINAL'):self.c.assess(self.rid,3,GOOD)
    def test_unit_disagreement_same_aggregate_rejected(self):
        before=self.c.get_record(self.rid)
        with self.assertRaisesRegex(Exception,'CONSENSUS_REJECTED'):
            self.assess(NO,own={'units':['LOST','KEPT'],'addition':'NONE'})
        self.assertEqual(before,self.c.get_record(self.rid))
    def test_addition_disagreement_rejected(self):
        with self.assertRaisesRegex(Exception,'CONSENSUS_REJECTED'):self.assess(OK,own={'units':['KEPT','KEPT'],'addition':'ADDED'})
    def test_uncertainty_cannot_publish(self):
        r=self.assess({'units':['KEPT','UNCLEAR'],'addition':'NONE'})
        self.assertEqual(r['attempts'][0]['status'],'REVIEW')
        with self.assertRaisesRegex(Exception,'NOT_READY'):self.c.publish(self.rid,1,0)
    def test_added_claim_blocks(self):
        r=self.assess({'units':['KEPT','KEPT'],'addition':'ADDED'})
        self.assertEqual(r['attempts'][0]['status'],'REJECTED')
    def test_ownership(self):
        fake.gl.message.sender_address='0xbbb'
        with self.assertRaisesRegex(Exception,'OWNER_ONLY'):self.c.assess(self.rid,0,GOOD)
    def test_stale_revision(self):
        with self.assertRaisesRegex(Exception,'STALE_REVISION'):self.c.assess(self.rid,1,GOOD)
        self.assertFalse(responses)
    def test_duplicate_candidate(self):
        self.assess(OK)
        with self.assertRaisesRegex(Exception,'DUPLICATE_CANDIDATE'):self.c.assess(self.rid,1,GOOD)
        self.assertFalse(responses)
    def test_rejected_attempt_not_publishable(self):
        self.assess(NO,BAD); self.assess(OK)
        with self.assertRaisesRegex(Exception,'NOT_PRESERVED'):self.c.publish(self.rid,2,0)
    def test_malformed_output_and_error_fail_closed(self):
        for bad in [{'units':['KEPT'],'addition':'NONE'},{'units':['KEPT','KEPT'],'addition':True},Exception('MODEL_UNAVAILABLE')]:
            with self.assertRaises(Exception): self.assess(OK,own=bad)
            self.assertEqual(self.record()['revision'],0)
            responses.clear()
    def test_duplicate_json_keys(self):
        with self.assertRaisesRegex(Exception,'DUPLICATE_JSON_KEY'):m.parse('{"addition":"NONE","addition":"ADDED"}')
    def test_seal_immutable_and_bounded(self):
        with self.assertRaisesRegex(Exception,'ALREADY_SEALED'):self.c.seal('library',json.dumps(UNITS))
        with self.assertRaisesRegex(Exception,'DUPLICATE_UNIT'):self.c.seal('other',json.dumps([UNITS[0]]*2))
        with self.assertRaisesRegex(Exception,'MUST_COMPRESS'):self.c.assess(self.rid,0,'x'*200)
    def test_ready_survives_later_rejection(self):
        self.assess(OK); r=self.assess(NO,BAD)
        self.assertEqual(r['state'],'READY')
        self.assertEqual(json.loads(self.c.publish(self.rid,2,0))['published'],0)
    def test_attempt_cap(self):
        for i in range(4):self.assess(NO,BAD+str(i))
        with self.assertRaisesRegex(Exception,'ATTEMPT_LIMIT'):self.c.assess(self.rid,4,GOOD)
    def test_hash_binds_order_and_candidate(self):
        a=m.digest({'protocol':m.PROTOCOL,'units':UNITS})
        self.assertEqual(a,self.record()['source_hash'])
        self.assertNotEqual(a,m.digest({'protocol':m.PROTOCOL,'units':list(reversed(UNITS))}))
    def test_validator_exception_or_nonreturn_rejected(self):
        self.assertFalse(m.agree('bad',lambda:OK,2))
        self.assertFalse(m.agree(Return(OK),lambda:1/0,2))
    def test_rejection_priority(self):
        self.assertEqual(m.verdict({'units':['LOST','UNCLEAR'],'addition':'NONE'}),'REJECTED')

if __name__=='__main__':unittest.main()
