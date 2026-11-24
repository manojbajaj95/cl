"""Cross-substrate swap/compose probe: two behaviours (A: all-uppercase, B: end with DONE)
each implemented as text (system instruction), weights (LoRA distilled from the code
implementation's outputs) or code (post-processor). Runs all 16 (A,B) substrate pairs on
held-out capital questions; scores A, B and retention (correct capital present)."""
import json, re, random, sys, torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model, PeftModel

SEED=int(sys.argv[2]) if len(sys.argv)>2 else 0
torch.manual_seed(SEED); random.seed(SEED); torch.set_num_threads(8)
M = "Qwen/Qwen2.5-0.5B-Instruct"
CAP = {"France":"Paris","Germany":"Berlin","Italy":"Rome","Spain":"Madrid","Japan":"Tokyo","China":"Beijing",
"India":"New Delhi","Russia":"Moscow","Canada":"Ottawa","Australia":"Canberra","Brazil":"Brasilia","Egypt":"Cairo",
"Kenya":"Nairobi","Mexico":"Mexico City","Argentina":"Buenos Aires","Peru":"Lima","Chile":"Santiago","Greece":"Athens",
"Turkey":"Ankara","Iran":"Tehran","Iraq":"Baghdad","Poland":"Warsaw","Sweden":"Stockholm","Norway":"Oslo",
"Finland":"Helsinki","Denmark":"Copenhagen","Portugal":"Lisbon","Ireland":"Dublin","Austria":"Vienna","Hungary":"Budapest",
"Thailand":"Bangkok","Vietnam":"Hanoi","Indonesia":"Jakarta","Philippines":"Manila","South Korea":"Seoul","Cuba":"Havana",
"Colombia":"Bogota","Venezuela":"Caracas","Nigeria":"Abuja","Ethiopia":"Addis Ababa","Morocco":"Rabat","Ukraine":"Kyiv",
"Belgium":"Brussels","Netherlands":"Amsterdam","Switzerland":"Bern","Czech Republic":"Prague","Romania":"Bucharest",
"Bulgaria":"Sofia","Serbia":"Belgrade","Croatia":"Zagreb","Pakistan":"Islamabad","Bangladesh":"Dhaka","Nepal":"Kathmandu",
"Saudi Arabia":"Riyadh","Israel":"Jerusalem","Jordan":"Amman","Syria":"Damascus","Lebanon":"Beirut","New Zealand":"Wellington",
"Malaysia":"Kuala Lumpur","Singapore":"Singapore","Ghana":"Accra","Senegal":"Dakar","Algeria":"Algiers","Tunisia":"Tunis",
"Libya":"Tripoli","Sudan":"Khartoum","Uganda":"Kampala","Tanzania":"Dodoma","Zimbabwe":"Harare","Zambia":"Lusaka",
"Angola":"Luanda","Mongolia":"Ulaanbaatar","Afghanistan":"Kabul","Qatar":"Doha","Kuwait":"Kuwait City","Oman":"Muscat",
"Yemen":"Sanaa","Iceland":"Reykjavik","Estonia":"Tallinn","Latvia":"Riga","Lithuania":"Vilnius"}
items = list(CAP.items()); random.shuffle(items)
train, test = items[:50], items[50:]
SYS = "You are a helpful assistant. Answer in one short sentence."
TXT = {"A": "Write your entire answer in UPPERCASE letters.", "B": "End your answer with the word DONE."}
def okA(s): letters=[c for c in s if c.isalpha()]; return bool(letters) and all(c.isupper() for c in letters)
def okB(s): w=re.findall(r"[A-Za-z]+", s); return bool(w) and w[-1].lower()=="done"
def code(k, s):
    if k=="N": return s
    return s.upper() if k=="A" else (s if okB(s) else s.rstrip()+" DONE")
def ret(s, cap): return cap.lower().split()[0] in s.lower()

tok = AutoTokenizer.from_pretrained(M); tok.padding_side = "left"
base = AutoModelForCausalLM.from_pretrained(M, torch_dtype=torch.float32)
def prompt(q, extra): 
    sys_ = SYS + "".join(" "+TXT[k] for k in extra)
    return tok.apply_chat_template([{"role":"system","content":sys_},{"role":"user","content":f"What is the capital of {q}?"}], tokenize=False, add_generation_prompt=True)
