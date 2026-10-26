// Read-only: no signer, deployment, transaction submission or appeal.
import {createClient} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';
import {TransactionHashVariant} from 'genlayer-js/types';
import fs from 'node:fs';
import crypto from 'node:crypto';
const root=new URL('../',import.meta.url);
const file=p=>JSON.parse(fs.readFileSync(new URL(p,root),'utf8'));
const need=(ok,message)=>{if(!ok)throw Error(message);};
const m=file('deployment.json');const c=createClient({chain:studionet});
need(await c.getChainId()===61999,'CHAIN_MISMATCH');
const source=await c.getContractCode(m.address);
need(source===fs.readFileSync(new URL('contracts/term_fence.py',root),'utf8'),'DEPLOYED_SOURCE_MISMATCH');
need(crypto.createHash('sha256').update(source).digest('hex')===m.source_sha256,'SOURCE_HASH_MISMATCH');
for(const [step,hash] of Object.entries(m.transactions)){
 const tx=await c.getTransaction({hash});
 need(tx.statusName==='FINALIZED',step+':NOT_FINALIZED');
 need(tx.result_name==='MAJORITY_AGREE',step+':NO_CONSENSUS');
 const leader=tx.consensus_data?.leader_receipt?.find(r=>r.mode==='leader');
 need(leader?.result?.status==='return',step+':EXECUTION_FAILED');
 need(tx.leader_only===false&&tx.execution_mode==='NORMAL',step+':NOT_FULL_CONSENSUS');
 need(tx.from_address.toLowerCase()===m.sender.toLowerCase(),'SENDER_MISMATCH');
 need(tx.to_address.toLowerCase()===m.address.toLowerCase(),'CONTRACT_MISMATCH');
 console.log(step+': FINALIZED / MAJORITY_AGREE / return');
}
const raw=await c.readContract({address:m.address,functionName:'get_record',args:[m.record_id],transactionHashVariant:TransactionHashVariant.LATEST_FINAL});
const r=JSON.parse(raw);const e=file('examples/library.json');
need(r.state==='PUBLISHED'&&r.revision===3&&r.published===1,'PUBLISHED_STATE_MISMATCH');
need(JSON.stringify(r.source_units)===JSON.stringify(e.source_units),'SOURCE_UNITS_MISMATCH');
need(r.attempts.length===2,'ATTEMPT_COUNT_MISMATCH');
need(r.attempts[0].candidate===e.negative_candidate&&r.attempts[0].status==='REJECTED','NEGATIVE_MISMATCH');
need(r.attempts[1].candidate===e.positive_candidate&&r.attempts[1].status==='PRESERVED','POSITIVE_MISMATCH');
const canonical=v=>Array.isArray(v)?'['+v.map(canonical).join(',')+']':v&&typeof v==='object'?'{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+canonical(v[k])).join(',')+'}':JSON.stringify(v);
const sha=v=>crypto.createHash('sha256').update(canonical(v)).digest('hex');
need(r.source_hash===sha({protocol:'termfence-1',units:r.source_units}),'RECORD_HASH_MISMATCH');
for(const a of r.attempts)need(a.candidate_hash===sha({source_hash:r.source_hash,candidate:a.candidate}),'CANDIDATE_HASH_MISMATCH');
console.log('Verified source, final receipts, controls, published selection and input hashes.');
process.exit(0);