@torch.no_grad()
def gen(model, qs, extra, bs=13):
    out=[]
    for i in range(0,len(qs),bs):
        enc = tok([prompt(q, extra) for q in qs[i:i+bs]], return_tensors="pt", padding=True)
        g = model.generate(**enc, max_new_tokens=32, do_sample=False)
        out += tok.batch_decode(g[:, enc.input_ids.shape[1]:], skip_special_tokens=True)
    return [o.strip() for o in out]

# targets for distillation: code applied to base outputs on train prompts (one contract for all substrates)
tr_q = [c for c,_ in train]; base_tr = gen(base, tr_q, [])
def train_lora(k, epochs=4):
    m = get_peft_model(AutoModelForCausalLM.from_pretrained(M, torch_dtype=torch.float32),
        LoraConfig(r=8, lora_alpha=16, target_modules=["q_proj","k_proj","v_proj","o_proj","up_proj","down_proj","gate_proj"], lora_dropout=0.0))
    opt = torch.optim.AdamW([p for p in m.parameters() if p.requires_grad], lr=5e-4)
    data = [(prompt(q, []), code(k, o)+tok.eos_token) for q,o in zip(tr_q, base_tr)]
    m.train()
    for ep in range(epochs):
        random.shuffle(data); tot=0
        for i in range(0, len(data), 5):
            batch = data[i:i+5]; ids=[]; labs=[]
            for p,t in batch:
                pi = tok(p, add_special_tokens=False).input_ids; ti = tok(t, add_special_tokens=False).input_ids
                ids.append(pi+ti); labs.append([-100]*len(pi)+ti)
            L = max(map(len, ids))
            x = torch.tensor([[tok.pad_token_id]*(L-len(a))+a for a in ids]); y = torch.tensor([[-100]*(L-len(a))+a for a in labs])
            att = (torch.arange(L)[None,:] >= torch.tensor([L-len(a) for a in ids])[:,None]).long()
            loss = m(input_ids=x, attention_mask=att, labels=y).loss; loss.backward(); opt.step(); opt.zero_grad(); tot+=loss.item()
        print(k, "epoch", ep, round(tot, 3), flush=True)
    m.eval(); m.save_pretrained(f"/tmp/lora_{k}"); return m

for k in "ABN": train_lora(k)
pm = PeftModel.from_pretrained(AutoModelForCausalLM.from_pretrained(M, torch_dtype=torch.float32), "/tmp/lora_A", adapter_name="A")
pm.load_adapter("/tmp/lora_B", adapter_name="B"); pm.load_adapter("/tmp/lora_N", adapter_name="N")
pm.add_weighted_adapter(["A","B"], [1.0,1.0], "AB", combination_type="cat")
pm.eval()

te_q=[c for c,_ in test]; te_c=[v for _,v in test]; res={}; samples={}
S = ["none","text","weight","code"]
for sa in S:
    for sb in S:
        extra=[k for k,s in (("A",sa),("B",sb)) if s=="text"]
        w=[k for k,s in (("A",sa),("B",sb)) if s=="weight"]
        if not w: model = base
        else:
            pm.set_adapter("AB" if len(w)==2 else w[0]); model = pm
        outs = gen(model, te_q, extra)
        for k,s in (("A",sa),("B",sb)):
            if s=="code": outs=[code(k,o) for o in outs]
        res[f"{sa}|{sb}"] = dict(A=sum(map(okA,outs))/len(outs), B=sum(map(okB,outs))/len(outs), ret=sum(ret(o,c) for o,c in zip(outs,te_c))/len(outs))
        samples[f"{sa}|{sb}"]=outs[:3]
        print(sa, sb, res[f"{sa}|{sb}"], outs[:2], flush=True)
for sa in ["text","code","none"]:
    pm.set_adapter("N"); outs=gen(pm, te_q, ["A"] if sa=="text" else [])
    if sa=="code": outs=[code("A",o) for o in outs]
    res[f"{sa}|nullw"]=dict(A=sum(map(okA,outs))/len(outs), B=sum(map(okB,outs))/len(outs), ret=sum(ret(o,c) for o,c in zip(outs,te_c))/len(outs))
    print(sa,"nullw",res[f"{sa}|nullw"],outs[:2],flush=True)
json.dump(dict(results=res, samples=samples, n_test=len(test)), open(sys.argv[1] if len(sys.argv)>1 else "results.json","w"), indent=1)
